////
////#define N_DIVS 10
////
////byte buffA[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////byte buffB[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////byte buffC[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////byte buffD[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////
////byte buffH[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////byte buffJ[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////byte buffK[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////byte buffL[N_DIVS] = {0x7C, 0x3E, 0x1F, 0x0F, 0x83, 0xC1, 0xE0, 0xF0, 0XF8};
////
////int i = 0;
////
////ISR(TIMER3_COMPB_vect){
////  PORTA = buffA[i];
////  PORTB = buffB[i];
////  PORTC = buffC[i];
////  PORTD = buffD[i];
////  
////  PORTH = buffH[i];
////  PORTJ = buffJ[i];
////  PORTK = buffK[i];
////  PORTL = buffL[i];
////
////  i = (++i) % N_DIVS ;
////  }
////
////void setup() {
////  // put your setup code here, to run once:
////
////  //set as output ports A C L B K F H D G J
////  DDRA = DDRC = DDRL = DDRB = DDRK = DDRF = DDRH = DDRD = DDRG = DDRJ = 0xFF;
////
////  //low signal on all of them
////  PORTA = PORTC = PORTL = PORTB = PORTK = PORTF = PORTH = PORTD = PORTG = PORTJ = 0xFF;
////
////  // Setting up Timer-based interrupt
////
////  pinMode(2, OUTPUT);
////  pinMode(5, OUTPUT);
////  pinMode(25, OUTPUT);
////  noInterrupts();
////
////  TCCR3A = bit (COM3B1) | bit (WGM31) | bit (WGM30); // Mode 15 (fast PWM w/ OCR3A), Clear on compare OC3B
////  TCCR3B = bit (WGM33) | bit (WGM32) | bit (CS30);  // Mode 15 (fast PWM w/ OCR3A), No prescaling
////
////  OCR3A = 400 -1; //(F_CPU/ 40000L)
////  OCR3B = 200;
////
//////  TIMSK3 = bit (OCIE3B);
////
////  interrupts();
////
////}
////
////void loop() {
////  
////}
//
//#include <avr/sleep.h>
//#include <avr/power.h>
//
//#define N_PATTERNS 32
//
//#define N_PORTS 10
//#define N_DIVS 10
//
////ports A C L B K F H D G J
//
//#define COMMAND_SWITCH 0b00000000
//#define COMMAND_DURATION 0b00110000
//#define MASK_DURATION 0b00111111
//#define COMMAND_COMMITDURATIONS 0b00010000
//
//#define WAIT(a) __asm__ __volatile__ ("nop")
//#define OUTPUT_WAVE(pointer, d)  PORTA = pointer[d*N_PORTS + 0]; PORTC = pointer[d*N_PORTS + 1]; PORTL = pointer[d*N_PORTS + 2]; PORTB = pointer[d*N_PORTS + 3]; PORTK = pointer[d*N_PORTS + 4]; PORTF = pointer[d*N_PORTS + 5]; PORTH = pointer[d*N_PORTS + 6];  PORTD = pointer[d*N_PORTS + 7]; PORTG = pointer[d*N_PORTS + 8]; PORTJ = pointer[d*N_PORTS + 9]
//
//static byte bufferA[N_PATTERNS * N_DIVS * N_PORTS];
//static byte bufferB[N_PATTERNS * N_DIVS * N_PORTS];
//
//void setup()
//{
//  //set as output ports A C L B K F H D G J
//  DDRA = DDRC = DDRL = DDRB = DDRK = DDRF = DDRH = DDRD = DDRG = DDRJ = 0xFF;
//  //low signal on all of them
//  PORTA = PORTC = PORTL = PORTB = PORTK = PORTF = PORTH = PORTD = PORTG = PORTJ = 0x00;
//
//  //clear the buffers
//  for (int i = 0; i < (N_PATTERNS * N_DIVS * N_PORTS); ++i) {
//    bufferA[i] = bufferB[i] = 0;
//  }
//
////initial pattern
//  for (int i = 0; i < (N_PORTS*N_DIVS/2); ++i){
//     bufferA[i] = 0xFF;
//  }
//  
//
//  //a patterns of 01s at pin 22, for debuging and adjusting times
// /*
//  for(int i = 0; i < N_DIVS; ++i){
//    if (i % 2 == 0){
//      bufferA[i * N_PORTS] |= 0b00001000;
//    }else{
//      bufferA[i * N_PORTS] &= 0b11110111;
//    }
//  }
// */
//  
//  // generate a sync signal of 40khz in pin 2
//  pinMode (2, OUTPUT);
//  noInterrupts();           // disable all interrupts
//  TCCR3A = bit (WGM10) | bit (WGM11) | bit (COM1B1); // fast PWM, clear OC1B on compare
//  TCCR3B = bit (WGM12) | bit (WGM13) | bit (CS10);   // fast PWM, no prescaler
//  OCR3A =  (F_CPU / 40000L) - 5; //should only be -1 but fine tunning with the scope determined that -5 gave 40kHz almost exactly
//  OCR3B = (F_CPU / 40000L) / 2;
//  interrupts();             // enable all interrupts
//
//  //sync in signal at pin 3
//  pinMode(3, INPUT_PULLUP); //please connect pin3 to pin 2
//
//
//  // disable everything that we do not need
//  ADCSRA = 0;  // ADC
//  power_adc_disable ();
//  power_spi_disable();
//  power_twi_disable();
//  power_timer0_disable();
//  power_usart1_disable();
//  power_usart2_disable();
//  power_usart3_disable();
//  //power_usart0_disable();
//
//  Serial.begin(115200);
//
//  byte bReceived = 0;
//  bool byteReady = false;
//  bool isSwitch = false;
//  bool isPatternForMe = false;
//  bool isDuration = false;
//  bool isCommitDurations = false;
//  byte nextMsg = 0;
//  int writtingIndex = 0;
//
//  bool emittingA = true;
//  byte* emittingPointerH = & bufferA[0];
//  byte* emittingPointerL = & bufferA[N_PORTS * N_DIVS / 2];
//  byte* emittingPointerZeroH = & bufferA[0];
//  byte* emittingPointerZeroL = & bufferA[N_PORTS * N_DIVS / 2];
//  byte* readingPointerH = & bufferB[0];
//  byte* readingPointerL = & bufferB[N_PORTS * N_DIVS / 2];
//
//  byte durations[N_PATTERNS];
//  byte durationsBuffer[N_PATTERNS];
//  for(int i = 0; i < N_PATTERNS; ++i){
//    durations[i] = durationsBuffer[i] = 0;
//  }
//  durations[0] = durationsBuffer[0] = 1;
//
//  byte currentPattern = 0;
//  byte currentPeriods = 0;
//  byte durationsPointer = 0;
//  byte currentDuration = 0;
//  bool patternComplete = false;
//  bool lastPattern = false;
//  byte nextPattern = 0;
//  byte nextDuration = 0;
//  bool returnToFirstPattern = false;
//LOOP:
//  while (PINE & 0b00100000); //wait for pin 3 (E5 Sync In) to go low
//
//  OUTPUT_WAVE(emittingPointerH, 0); byteReady = Serial._dataAvailable(); 
//  OUTPUT_WAVE(emittingPointerH, 1); bReceived = Serial._peekData(); 
//  OUTPUT_WAVE(emittingPointerH, 2); isSwitch = bReceived == COMMAND_SWITCH; isCommitDurations = bReceived == COMMAND_COMMITDURATIONS; 
//  OUTPUT_WAVE(emittingPointerH, 3); isPatternForMe = (bReceived & 0b00001111) == 1; ++currentPeriods; 
//  OUTPUT_WAVE(emittingPointerH, 4); nextMsg =  bReceived - 1; 
//  OUTPUT_WAVE(emittingPointerL, 0); isDuration = (bReceived & MASK_DURATION) == COMMAND_DURATION; nextPattern = currentPattern + 1;
//  OUTPUT_WAVE(emittingPointerL, 1); nextDuration = durations[nextPattern]; 
//  OUTPUT_WAVE(emittingPointerL, 2); patternComplete = (currentPeriods == durations[currentPattern]); 
//  OUTPUT_WAVE(emittingPointerL, 3); lastPattern = (currentPattern+1 == N_PATTERNS); returnToFirstPattern = nextDuration == 0;
//  OUTPUT_WAVE(emittingPointerL, 4); 
//  
//if (patternComplete){
//  currentPeriods = 0;
//  ++currentPattern;
//  if (lastPattern  || returnToFirstPattern){
//    currentPattern = 0;
//    emittingPointerH = emittingPointerZeroH;
//    emittingPointerL = emittingPointerZeroL;
//  }else{
//    emittingPointerH += (N_DIVS * N_PORTS);
//    emittingPointerL += (N_DIVS * N_PORTS);
//  } 
//}
//  
//  if (byteReady) {
//    if ( isSwitch ) {
//      Serial.write( COMMAND_SWITCH );
//      emittingA = !emittingA;
//      if (emittingA) {
//        emittingPointerH = & bufferA[0];
//        emittingPointerL = & bufferA[N_PORTS * N_DIVS / 2];
//        readingPointerH = & bufferB[0];
//        readingPointerL = & bufferB[N_PORTS * N_DIVS / 2];
//      } else {
//        emittingPointerH = & bufferB[0];
//        emittingPointerL = & bufferB[N_PORTS * N_DIVS / 2];
//        readingPointerH = & bufferA[0];
//        readingPointerL = & bufferA[N_PORTS * N_DIVS / 2];
//      }
//      emittingPointerZeroH = emittingPointerH;
//      emittingPointerZeroL = emittingPointerL;
//      
//      writtingIndex = 0;
//      durationsPointer = 0;
//    } else if ( isPatternForMe ) {
//        if (writtingIndex % 2 == 0) {
//          readingPointerH[writtingIndex / 2] = bReceived & 0xF0;
//        } else {
//          readingPointerH[writtingIndex / 2] |= (bReceived >> 4);
//        }
//        ++writtingIndex;
//    } else if (isDuration){
//        Serial.write( bReceived );
//        if (durationsPointer % 4 == 0) {
//          durationsBuffer[durationsPointer / 4] = bReceived & 0b11000000;
//        } else {
//          durationsBuffer[durationsPointer / 4] |= (bReceived & 0b11000000) >> (durationsPointer % 4 * 2);
//        }
//        ++durationsPointer;
//    }else if (isCommitDurations){
//      Serial.write( bReceived );
//      for(int i = 0; i<N_PATTERNS; ++i){
//        durations[i] = durationsBuffer[i];
//      }
//      durationsPointer = 0;
//    } else {
//      Serial.write( nextMsg );
//    }
//    Serial._discardByte();
//  }
//
//  goto LOOP;
//
//}
//
//void loop() {}


void setup(){

//DDRA = 0xFF;
//
//PORTA = 0xFF; 
pinMode(23, OUTPUT);
digitalWrite(23, HIGH);
}
void loop() {}
