from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.company_list),
    path('company/<int:id>/', views.company_view),
    path('profile/<int:id>/', views.profile_view)
]
