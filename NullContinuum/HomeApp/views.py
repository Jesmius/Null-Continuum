from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import RegisterForm, LoginForm
from .models import Campaign, CampaignMembership, CampaignCharacter

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'HomeApp/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'HomeApp/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    if request.user.is_gm():
        campaigns = Campaign.objects.filter(gm=request.user)
    else:
        campaigns = Campaign.objects.filter(memberships__player=request.user)
    return render(request, 'HomeApp/dashboard.html', {'campaigns': campaigns})


# ── Campaigns ────────────────────────────────────────────────

@login_required
def campaign_list(request):
    if request.user.is_gm():
        campaigns = Campaign.objects.filter(gm=request.user)
    else:
        campaigns = Campaign.objects.filter(memberships__player=request.user)
    return render(request, 'HomeApp/campaign_list.html', {'campaigns': campaigns})


@login_required
def campaign_create(request):
    if not request.user.is_gm():
        raise Http404
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Campaign.objects.create(name=name, gm=request.user)
            return redirect('campaign_list')
    return render(request, 'HomeApp/campaign_form.html')


@login_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    is_gm = request.user.is_gm() and campaign.gm == request.user
    is_member = CampaignMembership.objects.filter(campaign=campaign, player=request.user).exists()
    if not is_gm and not is_member:
        raise Http404

    memberships = campaign.memberships.select_related('player')
    submitted = campaign.submitted_characters.select_related('character')

    invite_error = None
    if is_gm and request.method == 'POST' and 'invite' in request.POST:
        username = request.POST.get('username', '').strip()
        try:
            player = User.objects.get(username=username, role='PLAYER')
            CampaignMembership.objects.get_or_create(campaign=campaign, player=player)
        except User.DoesNotExist:
            invite_error = f'Jogador "{username}" não encontrado.'
        return redirect('campaign_detail', pk=pk)

    player_characters = []
    if is_member and not is_gm:
        from CharSheet.models import Character
        already = set(campaign.submitted_characters.values_list('character_id', flat=True))
        player_characters = Character.objects.filter(player=request.user).exclude(pk__in=already)

    return render(request, 'HomeApp/campaign_detail.html', {
        'campaign': campaign,
        'is_gm': is_gm,
        'is_member': is_member,
        'memberships': memberships,
        'submitted': submitted,
        'invite_error': invite_error,
        'player_characters': player_characters,
    })


@login_required
def campaign_remove_member(request, pk, member_pk):
    campaign = get_object_or_404(Campaign, pk=pk, gm=request.user)
    if request.method == 'POST':
        CampaignMembership.objects.filter(pk=member_pk, campaign=campaign).delete()
    return redirect('campaign_detail', pk=pk)


@login_required
def campaign_submit_character(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if not CampaignMembership.objects.filter(campaign=campaign, player=request.user).exists():
        raise Http404
    if request.method == 'POST':
        char_pk = request.POST.get('character_pk')
        from CharSheet.models import Character
        char = get_object_or_404(Character, pk=char_pk, player=request.user)
        CampaignCharacter.objects.get_or_create(campaign=campaign, character=char)
    return redirect('campaign_detail', pk=pk)


@login_required
def campaign_remove_character(request, pk, char_pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    is_gm = request.user.is_gm() and campaign.gm == request.user
    is_owner = CampaignMembership.objects.filter(campaign=campaign, player=request.user).exists()
    if not is_gm and not is_owner:
        raise Http404
    if request.method == 'POST':
        entry = get_object_or_404(CampaignCharacter, campaign=campaign, character__pk=char_pk)
        if is_gm or entry.character.player == request.user:
            entry.delete()
    return redirect('campaign_detail', pk=pk)


@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk, gm=request.user)
    if request.method == 'POST':
        campaign.delete()
    return redirect('campaign_list')


@login_required
def campaign_toggle_level_up(request, pk, char_pk):
    campaign = get_object_or_404(Campaign, pk=pk, gm=request.user)
    entry = get_object_or_404(CampaignCharacter, campaign=campaign, character__pk=char_pk)
    if request.method == 'POST':
        char = entry.character
        char.level_up_available = not char.level_up_available
        char.save(update_fields=['level_up_available'])
    return redirect('campaign_detail', pk=pk)
