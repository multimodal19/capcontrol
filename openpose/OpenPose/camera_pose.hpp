// Command-line user intraface
#include <openpose/flags.hpp>
#include <camera_pose_extras.hpp>
#include <DeviceEnumerator/DeviceEnumerator.hpp>

// Down-scale factor for raw image
#define SCALE_FACTOR	4

// Number of faceKeyPoints
#define FACE_POINTS		70
// Default renderThreshold from WrapperStructFace.hpp
#define FACE_THRESHOLD	0.4f
// Some interesting points
#define FACE_LEFT_EAR	3 * 0
#define FACE_RIGHT_EAR	3 * 16
#define FACE_NOSE_TIP	3 * 30

// Number of handKeyPoints
#define HAND_POINTS		21
// Default renderThreshold from WrapperStructHand.hpp
#define HAND_THRESHOLD	0.2f
// Index finger
#define HAND_INDEX		3 * 8

// Directions for face
#define DIR_LEFT -1
#define DIR_STRAIGHT 0
#define DIR_RIGHT 1

#define N_CAMERAS 2
