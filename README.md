# pose_estimation_and_AR
Camera pose estimation with chessboard and describe simple AR things on it

## Modules used for this simple Camera_pose_estimation
* Numpy
* cv2

## Prerequiste
* <a href = "https://github.com/EarthRabbit/camera_calibration">Camera Calibration</a> is needed for <a color = "red">intrinsic values</a> and for your camera.
* From Camera Calibration, a video for capturing a chessboard.

## Description
* In Camera Calibration, we found a camera intrinsic matrix K and distortion coefficients.
* Now, we use intrinsic values of camera to find inner position where the the camera is.

## How?

1. Make your own shape which will be used for AR. For me, a simple crown.

```bibtex
box_upper = board_cellsize * np.array([[2, 4, 0], [2, 2, 0], [3, 3, 0], [4, 2, 0], [5, 3, 0], [6, 2, 0], [6, 4, 0]])
box_lower = board_cellsize * np.array([[2, 4, -1], [2, 2, -1], [3, 3, -1], [4, 2, -1], [5, 3, -1], [6, 2, -1], [6, 4, -1]])
```

2. Open a chessboard video and find chessboard corners as you did in camera_calibration.

```bibtex
complete, pts = cv.findChessboardCorners(img, board_pattern, board_criteria)

```