"""
Sincroniza todos os dados do rulebook/ com o banco de dados.
Substitui populate_feats. É o único comando que você precisa rodar
depois de editar arquivos em CharSheet/rulebook/.

Uso: python manage.py sync_rulebook
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from CharSheet.feat_models import FeatDefinition
from CharSheet.trait_models import TraitDefinition

from CharSheet.rulebook.feats import COMBAT_TREES, OPERATIONS_TREES
from CharSheet.rulebook.nl_feats import NL_GENERAL_TREE, SHIFTER_TREES, CHANGER_TREES, MAKER_TREES, LEAKER_TREES
from CharSheet.rulebook.traits import POSITIVE_TRAITS, NEGATIVE_TRAITS
from CharSheet.rulebook.background_traits import BACKGROUND_TRAITS


class Command(BaseCommand):
    help = 'Sincroniza o rulebook (feats, traits, backgrounds) com o banco.'

    def handle(self, *args, **options):
        with transaction.atomic():
            self._sync_feats()
            self._sync_nl_feats()
            self._sync_traits()
            self._sync_background_traits()
        self.stdout.write(self.style.SUCCESS('✓ Rulebook sincronizado com sucesso.'))

    # ─── Feats ──────────────────────────────────────────

    def _sync_feats(self):
        created, updated = 0, 0
        all_trees = [
            ('COMBAT', COMBAT_TREES),
            ('OPERATIONS', OPERATIONS_TREES),
        ]

        for category, tree_list in all_trees:
            for tree_name, tree_code, tree_desc, feats_data in tree_list:
                prev_feat = None
                for code, name, tier, desc in feats_data:
                    prereq = prev_feat if tier > 1 else None

                    feat, was_created = FeatDefinition.objects.update_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'category': category,
                            'tree': tree_name,
                            'tree_code': tree_code,
                            'tier': tier,
                            'prerequisite': prereq,
                            'description': desc,
                            'tree_description': tree_desc,
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1

                    if tier > 0:
                        prev_feat = feat

        self.stdout.write(f'  Feats: {created} criadas, {updated} atualizadas.')

    # ─── NL Feats ───────────────────────────────────────

    def _sync_nl_feats(self):
        created, updated = 0, 0

        all_nl_trees = [NL_GENERAL_TREE] + SHIFTER_TREES + CHANGER_TREES + MAKER_TREES + LEAKER_TREES

        for tree_name, tree_code, tree_desc, nl_frame, feats_data in all_nl_trees:
            prev_feat = None
            for code, name, tier, desc in feats_data:
                prereq = prev_feat if tier > 1 else None

                feat, was_created = FeatDefinition.objects.update_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'category': 'NON_LINEAR',
                        'nl_frame': nl_frame,
                        'tree': tree_name,
                        'tree_code': tree_code,
                        'tier': tier,
                        'prerequisite': prereq,
                        'description': desc,
                        'tree_description': tree_desc,
                    }
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

                if tier > 0:
                    prev_feat = feat

        self.stdout.write(f'  NL Feats: {created} criadas, {updated} atualizadas.')

    # ─── Traits ─────────────────────────────────────────

    def _sync_traits(self):
        created, updated = 0, 0

        for code, name, cost, desc in POSITIVE_TRAITS:
            _, was_created = TraitDefinition.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'kind': 'POSITIVE',
                    'cost': cost,
                    'description': desc,
                    'background_key': '',
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        for code, name, cost, desc in NEGATIVE_TRAITS:
            _, was_created = TraitDefinition.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'kind': 'NEGATIVE',
                    'cost': cost,  # já é negativo
                    'description': desc,
                    'background_key': '',
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  Traits (pos/neg): {created} criados, {updated} atualizados.')

    # ─── Background Traits ─────────────────────────────

    def _sync_background_traits(self):
        created, updated = 0, 0

        for bg_key, trait_list in BACKGROUND_TRAITS.items():
            for name, desc in trait_list:
                # Código único: BG_<bgkey>_<slug>
                slug = name.upper().replace(' ', '_').replace('-', '_')
                # Remover caracteres especiais
                slug = ''.join(c for c in slug if c.isalnum() or c == '_')
                code = f'BG_{bg_key}_{slug}'

                _, was_created = TraitDefinition.objects.update_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'kind': 'BACKGROUND',
                        'cost': 0,
                        'description': desc,
                        'background_key': bg_key,
                    }
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(f'  Background traits: {created} criados, {updated} atualizados.')
