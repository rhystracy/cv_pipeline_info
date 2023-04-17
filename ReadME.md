# CV Pipeline Info



First clear all docker images and containers, etc with docker desktop

Run "FOR /f "tokens=*" %i IN ('docker ps -aq') DO docker rm -f %i" to force delete all docker containers in command prompt

Open command prompt and go to cvat repo

Run "docker-compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml up -d" to bring up cvat and nuclio

CVAT on localhost:8080  nuclio on localhost:8070

Go into nuclio, make new project called cvat

In new project, make function from yaml

Use functions.yaml from cvat/serverless/pytorch/ultralytics/yolov8/nuclio (copied to this folder)

For function code, copy main.py from cvat/serverless/pytorch/ultralytics/yolov8/nuclio (also copied to this folder)

Then click configurations, scroll down to volume and create a new volume

Set name as "models", set host path as path to special models folder with yolo.pt file ("C:/Users/rhyst/Documents/Pickleball/models")

Set mount path as "/models" -> important for exactly this name as this is where the main.py script will look

Click deploy

Make sure docker container isn't infinite restarting on docker desktop, also ensure ports match up on nuclio and docker desktop

Then go to CVAT, model should automatically become available