#ifndef FMIF_H
#define FMIF_H
#include "fmtone.h"
//	public
extern void Fmdriver_init( void );
extern void Fmdriver_sendMidi( unsigned char byteStream );
extern void Fmdriver_SetTome(ToneData tone, int idx);
#endif