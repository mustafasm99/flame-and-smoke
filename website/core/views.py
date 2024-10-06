from django.shortcuts   import render
from django.http        import StreamingHttpResponse
from .cfamera           import GetCamera
from .models            import *
import cv2 
# Create your views here.

# video_url = "http://192.168.0.103/stream"
video_url   = 0

def video(e):
    return StreamingHttpResponse(GetCamera(video_url).gen_frame() , content_type='multipart/x-mixed-replace; boundary=frame')

def home(e):
    print(video_url)
    data    = fire.objects.all()
    return render(e , "home.html" , {"data":data})
