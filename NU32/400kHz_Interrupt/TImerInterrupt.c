#include "NU32.h" // constants, funcs for startup and UART
#include <xc.h>
#include <stdio.h>

#define MAX_MESSAGE_LENGTH 2000
#define CORE_TICKS 1000
#define WAVE_SEQUENCE_LENGTH 10

#define SHIFTS_COUNT 10

void Timer2_Startup(void);

void delay(int);

static volatile unsigned char wave_seq[WAVE_SEQUENCE_LENGTH] = {0x7C, 0x3E, 0x1F, 0x0F, 0x07, 0x83, 0xC1, 0xE0, 0xF0, 0xF8};
static volatile unsigned char i = 0;
static volatile char unsigned wave = 0xF8;
static char shifts[SHIFTS_COUNT];
static volatile int seq[10];

void parseShifts(char *shifts, char *string, int maxStringLength);
void parseWave(int *stamps);

void __ISR(_CORE_TIMER_VECTOR, IPL6SRS) CoreTimerISR(void)
{

    IFS0CLR = 0x1; // Reset Flag
    LATBINV = 0xFFFF;
    LATEINV = 0xFF;
    _CP0_SET_COUNT(0);
    _CP0_SET_COMPARE(CORE_TICKS);
}

// void __ISR(_TIMER_2_VECTOR, IPL6SRS) Timer3ISR(void){
//     IFS0CLR = 0x100;
//     LATBINV = 0xFFFF;
//     LATDINV = 0XFF;
//     LATEINV = 0xFF;
// }

// // KEEP
// void __ISR(_TIMER_2_VECTOR, IPL6SRS) Timer2ISR(void){

//     IFS0CLR = 0x100;
//     wave = wave_seq[i];
//     LATB = wave;
//     LATD = wave;
//     LATE = wave;
//     i = (++i % WAVE_SEQUENCE_LENGTH);
//     // char msg[MAX_MESSAGE_LENGTH];
//     // sprintf(msg, "%d\r\n", wave);
//     // NU32_WriteUART3(msg);
// }

int main(void)
{

    int step = 0;
    char msg[MAX_MESSAGE_LENGTH];

    NU32_Startup(); // cache on, interrupts on, LED/button init, UART init

    TRISF = 0xFFFC;
    LATF = 0x3;

    AD1PCFG = 0xFFFF;
    TRISB = 0x0;
    TRISD = 0x0;
    TRISE = 0x0;

    LATB = 0xFFFF;
    LATD = 0xFFF;
    LATE = 0xFF;

    // Timer2_Startup();
    // while(1){;}

    while (1)
    {
        // // TESTING PARSESHIFTS
        // NU32_ReadUART3(msg, MAX_MESSAGE_LENGTH);
        // NU32_WriteUART3(msg);
        // NU32_WriteUART3("\r\n");
        // parseShifts(shifts, msg, MAX_MESSAGE_LENGTH);
        // NU32_WriteUART3(shifts);


        parseWave(seq);
    }
    return 0;
}

//   while(1){
//     // NU32_WriteUART3(message);
//     delay();
//     // step++;
//     // msg[0] = step;
//     NU32_WriteUART3("hello\n\r");

//   }
// while(1){
//     delay(500);
//     // LATFINV = 0x3;
//     // NU32_WriteUART3("hello\n\r");

//     LATBINV = 0xFFFF;
//     // LATDINV = 0xFFF;
//     LATEINV = 0xFF;
//     // NU32_WriteUART3("hello\n\r");

void Timer2_Startup(void)
{
    __builtin_disable_interrupts();

    T2CONbits.ON = 1;
    // T2CONbits.TCS = 0;
    T2CONbits.TGATE = 0;
    T2CONbits.TCKPS = 0b0;
    PR2 = 199;

    IFS0CLR = 0x100;
    IPC2bits.T2IP = 6;
    IPC2bits.T2IS = 0;
    IEC0SET = 0x100;

    __builtin_enable_interrupts();
}

void delay(int delay_time)
{
    _CP0_SET_COUNT(0);
    while (_CP0_GET_COUNT() < delay_time)
    {
        ;
    }
}

// // CORE TIMER INTERRUPT
// __builtin_disable_interrupts();
// _CP0_SET_COMPARE(CORE_TICKS);
// IPC0bits.CTIP = 6;
// IPC0bits.CTIS = 0;
// IPC0bits.CTIP = 6;
// IFS0CLR = 0x01;
// IEC0 = 0b1;
// __builtin_enable_interrupts();
// _CP0_SET_COUNT(0);

void parseShifts(char *shifts, char *string, int maxStringLength)
{

// TODO: Need to ENfore no contiguous digits
    int i = 0;
    int j = 0;
    char _msg[MAX_MESSAGE_LENGTH];
    char _shifts[MAX_MESSAGE_LENGTH];

    for (j = 0; j < maxStringLength; ++j)
    {
 
        if ((string[j] > 47) & (string[j] < 58))
        {
            _shifts[i] = string[j] - 48;
            sprintf(_msg, "%d\r\n", _shifts[i]);
            NU32_WriteUART3(_msg);
            ++i;
            if (i == SHIFTS_COUNT)
            {
                break;
            }
        }
    }
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
