from django.urls import path

from . import views

app_name = 'inorder'
urlpatterns = [
    path('', views.list, name='index'),
    path('add', views.add, name='add'),
    path('search', views.search, name='search'),
    path('update/<int:inorder_id>', views.update, name='update'),
    path('delete/<int:inorder_id>', views.delete, name='delete'),
    path('detail/<int:inorder_id>', views.detail, name='detail'),
    path('<int:inorder_id>/addmore', views.addmore, name='addmore'),
    path('<int:inorder_id>/<int:inorderclothes_id>/editmore', views.editmore, name='editmore'),
    path('<int:inorder_id>/<int:inorderclothes_id>/deletemore', views.deletemore, name='deletemore')
]