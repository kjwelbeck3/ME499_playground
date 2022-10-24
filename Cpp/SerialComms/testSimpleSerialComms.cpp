#include "SimpleSerialComms.hpp"
#include <string>
#include <stdio.h>
#include <iostream>

int main(void){

    SimpleSerialComms t{115200};
    int sequence[] = {123, 34, 5, 12, 45, 12, 12, 12, 12, 12, 12, 12, 12, 12};
    string responseString = t.sendWaveSequence(sequence, (sizeof sequence / sizeof sequence[0]));

    std::cout << responseString;


    return 0;
}

// Run with:
// g++ -Wall -std=c++2a testSimpleSerialComms.cpp SimpleSerialComms.cpp serialib.cpp -o testClass
// ./testClass