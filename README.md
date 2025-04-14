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
valid, img = video.read()
...
complete, pts = cv.findChessboardCorners(img, board_pattern, board_criteria)
```

3. Find a translation vector and a rotation vector to find camera position.

```bibtex
_ , rvec, tvec = cv.solvePnP(obj_point, pts, K, distortion_coefficient)
```

4. Draw a line between a point and a point to make a 3-dimensional crown figure.

```bibtex
line_upper, _ = cv.projectPoints(box_upper, rvec, tvec, K, distortion_coefficient)
line_lower, _ = cv.projectPoints(box_lower, rvec, tvec, K, distortion_coefficient)
cv.polylines(img, [np.int32(line_upper)], True, (255, 255, 0), 2)
cv.polylines(img, [np.int32(line_lower)], True, (0, 255, 255), 2)
```

5. Additional: Mark a camera's XYZ value using cv.Rodrigues().

```bibtex
R, _ = cv.Rodrigues(rvec)
p = (-R.T @ tvec).flatten()
info = f"XYZ : [{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}]"
```

## Results
![Image](https://github.com/user-attachments/assets/dd9407b8-182c-46c9-89ae-eb0795382a47)