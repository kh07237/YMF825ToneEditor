#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h> 
#include <bcm2835.h>

#include "fmif.h"
#include "fmsd1.h"



int main(int argc, char *argv[])
{
    int i=0;
    unsigned char data[DATAMAX];
    int byte_len=0;

    if (!bcm2835_init()) return 1;
    initSPI();
    initSD1();
    Fmdriver_init();

    return 0;
}