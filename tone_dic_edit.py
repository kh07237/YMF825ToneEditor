import platform
import subprocess
import time
import threading
from tkinter import *
from tkinter import ttk
#import tone_dic
from tone_dic import tone,get_system_exclusive,load,save,get_tone_name_list
from client import *

#voice_commonのspinboxパラメータ情報
spinbox_info={
    'bo' : {'name':'基本オクターブ','from':0,'to':3},
    'lfo' : {'name':'LFO周波数','from':0,'to':3},
    'alg' : {'name':'アルゴリズム','from':0,'to':7},
}

#オペレーター単位のspinboxパラメータ情報
spinbox_info_op={
    'fb' : {'name':'FB','from':0,'to':7},
    'xof' : {'name':'XOF','from':0,'to':1},
    'ksr' : {'name':'KSR','from':0,'to':1},
    'ksl' : {'name':'KSL','from':0,'to':3},
    'AR' : {'name':'AR','from':0,'to':15},
    'DR' : {'name':'DR','from':0,'to':15},
    'SR' : {'name':'SR','from':0,'to':15},
    'RR' : {'name':'RR','from':0,'to':15},
    'SL' : {'name':'SL','from':0,'to':15},
    'TL' : {'name':'TL','from':0,'to':63},
    'dam' : {'name':'dam','from':0,'to':3},
    'eam' : {'name':'eam','from':0,'to':1},
    'dvb' : {'name':'dvb','from':0,'to':3},
    'evb' : {'name':'evb','from':0,'to':1},
    'dt' : {'name':'DT','from':0,'to':7},
    'mt' : {'name':'MT','from':0,'to':15},
    'WS' : {'name':'WS','from':0,'to':31},

}

#オペレータごとのパラメータ表示領域背景色
bkcolor_info_op=['lightgreen','pink','lightblue','yellow']



tlock = threading.Lock()
def test_tone_th_th():
    global cli
    global tlock
    with tlock:    
        cli.send('c008') 
        cli.send('903e7f') #Note ON
        time.sleep(2)
    with tlock:    
        cli.send('803e7f') #Note OFF



#サブスレッドでテスト音再生
def test_tone_th():
    th = threading.Thread(target = test_tone_th_th)
    th.start()


def send_tone():
    global cli
    sysex = get_system_exclusive().hex()
    with tlock:    
        print(f'system exclusive:{sysex}')
        cli.send(sysex)
        test_tone_th()

"""
def update_bo(val):
    #global bo
    b = int(val)
    if(tone['bo'] != b):
        tone['bo'] = b
        send_tone()
    

def update_fb(val):
    b = int(val)
    if(tone['fb'[0]] != b):
        tone['fb'[0]] = b
        send_tone()
"""
def OnEnter(p):
    print(f'OnEnter({p})')
    spin_update(0)
    spin_update_op(0)

#View変数(val)とModel変数(tone)を比較し、差があったら更新する
def spin_update(p):
    updated = False
    for p in spinbox_info:
        b = val[p].get()
        if(tone[p][0] != b):
            print(f'{p} updated.')
            if(p=='alg'):
                   set_alg_image(tone['alg'][0])
            tone[p][0] = b
            updated = True
    if updated:
        send_tone()
def spin_update_op(p):
    updated = False
    for op in range(4):
        for p in spinbox_info_op:
            b = val_op[p][op].get()
            if(tone[p][op] != b):
                print(f'{p}[{op}] updated.')
                tone[p][op] = b
                updated = True
    if updated:
        send_tone()

import tkinter.simpledialog as simpledialog

def OnLoad():
    global param
    print('onload')
    tone_select_dialog()
    root.wait_window(dialog)
    print(f'param={param.get()}')
    print(f'tonename={tonename}')
    load(param.get())
    update_ui()
    send_tone()

def OnSave_as():
        name = simpledialog.askstring('音色名','音色名')
        save(name)


def tone_select_dialog():
    global dialog,paramdialog,listbox
    #音色名リストの取得
    var = StringVar(value=get_tone_name_list())
    dialog = Toplevel()
    dialog.title('音色のロード')
    dialog.grab_set()
    paramdialog = StringVar()
    entry = ttk.Entry(dialog) #入力エリア
    listbox = Listbox(dialog,listvariable=var)
    listbox_scroll = ttk.Scrollbar(dialog,orient='vertical',command=listbox.yview)
    listbox['yscrollcommand'] = listbox_scroll.set
    okButton = Button(dialog,text='OK',command = closeDialog)

    listbox.grid(row=1,column=0)
    listbox_scroll.grid(row=1, column=1,sticky=N+S)
    okButton.grid(row=2,column=1)
    """
    #entry.pack()
    listbox.pack(side='left')
    listbox_scroll.pack(side='right',fill='both')
    okButton.pack(side='bottom')
    """
# closeする前にダイアログに入力された値を反映する
def closeDialog():
    global dialog,paramdialog,listbox
    global param,tonename
    sel = listbox.curselection()
    tonename = listbox.get(sel)
    param.set(tonename)
    dialog.destroy()

#ロードしたデータをUIに反映する
def update_ui():
    for p in spinbox_info: #voice_commonのspinbox
        b = tone[p][0]
        val[p].set(b)
    for p in spinbox_info_op:
        val_op[p][op].set(tone[p][op])
    set_alg_image(tone['alg'])
#アルゴリズム説明図
algimage = None
alg_images = []
alg_image_canvas = None
alg_image_id = None
def load_alg_images():
    global alg_images
    global algimage
    alg_images = [
            PhotoImage(file='algo0.png'),
            PhotoImage(file='algo1.png'),
            PhotoImage(file='algo2.png'),
            PhotoImage(file='algo3.png'),
            PhotoImage(file='algo4.png'),
            PhotoImage(file='algo5.png'),
            PhotoImage(file='algo6.png'),
            PhotoImage(file='algo7.png'),
    ]
    algimage = PhotoImage(file='algo0.png')
#アルゴリズム説明図のセット・切り替え
def set_alg_image(n):
    print(type(n),n)
    img = alg_images[n]
    #algimage = PhotoImage(file='algo1.png')
    alg_image_canvas.itemconfig(alg_image_id,image=img)

####################################################################################
##ここからスタート

load('PickBass')

#ウィンドウ
root = Tk()
root.minsize(width=250, height=150)
frame = ttk.Frame(root, padding=1)
frame2 = ttk.Frame(
    frame, width=200, height=100,
    borderwidth=10, relief='sunken')

param = StringVar()
tonename = ''
paramdialog = None #StringVar()
dialog = None #Toplevel()
listbox = None

#メニュー
menu_bar = Menu(root)
root.config(menu=menu_bar)
menu_file = Menu(menu_bar,tearoff=0)
menu_file_loadex = Menu(menu_file,tearoff=0)
for l in get_tone_name_list():
    menu_file_loadex.add_command(label = l,command=OnLoad)
menu_file.add_cascade(label='ロード',menu=menu_file_loadex)
menu_file.add_command(label='ロード',command = OnLoad)
menu_file.add_command(label='名前を付けて保存...',command=OnSave_as)
menu_bar.add_cascade(label='ファイル',menu=menu_file)

#キーバインド
root.bind('<Return>',OnEnter)


"""# コントロール配置行（row）の割り当て 
0,1 voice_common 0:ラベル,1:スピンボックス 以下同文
2,3 op1 
4,5 op2 
6,7 op3 
8,9 op4 
"""
# UIアイテム voice_common
val= {}#データバインド変数
label = {}
spinbox = {}
#UIアイテム　オペレーターごと
val_op= {} #データバインド変数
label_opno_text = ['OP1','OP2','OP3','OP4']
label_opno = list(range(4))
label_op = {}
spinbox_op = {}

#spinbox初期化、データバインド
i=0
for p in spinbox_info: #voice_commonのspinbox
    val[p] = IntVar()
    b = tone[p][0]
    val[p].set(b)
    #print(f'{p}:{b}')
    label[p] = ttk.Label(frame,text=spinbox_info[p]['name'])
    label[p].grid(row=0, column=i, sticky=(N, E, S, W))

    spinbox[p] = ttk.Spinbox(
        frame,
        width= 5,
        textvariable=val[p],
        from_=spinbox_info[p]['from'],
        to=spinbox_info[p]['to'],
        increment=1,
        background='green',
        #command=lambda: spin_update(p,val[p].get())) #pとして通知元情報を送ることを試みたが、実行時、通知元は一律最後に登録したアイテム名固定になってしまう。失敗。
        command=lambda: spin_update(p)) 
    spinbox[p].grid(row=1, column=i, sticky=(N, E, S, W))
    i = i+1


    for p in spinbox_info_op: #オペレータごとのspinbox
        val_op[p] = list(range(4))
        label_op[p] = list(range(4))
        spinbox_op[p] = list(range(4))

#オペレータNo.１列目見出しを配置
for op in range(4):
    label_opno[op] = ttk.Label(frame,text=label_opno_text[op],background=bkcolor_info_op[op])
    label_opno[op].grid(row=2+op+1, column=0, sticky=(N, E, S, W))
#オペレータパラメータ１行目見出しを配置
c=1
for p in spinbox_info_op:
    #print(f'{p}:{b}')
    l = ttk.Label(frame,text=spinbox_info_op[p]['name'])
    label_op[p] = l
    label_op[p].grid(row=2, column=c, sticky=(N, E, S, W))
    c = c+1

#各スピンボックスを配置
for op in range(4):
    c=1
    for p in spinbox_info_op:
        val_op[p][op] = IntVar()
        val_op[p][op].set(tone[p][op])
        spinbox_op[p][op] = ttk.Spinbox(
            frame,
            width= 3,
            textvariable=val_op[p][op],
            from_=spinbox_info_op[p]['from'],
            to=spinbox_info_op[p]['to'],
            increment=1,
            #command=lambda: spin_update_op(p,val_op[p][op].get())) 
            command=lambda: spin_update_op(p)) 
        spinbox_op[p][op].grid(row=2+op+1, column=c, pady=10,  sticky=(N, E, S, W))
        c = c+1

#アルゴリズム説明図を配置
load_alg_images()
alg_image_canvas = Canvas(frame,width=300,height=100)
#alg_image_id = alg_image_canvas.create_image(0,0,image=alg_images[0],anchor=NW)
alg_image_id = alg_image_canvas.create_image(0,0,image=algimage,anchor=NW)
alg_image_canvas.grid(row=12, column=0, rowspan = 4,columnspan = 4 )

#YMF825デバイスへソケット通信するためのクライアント
cli = InetClient(host="pizero2")

#起動確認音を鳴らす
cli.send('c001') #プログラムチェンジ 
cli.send('903e7f') #Note ON
time.sleep(0.5)
cli.send('903d7f') #Note ON
time.sleep(1)
cli.send('803e7f') #Note OFF
cli.send('803d7f') #Note OFF


frame.pack()
#frame2.pack()
send_tone()
root.mainloop()
cli.close()

