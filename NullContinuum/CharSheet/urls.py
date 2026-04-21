from django.urls import path
from . import views
from . import feat_views

urlpatterns = [
    path('personagens/', views.character_list, name='character_list'),
    path('personagens/novo/', views.character_create, name='character_create'),
    path('personagens/novo/<int:pk>/traits/', views.character_create_traits, name='character_create_traits'),
    path('personagens/novo/<int:pk>/feats/', views.character_create_feats, name='character_create_feats'),
    path('personagens/novo/<int:pk>/nl-feats/', views.character_create_nl_feats, name='character_create_nl_feats'),
    path('personagens/novo/<int:pk>/shifter/', views.character_create_shifter, name='character_create_shifter'),
    path('personagens/novo/<int:pk>/changer/', views.character_create_changer, name='character_create_changer'),
    path('personagens/novo/<int:pk>/maker/', views.character_create_maker, name='character_create_maker'),
    path('personagens/novo/<int:pk>/leaker/', views.character_create_leaker, name='character_create_leaker'),
    path('personagens/<int:pk>/', views.character_detail, name='character_detail'),
    path('personagens/<int:pk>/editar/', views.character_edit, name='character_edit'),
    path('personagens/<int:pk>/deletar/', views.character_delete, name='character_delete'),
    path('personagens/<int:pk>/combate/', views.combat_quick_update, name='combat_quick_update'),
    path('personagens/<int:pk>/construto/<int:schematic_pk>/hp/', views.construct_hp_update, name='construct_hp_update'),
    path('personagens/<int:pk>/feats/<str:tab>/', feat_views.character_feats, name='character_feats'),
    path('personagens/<int:pk>/feats/', feat_views.character_feats, name='character_feats_default'),
    path('personagens/<int:pk>/rank-up/', views.rank_up_view, name='rank_up'),

    # Inventory — Weapons
    path('personagens/<int:pk>/inventario/arma/add/', views.weapon_add, name='weapon_add'),
    path('personagens/<int:pk>/inventario/arma/<int:item_pk>/edit/', views.weapon_edit, name='weapon_edit'),
    path('personagens/<int:pk>/inventario/arma/<int:item_pk>/delete/', views.weapon_delete, name='weapon_delete'),

    # Inventory — Vestments / Shields
    path('personagens/<int:pk>/inventario/vestimenta/add/', views.vestment_add, name='vestment_add'),
    path('personagens/<int:pk>/inventario/vestimenta/<int:item_pk>/edit/', views.vestment_edit, name='vestment_edit'),
    path('personagens/<int:pk>/inventario/vestimenta/<int:item_pk>/delete/', views.vestment_delete, name='vestment_delete'),

    # Inventory — Consumables
    path('personagens/<int:pk>/inventario/consumivel/add/', views.consumable_add, name='consumable_add'),
    path('personagens/<int:pk>/inventario/consumivel/<int:item_pk>/edit/', views.consumable_edit, name='consumable_edit'),
    path('personagens/<int:pk>/inventario/consumivel/<int:item_pk>/delete/', views.consumable_delete, name='consumable_delete'),

    # Vehicles
    path('personagens/<int:pk>/veiculos/add/', views.vehicle_add, name='vehicle_add'),
    path('personagens/<int:pk>/veiculos/<int:item_pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('personagens/<int:pk>/veiculos/<int:item_pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    path('personagens/<int:pk>/veiculos/<int:item_pk>/hp/', views.vehicle_hp_update, name='vehicle_hp_update'),
]
