#UIパラメータ各項目に対応するデータ
#voice_commonデータ
bo = b'\x03'  #基本オクターブ 0-3
lfo = 3 #LFO 周波数 0-3
alg = 7 #FM アルゴリズム 0-7
#オペレーターごとのデータ
#  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
fb =    bytearray([7,0,0,0])   #フィードバック 0-7
xof =   bytes([1,0,0,0])   #ノートオフ無視 0/1
ksr =   bytes([1,0,0,0])   #キースケールセンシティブ0/1
ksl =   bytes([3,0,0,0])   #キースケールレベル 0-3
KC =    bytearray([0,0,0,0])   #fb/xof/ksr/kslを1バイトにパックしたもの
AR =    bytes([15,0,0,0])  #Attack Rate 0-15
DR =    bytes([15,0,0,0])  #Decay Rate 0-15
SR =    bytes([15,0,0,0])  #Sustain Rate 0-15
RR =    bytes([15,0,0,0])  #Release Rate 0-15
SL =    bytes([15,0,0,0])  #Sustain Level 0-15
TL =    bytes([63,0,0,0])  #Total Level 0-63
dam =   bytes([3,0,0,0])   #Modulation 0-3
eam =   bytes([1,0,0,0])   # 0/1
dvb =   bytes([3,0,0,0])    # 0-3
evb =   bytes([1,0,0,0])   # 0/1
VB =    bytearray([0,0,0,0])   #dam/eam/dvb/evbを1バイトにパックしたもの
dt =    bytes([7,0,0,0])   # Pitch Detune 0-7
mt =    bytes([15,0,0,0])  # Pitch Multi 0-15
PT =    bytearray([0,0,0,0])   #dt/mtを1バイトにパックしたもの
WS =    bytes([31,0,0,0])  # Wave Shape 0-31

def get_system_exclusive():
    #ビットアサインされているパラメータをパックする
    voice_common = bytes([(bo & 0b11) << 5 | (lfo & 0b11) << 3 | (alg & 0b111)])
    #print(f'{voice_common:X}')
    #print(voice_common)
    for op in range(4):
        KC[op] = (fb[op] & 0b111) << 4 | (xof[op] & 0b1) << 3 | (ksr[op] & 0b1) << 2 | (ksl[op] & 0b111) 
        VB[op] = (dam[op] & 0b11) << 5 | (eam[op] & 0b1) << 4 | (dvb[op] & 0b11) << 1 | (evb[op] & 0b1)
        PT[op] = (dt[op] & 0b111) << 4 | (mt[op] & 0b1111 )
        #print(f'{KC[op]:X}')
        #print(f'{VB[op]:X}')
        #print(f'{PT[op]:X}')

    #システムエクスクルーシブデータ(49バイト)の作成
    system_exclusive = bytes(b'\xf0\x43\x7f\x02\x00\x00\x00')
    system_exclusive += voice_common
    #  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
    for op in range(4):
        system_exclusive += bytes([KC[op]])
        system_exclusive += bytes([VB[op]])
        system_exclusive += bytes([AR[op]])
        system_exclusive += bytes([DR[op]])
        system_exclusive += bytes([SR[op]])
        system_exclusive += bytes([RR[op]])
        system_exclusive += bytes([SL[op]])
        system_exclusive += bytes([TL[op]])
        system_exclusive += bytes([VB[op]])
        system_exclusive += bytes([WS[op]])
    system_exclusive += b'\xf7'
    #print(system_exclusive.hex())
    print(f'len(system_exclusive)={len(system_exclusive)}')
    return system_exclusive






