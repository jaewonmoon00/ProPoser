import cv2
import numpy as np
import wget
import os
import mediapipe as mp
import time
from decouple import config
from mediapipe.framework.formats import landmark_pb2

def detect_human(frame, poses=None, calculate_accuracy=False):
    """
    takes an image and detect pose
    this function will be called once user selects the type of their group.
    """
    # use a pre-trained YOLOv3 or YOLOv4 model, for example.
    url = "https://pjreddie.com/media/files/yolov3.weights"
    weights_file = config('WEIGHTS_FILE')
    yolo_config = config('YOLO_CONFIG')
    if not os.path.isfile(weights_file):
        wget.download(url)
    #Load the YOLO model using OpenCV:
    net = cv2.dnn.readNet(weights_file, yolo_config)
    
    frame = cv2.flip(frame, 1)
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
            # SOLUTION: use non-maximum suppression (NMS) to eliminate overlapping bounding boxes
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
            #cv2.imshow("YOLOv3", frame)
            #cv2.waitKey(0)

    # MEDIAPIPE BEGINS HERE
    for i in range(len(cropped_frames)):
        person_frame = cropped_frames[i]
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

    # ON AND OFF: this is for suggesting a pose
    for pose in poses:
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic
        if pose["face_landmarks"] is not None:
            mp_drawing.draw_landmarks(frame, convert_dict_to_landmarks(pose["face_landmarks"]), mp_holistic.FACEMESH_CONTOURS)
        if pose["right_hand_landmarks"] is not None:
            mp_drawing.draw_landmarks(frame, convert_dict_to_landmarks(pose["right_hand_landmarks"]), mp_holistic.HAND_CONNECTIONS)
        if pose["left_hand_landmarks"] is not None:
            mp_drawing.draw_landmarks(frame, convert_dict_to_landmarks(pose["left_hand_landmarks"]), mp_holistic.HAND_CONNECTIONS)
        if pose["pose_landmarks"] is not None:
            mp_drawing.draw_landmarks(frame, convert_dict_to_landmarks(pose["pose_landmarks"]), mp_holistic.POSE_CONNECTIONS)
    #cv2.imshow("ProPoser", frame)
    return frame

# Helper functions for storing and loading poses
def convert_dict_to_landmarks(landmarks_dict):
    landmarks = landmark_pb2.NormalizedLandmarkList()
    for landmark_dict in landmarks_dict:
        landmark = landmarks.landmark.add()
        landmark.x = landmark_dict['x']
        landmark.y = landmark_dict['y']
        landmark.z = landmark_dict['z']
    return landmarks

def convert_landmarks_to_dict(landmarks):
    if landmarks is None:
        return None
    return [{'x': landmark.x, 'y': landmark.y, 'z': landmark.z} for landmark in landmarks.landmark]

def convert_results_to_dict(results):
    return {
        'face_landmarks': convert_landmarks_to_dict(results.face_landmarks),
        'pose_landmarks': convert_landmarks_to_dict(results.pose_landmarks),
        'left_hand_landmarks': convert_landmarks_to_dict(results.left_hand_landmarks),
        'right_hand_landmarks': convert_landmarks_to_dict(results.right_hand_landmarks),
    }

if __name__ == "__main__":
    detect_human()