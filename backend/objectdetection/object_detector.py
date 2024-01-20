import cv2
import numpy as np
import wget
import os
import mediapipe as mp
import time

def detect_human():
    """takes an image and detect pose"""
    # use a pre-trained YOLOv3 or YOLOv4 model, for example.
    url = "https://pjreddie.com/media/files/yolov3.weights"
    weights_file = "yolov3.weights"
    if not os.path.isfile(weights_file):
        wget.download(url)
    #Load the YOLO model using OpenCV:
    net = cv2.dnn.readNet(weights_file, "darknet/cfg/yolov3.cfg")
    frame = cv2.imread("multiple_people_pic.jpeg")
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers = net.getUnconnectedOutLayersNames()
    detections = net.forward(output_layers)
    # Showing informations on the screen
    person_boxes, confidences = [], []
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # try confidence > 0.7
            if confidence > 0.5 and class_id == 0:  # Assuming person class ID is 0
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                person_boxes.append([x, y, w, h])  # Note: NMSBoxes expects [x, y, w, h] format
                confidences.append(float(confidence))
            # use non-maximum suppression (NMS) to eliminate overlapping bounding boxes
            indices = cv2.dnn.NMSBoxes(person_boxes, confidences, 0.5, 0.4)
    cropped_frames = []
    for i in range(len(person_boxes)):
        if i in indices:
            # Edge case: when a person is at the edge of the image and the bounding box extends beyond the image.
            x, y, w, h = person_boxes[i]
            x = max(0, x)
            y = max(0, y)
            w = min(w, width - x)
            h = min(h, height - y)
            # SOLUTION: Create a copy of the original frame
            frame_copy = frame.copy()
            # Black out the areas that are not of interest
            frame_copy[:y, :] = 0
            frame_copy[y+h:, :] = 0
            frame_copy[:, :x] = 0
            frame_copy[:, x+w:] = 0
            cropped_frames.append(frame_copy)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
            cv2.imshow("YOLOv3", frame)
            cv2.waitKey(0)

    # MEDIAPIPE BEGINS HERE
    for person_frame in cropped_frames:
        if person_frame is not None and person_frame.size > 0:
            mp_drawing = mp.solutions.drawing_utils
            mp_holistic = mp.solutions.holistic
            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                # Recolor Feed
                image = cv2.cvtColor(person_frame, cv2.COLOR_BGR2RGB)
                # for better performance.
                image.flags.writeable = False
                # Make Detections
                results = holistic.process(image)
                if results is not None:
                    # Edge case: people with sunglasses on may not be detected
                    mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS)
                    mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                    mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                image.flags.writeable = True
                # Recolor image back to BGR for rendering
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.imshow("YOLOv3", frame)
                cv2.waitKey(0)
if __name__ == "__main__":
    detect_human()