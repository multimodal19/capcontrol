#include <camera_pose_extras.hpp>

double FPSCounter::clockToSeconds(clock_t ticks) {
	return (ticks / (double)CLOCKS_PER_SEC);
}

void FPSCounter::tick()
{
	frames++;
	clock_t now = clock();
	double deltaTime = clockToSeconds(now - startTime);

	// Calculate average over ~1 second
	if (deltaTime > FPS_UPDATE_RATE) {
		frameRate = (double)frames / deltaTime;
		frames = 0;
		startTime = now;
	}
}

double FPSCounter::getFPS()
{
	return frameRate;
}


cv::Mat SharedFrame::get() {
	mtx.lock();
	cv::Mat mat = frame;
	mtx.unlock();
	return mat;
}

void SharedFrame::set(cv::Mat mat) {
	mtx.lock();
	frame = mat;
	mtx.unlock();
}
