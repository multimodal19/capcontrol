// Command-line user intraface
#include <openpose/flags.hpp>
#include <camera_pose_extras.hpp>


// ============================ Shared variables ============================
FPSCounter fpsCounter_op;
SharedFrame sharedFrame;
SharedFrame sharedFrame_op;

bool stopped = false;
cv::Rect screenSize;


// Source: OpenPose example file 02_whole_body_from_image_default.cpp
void printKeypoints(const std::shared_ptr<std::vector<std::shared_ptr<op::Datum>>>& datumsPtr)
{
	try
	{
		// Example: How to use the pose keypoints
		if (datumsPtr != nullptr && !datumsPtr->empty())
		{
			op::log("Body keypoints: " + datumsPtr->at(0)->poseKeypoints.toString(), op::Priority::High);
			op::log("Face keypoints: " + datumsPtr->at(0)->faceKeypoints.toString(), op::Priority::High);
			op::log("Left hand keypoints: " + datumsPtr->at(0)->handKeypoints[0].toString(), op::Priority::High);
			op::log("Right hand keypoints: " + datumsPtr->at(0)->handKeypoints[1].toString(), op::Priority::High);
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
			auto imageToProcess = sharedFrame.get();
			cv::resize(imageToProcess, imageToProcess, cv::Size{ width, height });
			auto datumProcessed = opWrapper.emplaceAndPop(imageToProcess);
			if (datumProcessed != nullptr)
			{
				cv::Mat res = datumProcessed->at(0)->cvOutputData;

				// Do something with keypoints
				//printKeypoints(datumProcessed);

				sharedFrame_op.set(res);
				// op::log("Frame processed", op::Priority::High);
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


void camWindow() {
	std::string title = OPEN_POSE_NAME_AND_VERSION + " - PREVIEW";
	bool mirror = true;
	bool show_original = true;
	bool show_fps = true;

	// Create fullscreen preview window
	cv::namedWindow(title, cv::WINDOW_NORMAL);
	cv::setWindowProperty(title, cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN);
	
	// Get window dimensions
	screenSize = cv::getWindowImageRect(title);
	int width = screenSize.width;
	int height = screenSize.height;

	// Use DirectShow camera feed for full image
	cv::VideoCapture vc = cv::VideoCapture(0 + cv::CAP_DSHOW);
	// Set up video capture using the window dimensions to get nice scaling
	vc.set(cv::CAP_PROP_FRAME_WIDTH, width);
	vc.set(cv::CAP_PROP_FRAME_HEIGHT, height);
	//vc.set(cv::CAP_PROP_AUTOFOCUS, 1);
	//vc.set(cv::CAP_PROP_FPS, 60);

	if (!vc.isOpened()) {
		std::cerr << "Cannot access camera!";
		return;
	}

	// init
	{
		cv::Mat frame;
		vc >> frame;
		if (mirror) {
			cv::flip(frame, frame, 1);
		}

		sharedFrame.set(frame.clone());
		sharedFrame_op.set(frame.clone());
	}

	// Start OpenPose thread
	std::thread op_thread = std::thread(&openPose);
	
	
	cv::Mat frame;
	FPSCounter fpsCounter;
	int font = cv::FONT_HERSHEY_SIMPLEX;
	cv::Scalar font_color = cv::Scalar{ 255, 255, 255 };

	while (true)
	{
		// Read next frame
		vc >> frame;
		if (mirror) {
			cv::flip(frame, frame, 1);
		}
		sharedFrame.set(frame.clone());
		fpsCounter.tick();

		// Either use raw image from camera or processed one from OpenPose
		cv::Mat window_frame = show_original ? frame : sharedFrame_op.get().clone();

		// Show window & OpenPose FPS
		if (show_fps) {
			std::stringstream ss;
			double fps = fpsCounter.getFPS();
			double fps_o = fpsCounter_op.getFPS();
			ss << std::fixed << std::setprecision(1) << fps << " - " << fps_o;

			double font_size = 4;
			int y = 100;
			if (!show_original) {
				font_size /= SCALE_FACTOR;
				y /= SCALE_FACTOR;
			}
			cv::putText(window_frame, ss.str(), cv::Point{ 0, y }, font, font_size, font_color, 2, cv::LINE_AA);
		}
		
		// Show frame & check for keypress
		cv::imshow(title, window_frame);
		int key = cv::waitKey(10) & 0xFF;

		switch (key)
		{
		case 27: // escape
			cv::destroyWindow(title);
			vc.release();
			stopped = true;
			op_thread.join();
			return;
		case ' ': // space
			show_original = !show_original;
			break;
		case 'f':
			show_fps = !show_fps;
			break;
		case 'm':
			mirror = !mirror;
			break;
		default:
			break;
		}
	}
}

int main(int argc, char *argv[])
{
	camWindow();
}
