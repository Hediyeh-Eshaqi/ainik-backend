"""ainik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from Charity.views import CharityView, CharityWorkView, CharityListView, CharityWorkListView, RecommendedCharityWork
from Accounts.views import MyCharityView, UserPersonalityComponentsView, UserEditionView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('charity/create', CharityView.as_view(), name='create_charity'),
    path('charity/<int:charity_id>/addwork', CharityWorkView.as_view(), name='add_charity_work'),
    path('charity/<int:charity_id>/delete/<int:work_id>', CharityWorkView.as_view(), name='delete_charity_work'),
    path('charity/<int:charity_id>/delete', CharityView.as_view(), name='delete_charity'),
    path('charity/<int:charity_id>/', CharityView.as_view(), name='get_charity_public_data'),
    path('charity/list/', CharityListView.as_view(), name='get_charity_list'),
    path('charity/charity_work/list/', CharityWorkListView.as_view(), name='get_charity_work_list'),
    path('user/charites/', MyCharityView.as_view(), name='my_chairties'),
    path('user/personalityComponents/', UserPersonalityComponentsView.as_view(), name='create_personality_components'),
    path('user/edit/', UserEditionView.as_view(), name='edit_user_info'),
    path('user/recommendations/', RecommendedCharityWork.as_view(), name='get_recommended_charity_work')
]
