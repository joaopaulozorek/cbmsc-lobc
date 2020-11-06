from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.bc_list, name='bc_list'),
	path('bc/<user>', views.bc_detail, name='bc_detail'),
	path('cadastro/usuario', views.cadastro_usuario, name="cadastro_usuario"),
	path('login', views.logar_usuario, name="login"),
    
    #path('', views.post_list, name='post_list'),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)