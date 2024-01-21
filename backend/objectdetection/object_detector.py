import cv2
import numpy as np
import wget
import os
import mediapipe as mp
import json
from mediapipe.framework.formats import landmark_pb2
from decouple import config
import random

# TODO: error 값 구하기
# type_to_number = {"individual": 1, "couple": 2, "family": 4, "friends": 4}
pose_files = os.listdir('poses')

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
    print(weights_file, yolo_config)
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
    total_accuracy_score = 0
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
                    if calculate_accuracy:
                        results_dict = convert_results_to_dict(results)
                        # Calculate landmark difference and pose accuracy score for each part
                        total_accuracy_score_for_person = 0
                        number_of_parts = 0
                        for part in ['face_landmarks', 'pose_landmarks', 'left_hand_landmarks', 'right_hand_landmarks']:
                            # edge case: when there is unnecessary landmarks, we ignore it for now (we can give a penalty too)
                            if poses[i][part] is not None:
                                number_of_parts += 1
                                if results_dict[part] is None:
                                    # give a penalty
                                    continue
                                else:
                                    landmarks1 = results_dict[part]
                                    landmarks2 = poses[i][part]
                                    total_accuracy_score_for_person += calculate_pose_accuracy_score(landmarks1, landmarks2)
                        avg_accuracy_score_for_person = total_accuracy_score_for_person / number_of_parts
                        total_accuracy_score += avg_accuracy_score_for_person
                        print(i,"th person's accuracy score:", avg_accuracy_score_for_person)
                        #TODO: display the score & test with multiple people & get the avg of multiple people
                        #cv2.putText(frame, accuracy_score, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 215, 255), 5, cv2.LINE_AA)
                image.flags.writeable = True
                # Recolor image back to BGR for rendering
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if calculate_accuracy:
        try:
            avg_accuracy_score = int(round(total_accuracy_score / len(cropped_frames)))
            print("avg accuracy score among people:", avg_accuracy_score)
            return avg_accuracy_score
        except ZeroDivisionError:
            print("No person detected")
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

# Helper functions for calculating pose accuracy score
def calculate_pose_accuracy_score(landmarks1, landmarks2):
    difference = calculate_landmark_difference(landmarks1, landmarks2)
    Sum = sum((landmark['x'] + landmark['y'] + landmark['z']) for landmark in difference)
    avg = Sum / len(difference)
    accuracy_score = (1 - avg) * 100
    return accuracy_score

def calculate_landmark_difference(landmarks1, landmarks2):
    difference = []
    for landmark1, landmark2 in zip(landmarks1, landmarks2):
        difference.append({
            'x': abs(landmark1['x'] - landmark2['x']),
            'y': abs(landmark1['y'] - landmark2['y']),
            'z': abs(landmark1['z'] - landmark2['z']),
        })
    return difference

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

def save_pose(file):
    """takes jpeg file, apply holistic model, and save it as json. 
    WARNING: key value is always list beacuse there's always more than 1 pose in the original frame.
    """
    frame = cv2.imread(config("POSES_DIR") + file)
    # resize while maintaining the aspect ratio so that the height becomes 1080. (height: 1080, width: 1920)
    # TODO: if time permits, check the aspect ratio first, and then decide which one to use when resizing.
    height, width, _ = frame.shape
    new_height = 1080
    new_width = int(width * new_height / height)
    frame = cv2.resize(frame, (new_width, new_height))
    frames = generate_subboxes(frame)
    poses = []
    for frame in frames:
        mp_holistic = mp.solutions.holistic
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # for better performance.
            image.flags.writeable = False
            # Make Detections
            results = holistic.process(image)
            if results is not None:
                results_dict = convert_results_to_dict(results)
                # I decided to store them sequentially as a list.
                poses.append(results_dict)
    # slice the file name to remove the extension
    pose_name, _ = file.rsplit('.', 1)
    poses_d = {pose_name: poses}
    with open(f'poses_json/{pose_name}.json', 'w') as f:
        json.dump(poses_d, f)
    return poses_d

def load_pose(file):
    """takes json file and load it as a dictionary"""
    with open(file, 'r') as f:
        pose = json.load(f)
    return pose

def suggest_pose(number_of_people):
    """(int, frame) => dict (pose_name:[landmarks, landmarks, ...])
    takes number of people and returns poses
    """
    print("number of people is:", number_of_people)
    # Convert the number to a string
    number_str = str(number_of_people)
    # Get the list of files
    pose_files = os.listdir('poses')
    filtered_pose_files = [pose_file for pose_file in pose_files if number_str in pose_file]
    # shuffle
    random.shuffle(filtered_pose_files)
    # pick first
    pose_file = filtered_pose_files.pop()
    pose_name, _ = pose_file.rsplit('.', 1)
    poses_d = load_pose(f'poses_json/{pose_name}.json')
    return poses_d[pose_name]
    
def generate_subboxes(frame):
    url = "https://pjreddie.com/media/files/yolov3.weights"
    weights_file = config('WEIGHTS_FILE')
    yolo_config = config('YOLO_CONFIG')
    if not os.path.isfile(weights_file):
        wget.download(url)
    #Load the YOLO model using OpenCV:
    net = cv2.dnn.readNet(weights_file, yolo_config)
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
    return cropped_frames

if __name__ == "__main__":
    detect_human(2)
    pose_files = os.listdir('poses')
    for pose_file in pose_files:
        # ON AND OFF: to save poses
        save_pose(pose_file)
        #passfor pose_file in pose_files:
        # ON AND OFF: to save poses
        save_pose(pose_file)
        #pass