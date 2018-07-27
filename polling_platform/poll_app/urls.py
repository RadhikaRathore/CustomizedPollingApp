from django.urls import path, include
from poll_app import views


urlpatterns = [

    path('', views.home, name='home'),
    path('polls/', views.PollListView.as_view(), name='poll_list'),
    path('polls/add/', views.PollCreateView.as_view(), name='add_poll'),
    path('polls/<int:pk>/email/add', views.add_emailaddress, name='add_email'),
    path('polls/<int:poll_pk>/email/<int:email_pk>/', views.email_change, name='email_change'),
    path('polls/<int:poll_pk>/sendfirstlink', views.send_first_link, name='send_first_link'),
	path('polls/<int:poll_pk>/sendsecondlink', views.send_second_link, name='send_second_link'),
	path('polls/<int:poll_pk>/email/check', views.check_emailaddress, name='check_email'),
	path('polls/<int:poll_pk>/choice/<int:email_pk>/', views.add_choice, name='add_choice'),
	path('polls/<int:poll_pk>/addmorechoice/<int:email_pk>/', views.choice_change, name='choice_change'),
	path('polls/<int:poll_pk>/checkandsend/<int:email_pk>/', views.change_status, name='change_status'),
	path('polls/<int:poll_pk>/pollemail/check/', views.check_pollemailaddress, name='check_pollemail'),
	path('polls/<int:pk>/polldetail/<int:email_pk>/', views.PollDetailView.as_view(), name='poll_detail'),
	path('polls/<int:poll_pk>/vote/<int:email_pk>/', views.vote, name='vote'),
	path('polls/<int:poll_pk>/sendthirdlink', views.send_third_link, name='send_third_link'),
	path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	








]
