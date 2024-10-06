from django.urls    import path
from .views         import *
urlpatterns = [
    path("" , home , name="home"),
    path("video" , video , name="video")
]