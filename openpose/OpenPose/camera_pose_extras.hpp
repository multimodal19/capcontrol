#pragma once
// OpenPose dependencies
#include <openpose/headers.hpp>

#define FPS_UPDATE_RATE 1
#define SCALE_FACTOR 4

class FPSCounter
{
public:
	void tick();
	double getFPS();

private:
	double clockToSeconds(clock_t ticks);

	clock_t startTime = clock();
	unsigned int frames = 0;
	double  frameRate = 0;
};

class SharedFrame
{
public:
	cv::Mat get();
	void set(cv::Mat);

private:
	cv::Mat frame;
	std::mutex mtx;
};
