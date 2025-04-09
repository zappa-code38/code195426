import pygame as pg
from Define import *

df = Define

# プレイ画面の描画
def play(self):
    # 画面クリア（前回の表示を全てクリアする）
    # ----------------------------------------
    # 画面全体を塗りつぶす
    self.screen.fill(df.DARKGLAY)
    # 画面トップのスコアーエリアの背景を塗りつぶす
    rect = pg.Rect(self.canvasLeft,0, df.WIDTH,df.PLAY_TOP)
    pg.draw.rect(self.screen, df.BLACK, rect)
    # プレイエリアの背景を塗りつぶす
    rect = pg.Rect(self.canvasLeft,df.PLAY_TOP, df.WIDTH,df.HEIGHT)
    pg.draw.rect(self.screen, df.GLAY, rect)

    # パドルの描画
    rect = pg.Rect(self.canvasLeft + self.paddle.x,self.paddle.y, self.paddle_w,self.paddle_h)
    pg.draw.rect(self.screen, df.WHITE, rect) 