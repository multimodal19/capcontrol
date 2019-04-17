#include <camera_pose_extras.hpp>

double FPSCounter::clockToSeconds(clock_t ticks)
{
	return (ticks / (double)CLOCKS_PER_SEC);
}

void FPSCounter::tick()
{
	frames++;
	clock_t now = clock();
	double deltaTime = clockToSeconds(now - startTime);

	// Calculate average over ~1 second
	if (deltaTime > FPS_UPDATE_RATE)
	{
		frameRate = (double)frames / deltaTime;
		frames = 0;
		startTime = now;
	}
}

double FPSCounter::getFPS()
{
	return frameRate;
}


cv::Mat SharedFrame::get()
{
	mtx.lock();
	cv::Mat mat = frame;
	mtx.unlock();
	return mat;
}

void SharedFrame::set(cv::Mat mat)
{
	mtx.lock();
	frame = mat;
	mtx.unlock();
}


ZMQPublisher::ZMQPublisher(std::string topic, std::string addr)
// Prepare context and socket
	: context(1), socket(context, ZMQ_PUB)
{
	this->topic = topic;
	std::cout << "Connecting publisher to " + addr << std::endl;
	socket.connect("tcp://" + addr);
}

ZMQPublisher::~ZMQPublisher()
{
	socket.close();
	context.close();
}

void ZMQPublisher::send(std::string msg)
{
	// Send message in format: topic!message
	std::string message = topic + "!" + msg;
	zmq::message_t request(message.data(), message.size());
	socket.send(request);
}

ZMQSubscriber::ZMQSubscriber(std::string topic, cb_T callback, std::string addr)
// Prepare context and socket
	: context(1), socket(context, ZMQ_SUB)
{
	this->topic = topic;
	this->callback = callback;
	std::cout << "Connecting subscriber to " + addr << std::endl;
	socket.setsockopt(ZMQ_SUBSCRIBE, topic.data(), topic.size());
	socket.connect("tcp://" + addr);

	thread = std::thread(&ZMQSubscriber::receiveLoop, this);
}

ZMQSubscriber::~ZMQSubscriber()
{
	stopped = true;
	socket.close();
	context.close();
	thread.join();
}

void ZMQSubscriber::receiveLoop()
{
	zmq::message_t message;
	std::string msg;
	while (!stopped)
	{
		try
		{
			// Receive message, cast to string, strip off topic & call callback
			socket.recv(&message);
			msg = std::string(static_cast<char*>(message.data()), message.size());
			callback(msg.substr(topic.size() + 1));
		}
		catch (zmq::error_t& e)
		{
		}
	}
}
