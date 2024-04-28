"""Main script to run the object detection routine."""
import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

INTRUDER_LIST = ["cat", "dog"]
DETECTION_SENSITIVITY = 0.40
# import utils_apache as utils  # if you want live video feed


MODEL = "efficientdet_lite0.tflite"
CAMERA_ID = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
NUM_THREADS = 1
ENABLE_EDGETPU = False

def detect_objects() -> None:
    """
    Continuously run inference on images acquired from the camera.
    """

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(CAMERA_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    fps_avg_frame_count = 10

    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=MODEL, use_coral=ENABLE_EDGETPU, num_threads=NUM_THREADS
    )
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3
    )
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options
    )
    detector = vision.ObjectDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    success, image = cap.read()
    if not success:
        sys.exit(
            'ERROR: Unable to read from webcam. Please verify your webcam settings.'
        )
    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                sys.exit(
                    "ERROR: Unable to read from webcam. Please verify your webcam settings."
                )

            counter += 1
            image = cv2.flip(image, 1)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Create a TensorImage object from the RGB image.
            input_tensor = vision.TensorImage.create_from_array(rgb_image)

            # Run object detection estimation using the model.
            detection_result = detector.detect(input_tensor)
            if detection_result:
                stopObjectInView = False
                for detection in detection_result.detections:
                    category = detection.categories[0]
                    category_name = category.category_name
                    probability = round(category.score, 2)
                    if probability > DETECTION_SENSITIVITY:
                        print(
                                "Detected: " + category_name,
                                "probability: " + str(probability),
                            )
                        if category_name in INTRUDER_LIST:
                            print(
                                "Detected: " + category_name,
                                "probability: " + str(probability),
                            )
    except KeyboardInterrupt:
        cap.release()

if __name__ == "__main__":
    detect_objects()