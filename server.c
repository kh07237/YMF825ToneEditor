//参考サイト
// https://daeudaeu.com/socket/

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <bcm2835.h>
#include "fmif.h"
#include "fmsd1.h"

//#define SERVER_ADDR "127.0.0.1"
#define SERVER_ADDR "0.0.0.0"
#define SERVER_PORT 8080
#define BUF_SIZE 1024
#define DATAMAX 60 //bytes
unsigned char data[DATAMAX];

//int transfer(int);

int BytesFromHexString(unsigned char *data, const char *string, int  len) {
    //printf("string:%s\n", string);
    //int len = (int)strlen(string);
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

int transfer(int sock) {

    int recv_size, send_size;
    char recv_buf[BUF_SIZE], send_buf;

    int i=0;
    //unsigned char data[DATAMAX];
    int byte_len=0;


    while (1) {

        /* クライアントから文字列を受信 */
        recv_size = recv(sock, recv_buf, BUF_SIZE, 0);
        if (recv_size == -1) {
            printf("recv error\n");
            break;
        }
        if (recv_size == 0) {
            /* 受信サイズが0の場合は相手が接続閉じていると判断 */
            printf("connection aborted.\n");
            break;
        }
        
        /* 受信したデータを表示 */
        //printf("recv_buf:%s\n", recv_buf);
        //受信したデータをFMDriverへ送信
        byte_len = BytesFromHexString(data, recv_buf, recv_size);
        //printf("byte_len = %d\n", byte_len);
        printf("SendMidi:");
        if(byte_len <= DATAMAX ){
            for(i=0; i<byte_len; i++){
                printf("%02X",data[i]);
                Fmdriver_sendMidi(data[i]);
            }
            printf("\n");
        }

        
        /* 文字列が"finish"ならクライアントとの接続終了 */
        if (strcmp(recv_buf, "finish") == 0) {

            /* 接続終了を表す0を送信 */
            printf("finish recieved.\n");
            send_buf = 0;
            send_size = send(sock, &send_buf, 1, 0);
            if (send_size == -1) {
                printf("send error\n");
                break;
            }
            break;
        } else {
            /* "finish"以外の場合はクライアントとの接続を継続 */
            send_buf = 1;
            send_size = send(sock, &send_buf, 1, 0);
            if (send_size == -1) {
                printf("send error\n");
                break;
            }
            //受信バッファをクリア
            memset(recv_buf, 0, BUF_SIZE);
        }
        //printf("send_buf=%d\n",send_buf);
    }

    return 0;
}

int main(void) {
    int w_addr, c_sock;
    int i;
    struct sockaddr_in a_addr;

    /*SPI,FM音源YMF825初期化*/
    if (bcm2835_init() == 0) return -1;
    initSPI();
    initSD1();
    Fmdriver_init();
    printf("FMdriver init end.\n");
   //Program Change   
    Fmdriver_sendMidi(0xc0);
    Fmdriver_sendMidi(8);

    //note on
    Fmdriver_sendMidi(0x90);
    Fmdriver_sendMidi(0x3e);
    Fmdriver_sendMidi(0x7f);
    sleep(1);

    //note off
    Fmdriver_sendMidi(0x80);
    Fmdriver_sendMidi(0x3e);
    Fmdriver_sendMidi(0x7f);

    /* ソケットを作成 */
    w_addr = socket(AF_INET, SOCK_STREAM, 0);
    if (w_addr == -1) {
        printf("socket error\n");
        return -1;
    }

    memset(&a_addr, 0, sizeof(struct sockaddr_in));

    /* サーバーのIPアドレスとポートの情報を設定 */
    a_addr.sin_family = AF_INET;
    a_addr.sin_port = htons((unsigned short)SERVER_PORT);
    a_addr.sin_addr.s_addr = inet_addr(SERVER_ADDR);

    /* ソケットに情報を設定 */
    if (bind(w_addr, (const struct sockaddr *)&a_addr, sizeof(a_addr)) == -1) {
        printf("bind error\n");
        close(w_addr);
        return -1;
    }

    /* ソケットを接続待ちに設定 */
    if (listen(w_addr, 3) == -1) {
        printf("listen error\n");
        close(w_addr);
        return -1;
    }

    while (1) {
        /* 接続要求の受け付け（接続要求くるまで待ち） */
        printf("Waiting connect...\n");
        c_sock = accept(w_addr, NULL, NULL);
        if (c_sock == -1) {
            printf("accept error\n");
            close(w_addr);
            return -1;
        }
        printf("Connected!!\n");

        /* 接続済のソケットでデータのやり取り */
        transfer(c_sock);

        /* ソケット通信をクローズ */
        close(c_sock);

        /* 次の接続要求の受け付けに移る */
    }

    /* 接続待ちソケットをクローズ */
    close(w_addr);

    return 0;
}
