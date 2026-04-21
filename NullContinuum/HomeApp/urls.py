from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Campaigns
    path('campanhas/', views.campaign_list, name='campaign_list'),
    path('campanhas/nova/', views.campaign_create, name='campaign_create'),
    path('campanhas/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campanhas/<int:pk>/deletar/', views.campaign_delete, name='campaign_delete'),
    path('campanhas/<int:pk>/remover-membro/<int:member_pk>/', views.campaign_remove_member, name='campaign_remove_member'),
    path('campanhas/<int:pk>/submeter-personagem/', views.campaign_submit_character, name='campaign_submit_character'),
    path('campanhas/<int:pk>/remover-personagem/<int:char_pk>/', views.campaign_remove_character, name='campaign_remove_character'),
    path('campanhas/<int:pk>/level-up/<int:char_pk>/', views.campaign_toggle_level_up, name='campaign_toggle_level_up'),
]
