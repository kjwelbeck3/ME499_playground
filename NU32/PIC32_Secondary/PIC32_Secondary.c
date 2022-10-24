#include "NU32.h" // constants, funcs for startup and UART
#include <xc.h>
#include <stdio.h>

#define MAX_MESSAGE_LENGTH 2000
#define CORE_TICKS 1000
#define WAVE_SEQUENCE_LENGTH 10
#define SHIFTS_COUNT 10

void Timer2_Startup(void);
void ExternalInt4_Startup(void);

void delay(int);
void parseShifts(char *shifts, char *string, int maxStringLength);
void parseWave(int *stamps);

static volatile unsigned char wave_seq[WAVE_SEQUENCE_LENGTH] = {0x7C, 0x3E, 0x1F, 0x0F, 0x07, 0x83, 0xC1, 0xE0, 0xF0, 0xF8};
static volatile unsigned char i = 0;
static volatile char unsigned wave = 0xF8;
static char shifts[SHIFTS_COUNT];
static volatile int seq[10];


// void __ISR(_TIMER_2_VECTOR, IPL6SRS) Timer2ISR(void){

//     IFS0CLR = 0x100;
//     wave = wave_seq[i];
//     LATCINV = 0x2000;
//     LATB = wave;
//     LATD = wave;
//     LATE = wave;
    
//     i = (++i % WAVE_SEQUENCE_LENGTH);
// }

void __ISR(_EXTERNAL_4_VECTOR, IPL6SRS) ExtInt4(void){
    
    IFS0CLR = 0x80000;
    wave = wave_seq[i];
    LATCINV = 0x2000;
    LATB = wave & (wave << 8);
    LATD = wave & 0b11111110;
    LATE = wave;
    
    i = (++i % WAVE_SEQUENCE_LENGTH);
    
}

int main(void)
{
    int step = 0;
    char msg[MAX_MESSAGE_LENGTH];

    NU32_Startup(); // cache on, interrupts on, LED/button init, UART init

    TRISF = 0xFFFC;
    LATF = 0x3;

    AD1PCFG = 0xFFFF;
    TRISB = 0x0;
    TRISDCLR = 0xFF;
    TRISE = 0x0;
    TRISC = ~(0x2000);

    LATB = 0xFFFF;
    LATD = 0xFF & 0b11111110;
    LATE = 0xFF;
    LATC = 0x2000; //13

    // Timer2_Startup();
    ExternalInt4_Startup();

    while (1)
    {
        parseWave(seq);
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
//     PR2 = 199;

//     IFS0CLR = 0x100;
//     IPC2bits.T2IP = 6;
//     IPC2bits.T2IS = 0;
//     IEC0SET = 0x100;

//     __builtin_enable_interrupts();
// }

void ExternalInt4_Startup(void){
    
    __builtin_disable_interrupts();

    IFS0CLR = 0x80000;
    IPC4bits.INT4IP = 6;
    IPC4bits.INT4IS = 0;
    IEC0SET = 0x80000;

    __builtin_enable_interrupts();

}

void delay(int delay_time)
{
    _CP0_SET_COUNT(0);
    while (_CP0_GET_COUNT() < delay_time){;}
}


void parseWave(int *stamps)
{
    char _msg[MAX_MESSAGE_LENGTH];
    int _stamps[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    char _sth[200];

    NU32_WriteUART3("(10x) space-separated integers [eg. 1 1 1 1 1 1 1 1 1 1]:\r\n");
    NU32_ReadUART3(_msg, MAX_MESSAGE_LENGTH);
    NU32_WriteUART3(_msg);
    NU32_WriteUART3("\r\n");

    sscanf(_msg, 
            "%u %u %u %u %u %u  %u %u %u %u", 
            &_stamps[0], &_stamps[1], 
            &_stamps[2], &_stamps[3], 
            &_stamps[4], &_stamps[5], 
            &_stamps[6], &_stamps[7], 
            &_stamps[8], &_stamps[9]);

    for (int i = 0; i < 10; i++ ){
        sprintf(_msg, "%u : %30x \r\n", _stamps[i], _stamps[i]);
        NU32_WriteUART3(_msg);
    }

    stamps = _stamps;
}
