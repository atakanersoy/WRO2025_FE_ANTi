import cv2
import numpy as np

# Checkerboard size (9x6 inner corners)
CHECKERBOARD = (9, 6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Lists for 3D and 2D points
objpoints = []
imgpoints = []

# Generate grid points
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Start camera
cap = cv2.VideoCapture(0) # webcam for testing
if not cap.isOpened():
    print("Error: Cannot open camera!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot retrieve frame!")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect checkerboard pattern
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if found:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, found)

    # Display frame
    cv2.imshow('Live Camera - Checkerboard Detection', frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close camera
cap.release()
cv2.destroyAllWindows()
