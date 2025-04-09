import os
import argparse
import pygame as pg
from Define import *
from Stages import *
import Play
import Draw

execFilePath = os.path.dirname(__file__)
os.chdir(execFilePath)

df = Define

class BlockBreaker():
    def __init__(self,args):
        self.fullScreen = args.fullScreen

        pg.init()
        self.sysInit()
        self.setButtonLayout()
    
    # 効果音の再生
    def playSound(self, sname):
        sound = pg.mixer.Sound(self.sound_fx[sname][0])
        sound.set_volume(self.sound_fx[sname][1])
        sound.play()

    @staticmethod
    def getWindowCenterShift(screenW,screenH):
        xx = (screenW - df.WIDTH) // 2
        yy = (screenH - df.HEIGHT) // 2
        return xx,yy

    def setButtonLayout(self):
        # システムパーツ　ボタンなど
        self.btn_W = 160
        self.btn_H = 40
        self.btn_Ws = 100
        self.btnFont = pg.font.SysFont(None, 42)
        # タイトル画面
        self.btnText_topStart = self.btnFont.render("START", True, (0,255,0))
        self.btnText_topReturn = self.btnFont.render("RETURN", True, (255,255,0))
        self.btnText_topReturnDisabled = self.btnFont.render("RETURN", True, (96,96,96))
        self.btnText_topQuit = self.btnFont.render("QUIT", True, (0,0,0))
        # プレイ画面
        self.btnText_start = self.btnFont.render("START", True, (0,255,0))
        self.btnText_exit = self.btnFont.render("EXIT", True, (255,255,0))

        self.buttonLayout()

    def buttonLayout(self):
        self.btn_topStart = pg.Rect(self.canvasLeft + df.WIDTH/2 - self.btn_W/2, df.HEIGHT-100,self.btn_W,self.btn_H)
        self.btn_topReturn = pg.Rect(self.canvasLeft + df.WIDTH - (140 + self.btn_W) , df.HEIGHT-100,self.btn_W,self.btn_H)
        self.btn_topQuit = pg.Rect(self.canvasLeft + 140, df.HEIGHT-100,self.btn_Ws,self.btn_H)

        self.btn_start = pg.Rect(self.canvasLeft + df.WIDTH/2 - self.btn_W/2, df.HEIGHT-150,self.btn_W,self.btn_H)
        self.btn_exit = pg.Rect(self.canvasLeft + df.WIDTH/2 - self.btn_W/2, df.HEIGHT-80,self.btn_W,self.btn_H)

    def changeFullScreen(self):
        if self.fullScreen == True:
            self.screen = pg.display.set_mode((df.SCREEN_W,df.SCREEN_H), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((df.SCREEN_W,df.SCREEN_H))


    def loadResources(self):
        self.img_title = pg.image.load('parts/title.png')

        self.img_blockList = list()
        for i in range(7):
            loadImage = pg.image.load(f'parts/block_{i:04d}.png')
            scaled_image = pg.transform.scale(loadImage, (self.block_w, self.block_h))
            self.img_blockList.append(scaled_image)

        self.img_backList = list()
        for i in range(6):
            self.img_backList.append(pg.image.load(f'parts/back_{i:04d}.png'))

        self.img_ballList = list()
        for i in range(9):
            self.img_ballList.append(pg.image.load(f'parts/ball_{i:04d}.png'))

        self.img_paddleList = list()
        for i in range(1):
            self.img_paddleList.append(pg.image.load(f'parts/paddle_{i:04d}.png'))    

        self.img_heartList = list()
        for i in range(1):
            self.img_heartList.append(pg.image.load(f'parts/heart_{i:04d}.png'))  

        self.img_numList = list()
        for i in range(10):
            self.img_numList.append(pg.image.load(f'parts/num_{i:02d}.png'))  

        self.img_fontList = list()
        s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in s:
            self.img_fontList.append(pg.image.load(f'parts/{i}.png'))
        self.fontW = self.img_fontList[0].get_width()
        self.fontH = self.img_fontList[0].get_height()

        self.sound_fx = {
            # key          # value : サウンドファイル,ボリューム
            'hit_paddle' :('sound/hit_paddle.mp3',0.2),   # パドルヒット
            'hit_block'  :('sound/hit_block.mp3',1.0),   # ブロックヒット
            'clear_stage':('sound/clear_stage.mp3',1.0), # ステージヒット
            'game_over'  :('sound/game_over.mp3',0.4),     # ゲームオーバー
            'hit_etc'    :('sound/hit_etc.mp3',0.3),       # 壁ヒット
            'title_start':('sound/title_start.mp3',0.5),      # ゲームスタート時
            'start'      :('sound/start.mp3',0.5)    # ステージスt－ト時
        }

    def sysInit(self):
        pg.mixer.pre_init(44100, -16, 1, 4096)

        self.clock = pg.time.Clock()
        self.caption = pg.display.set_caption("Block Breaker")
   
        self.changeFullScreen()

        self.canvasLeft:int
        self.canvasTop:int
        window_width, window_height = pg.display.get_window_size()
        self.canvasLeft,self.canvasTop = self.getWindowCenterShift(window_width,window_height)

        self.font = pg.font.Font(None, 64)

        #self.status = 'START_STAGE'
        self.status = 'TITLE'

        self.returnFlag = False

        self.stageNo = 0
        self.startFlag:bool

        self.gameOver = False

        self.pause = False

        self.level = 1
        self.stage = 0
        self.score = 0
        self.life = 3
        self.stage_display_no = 0

        # スコアエリア
        self.topRect = pg.Rect(0, 0, df.WIDTH, df.PLAY_TOP)

        # ボールの半径
        self.ball_radius = df.BALL_RADIUS

        # パドルの表示サイズ
        self.paddle_w = df.PADDLE_W       # 幅
        self.paddle_h = df.PADDLE_H       # 高さ

        # ブロックのサイズ
        self.block_w = df.BLOCK_W        # 幅
        self.block_h = df.BLOCK_H        # 高さ

        self.block_layout = Stages.stage

        self.loadResources()
        
    def stageInit(self):
        
        # マウスカーソル非表示
        pg.mouse.set_visible(False)

        self.startFlag = False

        # パドル初期化
        # パドル座標を画面中央、下から６４ドットの位置にする。
        x = df.WIDTH / 2
        y = df.SCREEN_H - 64
        # パドル表示位置は、(x,y)座標が中央になるように設定
        self.paddle = pg.Rect(x - (self.paddle_w / 2),y - (self.paddle_h / 2), self.paddle_w,self.paddle_h)

        # ボールの座標
        # パドルの上面中央の位置にセット
        self.ball_x = self.paddle.centerx
        self.ball_y = self.paddle.centery - self.paddle_h / 2

        # ボールの速度
        self.speed_x = 0.0
        self.speed_y = 0.0

        # マウスカーソル初期位置
        # パドル座標に合わせる
        pg.mouse.set_pos((self.canvasLeft+x,y)) # = (x,y)

        # ステージブロック作成　（横１０ブロック構成）
        self.blocks = []
        max = len(self.block_layout[self.stage_display_no])
        for cc in range(max):
            if self.block_layout[self.stage_display_no][cc] != 0:
                x = (cc % 10) * (self.block_w+4) + 58
                y = int(cc / 10) * (self.block_h+4) + 64 + df.PLAY_TOP
                type = self.block_layout[self.stage_display_no][cc]-1
                self.blocks.append((pg.Rect(x,y,self.block_w,self.block_h),type))

        self.status = 'PLAY'
        self.overCount = 0

    def resetGame(self):
        self.level = 1
        self.stage = 0
        self.score = 0
        self.life = 3
        self.stage_display_no = 0
        self.gameOver = False
        self.overCount = 0
        self.status = 'START_STAGE'

    def main(self):
        while True:
            if self.status == 'TITLE':
                Play.title(self)
                Draw.title(self)

            elif self.status == 'START_STAGE':
                self.stageInit()

            elif self.status == 'PLAY':
                Play.play(self)
                Draw.play(self)

            elif self.status == 'GAME_OVER':
                Play.over(self)
                Draw.play(self)

            pg.display.update()
            self.clock.tick(60)

# ------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullScreen", action='store_true', help="full screen")
    args = parser.parse_args()

    game = BlockBreaker(args)
    game.main()