from django.urls import path

from . import views

app_name = 'outorder'
urlpatterns = [
    path('', views.list, name='index'),
    path('add', views.add, name='add'),
    path('search', views.search, name='search'),
    path('update/<int:outorder_id>', views.update, name='update'),
    path('delete/<int:outorder_id>', views.delete, name='delete'),
    path('detail/<int:outorder_id>', views.detail, name='detail'),
    path('<int:outorder_id>/addmore', views.addmore, name='addmore'),
    path('<int:outorder_id>/<int:outorderclothes_id>/editmore', views.editmore, name='editmore'),
    path('<int:outorder_id>/<int:outorderclothes_id>/deletemore', views.deletemore, name='deletemore')
]