#UIパラメータ各項目に対応するデータ
tone = {
  #voice_commonデータ
    'bo' :  [3],                # 基本オクターブ 0-3
    'lfo' : [3],                      # LFO 周波数 0-3
    'alg' : [7],                      # FM アルゴリズム 0-7
  #オペレーターごとのデータ 小文字の要素は複数まとめてその下の大文字のバイトにパックされる
    #  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
    #'fb' :   bytearray(b'\x07\x00\x00\x00'),    # フィードバック 0-7
    'fb' :    [7,6,5,4],    # フィードバック 0-7
    'xof' :   [1,0,0,0],     # ノートオフ無視 0/1
    'ksr' :   [1,0,0,0],     # キースケールセンシティブ0/1
    'ksl' :   [3,0,0,0],     # キースケールレベル 0-3
    #KC
    'AR' :    [15,0,0,0],    # Attack Rate 0-15
    'DR' :    [15,0,0,0],    # Decay Rate 0-15
    'SR' :    [15,0,0,0],    # Sustain Rate 0-15
    'RR' :    [15,0,0,0],    # Release Rate 0-15
    'SL' :    [15,0,0,0],    # Sustain Level 0-15
    'TL' :    [63,0,0,0],    # Total Level 0-63
    'dam' :   [3,0,0,0],     # Modulation 0-3
    'eam' :   [1,0,0,0],     # 0/1
    'dvb' :   [3,0,0,0],     # 0-3
    'evb' :   [1,0,0,0],     # 0/1
    #VB
    'dt' :    [7,0,0,0],     # Pitch Detune 0-7
    'mt' :    [15,0,0,0],    # Pitch Multi 0-15
    #PT
    'WS' :    [31,0,0,0]     # Wave Shape 0-31
}
def loadsub(data):
  KC = [0,0,0,0]
  VB = [0,0,0,0]
  PT = [0,0,0,0]

  voice_common = data[0]
  #tone['bo']    = [(voice_common & 0b01100000) >> 5]
  tone['bo'][0]    = (voice_common & 0b01100000) >> 5
  tone['lfo'][0]   = (voice_common & 0b00011000) >> 3
  tone['alg'][0]   = (voice_common & 0b00000111) 

  for op in range(4):
    KC[op]          = data[ 1+op*10]
    tone['fb'][op]    = (KC[op] & 0b01110000) >> 4
    tone['xof'][op]   = (KC[op] & 0b00001000) >> 3 
    tone['ksr'][op]   = (KC[op] & 0b00000100) >> 2 
    tone['ksl'][op]   = (KC[op] & 0b00000011)  
    tone['AR'][op]  = data[ 2+op*10]
    tone['DR'][op]  = data[ 3+op*10]
    tone['SR'][op]  = data[ 4+op*10]
    tone['RR'][op]  = data[ 5+op*10]
    tone['SL'][op]  = data[ 6+op*10]
    tone['TL'][op]  = data[ 7+op*10]
    VB[op]          = data[ 8+op*10]
    tone['dam'][op]   = (VB[op] & 0b01100000) >> 5 
    tone['eam'][op]   = (VB[op] & 0b00010000) >> 4 
    tone['dvb'][op]   = (VB[op] & 0b00000110) >> 1
    tone['evb'][op]   = (VB[op] & 0b00000001)
    PT[op]          = data[ 9+op*10]
    tone['dt'][op]    = (PT[op] & 0b01110000) >> 4
    tone['mt'][op]    = (PT[op] & 0b00001111)
    tone['WS'][op]    = data[10+op*10]
    #print(tone)

def load(name):
  print(f'load:{name}')
  with open('tonedata.txt') as f:
    lines = f.readlines()
    i = 0
    for line in lines:
      if name in line:
          print(lines[i].rstrip())
          tonebytestr = lines[i+2].rstrip()
          tonebytestr = tonebytestr.replace(',','')
          tonebytes = bytearray.fromhex(tonebytestr)
          #print(lines[i+2].rstrip())
          if len(tonebytes) == 41:
            print (tonebytes)
            loadsub(tonebytes)

      i = i+1

def get_tone_name_list():
  with open('tonedata.txt') as f:
    lines = f.readlines()
    tone_name_list = []
    i = 0
    for line in lines:
      if 'Name:' in line:
          tone_name = lines[i].split(':')[1].lstrip().rstrip()
          tone_name_list.append(tone_name)
      i = i+1
    return tone_name_list



def save(name):
    s=''
    tone_bytes = get_tone_data_bytes()
    for d in tone_bytes:
      s += '{:02x}'.format(d)+','
    s = s.rstrip(',')  
    print(s)
    with open('tonedata.txt', mode='a') as f:
      f.write ('Name: '+name + '\n')
      f.write ('Author: YSL\n')
      f.write (s + '\n\n')

def get_system_exclusive():
  #システムエクスクルーシブデータ(49バイト)の作成
    system_exclusive = bytearray(b'\xf0\x43\x7f\x02\x00\x00\x00')
    system_exclusive += get_tone_data_bytes()
    system_exclusive += b'\xf7'
    #print(system_exclusive[7:])
    #print(system_exclusive.hex())
    print(f'len(system_exclusive)={len(system_exclusive)}')
    return system_exclusive

#tonedata本体41バイトを作成する
def get_tone_data_bytes():
    #ビットアサインされているパラメータをパックする
    voice_common = bytes([(tone['bo'][0] & 0b11) << 5 | (tone['lfo'][0] & 0b11) << 3 | (tone['alg'][0] & 0b111)])
    #print(f'{voice_common:X}')
    #print(voice_common)
    KC = [0,0,0,0]
    VB = [0,0,0,0]
    PT = [0,0,0,0]
    for op in range(4):
        KC[op] = (tone['fb'][op] & 0b111) << 4 | (tone['xof'][op] & 0b1) << 3 | (tone['ksr'][op] & 0b1) << 2 | (tone['ksl'][op] & 0b111) 
        VB[op] = (tone['dam'][op] & 0b11) << 5 | (tone['eam'][op] & 0b1) << 4 | (tone['dvb'][op] & 0b11) << 1 | (tone['evb'][op] & 0b1)
        PT[op] = (tone['dt'][op] & 0b111) << 4 | (tone['mt'][op] & 0b1111 )
        #print(f'{KC[op]:X}')
        #print(f'{VB[op]:X}')
        #print(f'{PT[op]:X}')
    system_exclusive = bytearray(voice_common)# "system_exclusive"変数はここの関数内では返す値tonedataのことを指す。
    #  KC | AR | DR | SR | RR | SL | TL | VB | PT | WS
    for op in range(4):
        system_exclusive += bytes([KC[op]])
        system_exclusive += bytes([tone['AR'][op]])
        system_exclusive += bytes([tone['DR'][op]])
        system_exclusive += bytes([tone['SR'][op]])
        system_exclusive += bytes([tone['RR'][op]])
        system_exclusive += bytes([tone['SL'][op]])
        system_exclusive += bytes([tone['TL'][op]])
        system_exclusive += bytes([VB[op]])
        system_exclusive += bytes([PT[op]])
        system_exclusive += bytes([tone['WS'][op]])
    return system_exclusive

if __name__ == '__main__':
  get_tone_name_list()
  #load('GrandPiano')
  #get_system_exclusive()
  