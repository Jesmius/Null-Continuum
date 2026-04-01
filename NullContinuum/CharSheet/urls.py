from django.urls import path
from . import views

urlpatterns = [
    path('personagens/', views.character_list, name='character_list'),
    path('personagens/novo/', views.character_create, name='character_create'),
    path('personagens/<int:pk>/', views.character_detail, name='character_detail'),
    path('personagens/<int:pk>/editar/', views.character_edit, name='character_edit'),
    path('personagens/<int:pk>/deletar/', views.character_delete, name='character_delete'),
    path('personagens/<int:pk>/combate/', views.combat_quick_update, name='combat_quick_update'),
]
