#include <camera_pose.hpp>


// ============================ Shared variables ============================
FPSCounter fpsCounter_op;
std::vector<SharedFrame*> sharedFrames;
SharedFrame sharedFrame_op;
ZMQPublisher* publisher;
std::vector<std::thread> camThreads;

bool stopped = false;
bool mirrored = true;
bool cameraReady = false;
cv::Rect screenSize;
int turnThreshold = 10;
int faceDirection = DIR_STRAIGHT;


/*
Determine face direction based on distance between ears and nose. If the face
is turned, the "hidden" ear point is nearly at the same place as the nose.
Thus the distance between them gets very small, while the distance to the
other ear increases with the turn angle.
*/
void calcFaceDirection(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>> & datumsPtr)
{
	auto faceKeyPoints = datumsPtr->at(0)->faceKeypoints;

	// Skip if accuracy is too low
	if (faceKeyPoints[FACE_NOSE_TIP + 2] < FACE_THRESHOLD) return;

	// Get horizontal distances between important points
	int leftDist = faceKeyPoints[FACE_NOSE_TIP] - faceKeyPoints[FACE_LEFT_EAR];
	int rightDist = faceKeyPoints[FACE_RIGHT_EAR] - faceKeyPoints[FACE_NOSE_TIP];

	// Reverse direction if not in mirrored mode
	if (!mirrored) {
		std::swap(leftDist, rightDist);
	}

	//std::cout << leftDist << ", " << rightDist << std::endl;

	if (leftDist < turnThreshold && rightDist > turnThreshold) {
		if (faceDirection != DIR_LEFT) {
			faceDirection = DIR_LEFT;
			std::cout << "looking left" << std::endl;
			publisher->send("face left");
		}
	}
	else if (leftDist > turnThreshold && rightDist < turnThreshold) {
		if (faceDirection != DIR_RIGHT) {
			faceDirection = DIR_RIGHT;
			std::cout << "looking right" << std::endl;
			publisher->send("face right");
		}
	}
	else if (faceDirection != DIR_STRAIGHT)
	{
		faceDirection = DIR_STRAIGHT;
		std::cout << "looking straight" << std::endl;
		publisher->send("face straight");
	}
}

/*
Determine Index finger position of both hands.
*/
void calcIndexPosition(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>> & datumsPtr)
{
	for (size_t i = 0; i < 2; i++)
	{
		auto handKeyPoints = datumsPtr->at(0)->handKeypoints[i];

		// Skip if no hand detected
		if (handKeyPoints.getSize(0) == 0) continue;
		// Skip if values are unreliable
		if (handKeyPoints[HAND_INDEX + 2] < HAND_THRESHOLD) continue;

		// Get index finger position scaled back to full screen
		int ix = handKeyPoints[HAND_INDEX] * SCALE_FACTOR;
		int iy = handKeyPoints[HAND_INDEX + 1] * SCALE_FACTOR;
		
		// Take mirroring into account to figure out correct hand
		std::string which = (mirrored ? 1 - i : i) == 0 ? "left" : "right";

		//std::cout << which << ix << ", " << iy << std::endl;

		// Send position in format: hand $which $ix $iy
		// Reverse hands if in mirrored mode
		std::stringstream ss;
		ss << "hand " + which + " " << ix << " " << iy;
		publisher->send(ss.str());
	}
}

void evaluateKeypoints(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>>& datumsPtr)
{
	try
	{
		// Example: How to use the pose keypoints
		if (datumsPtr != nullptr && !datumsPtr->empty())
		{
			// Skip if no faces detected
			if (datumsPtr->at(0)->faceKeypoints.getSize(0) > 0) {
				calcFaceDirection(datumsPtr);
			}
			calcIndexPosition(datumsPtr);
		}
		else
			op::log("Nullptr or empty datumsPtr found.", op::Priority::High);
	}
	catch (const std::exception& e)
	{
		op::error(e.what(), __LINE__, __FUNCTION__, __FILE__);
	}
}

void openPose() {
	try
	{
		// Configuring OpenPose
		op::log("Configuring OpenPose...", op::Priority::High);
		op::Wrapper opWrapper{ op::ThreadManagerMode::Asynchronous };

		// Limit to 1 person
		op::WrapperStructPose poseConfig;
		poseConfig.numberPeopleMax = 1;
		opWrapper.configure(poseConfig);

		// Separate output display
		//opWrapper.configure(op::WrapperStructGui{ op::DisplayMode::Display2D });

		// Add hand and face
		opWrapper.configure(op::WrapperStructFace{ true });
		opWrapper.configure(op::WrapperStructHand{ true });
		// Set to single-thread (for sequential processing and/or debugging and/or reducing latency)
		// opWrapper.disableMultiThreading();

		int width = screenSize.width / SCALE_FACTOR;
		int height = screenSize.height / SCALE_FACTOR;

		// Starting OpenPose
		op::log("Starting thread(s)...", op::Priority::High);
		opWrapper.start();

		while (!stopped) {
			// Process and display image
			auto imageToProcess = sharedFrames[0]->get();
			cv::resize(imageToProcess, imageToProcess, cv::Size{ width, height });
			auto datumProcessed = opWrapper.emplaceAndPop(imageToProcess);
			if (datumProcessed != nullptr)
			{
				// Do something with keypoints
				evaluateKeypoints(datumProcessed);

				sharedFrame_op.set(datumProcessed->at(0)->cvOutputData);
				fpsCounter_op.tick();
			}
			else
				op::log("Frame could not be processed.", op::Priority::High);
		}
	}
	catch (const std::exception& e)
	{
		op::error(e.what(), __LINE__, __FUNCTION__, __FILE__);
	}
}


/*
Ask user to choose one from the installed cameras
*/
int chooseCamera() {
	// Print information about the available cameras
	std::cout << "Available cameras:" << std::endl;
	auto devices = DeviceEnumerator::getVideoDevicesMap();
	for (auto const &device : devices) {
		std::cout << "(" << device.first << ") " + device.second.deviceName << std::endl;
	}

	// Prompt user to select a camera
	int deviceCount = devices.size() - 1;
	std::cout << "Select a camera (0 to " << deviceCount << "): ";
	int index = 0;
	if (!(std::cin >> index) || index < 0 || index > deviceCount) {
		// Exit on invalid input
		exit(EXIT_FAILURE);
	}

	return index;
}

/*
Continuosly read from camera and store current frame
*/
void cameraLoop(cv::VideoCapture vc, int i) {
	cv::Mat frame;

	while (!stopped)
	{
		vc >> frame;
		if (mirrored) {
			cv::flip(frame, frame, 1);
		}
		sharedFrames[i]->set(frame.clone());
	}
}

/*
Convenience method for cv::putText
*/
void cvWrite(cv::Mat frame, std::string text, int y = 50) {
	double factor = (double)frame.rows / screenSize.height;

	y *= factor;
	double font_size = 2 * factor;
	int font = cv::FONT_HERSHEY_SIMPLEX;
	cv::Scalar font_color = cv::Scalar{ 255, 255, 255 };
	cv::putText(frame, text, cv::Point{ 0, y }, font, font_size, font_color, 2, cv::LINE_AA);
}


/*
Set up camera stream & read from camera
*/
void startCamera(int i, int cameraIndex, int width, int height) {
	// Attempt to read from camera multiple times (necessary for USB/IP)
	for (size_t _i = 0; _i < 10; _i++)
	{
		// Use DirectShow camera feed for full image
		cv::VideoCapture vc(cameraIndex + cv::CAP_DSHOW);
		// Set up video capture using the window dimensions to get nice scaling
		vc.set(cv::CAP_PROP_FRAME_WIDTH, width);
		vc.set(cv::CAP_PROP_FRAME_HEIGHT, height);

		// Read test frame and restart if unsuccessful
		if (!vc.isOpened()) continue;
		cv::Mat frame;
		vc >> frame;
		if (frame.empty()) continue;

		if (i == 0) {
			cameraReady = true;
		}

		// Success, start reading from camera
		cameraLoop(vc, i);
		return;
	}

	std::cerr << "Cannot access camera #" << i << " (" << cameraIndex << ")!" << std::endl;
}


void setupCapture() {
	// Create fullscreen preview window
	cv::namedWindow("SizeProbe", cv::WINDOW_NORMAL);
	cv::setWindowProperty("SizeProbe", cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN);

	// Get window dimensions
	screenSize = cv::getWindowImageRect("SizeProbe");
	int width = screenSize.width;
	int height = screenSize.height;

	// Destroy window again, to avoid gray window staying behind
	cv::destroyWindow("SizeProbe");

	int n_cameras = 1;
	std::cout << "How many cameras? ";
	if (!(std::cin >> n_cameras) || n_cameras < 1) {
		exit(EXIT_FAILURE);
	}

	// Ask which cameras to use, then start them
	std::cout << std::endl;
	std::vector<int> ids;
	for (size_t i = 0; i < n_cameras; i++)
	{
		std::cout << "Choose camera #" << i << std::endl;
		ids.push_back(chooseCamera());
		std::cout << std::endl;
	}
	std::cout << "Starting cameras!" << std::endl;
	for (size_t i = 0; i < n_cameras; i++)
	{
		sharedFrames.push_back(new SharedFrame);
		camThreads.push_back(std::thread(&startCamera, i, ids[i], width, height));
	}

	// Store placeholder images to avoid crashes
	cv::Mat placeholder(1080, 1920, 16, cv::Scalar(0,0,0));
	cvWrite(placeholder, "Image not ready", 100);
	for (size_t i = 0; i < n_cameras; i++)
	{
		sharedFrames[i]->set(placeholder);
	}
	sharedFrame_op.set(placeholder);
}


void camWindow() {
	std::string title = OPEN_POSE_NAME_AND_VERSION + " - PREVIEW";
	bool show_original = true;
	bool show_fps = false;
	int i_camera = 0;

	// Initialize camera sources
	setupCapture();

	// Start OpenPose thread
	std::cout << "Starting OpenPose" << std::endl;
	std::thread op_thread = std::thread(&openPose);

	// Wait for main camera before proceeding
	while (!cameraReady) {
		Sleep(100);
	}
	
	cv::Mat frame;
	FPSCounter fpsCounter;

	// Create fullscreen preview window
	cv::namedWindow(title, cv::WINDOW_NORMAL);
	cv::setWindowProperty(title, cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN);

	while (!stopped)
	{
		// Either use raw image from camera or processed one from OpenPose
		frame = show_original ? sharedFrames[i_camera]->get().clone() : sharedFrame_op.get().clone();
		fpsCounter.tick();

		// Show window & OpenPose FPS
		if (show_fps) {
			std::stringstream ss;
			double fps = fpsCounter.getFPS();
			double fps_o = fpsCounter_op.getFPS();
			ss << std::fixed << std::setprecision(1) << fps << " - " << fps_o;
			cvWrite(frame, ss.str());
		}
		
		// Show frame & check for keypress
		cv::imshow(title, frame);
		int key = cv::waitKey(10) & 0xFF;

		switch (key)
		{
		case 27: // escape
			cv::destroyWindow(title);
			stopped = true;
			break;
		case ' ': // space
			show_original = !show_original;
			break;
		case 'f':
			show_fps = !show_fps;
			break;
		case 'm':
			mirrored = !mirrored;
			break;
		case 'w':
			turnThreshold += 1;
			std::cout << "new threshold: " << turnThreshold << std::endl;
			break;
		case 's':
			turnThreshold -= 1;
			std::cout << "new threshold: " << turnThreshold << std::endl;
			break;
		case 'c':
			// Loop through available cameras
			i_camera = (i_camera + 1) % camThreads.size();
			break;
		default:
			break;
		}
	}

	// Join all threads
	op_thread.join();
	for (auto &thread : camThreads)
	{
		thread.join();
	}
}

int main(int argc, char *argv[])
{
	if (argc < 3) {
		std::cout << "No arguments specified, using default values!" << std::endl;
		publisher = new ZMQPublisher("openpose");
	}
	else {
		std::stringstream ss;
		ss << argv[1] << ":" << argv[2];
		publisher = new ZMQPublisher("openpose", ss.str());
	}

	camWindow();
}
