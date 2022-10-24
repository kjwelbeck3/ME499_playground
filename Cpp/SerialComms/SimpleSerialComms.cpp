#include "SimpleSerialComms.hpp"

SimpleSerialComms::SimpleSerialComms(string port, int baud)
    : _port(port), _baud(baud)
{
    serial.openDevice(port.c_str(), _baud);
    // Need to Verify sucess 
}

SimpleSerialComms::SimpleSerialComms(string port)
    : SimpleSerialComms{port, default_baud} {}

SimpleSerialComms::SimpleSerialComms(int baud)
    : SimpleSerialComms{"/dev/ttyUSB0", baud} {}

SimpleSerialComms::SimpleSerialComms()
    : SimpleSerialComms("/dev/ttyUSB0", default_baud) {}

string SimpleSerialComms::sendWaveSequence(int seq[], int seqLength)
{
    string command;
    char responseFrom[cStringMaxLengthChars];

    int i = 0;
    for (i = 0; i < seqLength; i++)
    {
        command.append(std::to_string(seq[i]));
        command.append(" ");
    }
    command.append("\r\n");

    serial.writeString(command.c_str());

    serial.readString(responseFrom, '\n', responseMaxLengthBytes, serialReadTimeout_ms);

    return string(responseFrom);
}


