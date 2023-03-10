//	fmtone.c
#include 	<stdio.h>
#include	"fmtype.h"
#include	"fmtone.h"
#include	"fmsd1.h"

#define		IMMUTABLE_TONE_MAX		8
#define		MUTABLE_TONE_MAX		IMMUTABLE_TONE_MAX
#define		AVAILABLE_TONE_NUMBER	(IMMUTABLE_TONE_MAX+MUTABLE_TONE_MAX)
#define		MAX_EXCLUSIVE_HEADER_SIZE	5

#define 	MAX_ELEMENT_PRM			2
#define		OPERATOR_PRM_REG_SZ		7
#define 	MAX_TONE_PRM_SZ 		(MAX_FM_OPERATOR*OPERATOR_PRM_REG_SZ + MAX_ELEMENT_PRM)

typedef enum {
	WAIT_DATA,
	DURING_SETTING,
	SET_STATE_MAX
} SET_STATE;

//	Variable
static SET_STATE _toneSetState;
static int _tprmIndex;
static ToneData _userTone[MUTABLE_TONE_MAX];
static const ToneData TPRM[IMMUTABLE_TONE_MAX] = {

	{	//	GrandPiano
		0x0b,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x01,0x0f,0x07,0x00,0x06,0x0f,0x27,0x00,0x01,0x08},	// op1
			{0x07,0x0e,0x03,0x02,0x03,0x02,0x28,0x00,0x05,0x00},	// op2
			{0x00,0x0d,0x01,0x01,0x04,0x03,0x22,0x01,0x01,0x00},	// op3
			{0x06,0x0d,0x02,0x02,0x06,0x04,0x00,0x01,0x01,0x00}		// op4
		}
	},
	{	// E.Piano
		0x0d,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x54,0x0f,0x04,0x05,0x0c,0x0b,0x23,0x44,0x07,0x12},	// op1
			{0x02,0x0f,0x02,0x01,0x08,0x0f,0x04,0x45,0x01,0x00},	// op2
			{0x25,0x0f,0x00,0x01,0x0b,0x01,0x12,0x44,0x01,0x00},	// op3
			{0x04,0x0f,0x02,0x01,0x07,0x0f,0x04,0x41,0x01,0x00}		// op4
		}
	},
	{	//	TenorSax
		0x0d,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x36,0x07,0x03,0x00,0x00,0x00,0x05,0x44,0x01,0x01},	// op1
			{0x00,0x07,0x02,0x00,0x09,0x00,0x0f,0x43,0x01,0x08},	// op2
			{0x36,0x07,0x03,0x00,0x00,0x00,0x08,0x44,0x01,0x09},	// op3
			{0x02,0x07,0x02,0x00,0x09,0x00,0x0d,0x43,0x01,0x00}		// op4
		}
	},
	{	//	PickBass
		0x0b,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x56,0x0f,0x07,0x02,0x03,0x01,0x13,0x44,0x01,0x00},	// op1
			{0x04,0x0c,0x0b,0x04,0x06,0x07,0x15,0x44,0x07,0x00},	// op2
			{0x06,0x0f,0x09,0x02,0x06,0x02,0x17,0x44,0x02,0x00},	// op3
			{0x04,0x0b,0x02,0x06,0x08,0x06,0x00,0x44,0x01,0x00}		// op4
		}
	},
	{	//	TnklBell
		0x0d,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x31,0x0f,0x06,0x03,0x04,0x05,0x10,0x44,0x0e,0x00},	// op1
			{0x02,0x0c,0x06,0x07,0x06,0x0e,0x0b,0x44,0x02,0x00},	// op2
			{0x00,0x0c,0x06,0x02,0x02,0x05,0x1e,0x44,0x77,0x01},	// op3
			{0x00,0x0f,0x05,0x04,0x05,0x0d,0x01,0x54,0x06,0x00}		// op4
		}
	},
	{	//	NewAgePd
		0x0d,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x54,0x0f,0x0f,0x03,0x03,0x00,0x26,0x44,0x07,0x01},	// op1
			{0x02,0x0f,0x07,0x04,0x04,0x00,0x0b,0x44,0x05,0x00},	// op2
			{0x62,0x06,0x01,0x00,0x01,0x00,0x18,0x03,0x71,0x01},	// op3
			{0x02,0x08,0x01,0x00,0x05,0x01,0x00,0x03,0x01,0x00}		// op4
		}
	},
	{	//	Rim Shot
		0x0d,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x7c,0x0f,0x00,0x05,0x05,0x00,0x05,0x44,0x0c,0x02},	// op1
			{0x0c,0x0f,0x07,0x07,0x07,0x07,0x00,0x44,0x0b,0x00},	// op2
			{0x08,0x0f,0x0a,0x06,0x06,0x08,0x00,0x44,0x0c,0x00},	// op3
			{0x08,0x0f,0x07,0x07,0x07,0x07,0x00,0x44,0x07,0x02}		// op4
		}
	},
	{	//	Castanet
		0x0d,	//	VoiceCommon
		{ //  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
			{0x68,0x0f,0x07,0x05,0x09,0x0f,0x02,0x44,0x07,0x01},	// op1
			{0x0c,0x0a,0x08,0x05,0x0f,0x0f,0x00,0x44,0x05,0x06},	// op2
			{0x08,0x0f,0x05,0x06,0x05,0x00,0x27,0x44,0x02,0x05},	// op3
			{0x08,0x0c,0x0a,0x09,0x09,0x0a,0x14,0x44,0x05,0x00}		// op4
		}
	}
};
const unsigned char tExcCheck[MAX_EXCLUSIVE_HEADER_SIZE] = {
	0x43,	//	Exclusive:1, Yamaha ID
	0x7f,	//	Exclusive:2, Make/DIY ID1
	0x02,	//	Exclusive:3, Make/DIY ID2
	0x00,	//	Exclusive:4, YMF825 ID
	0x00	//	Exclusive:5, reserved
};
void Tone_init( void )
{
	int i;
	for ( i=0; i<MUTABLE_TONE_MAX; i++ ){
		_userTone[i] = TPRM[i];
	}
	_toneSetState = WAIT_DATA;
	_tprmIndex = 0;

	Tone_sendTone();
}

//ToneData?????????????????????????????????????????????????????????????????????
void Tone_setTone(ToneData tone, int idx)
{
	printf("SetTone.\n");
	if(idx<0 || idx >= MUTABLE_TONE_MAX) {
		return;
	}
	_userTone[idx] = tone;
	Tone_sendTone();
	printf("SetTone End.\n");

}

void Tone_setToneExc( unsigned char data, int excNum )
{
	if ( _toneSetState == WAIT_DATA ){
		if (( excNum == 1 ) && ( data == tExcCheck[0] )){
			_toneSetState = DURING_SETTING;
		}
	}
	else if ( _toneSetState == DURING_SETTING ){
		if ( excNum-1 < MAX_EXCLUSIVE_HEADER_SIZE ){
		 	if ( data != tExcCheck[excNum-1] ){ _toneSetState = WAIT_DATA; }
		}
		else if ( excNum == 6 ){
			if ( data < MUTABLE_TONE_MAX ){ _tprmIndex = data; }
			else { _toneSetState = WAIT_DATA; }
		}
		else if ( excNum == 7 ){
			_userTone[_tprmIndex].voiceCommon = data;
		}
		else if ( excNum < 48 ){
				_userTone[_tprmIndex].opPrm[(excNum-8)/MAX_OPERATOR_PRM][(excNum-8)%MAX_OPERATOR_PRM] = data;
			}
		else { _toneSetState = WAIT_DATA; }
	}
}
void Tone_sendTone( void )
{
	int	i,j;
	unsigned char regImage[MAX_TONE_PRM_SZ*AVAILABLE_TONE_NUMBER + 1 + 4]; // 485

	//	top
	regImage[0] = 0x80 + AVAILABLE_TONE_NUMBER;

	for ( i=0; i<AVAILABLE_TONE_NUMBER; i++ ){
		unsigned char* riPtr = &regImage[MAX_TONE_PRM_SZ*i + 1];

		ToneData* td;
		if ( i < IMMUTABLE_TONE_MAX ){
			td = (ToneData*)&(TPRM[i]);
		}
		else {
			td = (ToneData*)&(_userTone[i-IMMUTABLE_TONE_MAX]);
		}

		riPtr[0] = (td->voiceCommon & 0x60)>>5;
		riPtr[1] = ((td->voiceCommon & 0x18)<<3) | (td->voiceCommon & 0x07);

		for ( j=0; j<MAX_FM_OPERATOR; j++ ){
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+0] = (td->opPrm[j][3] << 4) | (td->opPrm[j][0] & 0x08) | ((td->opPrm[j][0] & 0x04)>>2);
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+1] = (td->opPrm[j][4] << 4) | td->opPrm[j][2];
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+2] = (td->opPrm[j][1] << 4) | td->opPrm[j][5];
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+3] = (td->opPrm[j][6] << 2) | (td->opPrm[j][0] & 0x03);
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+4] = td->opPrm[j][7];
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+5] = ((td->opPrm[j][8] & 0x0f) << 4) | ((td->opPrm[j][8] & 0xf0) >> 4);
			riPtr[MAX_ELEMENT_PRM+OPERATOR_PRM_REG_SZ*j+6] = (td->opPrm[j][9] << 3) | ((td->opPrm[j][0] & 0x70) >> 4);
		}
	}

	//	end 
	regImage[MAX_TONE_PRM_SZ*AVAILABLE_TONE_NUMBER + 1] = 0x80;
	regImage[MAX_TONE_PRM_SZ*AVAILABLE_TONE_NUMBER + 2] = 0x03;
	regImage[MAX_TONE_PRM_SZ*AVAILABLE_TONE_NUMBER + 3] = 0x81;
	regImage[MAX_TONE_PRM_SZ*AVAILABLE_TONE_NUMBER + 4] = 0x80;

	//	 Soft Reset
//    writeSingle(26,0xa3);
//    writeSingle(26,0x00);
	writeSingle(8,0xf6);
	delayMs(1);
	writeSingle(8,0x00);

	writeBurst( 7, regImage, MAX_TONE_PRM_SZ*AVAILABLE_TONE_NUMBER + 5 );
}