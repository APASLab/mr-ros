# Mobile Robotics – ROS 2 packages

ROS 2 (Python) packages for the Mobile Robotics course, University of Rijeka.

## Installation

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/APASLab/mr-ros.git .
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Large files (for mobrob_v06)

The YOLO weights and videos are not stored in the repository. Download them from the
[releases page](https://github.com/APASLab/mr-ros/releases):

```bash
cd ~/ros2_ws/src/mobrob_v06/data
REPO=https://github.com/APASLab/mr-ros/releases/download
curl -L -O $REPO/data-v1/airport.mp4
curl -L -O $REPO/data-v1/autocross.mp4
curl -L -o yolov3/yolov3.weights $REPO/data-v1/yolov3.weights
```

## Updating

```bash
cd ~/ros2_ws/src && git pull
```

## Credits

YOLOv3 weights: Redmon & Farhadi, <https://pjreddie.com/darknet/yolo/> (Darknet, public domain).
