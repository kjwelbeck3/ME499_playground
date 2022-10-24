#include <string>
#include <stdio.h>
#include "serialib.h"


using std::string;

constexpr int default_baud = 115200;
constexpr int cStringMaxLengthChars = 200;
constexpr int responseMaxLengthBytes = 200;
constexpr int serialReadTimeout_ms = 5000;

class SimpleSerialComms
{
  string _port;
  int _baud;
  serialib serial;

public:

  /**************************
   * Constructors
  **************************/
  
  SimpleSerialComms(string port, int baud);
  

  SimpleSerialComms(string port);

  SimpleSerialComms(int baud);

  SimpleSerialComms();

  // // virtual ~SimpleSerialComms();

  /**************************
   * Accessors and (?) Mutators
  **************************/

  string getPortName();

  int getBaudrate();

  // void testSerial();

  /**************************
   * Accessors and (?) Mutators
  **************************/
  string sendWaveSequence(int seq[], int seqLength);


};

// NEED TO ADD A DESTRUCTOR FUNCTION to close the serial comms