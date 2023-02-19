# YMF825 ToneEditor
 Ver. 0.1
## 機能概要
  - Raspberry Piに接続したFM音源YMF825ボードの音色パラメータをGUIで編集する。
  - 編集した音色でテスト音発音
  - 音色定義ファイルから音色名を指定して読み込み
  - 音色に名前を付けて保存  


## ソースファイルの説明
| ファイル名 | 役割         | 
| ------------------------ | ---------------------------- | 
| <python側>
| tone_dic_edit.py |GUIメインプログラム  
| tone_dic.py |音色パラメータを辞書形式で保持、音色データファイルからのロード、セーブ、システムエクスクルーシブ送信、ソケット通信クライアントはサーバーへMIDIデータを送信する。
| algo*.png | GUIへ表示するためのアルゴリズム説明図
|  <C言語側>
| server.c | ソケット通信サーバー。クライアントから受信したMIDIデータをfmifへ送信する。
| fmif.c | YMF825へMIDIデータを送信する。
| makefile | メイクファイル

## C言語側ビルド方法
```
$ make ymf825srv
```
## C言語側サーバープログラムの起動
```
$ sudo ./ymf825srv
```

