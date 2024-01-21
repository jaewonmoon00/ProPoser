from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
from imutils.video import WebcamVideoStream
from .object_detector import (
    detect_human,
    save_pose,
    suggest_pose,
)
import time
import os
from .models import Pose
# to use in-memory file, which is faster because it resides in memory (RAM) rather than on disk
import io
from PIL import Image
from django.core.files.base import ContentFile
# django rest framework
from rest_framework.decorators import api_view
from .serializers import PoseSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def gen(camera, num_people=1):
    start_time = time.time()
    poses = suggest_pose(num_people)
    while True:
        frame = camera.read()
        # Process the frame using detect_human
        processed_frame = detect_human(frame, poses)
        # Calculate remaining time
        remaining_time = 10 - (time.time() - start_time)
        # Convert remaining time to string
        remaining_time_str = str(int(remaining_time))
        # Calculate the center position
        height, width, _ = frame.shape
        center_x = width // 2
        center_y = height // 2
        if time.time() - start_time > 10:
            accuracy_score = detect_human(frame, poses, calculate_accuracy=True)
            # Display score
            cv2.putText(
                processed_frame,
                str(accuracy_score),
                (center_x, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                5,  # Increase this value to make the text bigger
                (0, 215, 255),
                5,
                cv2.LINE_AA,
            )
            # Convert the frame from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the OpenCV image (NumPy array) to a PIL image
            pil_image = Image.fromarray(rgb_frame)
            # Create an in-memory file
            img_io = io.BytesIO()
            # Save the PIL image to the in-memory file
            pil_image.save(img_io, format="JPEG")
            # Create a Django ContentFile from the in-memory file
            img_content = ContentFile(img_io.getvalue(), "snapshot.jpg")
            pose = Pose(name="pose_name", accuracy_score=accuracy_score)
            # Save the image to the Pose's image field
            pose.image.save("snapshot.jpg", img_content)
            pose.save()
            break
        
        # Display remaining time on camera screen
        cv2.putText(
            processed_frame,
            remaining_time_str,
            (center_x, center_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (255, 255, 255),
            5,
            cv2.LINE_AA,
        )
        # Convert the processed frame to JPEG
        ret, jpeg = cv2.imencode(".jpg", processed_frame)
        if ret:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

@api_view(["POST", "GET"])
def stream_video(request):
    pose_files = os.listdir("poses")
    for pose_file in pose_files:
        # ON AND OFF: to save poses
        #save_pose(pose_file)
        pass
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