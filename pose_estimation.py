import numpy as np
import cv2 as cv

# intrinsic values for my camera - from camera calibration
K = np.array([[999.3943898, 0, 661.313247],
             [0, 1000.30283, 345.830421],
             [0, 0, 1]])
distortion_coefficient = np.array([0.101053364, -1.08734546, 0.00605023966, 0.00177100243, 3.69476778])

# chessboard patterns
board_pattern = (8, 6)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

# inserting crown shape
box_upper = board_cellsize * np.array([[2, 4, 0], [2, 2, 0], [3, 3, 0], [4, 2, 0], [5, 3, 0], [6, 2, 0], [6, 4, 0]])
box_lower = board_cellsize * np.array([[2, 4, -1], [2, 2, -1], [3, 3, -1], [4, 2, -1], [5, 3, -1], [6, 2, -1], [6, 4, -1]])

obj_point = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

video_file = "data/chessboard1.mp4"
video = cv.VideoCapture(video_file)

while True:
    valid, img = video.read()
    if not valid:
        break
    
    complete, pts = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if complete:
        _ , rvec, tvec = cv.solvePnP(obj_point, pts, K, distortion_coefficient)
        
        line_upper, _ = cv.projectPoints(box_upper, rvec, tvec, K, distortion_coefficient)
        line_lower, _ = cv.projectPoints(box_lower, rvec, tvec, K, distortion_coefficient)      
        cv.polylines(img, [np.int32(line_upper)], True, (255, 255, 0), 2)
        cv.polylines(img, [np.int32(line_lower)], True, (0, 255, 255), 2)
        for b, t in zip(line_lower, line_upper):
            cv.line(img, np.int32(b.flatten()), np.int32(t.flatten()), (0, 0, 255), 2)
        
        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f"XYZ : [{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}]"
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0))
        
    cv.imshow("AR with chessboard", img)
    key = cv.waitKey(10)
    if key == ord(" "):
        key = cv.waitKey()
    elif key == 27:
        break
    
video.release()
cv.destroyAllWindows()