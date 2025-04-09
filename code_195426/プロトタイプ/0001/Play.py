import sys
import pygame as pg
from Define import *

df = Define

# グローバル関数
# ----------------------------

# ゲーム終了条件
# ウィンドウの右上「ｘ」が押されたか？ または Escキーが押されたか？
def should_exit(evt):
    return evt.type == pg.QUIT or (evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE)

# マウスが移動したか？    
def checkPaddleMove(self, evt):

    xpos = self.paddle.centerx

    if evt.type == pg.MOUSEMOTION:

        mouse_x, mouse_y = evt.pos
        xpos = mouse_x-self.canvasLeft

    result = False
    if xpos != self.paddle.centerx:
        result = True

    return result,xpos

def changeScreenSize(self,evt):
    if evt.type == pg.KEYDOWN and evt.key == pg.K_F2:

        if self.fullScreen == False:
            self.screen = pg.display.set_mode((df.SCREEN_W,df.SCREEN_H), pg.FULLSCREEN)
            self.fullScreen = True
        else:
            self.screen =  pg.display.set_mode((df.SCREEN_W,df.SCREEN_H))
            self.fullScreen = False

# ------------------------------------------------------------
# プレイ画面の操作
def play(self):
    # 全てのキーの状態を取得
    keyPress = pg.key.get_pressed()

    # マウスが動いたらTrueになり、paddleMoveXにマウス位置が代入される
    paddleMoveFlag = False
    paddleMoveX = 0

    # 全ての操作イベントを確認
    # --------------------------------------------------------    
    for evt in pg.event.get():
        # ゲーム終了を指示したか？
        if should_exit(evt):sys.exit()
        # マウスが移動したか？
        paddleMoveFlag,paddleMoveX = checkPaddleMove(self,evt)

        # 全画面表示切り替え
        changeScreenSize(self,evt)

    # パドル移動
    # --------------------------------------------------------
    if paddleMoveFlag == True:
        # マウスが移動したら、その位置をパドル位置として指定
        xpos = paddleMoveX
    else:
        # マウスが動いていなければ、現状のパドルの位置を取り出す
        xpos = self.paddle.centerx
    # 移動キー押下でパドル位置を移動
    if(keyPress[pg.K_LEFT]): xpos -= 8
    elif(keyPress[pg.K_RIGHT]): xpos += 8
    elif(keyPress[pg.K_a]): xpos -= 8
    elif(keyPress[pg.K_d]): xpos += 8

    # パドル位置が画面にはみ出さないか確認
    # 画面の左右内にいる
    if xpos >= (self.paddle_w / 2) and xpos <= (df.WIDTH - (self.paddle_w / 2)):
        # 何もしない！
        pass
    # 画面左からはみ出ていたら、画面左ジャストの位置に補正
    elif xpos < (self.paddle_w /2): xpos = self.paddle_w / 2
    # 画面右からはみ出ていたら、画面右ジャストの位置に補正
    elif xpos > (df.WIDTH - (self.paddle_w / 2)): xpos = (df.WIDTH - (self.paddle_w / 2))

    # パドルの位置を更新
    self.paddle.centerx = xpos
