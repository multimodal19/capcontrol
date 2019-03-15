import cv2


cv2.namedWindow("preview", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(
    "preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Get window dimensions
x, y, width, height = cv2.getWindowImageRect("preview")

# Set up video capture using the window dimensions to get nice scaling
vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# Check video capture by getting first frame
if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

font = cv2.FONT_HERSHEY_SIMPLEX
while rval:
    cv2.putText(
        frame, "Whatever", (0, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.ellipse(frame, (150, 200), (100, 50), 0, 0, 180, 255, -1)
    cv2.circle(frame, (350, 200), 63, (0, 0, 255), -1)
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
