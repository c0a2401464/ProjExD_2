import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
        """
        引数：こうかとんRect
        戻り値：タプル（横方向判定結果，縦方向判定結果）
        画面内ならTrue，画面外ならFalse
        """
        yoko,tate = True,True
        if obj_rct.left < 0 or WIDTH < obj_rct.right:
            yoko = False
        if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
            tate = False
        return yoko, tate

def gameover(screen: pg.Surface) -> None:
    blackout = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(blackout,(0,0,0),(0,0,1100,650))
    blackout.set_alpha(200)
    screen.blit(blackout,(0,0))
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",True,(255,255,255))
    screen.blit(txt, [400,280])
    kk8_img = pg.image.load("fig/8.png")
    screen.blit(kk8_img,[330,280])
    screen.blit(kk8_img,[730,280])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  # 黒背景を透過
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"),0,0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH),random.randint(0,WIDTH)
    bb_img.set_colorkey((0, 0, 0))
    vx,vy = +5,+5
    bb_imgs, bb_accs = init_bb_imgs()  # 爆弾の画像と加速段階の初期化



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]= mv[0]
                sum_mv[1]= mv[1]

        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        # 最大でlevel = 9まで
        avx = vx*bb_accs[min(tmr // 500, 9)]
        avy = vy*bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
