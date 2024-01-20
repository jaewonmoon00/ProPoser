import cv2
from django.http import StreamingHttpResponse
from imutils.video import WebcamVideoStream
from .serializers import PoseSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Pose
from rest_framework.decorators import api_view
import time
from .object_detector import (
    detect_human,
    suggest_pose
)
# Create your views here.
def gen(camera, num_people=1):
    poses = suggest_pose(num_people)
    while True:
        frame = camera.read()
        # Process the frame using detect_human
        processed_frame = detect_human(frame, poses)
        # Convert the processed frame to JPEG
        ret, jpeg = cv2.imencode(".jpg", processed_frame)
        if ret:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            
@api_view(["POST", "GET"])
def stream_video(request):
    # Start the webcam video stream
    webcam = WebcamVideoStream(src=0).start()
    try:
        party_size = request.GET.get('partySize')
        # Stream the video
        return StreamingHttpResponse(
            gen(webcam, party_size),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )
    except StopIteration:
        # Stop the webcam video stream when the client disconnects
        webcam.stop()

# TODO: we need to send 4 poses recently taken from camera_feed/
@api_view(["GET", "POST"])
def get_poses(request):
    if request.method == "GET":
        poses = Pose.objects.all()
        serializer = PoseSerializer(poses, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        return Response({"message": "POST method not implemented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED)
    else:
        return Response({"error": "Invalid method"}, status=status.HTTP_400_BAD_REQUEST)