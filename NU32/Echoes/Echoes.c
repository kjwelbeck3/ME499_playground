#include "NU32.h" // constants, funcs for startup and UART
#include <xc.h>
#include <stdio.h>
#include <string.h>

#define MAX_MESSAGE_LENGTH 2000
#define DELAY_TIME 1000000
#define WAVE_SEQ_LENGTH 10
#define ID 1

void delay(int);

int main(void)
{
    char msg[MAX_MESSAGE_LENGTH];
    int rcvd = 10;

    int waveSeq[WAVE_SEQ_LENGTH] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    // int waveSeq[WAVE_SEQ_LENGTH] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
    // int waveSeq[WAVE_SEQ_LENGTH];
    
    int waveSeqCount = 0;
    char new_msg[MAX_MESSAGE_LENGTH + 100];
    char resp[MAX_MESSAGE_LENGTH];

    NU32_Startup(); // cache on, interrupts on, LED/button init, UART init

    while (1)
    {
        NU32_ReadUART3(msg, MAX_MESSAGE_LENGTH);
        // NU32_WriteUART3(msg);
        // NU32_WriteUART3("\r\n");

        sscanf(msg,
               "%u %u %u %u %u %u  %u %u %u %u",
               &waveSeq[0], &waveSeq[1],
               &waveSeq[2], &waveSeq[3],
               &waveSeq[4], &waveSeq[5],
               &waveSeq[6], &waveSeq[7],
               &waveSeq[8], &waveSeq[9]);

        // Count recieved wave sequence size
        
        for (int i = 0; i < WAVE_SEQ_LENGTH; i++)
        {
            if (waveSeq[i] != 0)
            {
                waveSeqCount++;
            }
        }

        // Return Source [Destination] and WaveSequenceCount
        sprintf(resp, "%d %d \r\n", ID, waveSeqCount);
        NU32_WriteUART3(resp);

        // Reseting wave sequence array and count
        waveSeqCount = 0;
        memset(waveSeq, 0, sizeof waveSeq);
        // fill_n(waveSeq, WAVE_SEQ_LENGTH, 0);


    }

    return 0;
}

void delay(int delay_time)
{
    _CP0_SET_COUNT(0);
    while (_CP0_GET_COUNT() < delay_time)
    {
        ;
    }
}
