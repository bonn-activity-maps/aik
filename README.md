# AIK

## Install
This library requires numpy and OpenCV3
```bash
pip install git+https://github.com/actions-in-kitchens/aik.git
```

## Usage

```python
from aik.dataset import AIK
import aik.geometry as gm

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# load dataset
aik = AIK('/path/to/dataset/dir')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get all images and all cameras for a given frame:
frame = 20
Images, Cameras = aik.get_frame(frame)
# len(Images) == n_cameras
# len(Cameras) == n_cameras

# Load image path' instead of images. Paths are rooted at the dataset folder
Paths, Cameras = aik.get_frame(frame, return_paths=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# project a 3D point onto a camera
pt3d = [0, 0, 0]
cam0 = Cameras[0]
pt2d_in_cam0 = cam0.project_points(pt3d)  # position is in pixel

# get 3D position in camera:
pos = cam0.location()  # position is in world coordinates

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# find epipolar line in cam2 of a point in cam1:
cam1 = Cameras[1]
cam2 = Cameras[2]

pt1 = [500, 200]  # 2D point in cam1
epiline = gm.compute_epiline(pt1, cam1, cam2)

# ax + by + c = 0 ==> y = (-c -ax)/b
y = lambda x, a, b, c: (-c - a * x)/b

x0 = 0
y0 = y(x0, *epiline)

x1 = 1600
y1 = y(x1, *epiline)

# The line passing through (x0, y0) and (x1, y1) is the epipolar line

# Serialization:
json_str = cam1.to_json()

# De-Serialization:
from aik.camera import Camera
cam_new = Camera.from_json(json_str)

```
