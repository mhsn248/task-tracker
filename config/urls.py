from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):

    def get_success_url(self):

        if self.request.user.groups.filter(
            name='Teacher'
        ).exists():

            return '/tasks/teacher/students/'

        return '/tasks/daily/'


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),

    path('tasks/', include('tasks.urls')),

    path(
        'login/',
        CustomLoginView.as_view(),
        name='login',
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
]
