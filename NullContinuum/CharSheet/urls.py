from django.urls import path
from . import views
from . import feat_views

urlpatterns = [
    path('personagens/', views.character_list, name='character_list'),
    path('personagens/novo/', views.character_create, name='character_create'),
    path('personagens/novo/<int:pk>/feats/', views.character_create_feats, name='character_create_feats'),
    path('personagens/<int:pk>/', views.character_detail, name='character_detail'),
    path('personagens/<int:pk>/editar/', views.character_edit, name='character_edit'),
    path('personagens/<int:pk>/deletar/', views.character_delete, name='character_delete'),
    path('personagens/<int:pk>/combate/', views.combat_quick_update, name='combat_quick_update'),
    # Feats (read-only view)
    path('personagens/<int:pk>/feats/<str:tab>/', feat_views.character_feats, name='character_feats'),
    path('personagens/<int:pk>/feats/', feat_views.character_feats, name='character_feats_default'),
    # Rank Up
    path('personagens/<int:pk>/rank-up/', views.rank_up_view, name='rank_up'),
]
