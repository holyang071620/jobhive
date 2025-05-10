from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('all/', views.all_jobs, name='all_jobs'),
    path('search-users/', views.search_users, name='search_users'),
    path('my-applicants/', views.my_applicants, name='my_applicants'),

]
