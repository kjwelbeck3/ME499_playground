#include <string>
#include <stdio.h>
#include <iostream>

// Linux Headers
#include <fcntl.h>   // Contains file controls like O_RDWR
#include <errno.h>   // Error integer and strerror() function
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h>  // write(), read(), close()

// using namespace std;

int main()
{

    // int serial_port = open("/dev/ttyUS0B", O_RDWR);

    // //check for errors
    // if (serial_port < 0)
    // {
    //     printf("Error %i from open: %s\n", errno, strerror(errno));
    // }

    // // Create new termios struct, we call it 'tty' for convention
    // // No need for "= {0}" at the end as we'll immediately write the existing
    // // config to this struct
    // struct termios tty;

    // // Read in existing settings, and handle any error
    // // NOTE: This is important! POSIX states that the struct passed to tcsetattr()
    // // must have been initialized with a call to tcgetattr() overwise behaviour
    // // is undefined
    // if (tcgetattr(serial_port, &tty) != 0)
    // {
    //     printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
    // }

    std::cout << "Hello World\r\n";    

    return 0;
}


// RUNTIME INSTRUCTION
// // g++ -Wall -std=c++2a testSerial.cpp serialib.cpp -o test-exe

