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


ZMQPublisher::ZMQPublisher(std::string topic, std::string addr)
	// Prepare context and socket
	: context(1), socket(context, ZMQ_PUB)
{
	this->topic = topic;
	std::cout << "Connecting to the coordinator at " + addr << std::endl;
	socket.connect("tcp://" + addr);
}

ZMQPublisher::~ZMQPublisher()
{
	socket.close();
}

void ZMQPublisher::send(std::string msg)
{
	// Send message in format: topic!message
	std::string message = topic + "!" + msg;
	zmq::message_t request(message.data(), message.size());
	socket.send(request);
}
