import sys
import pygame as pg

# デファイン値
# ---------------------------------
# カラー値
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GLAY = (128,128,128)
BLACK = (0,0,0)
DARKGLAY = (64,64,64)

# コンテンツサイズ
PLAY_TOP = 60
WIDTH = 853
HEIGHT = 720 - PLAY_TOP

# 画面サイズ
SCREEN_W = 1280
SCREEN_H = 720

# 各パーツサイズ
PADDLE_W = 96
PADDLE_H = 16

class BlockBreaker():
    # インスタンス作成時にコールされる
    def __init__(self):
        # pygame初期化
        pg.init()
        # 独自の初期化処理
        self.sysInit()

    def sysInit(self):

        # pygameの時間処理を設定
        self.clock = pg.time.Clock()
        # キャプションにゲームタイトルを表示
        pg.display.set_caption("Block Breaker")
        # ゲーム全体の画面サイズを設定してスクリーンを初期化
        self.screen = pg.display.set_mode((SCREEN_W,SCREEN_H))
        # 起動時は全画面表示にしない
        self.fullScreen = False

        # プレイエリアの縦横比（アスペクト比）がスクリーンサイズに影響しないように、
        # プレイエリアをスクリーン中央に表示させる。
        # 縦サイズはスクリーンサイズに合わせてあるので、横方向の表示左座標(canvasLeft)のみ必要となる
        window_width, window_height = pg.display.get_window_size()
        self.canvasLeft,_ = self.getWindowCenterShift(window_width,window_height)

        # パドル初期化
        # パドル座標を画面中央、下から６４ドットの位置にする。
        x = WIDTH / 2
        y = SCREEN_H - 64
        # パドルの表示サイズ
        self.paddle_w = PADDLE_W       # 幅
        self.paddle_h = PADDLE_H       # 高さ
        # パドル表示位置は、(x,y)座標が中央になるように矩形設定
        self.paddle = pg.Rect(x - (self.paddle_w / 2),y - (self.paddle_h / 2), self.paddle_w,self.paddle_h)

    @staticmethod   # selfを継承しない関数
    def getWindowCenterShift(screenW,screenH):
        xx = (screenW - WIDTH) // 2
        yy = (screenH - HEIGHT) // 2
        return xx,yy

    # ゲーム終了条件
    # ウィンドウの右上「ｘ」が押されたか？ または Escキーが押されたか？ 
    def should_exit(self,evt):
        return evt.type == pg.QUIT or (evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE)
    
    # マウスが移動したか？
    def checkPaddleMove(self, evt):

        xpos = self.paddle.centerx

        if evt.type == pg.MOUSEMOTION:

            mouse_x, _ = evt.pos
            xpos = mouse_x-self.canvasLeft

        result = False
        if xpos != self.paddle.centerx:
            result = True

        return result,xpos

    def changeScreenSize(self,evt):
        if evt.type == pg.KEYDOWN and evt.key == pg.K_F2:

            if self.fullScreen == False:
                self.screen = pg.display.set_mode((SCREEN_W,SCREEN_H), pg.FULLSCREEN)
                self.fullScreen = True
            else:
                self.screen =  pg.display.set_mode((SCREEN_W,SCREEN_H))
                self.fullScreen = False

    # プレイヤーの操作
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
            if self.should_exit(evt):sys.exit()
            # マウスが移動したか？
            paddleMoveFlag,paddleMoveX = self.checkPaddleMove(evt)

            # 全画面表示切り替え
            self.changeScreenSize(evt)

        # パドル移動
        # --------------------------------------------------------
        if paddleMoveFlag == True:
            # マウスが移動したら、その位置をパドル位置として指定
            xpos = paddleMoveX
        else:
            # マウスが動いていなければ、現状のパドルの位置を取り出す
            xpos = self.paddle.centerx
        # 移動キー押下でパドル位置を更新
        if(keyPress[pg.K_LEFT]): xpos -= 8
        elif(keyPress[pg.K_RIGHT]): xpos += 8
        elif(keyPress[pg.K_a]): xpos -= 8
        elif(keyPress[pg.K_d]): xpos += 8

        # パドル位置が画面にはみ出さないか確認
        # 画面の左右内にいる
        if xpos >= (self.paddle_w / 2) and xpos <= (WIDTH - (self.paddle_w / 2)):
            # 何もしない！
            pass
        # 画面左からはみ出ていたら、画面左ジャストの位置に補正
        elif xpos < (self.paddle_w /2): xpos = self.paddle_w / 2
        # 画面右からはみ出ていたら、画面右ジャストの位置に補正
        elif xpos > (WIDTH - (self.paddle_w / 2)): xpos = (WIDTH - (self.paddle_w / 2))

        # パドルの位置を更新
        self.paddle.centerx = xpos

    # 画面描画
    def draw(self):
        # 画面クリア（前回の表示を全てクリアする）
        # ----------------------------------------
        # 画面全体を塗りつぶす
        self.screen.fill(DARKGLAY)
        # 画面トップのスコアーエリアの背景を塗りつぶす
        rect = pg.Rect(self.canvasLeft,0, WIDTH,PLAY_TOP)
        pg.draw.rect(self.screen, BLACK, rect)
        # プレイエリアの背景を塗りつぶす
        rect = pg.Rect(self.canvasLeft,PLAY_TOP, WIDTH,HEIGHT)
        pg.draw.rect(self.screen, GLAY, rect)

        # パドルの描画
        rect = pg.Rect(self.canvasLeft + self.paddle.x,self.paddle.y, self.paddle_w,self.paddle_h)
        pg.draw.rect(self.screen, WHITE, rect)

    def main(self):
        # ゲーム終了まで繰り返す
        while True:

            self.play()
            self.draw()

            # 描画内容をスクリーンに反映
            pg.display.update()
            # 秒間６０フレーム
            self.clock.tick(60)

# ------------------------------------------------------------
# pygame：ゲームシステム／プロトタイプ　ーーー　１ファイル記述型
# ------------------------------------------------------------
if __name__ == '__main__':
    # BlockBreakerクラスのインスタンスを作成
    game = BlockBreaker()
    # mainメソッドを呼び出す
    game.main()