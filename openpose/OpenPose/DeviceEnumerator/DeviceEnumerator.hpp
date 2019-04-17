#pragma once

// SOURCE: https://github.com/studiosi/OpenCVDeviceEnumerator

#include <Windows.h>
#include <dshow.h>

#pragma comment(lib, "strmiids")

#include <map>
#include <string>

struct Device
{
	int id; // This can be used to open the device in OpenCV
	std::string devicePath;
	std::string deviceName; // This can be used to show the devices to the user
};

class DeviceEnumerator
{

public:

	static std::map<int, Device> getDevicesMap(const GUID deviceClass);
	static std::map<int, Device> getVideoDevicesMap();
	static std::map<int, Device> getAudioDevicesMap();

private:

	static std::string ConvertBSTRToMBS(BSTR bstr);
	static std::string ConvertWCSToMBS(const wchar_t* pstr, long wslen);

};