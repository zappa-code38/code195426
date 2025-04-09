import os
import pygame as pg
from Define import *
import Play
import Draw

execFilePath = os.path.dirname(__file__)
os.chdir(execFilePath)

df = Define

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
        self.caption = pg.display.set_caption("Block Breaker")
        # ゲーム全体の画面サイズを設定してスクリーンを初期化
        self.screen = pg.display.set_mode((df.SCREEN_W,df.SCREEN_H))
        # 起動時は全画面表示にしない
        self.fullScreen = False

        # プレイエリアの縦横比（アスペクト比）がスクリーンサイズに影響しないように、
        # プレイエリアをスクリーン中央に表示させる。
        # 縦サイズはスクリーンサイズに合わせてあるので、横方向の表示左座標(canvasLeft)のみ必要となる
        window_width, window_height = pg.display.get_window_size()
        self.canvasLeft,_ = self.getWindowCenterShift(window_width,window_height)

        # パドル初期化
        # パドル座標を画面中央、下から６４ドットの位置にする。
        x = df.WIDTH / 2
        y = df.SCREEN_H - 64
        # パドルの表示サイズ
        self.paddle_w = df.PADDLE_W       # 幅
        self.paddle_h = df.PADDLE_H       # 高さ
        # パドル表示位置は、(x,y)座標が中央になるように矩形設定
        self.paddle = pg.Rect(x - (self.paddle_w / 2),y - (self.paddle_h / 2), self.paddle_w,self.paddle_h)

    @staticmethod   # selfを継承しない関数
    def getWindowCenterShift(screenW,screenH):
        xx = (screenW - df.WIDTH) // 2
        yy = (screenH - df.HEIGHT) // 2
        return xx,yy

    def main(self):
        # ゲーム終了まで繰り返す
        while True:

            Play.play(self)
            Draw.play(self)

            # 描画内容をスクリーンに反映
            pg.display.update()
            # 秒間６０フレーム
            self.clock.tick(60)

# ------------------------------------------------------------
# pygame：ゲームシステム／プロトタイプ　ーーー　ファイル分割記述型
# ------------------------------------------------------------
if __name__ == '__main__':
    # BlockBreakerクラスのインスタンスを作成
    game = BlockBreaker()
    # mainメソッドを呼び出す
    game.main()