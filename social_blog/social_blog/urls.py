from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'


urlpatterns = [
    path('', include('blog.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/registration/', CreateView.as_view(
         template_name='registration/registration_form.html',
         form_class=UserCreationForm, success_url=reverse_lazy('blog:index'),
         ), name='registration',),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG is True:
    import debug_toolbar
    urlpatterns = [url(r'^__debug__/',
                   include(debug_toolbar.urls)), ] + urlpatterns
