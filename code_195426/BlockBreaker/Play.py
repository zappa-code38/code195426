import sys
import pygame as pg
from Define import *

df = Define

# 数値の符号を判別する関数
def sgn(a):
    return 1 if a > 0 else -1

# TITLE -----------------------
def should_titleStart(self, evt):
    return (evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE) or \
    (evt.type == pg.MOUSEBUTTONDOWN and self.btn_topStart.collidepoint(evt.pos[0],evt.pos[1]))

def should_titleExit(self,evt):
    return evt.type == pg.QUIT or (evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE) or \
    (evt.type == pg.MOUSEBUTTONDOWN and self.btn_topQuit.collidepoint(evt.pos[0],evt.pos[1]))

def should_titleReturn(self, evt):
    return self.returnFlag == True and \
    (evt.type == pg.MOUSEBUTTONDOWN and self.btn_topReturn.collidepoint(evt.pos[0],evt.pos[1]))

# PLAY ------------------------
def should_exit(evt):
    return evt.type == pg.QUIT

def should_exitTop(evt):
    return evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE

def should_gotoTop(self,evt):
    return  evt.type == pg.MOUSEBUTTONDOWN and self.btn_exit.collidepoint(evt.pos[0],evt.pos[1])

def should_restart(self, evt):
    return  ((evt.type == pg.KEYDOWN and evt.key == pg.K_RETURN)  or  
      (evt.type == pg.MOUSEBUTTONDOWN and self.btn_start.collidepoint(evt.pos[0],evt.pos[1])))

def should_start(self, evt):
    if self.startFlag == True: return False
    return evt.type == pg.MOUSEBUTTONDOWN or (evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE)

def should_pause(self, evt):
    return self.gameOver == False and evt.type == pg.KEYDOWN and evt.key == pg.K_F12

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
            self.fullScreen = True
        else:
            self.fullScreen = False

        self.changeFullScreen()

# ------------------------------------------------------------
def title(self):
    for evt in pg.event.get():
        if should_titleExit(self,evt):sys.exit()

        if should_titleStart(self,evt):
            self.resetGame()
            self.playSound("title_start")
            self.returnFlag = False
            return
        if should_titleReturn(self,evt):
            self.status = 'PLAY'
            self.returnFlag = False
            # マウスカーソル表示
            pg.mouse.set_visible(False)

        changeScreenSize(self,evt)


def over(self):
    for evt in pg.event.get():
        if should_exit(evt):sys.exit()

        if should_exitTop(evt):
            self.resetGame()
            self.status = 'TITLE'
        
        if should_gotoTop(self,evt):
            self.resetGame()
            self.status = 'TITLE'

        if should_restart(self,evt):
            self.resetGame()
            return


def play(self):

    keyPress = pg.key.get_pressed()

    paddleMoveFlag = False
    paddleMoveX = 0
    for evt in pg.event.get():

        if should_exit(evt):sys.exit()
        
        if should_exitTop(evt):
            self.status = 'TITLE'
            # マウスカーソル表示
            pg.mouse.set_visible(True)
            self.returnFlag = True

        if should_start(self,evt):
            self.startFlag = True
            self.speed_x = 2.0 + self.level*0.6
            self.speed_y = -2.5 - self.level*0.6
            self.playSound("start")
            return

        if should_pause(self,evt):
            if self.pause == False:
                self.pause = True
            else:
                self.pause = False

        paddleMoveFlag,paddleMoveX = checkPaddleMove(self,evt)

        changeScreenSize(self,evt)

    if self.pause == True: return

    if paddleMoveFlag == True:
        xpos = paddleMoveX
    else:
        xpos = self.paddle.centerx
    # 移動キー押下でパドル位置を移動
    if(keyPress[pg.K_LEFT]): xpos -= 8
    elif(keyPress[pg.K_RIGHT]): xpos += 8
    elif(keyPress[pg.K_a]): xpos -= 8
    elif(keyPress[pg.K_d]): xpos += 8

    # パドル位置が画面にはみ出さないか確認
    # 画面の左右内にいる
    if xpos >= (self.paddle_w / 2) and xpos <= (df.WIDTH - (self.paddle_w / 2)):
        #self.paddle.centerx = xpos
        pass
    # 画面左からはみ出ていたら、画面左ジャストの位置に補正
    elif xpos < (self.paddle_w /2): xpos = self.paddle_w / 2
    # 画面右からはみ出ていたら、画面右ジャストの位置に補正
    elif xpos > (df.WIDTH - (self.paddle_w / 2)): xpos = (df.WIDTH - (self.paddle_w / 2))

    self.paddle.centerx = xpos

    # ボール移動方向
    x = self.ball_x + self.speed_x
    y = self.ball_y + self.speed_y
    # 画面枠に対するボールの反射
    soundFlag = False
    if x < self.ball_radius or x > (df.WIDTH - self.ball_radius): 
        self.speed_x = -self.speed_x
        soundFlag = True
    if y < df.PLAY_TOP + self.ball_radius: 
        self.speed_y = -self.speed_y
        soundFlag = True 
    if y >df.HEIGHT: 
        self.overCount += 1
        soundFlag = False
    
    if soundFlag == True:
        self.playSound("hit_etc")

    # パドルに対するボールの反射
    dx = self.paddle.centerx - x
    dy = self.paddle.centery - y
    if dy == 0: dy = 1
    if abs(dx) < (self.paddle_w / 2 + self.ball_radius) and abs(dy) < (self.paddle_h / 2 +self.ball_radius):
        if abs(dx / dy) > (self.paddle_w / self.paddle_h):
            self.speed_x = -self.speed_x
            self.ball_x = self.paddle.centerx - sgn(dx) * (self.paddle_w/2 + self.ball_radius)
        else:
            self.speed_x = -dx / 10
            self.speed_y = -self.speed_y
            self.ball_y = self.paddle.centery - sgn(dy) * (self.paddle_h/2 + self.ball_radius)

        # パドルヒット時の効果音
        self.playSound("hit_paddle")

    debugFlag = False
    # ブロックに対するボールの反射
    for block in self.blocks:
        dx = block[0].centerx - x
        dy = block[0].centery - y
        if dy == 0: dy = 1
        if abs(dx) < (self.block_w / 2 + self.ball_radius) and abs(dy) < (self.block_h / 2 + self.ball_radius):
            # ブロックヒット！
            if abs(dx / dy) > (self.block_w / self.block_h):
                self.speed_x = -self.speed_x
                self.ball_x = block[0].centerx - sgn(dx) * (self.block_w / 2 +self.ball_radius)
            else:
                self.speed_y = -self.speed_y
                self.ball_y = block[0].centery - sgn(dy) * (self.block_h / 2 + self.ball_radius)

            # ブロックを消して、得点加算
            self.blocks.remove(block)
            yy = block[0].y - (64 + df.PLAY_TOP)
            self.score += 10 * (5 - int(yy / df.BLOCK_H)) * self.level

            # ブロックヒット時の効果音
            self.playSound("hit_block")

            debugFlag = True

            break


    self.ball_x += self.speed_x
    self.ball_y += self.speed_y

    if self.startFlag == False:
        self.ball_x = self.paddle.centerx
        self.ball_y = self.paddle.centery - (self.paddle_h / 2 + self.ball_radius)

    if self.overCount > 0:

        # ゲームオーバー時の効果音
        if self.overCount == 10:
            self.playSound("game_over")
            # マウスカーソル表示
            pg.mouse.set_visible(True)


        if self.overCount > 100:

            self.life -= 1

            if self.life < 0:    
                self.gameOver = True
                self.status = 'GAME_OVER'

            else:
                self.status = 'START_STAGE'

    # 全ブロッククリアしたか？
    #if debugFlag == True:
    if len(self.blocks) == 0:
        self.stage += 1
        self.stage_display_no += 1
        if self.stage_display_no >= len(self.block_layout): 
            self.stage_display_no = 0
            #   全ステージパターンクリア毎にライフ加算
            self.life += 1

        # レベルは２ステージクリア毎に１つアップする
        self.level = 1 + int(self.stage/2)

        # ステージクリア時の効果音
        self.playSound("clear_stage")

        self.status = 'START_STAGE'