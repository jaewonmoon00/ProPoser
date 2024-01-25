# ProPoser

Recommends suitable selfie poses based on the party size and gives a score based on pose accuracy.

Demo video on Youtube
https://www.youtube.com/watch?v=IdioDkYK1vg&ab_channel=JWM

json file names should be followed by the size of party
ex) pose_name_4, pose_name_2, ...

REFERENCE

for detecting multiple people: yolov3
https://shawntng.medium.com/multi-person-pose-estimation-with-mediapipe-52e6a60839dd

to install darknet to be able to use yolo models,
https://pjreddie.com/darknet/yolo/

useful Youtube tutorial for extracting landmark of each person detected: mediapipe holistic model
https://youtu.be/pG4sUNDOZFg?si=Exc2v2ELnvpQoetm

TODO:

-   Make users take 4 pictures.
-   Each column of the result page should be for only one pose. => all those pictures under same pose name should be followed below your picture.
-   Save button should allow you to save the recently taken pictures.
-   Collect more sample pictures.
-   Figure out how to store the pictures locally once you load it to minimize the get requests.
-   Should it dynamically show newly updated pictures when other people generate?
