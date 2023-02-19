#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h> 
#include <bcm2835.h>

#include "fmif.h"
#include "fmsd1.h"

#define DATAMAX 60 //bytes

int BytesFromHexString(unsigned char *data, const char *string) {
    //printf("string:%s\n", string);
    int len = (int)strlen(string);
    int byte_len = len/2;
    if(byte_len > DATAMAX){ //文字列の長さがバイトバッファの長さx2を超えていたらバイトバッファの長さで制限する
        len = DATAMAX*2;
        byte_len = DATAMAX;
    } 
    for (int i=0; i<len; i+=2) {
        unsigned int x;
        sscanf((char *)(string + i), "%02x", &x);
        data[i/2] = x;
    }

    for(int i=0; i<byte_len; i++)
    {
        //printf("%02X",data[i]);
    }
    //printf("\n");

    return byte_len;
}


int main(int argc, char *argv[])
{
    int i=0;
    unsigned char data[DATAMAX];
    int byte_len=0;
#if 1
    if (!bcm2835_init()) return 1;
    initSPI();
    initSD1();
#endif
    Fmdriver_init();

    //printf("argv[1]=%s\n",argv[1]);
    byte_len = BytesFromHexString(data,argv[1]);
    //printf("SendMidi:");
    if(byte_len <= DATAMAX ){
        for(i=0; i<byte_len; i++){
            //printf("%02X",data[i]);
            Fmdriver_sendMidi(data[i]);
        }
        //printf("\n");
    }

}