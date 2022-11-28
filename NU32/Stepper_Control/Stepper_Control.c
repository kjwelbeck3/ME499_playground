#include "NU32.h" // constants, funcs for startup and UART
#include <xc.h>
#include <stdio.h>

#define MAX_MESSAGE_LENGTH 20
#define METRONOME 50000
#define M1_DISABLE LATBbits.LATB1
#define M1_DIR LATBbits.LATB2
#define M2_DISABLE LATBbits.LATB4
#define M2_DIR LATBbits.LATB5


// void Timer2_Startup(void);
void Timer3_OC1_Startup(void);
void getCommand();
void delay(int delay_time);


// // KEEP
// void __ISR(_TIMER_2_VECTOR, IPL6SRS) Timer2ISR(void){

//     IFS0CLR = 0x100; //8;
//     wave = wave_seq[i];
//     LATCINV = 0x2000;
//     LATB = wave;
//     LATD = wave & 0b11111110;
//     LATE = wave;
    
//     i = (++i % WAVE_SEQUENCE_LENGTH);
// }

int main(void)
{

    NU32_Startup(); // cache on, interrupts on, LED/button init, UART init

    AD1PCFG = 0xFFFF;           // PortB as digital I/O
    TRISBCLR = 0b110110;        // PortB 1,2,4,5 as digital output pins 
    M1_DISABLE = 1;             // Start with motors disabled
    M2_DISABLE = 1;
    
    Timer3_OC1_Startup();       // PWM on D0

    while (1)
    {
        getCommand();
    }
    return 0;
}


// void Timer2_Startup(void)
// {
//     __builtin_disable_interrupts();

//     T2CONbits.ON = 1;
//     // T2CONbits.TCS = 0;
//     T2CONbits.TGATE = 0;
//     T2CONbits.TCKPS = 0b0;
//     PR2 = METRONOME -1;

//     IFS0CLR = 0x100; //0x100;
//     IPC2bits.T2IP = 6;
//     IPC2bits.T2IS = 0;
//     IEC0SET = 0x100;//8; //0x100;

//     __builtin_enable_interrupts();
// }

void Timer3_OC1_Startup(void){
    __builtin_disable_interrupts();

    T3CONbits.ON = 1;
    T3CONbits.TGATE = 0;
    T3CONbits.TCKPS = 0b1;
    PR3 = METRONOME/2 -1;

    OC1CONbits.ON = 1;
    OC1CONbits.OC32 = 0;
    OC1CONbits.OCTSEL = 1;
    OC1CONbits.OCM = 0b011;
    OC1R = METRONOME/2 -1;

    __builtin_enable_interrupts();
}

void delay(int delay_time)
{
    _CP0_SET_COUNT(0);
    while (_CP0_GET_COUNT() < delay_time){;}
}


void getCommand()
{
    char command[MAX_MESSAGE_LENGTH];
    int command_int = 0;

    NU32_WriteUART3("Enter Command Code [10=D1/20=D2/11=F1/21=F2/12=R1/22R2]):\r\n");
    NU32_ReadUART3(command, MAX_MESSAGE_LENGTH);

    sscanf(command, "%u", &command_int);

    switch (command_int)
    {
    case 10:
        M1_DISABLE = 1;
        break;

    case 11:
        M1_DIR = 1;
        M1_DISABLE = 0;
        break;

    case 12:
        M1_DIR = 0;
        M1_DISABLE = 0;
        break;

    case 20:
        M2_DISABLE = 1;
        
        break;
    
    case 21:
        M2_DIR = 1;
        M2_DISABLE = 0;
        break;
    
    case 22:
        M2_DIR = 0;
        M2_DISABLE = 0;
        break;

    case 00:
        M1_DISABLE = 1;
        M2_DISABLE = 1;
        break;

    default:
        M1_DISABLE = 1;
        M2_DISABLE = 1;

    }

    NU32_WriteUART3(command); //ACK with rcvd code
    NU32_WriteUART3("\r\n");

}

