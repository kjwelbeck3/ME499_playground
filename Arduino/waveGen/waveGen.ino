
bool stat = false;

void setup() {
  // put your setup code here, to run once:

  //set as output ports A C L B K F H D G J
  DDRA = DDRC = DDRL = DDRB = DDRK = DDRF = DDRH = DDRD = DDRG = DDRJ = 0xFF;

  //low signal on all of them
  PORTA = PORTC = PORTL = PORTB = PORTK = PORTF = PORTH = PORTD = PORTG = PORTJ = 0x00;

  // Setting up Timer/Counter 3
  // generate a sync signal of 40khz in pin 2
  pinMode (2, OUTPUT);


  noInterrupts();           // disable all interrupts

  // OPT1: Waveform Mode to fast PWM, ClockSelect with no prescaling, Output Compare mode to clear
  TCCR3A = bit (WGM30) | bit (WGM31) | bit (COM3B1); // fast PWM, clear OC1B on compare
  TCCR3B = bit (WGM32) | bit (WGM33) | bit (CS30);   // fast PWM, no prescaler

  OCR3A = (F_CPU / 400000L) - 1; //should only be -1 but fine tunning with the scope determined that -5 gave 40kHz almost exactly
  OCR3B = (F_CPU / 400000L) / 2;

  TIMSK3 = bit (OCIE3B);




  //  // OPT2: Fast PWM, Match against ICR3 for count resolution
  //  TCCR3A = bit (WGM31) | bit (COM3B1);
  //  TCCR3B = bit (WGM33) | bit (WGM32) | bit (CS30); // CTC (non PWM), TOP defined by ICR3, no clock prescaling
  //
  //  ICR3 = (F_CPU / 40000L) -1;





  //  ICR3
  //
  //  TIMSK3 = bit (OCIE3B);
  interrupts();             // enable all interrupts

}


ISR(TIMER3_COMPB_vect) {
  if (stat == true) {
    digitalWrite(8, LOW);
    stat = false;
  }
  else {
    digitalWrite(8, HIGH);
    stat = true;
  }
}



void loop() {
  // put your main code here, to run repeatedly:

}
