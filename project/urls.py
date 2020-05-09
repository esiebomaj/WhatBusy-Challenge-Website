"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from profiles import views as profile_views
from django.conf import settings
from django.conf.urls.static import static
from checkout import views as checkout_views



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    path('', profile_views.Home.as_view(), name='home'),
    path('<int:pk>', profile_views.PostDetailView.as_view(), name='post_detail'),
    path('profile/<int:pk>', profile_views.ProfileView.as_view(), name='profile'),
    path('profile/new', profile_views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/<int:pk>/delete', profile_views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('profile/<int:pk>/update', profile_views.ProfileUpdateView.as_view(), name='profile_update'),
    path('contact/', profile_views.contactview, name='contact'),
    path('checkout/', checkout_views.checkoutview, name='checkout'),
    path('payment', checkout_views.PaymentView, name='payment'),
    path('charge/', checkout_views.charge, name='charge'),
    path('success/<str:args>/', checkout_views.successMsg, name='success'),
    path('premium/', checkout_views.PremiumView.as_view(), name='premium'),
    path('update_membership/<sub_id>', checkout_views.update_membership_view, name='update_membership'),
    path('cancel_membership/', checkout_views.cancelsub, name='cancel_membership'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

