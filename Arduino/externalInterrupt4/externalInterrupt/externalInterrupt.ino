// Goal: External/Timer-based interrupt service routines

// MSK Registers: to select which pins trigger interrupts
//

bool stat = false;


void setup() {
  // put your setup code here, to run once:

  // External interrupt on INT4 == D2 == OC3B
  // On any edge

  // DIRECTION AND LOW

  //set as output ports A C L B K F H D G J
  DDRA = DDRC = DDRL = DDRB = DDRK = DDRF = DDRH = DDRD = DDRG = DDRJ = 0xFF;

  //low signal on all of them
  PORTA = PORTC = PORTL = PORTB = PORTK = PORTF = PORTH = PORTD = PORTG = PORTJ = 0x00;

  pinMode(13, OUTPUT);

  noInterrupts();

  //External Interrupt Control Register B --> sense control bits
  EICRB = bit (ISC40); // Any logical change
  //EICRB = bit (ISC41); // falling edge
  //EICRB = bit (ISC40) | bit (ISC41); // rising edge

  // External Interrupt Mask Register --> enable bits
  EIMSK = bit (INT4);

  // External Interrupt Flag Register --> status of interupt
  // Auto cleared, but can be manually cleared by writing a logical 1
  // ie EIFR = bit (INTF4)

  interrupts();
}


// INTERRUPT VECTOR
ISR(INT4_vect) {
  if (stat == true) {
    digitalWrite(13, LOW);
    stat = false;
  }
  else {
    digitalWrite(13, HIGH);
    stat = true;
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
