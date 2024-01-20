import cv2
from django.http import StreamingHttpResponse
from imutils.video import WebcamVideoStream
from .serializers import PoseSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Pose
from rest_framework.decorators import api_view
# Create your views here.
def gen(camera):
    while True:
        frame = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def stream_video(request):
    return StreamingHttpResponse(gen(WebcamVideoStream(src=0).start()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(["GET", "POST"])
def get_poses(request):
    if request == "GET":
        poses = Pose.objects.all()
        serializer = PoseSerializer(poses, many=True)
        return Response(serializer.data)
    elif request == "POST":
        pass
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
