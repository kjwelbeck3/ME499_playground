#include <string>
#include <stdio.h>
#include <iostream>
#include "serialib.h"

int main()
{
    // Connect to Port
    serialib serial;
    int statusCode = serial.openDevice("/dev/ttyUSB0", 115200);
    std::cout << "statusCode: " << statusCode << std::endl;
    if (statusCode!=1) {
        return 1;
    }


    // Send String; Read Response
    char s1[200];
    serial.writeString("1 2 3 345 6 77 \r\n");
    serial.readString(s1, '\n', 200, 5000);

    std::cout << "recvd: " << std::string(s1); // << std::endl;

    serial.closeDevice();

    return 0;
}