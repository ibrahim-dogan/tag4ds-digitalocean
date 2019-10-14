from django.urls import path

from fileupload import views

urlpatterns = [
    path('', views.upload_file, name='upload_page'),
    path('prepare/<int:id>', views.prepare_tags, name='prepare_tags'),
    path('tag-process/<int:id>/<int:row>', views.tag_process, name='tag_process'),
    path('download/<int:id>', views.download, name='download'),
    path('validate/<int:id>', views.validate, name='validate')
]
