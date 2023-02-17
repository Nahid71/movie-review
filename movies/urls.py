from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review/',views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<str:pk>/',views.RetrieveUpdateDestroyMovieAPIView.as_view(),name='get_delete_update_review'),
    path('report/crate/',views.CreateReportAPIView.as_view(),name='post_report'),
    path('report/list/',views.ListReportAPIView.as_view(),name='list_report'),
    path('report/<str:pk>/',views.RetrieveUpdateDestroyReportAPIView.as_view(),name='get_delete_update_report')
]