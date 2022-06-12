import cv2
import numpy as np
import torch


class Detector:
    def __init__(self):
        self.net = cv2.dnn.readNetFromDarknet('/Users/dizadi/Desktop/tellocopter/perception/darknet/cfg/yolov3.cfg', '/Users/dizadi/Desktop/tellocopter/perception/darknet/cfg/yolov3.weights')
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.ln = self.net.getLayerNames()
        # Load names of classes and get random colors
        self.classes = open('/Users/dizadi/Desktop/tellocopter/perception/darknet/data/coco.names').read().strip().split('\n')
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype='uint8')

        
    def detect(self, image, annotate_image=False):
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.ln)
        boxes = []
        confidences = []
        classIDs = []
        h, w = image.shape[:2]

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores, axis=0)
                confidence = scores[classID]
                if confidence > 0.5:
                    box = detection[:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    box = [x, y, int(width), int(height)]
                    boxes.append(box)
                    confidences.append(float(confidence))
                    classIDs.append(classID)
                    
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        bboxes = []
        class_ids = []
        confs = []
        if len(indices) > 0:
            for i in indices.flatten():
                bbox = [boxes[i][0], boxes[i][1],boxes[i][2], boxes[i][3]]
                bboxes.append(bbox)

                class_id = self.classes[classIDs[i]]
                class_ids.append(class_id)

                conf = confidences[i]
                confs.append(conf)

        return bboxes, class_ids, confs
    
class ObstacleDetector:
    def __init__(self):
        pass

    def detect(self, image):
        image = cv2.resize(image, (400, 224))

        # convert to HSV and extract saturation channel
        sat = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2HSV)[:, :, 1]

        # threshold
        thresh = cv2.threshold(sat, 90, 150, 0)[1]

        # apply morphology close to fill interior regions in mask
        kernel = np.ones((29, 29), np.uint8)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((31, 31), np.uint8)
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

        # get contours (presumably only 1) and fit to simple polygon (quadrilateral)
        image, contours, hierarchy = cv2.findContours(
            morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return image, contours, hierarchy


class KeypointDetector:
    def detect(self, image):
        k,d = orb.detect(image)
        return k, d