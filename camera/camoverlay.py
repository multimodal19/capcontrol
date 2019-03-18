import cv2
import numpy as np


def blend1(background, background_mask, overlay_part):
    # Create a masked out background image, converting to range 0.0 - 1.0
    bg_part = (background * (1 / 255.0)) * (background_mask * (1 / 255.0))
    # Add pictures together, rescale back to an 8 bit integer image
    return np.uint8(cv2.addWeighted(bg_part, 255.0, overlay_part, 255.0, 0.0))


def blend2(alpha, img1, img2):
    result = np.zeros((vheight, vwidth, 3), np.uint8)
    result[:, :, 0] = (1. - alpha) * img1[:, :, 0] + alpha * img2[:, :, 0]
    result[:, :, 1] = (1. - alpha) * img1[:, :, 1] + alpha * img2[:, :, 1]
    result[:, :, 2] = (1. - alpha) * img1[:, :, 2] + alpha * img2[:, :, 2]
    return result


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

# Get video dimensions to resize overlay
vheight, vwidth, _ = frame.shape
# Load overlay image
img = cv2.imread("filter_rage.png", -1)
# Resize image to video dimensions
overlay = cv2.resize(img,(vwidth, vheight))

# Preparation for blend1
# Split out the transparency mask from the colour info
overlay_img = overlay[:,:,:3]   # Grab the BRG planes
overlay_mask = overlay[:,:,3:]  # And the alpha plane
# Calculate the inverse mask
background_mask = 255 - overlay_mask
# Turn the masks into three channels, so we can use them as weights
overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
# Create masked out overlay, converting to floating point in range 0.0 - 1.0
overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

# Preparation for blend2
alpha = overlay[:, :, 3] / 255.0

while rval:
    result = blend1(frame, background_mask, overlay_part)
    #result = blend2(alpha, frame, overlay)

    cv2.imshow("preview", result)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
