import json
import base64
from PIL import Image
import io
#import torch
from ultralytics import YOLO
import numpy as np

def init_context(context):
    context.logger.info("Init context...  0%")

    # Read the DL model
    #model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
    model = YOLO("/models/best.pt") #YOLO("/opt/nuclio/best.pt") #YOLO("C:/Users/rhyst/Documents/Pickleball/best.pt") #YOLO("best.pt")
    context.user_data.model = model

    context.logger.info("Init context...100%")

def handler(context, event):
    context.logger.info("Run yolo-v8 model")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    threshold = float(data.get("threshold", 0.5))
    context.user_data.model.conf = threshold
    image = Image.open(buf)
    #yolo_results_json = context.user_data.model(image).pandas().xyxy[0].to_dict(orient='records')

    outputs_yolo = context.user_data.model(image)

    boxes = outputs_yolo[0].boxes

    # Convert boxes to numpy array
    boxes_np = np.array(boxes.xyxy)

    # Extract label and score
    labels = []#boxes.names
    scores = boxes.conf
    classes = boxes.cls

    for element in classes:
        if element == 0:
            labels.append("Bounce")
        if element == 1:
            labels.append("Player_1")
        if element == 2:
            labels.append("Player_2")
        if element == 3:
            labels.append("Ball")

    # Extract box coordinates
    xtl = boxes_np[:, 0] #I think tl is actually bottom left
    ytl = boxes_np[:, 1]
    xbr = boxes_np[:, 2] #I think br is actually top right
    ybr = boxes_np[:, 3]

    # Create array of CVAT box format dictionaries
    cvat_boxes = []
    for i in range(len(labels)):
        box_dict = {'name': labels[i], 'class':int(classes[i]), 'confidence': float(scores[i]), 'xmin': float(xtl[i]), 'ymin': float(ytl[i]), 'xmax': float(xbr[i]), 'ymax': float(ybr[i])}
        cvat_boxes.append(box_dict)
    
    yolo_results_json = cvat_boxes

    encoded_results = []
    for result in yolo_results_json:
        encoded_results.append({
            'confidence': result['confidence'],
            'label': result['name'],
            'points': [
                result['xmin'],
                result['ymin'],
                result['xmax'],
                result['ymax']
            ],
            'type': 'rectangle'
        })

    return context.Response(body=json.dumps(encoded_results), headers={},
        content_type='application/json', status_code=200)
