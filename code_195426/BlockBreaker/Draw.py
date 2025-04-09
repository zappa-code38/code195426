import pygame as pg
from Define import *

df = Define

def drawAlpha(self,str,x,y):
    length = len(str) * self.fontW
    now_x = x - length/2
    now_y = y-self.fontH / 2
    for s in str:
        code = ord(s)
        code -= 65
        self.screen.blit(self.img_fontList[code],(now_x,now_y))
        ww = self.img_fontList[code].get_width()
        now_x += ww 

def drawNum(self,num,x,y,sp):
    now_x = x
    count = 0
    while num > 0:
        val = num % 10
        self.screen.blit(self.img_numList[val],(now_x,y))
        now_x -= 30
        num //= 10    
        count += 1
    if count < sp:
        for i in range(sp-count):
            self.screen.blit(self.img_numList[0],(now_x,y))
            now_x -= 30

def dispText_center(self,text, x, y):
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

# ------------------------------------------------------------
def title(self):
    # 画面クリア（前回の表示を全てクリアする）
    self.screen.fill(df.DARKGLAY)

    self.screen.blit(self.img_title,(self.canvasLeft,0))

    pg.draw.rect(self.screen, (128, 128, 128), self.btn_topStart)
    dispText_center(self,self.btnText_topStart, self.btn_topStart.centerx, self.btn_topStart.centery)

    if self.returnFlag == True:
        pg.draw.rect(self.screen, (128, 128, 128), self.btn_topReturn)
        dispText_center(self,self.btnText_topReturn, self.btn_topReturn.centerx, self.btn_topReturn.centery)
    else:
        pg.draw.rect(self.screen, (64, 64, 64), self.btn_topReturn)
        dispText_center(self,self.btnText_topReturnDisabled, 
                        self.btn_topReturn.centerx, self.btn_topReturn.centery)

    pg.draw.rect(self.screen, (128, 128, 128), self.btn_topQuit)
    dispText_center(self,self.btnText_topQuit, self.btn_topQuit.centerx, self.btn_topQuit.centery)

def play(self):

    # 画面クリア（前回の表示を全てクリアする）
    self.screen.fill(df.DARKGLAY)

    # 背景画像の描画
    index = 0
    if self.level == 1 and self.stage_display_no == 0: index = 0
    else:
        if self.stage_display_no == 0:      index = 1
        elif self.stage_display_no == 1:    index = 1
        elif self.stage_display_no == 2:    index = 2
        elif self.stage_display_no == 3:    index = 3
        elif self.stage_display_no < 6:     index = 4
        else:                               index = 5

    self.screen.blit(self.img_backList[index],(self.canvasLeft,df.PLAY_TOP))


    # スコアエリアの描画
    topRect = pg.Rect(self.canvasLeft, 0, df.WIDTH, df.PLAY_TOP)
    pg.draw.rect(self.screen, df.BLACK ,topRect)

    alph_y = 12
    num_y = df.PLAY_TOP - 40

    # LEVEL
    drawAlpha(self,"LEVEL",self.canvasLeft + 16 + 100/2, alph_y)

    x = 16 + 100/2 + 30 /2
    sp = 3
    drawNum(self,self.level,self.canvasLeft + x,num_y,sp)

    # STAGE
    drawAlpha(self,"STAGE",self.canvasLeft + df.WIDTH - (16 + 100/2), alph_y)

    x = df.WIDTH - (16 + 100/2 - 30/2)
    sp = 3
    drawNum(self,self.stage+1,self.canvasLeft + x,num_y,sp)

    # SCORE
    drawAlpha(self,"SCORE",self.canvasLeft + df.WIDTH / 2, alph_y)
    
    x = df.WIDTH / 2 + 30*3
    sp = 8
    drawNum(self,self.score,self.canvasLeft + x,num_y,sp)

    # ハートの描画
    x = self.canvasLeft + df.WIDTH - 40
    y = df.SCREEN_H - 40
    for i in range(self.life):
        self.screen.blit(self.img_heartList[0],(x,y))
        x -= 40

    # -----------------

    # ブロックの描画
    for rect,type in self.blocks:
        self.screen.blit(self.img_blockList[type],(self.canvasLeft+rect.x,rect.y))

    # ボールの描画
    self.screen.blit(self.img_ballList[2],
                     (self.canvasLeft + int(self.ball_x)-self.ball_radius, int(self.ball_y)-self.ball_radius))

    if self.overCount > 10:

        if self.gameOver == True:
            imageText = self.font.render("GAME OVER", True, df.WHITE)
            
            pg.draw.rect(self.screen, (128, 128, 128), self.btn_start)
            dispText_center(self,self.btnText_start, self.btn_start.centerx, self.btn_start.centery)

            pg.draw.rect(self.screen, (128, 128, 128), self.btn_exit)
            dispText_center(self,self.btnText_exit, self.btn_exit.centerx, self.btn_exit.centery)  

        else:
            imageText = self.font.render("LOSS !", True, df.WHITE)

        dispText_center(self,imageText,self.canvasLeft + df.WIDTH/2,df.HEIGHT/2 +df.PLAY_TOP)            

    if self.gameOver == False:
        # パドルの描画
        self.screen.blit(self.img_paddleList[0],(self.canvasLeft + self.paddle.x,self.paddle.y))

    if self.pause == True:
        imageText = self.font.render("PAUSE", True, df.WHITE)
        dispText_center(self,imageText,self.canvasLeft + df.WIDTH/2,df.HEIGHT/2 +df.PLAY_TOP)   
    