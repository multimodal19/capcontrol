#pragma once
// OpenPose dependencies
#include <openpose/headers.hpp>
#include <zmq.hpp>

#define FPS_UPDATE_RATE 1

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

class ZMQPublisher
{
public:
	ZMQPublisher(std::string topic, std::string addr = "localhost:4000");
	~ZMQPublisher();
	void send(std::string msg);

private:
	zmq::context_t context;
	zmq::socket_t socket;
	std::string topic;
};

// Callback type for delivering messages
typedef void(*cb_T)(std::string);

class ZMQSubscriber
{
public:
	ZMQSubscriber(std::string topic, cb_T callback, std::string addr = "localhost:4001");
	~ZMQSubscriber();

private:
	zmq::context_t context;
	zmq::socket_t socket;
	std::string topic;
	cb_T callback;
	std::thread thread;
	bool stopped = false;
	void receiveLoop();
};
