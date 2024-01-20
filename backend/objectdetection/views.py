import cv2
from django.http import StreamingHttpResponse
from imutils.video import WebcamVideoStream
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