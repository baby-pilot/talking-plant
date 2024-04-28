# Software based on TensorFlow examples detect.py at
#
#       https://github.com/tensorflow/examples
#
# License:
# Copyright 2024 John Pan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main script to run the object detection routine."""
import sys

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
from bt_speak import AlertMode
from utils import IntervalExponentialBackOff

backoff_interval = IntervalExponentialBackOff()

# import utils_apache as utils  # if you want live video feed


MODEL = "efficientdet_lite0.tflite"
CAMERA_ID = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
NUM_THREADS = 1
ENABLE_EDGETPU = False
INTRUDER_LIST = ["cat", "dog"]
DETECTION_SENSITIVITY = 0.40

class ObjectDetector:
    def __init__(self, notify_event):
        self.notify_event = notify_event

    def detect_objects(self, alert_q) -> None:
        """
        Continuously run inference on images acquired from the camera.
        """

        # Start capturing video input from the camera
        cap = cv2.VideoCapture(CAMERA_ID)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

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
        try:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    sys.exit(
                        "ERROR: Unable to read from webcam. Please verify your webcam settings."
                    )

                image = cv2.flip(image, 1)

                # Convert the image from BGR to RGB as required by the TFLite model.
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Create a TensorImage object from the RGB image.
                input_tensor = vision.TensorImage.create_from_array(rgb_image)

                # Run object detection estimation using the model.
                detection_result = detector.detect(input_tensor)
                if detection_result:
                    for detection in detection_result.detections:
                        category = detection.categories[0]
                        category_name = category.category_name
                        probability = round(category.score, 2)
                        if probability > DETECTION_SENSITIVITY:
                            if category_name in INTRUDER_LIST:
                                print(
                                    "Detected: " + category_name,
                                    "probability: " + str(probability),
                                )
                                if not self.notify_event.is_set() or backoff_interval.back_off_passed():
                                    print("Alerting about intruder")
                                    self.notify_event.set()
                                    alert_q.append(AlertMode.NEED_DEFENSE)
                                    backoff_interval.set()
                                else:
                                    print("Intruder alert already queued")
                            else:
                                print("Intruder cleared")
                                if self.notify_event.is_set():
                                    self.notify_event.clear()
                                    backoff_interval.reset()

        except KeyboardInterrupt:
            cap.release()
