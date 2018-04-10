import pygame,pickle,FCobjects,FCweapons
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (117,117,117)
BGGREY = (31,31,31)
MRED = (173,16,16)
RBLUE = (0,0,179)
RGREEN = (32,179,16)
TPYELLOW = (229,237,0)
HEALGREEN = (13,189,19)
INVISCOL = (63,171,153)

mapname="tptest"
guns_allowed = True
startPos=[650,10,30,10]

map_info = pickle.load(open(mapname+".p","rb"))

"""[[WHITE,0,400,100,10,False],
[WHITE,0,300,100,10,False],
[WHITE,0,215,100,10,False],
[WHITE,600,215,100,10,False],
[WHITE,0,480,700,20,False],
[WHITE,600,400,100,10,False],
[WHITE,600,300,100,10,False],
[WHITE,300,350,100,10,False],
[WHITE,150,215,400,10,False],
[WHITE,340,184,20,31,False],
[WHITE,340,449,20,31,False],
[WHITE,0,150,20,20,False],
[BLACK,340,10,20,20,False],
[WHITE,680,15z0,20,20,False],
[WHITE,175,60,20,20,False],
[WHITE,505,60,20,20,False],
]"""

font = pygame.font.SysFont('Calibri', 20,True,False)

heal_respawn_list = []
p_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
bb_list = pygame.sprite.Group()
instaDeath_list = pygame.sprite.Group()
tp_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
heal_list = pygame.sprite.Group()
bullet1_list = pygame.sprite.Group()
bullet2_list = pygame.sprite.Group()
shield1_list = pygame.sprite.Group()

def GUIUpdates():
    lives1 = font.render(str(player1.life), 1,MRED)
    lives2 = font.render(str(player2.life), 1,RBLUE)
    player1_clip = font.render(str(player1.currWeapon.currentClip), 1,GREY)
    player2_clip = font.render(str(player2.currWeapon.currentClip), 1,GREY)
    if guns_allowed:
        player1_wins = font.render(str(player1.score), 1,MRED)
        player2_wins = font.render(str(player2.score), 1,RBLUE)
    elif not guns_allowed:
        player1_wins = font.render(str(player1.deaths), 1,MRED)
        player2_wins = font.render(str(player2.deaths), 1,RBLUE)
    return player1_wins,player2_wins,lives1,lives2,player2_clip,player1_clip

def collisions(blink_blue,blink_red):
    for item in bullet1_list:
        bull_dis = pygame.sprite.spritecollide(item,p_list,False)
        for i in bull_dis:
            item.kill()

        bull_dis = pygame.sprite.spritecollide(item,bb_list,False)
        for i in bull_dis:
            item.kill()
            print("b del")
    for item in bullet2_list:
        bull_dis = pygame.sprite.spritecollide(item,p_list,False)
        for i in bull_dis:

            item.kill()
        bull_dis = pygame.sprite.spritecollide(item,bb_list,False)
        for i in bull_dis:
            item.kill()
            print("b del")
    coll_list = pygame.sprite.spritecollide(player1, bullet2_list, True)
    for i in coll_list:
        if blink_red == 0:
            blink_red = 6
        player1.life -= 1
        player1.been_shot = 30
        if player1.rect.x - player2.rect.x < 0:
            player1.shot_push = -4
            player1.shot_recovery = 4/30
            if player1.change_x==-4.5:
                player1.shot_push = -10
                player1.shot_recovery = 7/30
            elif player1.change_x==5:
                player1.been_shot = 20
                player1.shot_push = -2
                player1.shot_recovery = 2/20
        elif player1.rect.x - player2.rect.x > 0:
            player1.shot_push = 4
            player1.shot_recovery = 4/30
            if player1.change_x==5:
                player1.shot_push = 10
                player1.shot_recovery = 7/30
            elif player1.change_x==-4.5:
                player1.been_shot = 20
                player1.shot_push = 2
                player1.shot_recovery = 2/20
        if player1.change_y==0:
            player1.change_y += -2
    coll_list = pygame.sprite.spritecollide(player2, bullet1_list, True)
    for i in coll_list:
        if blink_blue == 0:
            blink_blue = 6
        player2.life -= 1
        player2.been_shot = 30
        if player2.rect.x - player1.rect.x < 0:
            player2.shot_push = -4
            player2.shot_recovery = 4/30
            if player2.change_x==-4.5:
                player2.shot_push = -10
                player2.shot_recovery = 7/30
            elif player2.change_x==5:
                player2.been_shot = 20
                player2.shot_push = -2
                player2.shot_recovery = 2/20
        elif player2.rect.x - player1.rect.x > 0:
            player2.shot_push = 4
            player2.shot_recovery = 4/30
            if player2.change_x==5:
                player2.shot_push = 10
                player2.shot_recovery = 7/30
            elif player2.change_x==-4.5:
                player2.been_shot = 20
                player2.shot_push = 2
                player2.shot_recovery = 2/20
        if player1.change_y==0:
            player2.change_y += -2
    instad_list = pygame.sprite.spritecollide(player1, instaDeath_list,False)
    for i in instad_list:
        #player1.life-=1
        player1.rect.x = int(startPos[0])
        player1.rect.y = int(startPos[1])
    instad_list = pygame.sprite.spritecollide(player2, instaDeath_list,False)
    for i in instad_list:
        #player2.life-=1
        player2.rect.x = int(startPos[0])
        player2.rect.y = int(startPos[1])
    tp_collision_list = pygame.sprite.spritecollide(player1, tp_list, False)
    if len(tp_collision_list)<2 and len(tp_collision_list)!=0:
        for i in tp_collision_list:
            if i.tpdest=="spawn":
                player1.rect.x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.rect.x = int(i.tpdest.split(",")[0])
                player1.rect.y = int(i.tpdest.split(",")[1])
        player1.deaths+=1
    if len(tp_collision_list)>1:
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.top)
        tp_collision_cords.sort()
        if tp_collision_cords[0]==tp_collision_cords[1]:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player1.rect.x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        elif player1.rect.top<tp_collision_cords[0] and player1.change_y>0:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player1.rect.x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.bottom)
        tp_collision_cords.sort()
        if tp_collision_cords[-1]==tp_collision_cords[-2]:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player1.rect.x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.rect.x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        elif player1.rect.top>max(tp_collision_cords) and player1.change_y<0:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player1.rect.x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.rect.x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        player1.deaths+=1
    tp_collision_list = pygame.sprite.spritecollide(player2, tp_list, False)
    if len(tp_collision_list)==1:
        for i in tp_collision_list:
            if i.tpdest=="spawn":
                player2.rect.x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.rect.x = int(i.tpdest.split(",")[0])
                player2.rect.y = int(i.tpdest.split(",")[1])
        player2.deaths+=1
    if len(tp_collision_list)>1:
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.top)
        tp_collision_cords.sort()
        if tp_collision_cords[0]==tp_collision_cords[1]:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player2.rect.x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        elif player2.rect.top<min(tp_collision_cords) and player2.change_y>0:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player2.rect.x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.bottom)
        tp_collision_cords.sort()
        if tp_collision_cords[-1]==tp_collision_cords[-2]:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player2.rect.x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.rect.x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        elif player2.rect.top>max(tp_collision_cords) and player2.change_y<0:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player2.rect.x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.rect.x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        player2.deaths+=1
    heal_collision_list = pygame.sprite.spritecollide(player1, heal_list, False)
    for i in heal_collision_list:
        player1.life+=1
        i.kill()
        heal_respawn_list.append(i)
    heal_collision_list = pygame.sprite.spritecollide(player2, heal_list, False)
    for i in heal_collision_list:
        player2.life+=1
        i.kill()
        heal_respawn_list.append(i)
    return blink_blue,blink_red

def keyPressed(key):
    keys=pygame.key.get_pressed()
    if keys[key]:
        return True
    else:
        return False

try:guns_allowed = map_info[0][4]
except:pass


if len(map_info[0])>=4:
    startPos=map_info[0][:4]
player1 = FCobjects.player(MRED,int(startPos[0]),int(startPos[1]),1)
all_sprites.add(player1)
player_list.add(player1)

player2 = FCobjects.player(RBLUE,int(startPos[2]),int(startPos[3]),2)
all_sprites.add(player2)
player_list.add(player2)


for i in range(1,len(map_info)):
    print(map_info[i])
    if map_info[i][0]=="white":
        map_info[i][0]=WHITE
    if map_info[i][0]=="black" or map_info[i][0]=="grey":
        map_info[i][0]=GREY
    if map_info[i][0]=="yellow":
        map_info[i][0]=TPYELLOW
    if map_info[i][0]=="green":
        map_info[i][0]=HEALGREEN
    if map_info[i][6]=="normal":
        platform = FCobjects.Block(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4])
        p_list.add(platform)
    elif map_info[i][6]=="killer":
        platform = FCobjects.Block(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4])
        instaDeath_list.add(platform)
    elif map_info[i][6]=="teleporter":
        platform = FCobjects.teleporterBlock(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4],map_info[i][7])
        tp_list.add(platform)
    elif map_info[i][6]=="healer":
        platform = FCobjects.healBlock(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4],map_info[i][7])
        heal_list.add(platform)
    all_sprites.add(platform)

bullet_block = FCobjects.Block(BLACK, -30,0,20,500)
bb_list.add(bullet_block)
all_sprites.add(bullet_block)
bullet_block = FCobjects.Block(BLACK, 710,0,20,500)
bb_list.add(bullet_block)
all_sprites.add(bullet_block)


def main():
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    icon=pygame.image.load("icon.png")
    pygame.display.set_caption("Fight Clip")
    if guns_allowed:
        player1.currWeapon=FCweapons.handGun(1)
        player2.currWeapon=FCweapons.handGun(2)
    gun_xoffset=4
    blink_red = 0
    blink_blue = 0
    done = False
    slowmo=False
    clock = pygame.time.Clock()
    while not done:
        if keyPressed(pygame.K_DOWN):
            player1.crouch()
        if keyPressed(pygame.K_s):
            player2.crouch()
        if keyPressed(pygame.K_SPACE):
            slowmo=True
        else:
            slowmo=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT:
                    player1.change_x = -4.5
                    if player1.crouching:
                        player1.change_x = -3.5
                if event.key == pygame.K_RIGHT:
                    player1.change_x = 5
                    if player1.crouching:
                        player1.change_x = 3.5
                if event.key == pygame.K_RCTRL:
                    player1.jump(p_list)
                if event.key == pygame.K_PERIOD:
                    player1.shoot(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites)
                if event.key == pygame.K_UP:
                    player1.reload()
                if event.key == pygame.K_a:
                    player2.change_x = -4.5
                    if player2.crouching:
                        player2.change_x = -3.5
                if event.key == pygame.K_d:
                    player2.change_x = 5
                    if player2.crouching:
                        player2.change_x = 3.5
                if event.key == pygame.K_LSHIFT:
                    player2.jump(p_list)
                if event.key == pygame.K_s:
                    player2.crouch()
                if event.key == pygame.K_LESS:
                    player2.shoot(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites)
                if event.key == pygame.K_w:
                    player2.reload()
                if event.key == pygame.K_F11:
                    player1.bt = 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player1.change_x < 0:
                    player1.change_x = 0
                if event.key == pygame.K_RIGHT and player1.change_x > 0:
                    player1.change_x = 0
                if event.key == pygame.K_DOWN:
                    player1.stand(p_list)
                if event.key == pygame.K_a and player2.change_x < 0:
                    player2.change_x = 0
                if event.key == pygame.K_d and player2.change_x > 0:
                    player2.change_x = 0
                if event.key == pygame.K_s:
                    player2.stand(p_list)
        blink_blue,blink_red=collisions(blink_blue,blink_red)
        screen.fill(BGGREY)
        player1_wins,player2_wins,lives1,lives2,player2_clip,player1_clip = GUIUpdates()
        all_sprites.update()
        player1.movement_and_collision(p_list,player1,player2)
        player2.movement_and_collision(p_list,player1,player2)
        all_sprites.draw(screen)
        player_list.draw(screen)
        screen.blit(player1_wins, (400,481))
        screen.blit(player2_wins, (285,481))
        if guns_allowed:
            screen.blit(lives1, (player1.rect.x+(10-(lives1.get_width()/2)),player1.rect.y-lives1.get_height()-3))
            screen.blit(lives2, (player2.rect.x+(10-(lives2.get_width()/2)),player2.rect.y-lives2.get_height()-3))
            if player1.rect.x - player2.rect.x <= 0:
                screen.blit(player1_clip, (player1.rect.x-5-player1_clip.get_width(),player1.rect.y+2))
                screen.blit(gun0_image_right, (player1.rect.x+4,player1.rect.y+7))
            elif player1.rect.x - player2.rect.x > 0:
                screen.blit(player1_clip, (player1.rect.x+24,player1.rect.y+2))
                screen.blit(gun0_image_left, (player1.rect.x-24,player1.rect.y+7))
            if player2.rect.x - player1.rect.x <= 0:
                screen.blit(player2_clip, (player2.rect.x-5-player2_clip.get_width(),player2.rect.y+2))
                screen.blit(gun0_image_right, (player2.rect.x+4,player2.rect.y+7))
            elif player2.rect.x - player1.rect.x > 0:
                screen.blit(player2_clip, (player2.rect.x+24,player2.rect.y+2))
                screen.blit(gun0_image_left, (player2.rect.x-24,player2.rect.y+7))
        if len(heal_respawn_list)>0:
            for j in heal_respawn_list:
                if j.heal_timer<int(j.heal_respawn_time)*60:
                    j.heal_timer += 1
                else:
                    heal_list.add(j)
                    all_sprites.add(j)
                    j.heal_timer=0
                    heal_respawn_list.remove(j)
        if blink_red > 0:
            pygame.draw.rect(screen, MRED, [0,0,700,500])
            blink_red-=1
            print("blinked")
        if blink_blue > 0:
            pygame.draw.rect(screen, RBLUE, [0,0,700,500])
            blink_blue-=1
            print("blinked")
        pygame.display.flip()
        if player1.life<=0 or player1.rect.y > 800:
            player1.life = 0
            while player1.life == 0 and not done:
                screen.fill(BLACK)
                all_sprites.draw(screen)
                q = font.render("Royal wins, wanna play again bruh?",1,RBLUE)
                screen.blit(q,(200,150))
                screen.blit(player1_wins, (400,481))
                screen.blit(player2_wins, (285,481))
                if guns_allowed:
                    screen.blit(lives1, (player1.rect.x+(10-(lives1.get_width()/2)),player1.rect.y-lives1.get_height()-3))
                    screen.blit(lives2, (player2.rect.x+(10-(lives2.get_width()/2)),player2.rect.y-lives2.get_height()-3))
                    if player1.rect.x - player2.rect.x <= 0:
                        screen.blit(player1_clip, (player1.rect.x-5-player1_clip.get_width(),player1.rect.y+2))
                        screen.blit(gun0_image_right, (player1.rect.x+4,player1.rect.y+7))
                    elif player1.rect.x - player2.rect.x > 0:
                        screen.blit(player1_clip, (player1.rect.x+24,player1.rect.y+2))
                        screen.blit(gun0_image_left, (player1.rect.x-24,player1.rect.y+7))
                    if player2.rect.x - player1.rect.x <= 0:
                        screen.blit(player2_clip, (player2.rect.x-5-player2_clip.get_width(),player2.rect.y+2))
                        screen.blit(gun0_image_right, (player2.rect.x+4,player2.rect.y+7))
                    elif player2.rect.x - player1.rect.x > 0:
                        screen.blit(player2_clip, (player2.rect.x+24,player2.rect.y+2))
                        screen.blit(gun0_image_left, (player2.rect.x-24,player2.rect.y+7))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            player1.reset(startPos,player1,player2)
                            player2.reset(startPos,player1,player2)
                            player2.score += 1
                            player1.deaths+=1
                            blink_red = 0
                            blink_blue = 0
                        elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                            done = True
                pygame.display.flip()
        if player2.life<=0 or player2.rect.y > 800:
            player2.life = 0
            while player2.life == 0 and not done:
                screen.fill(BLACK)
                all_sprites.draw(screen)
                q = font.render("Ruby wins, wanna play again bruh?",1,MRED)
                screen.blit(q,(200,150))
                screen.blit(player1_wins, (400,481))
                screen.blit(player2_wins, (285,481))
                if guns_allowed:
                    screen.blit(lives1, (player1.rect.x+(10-(lives1.get_width()/2)),player1.rect.y-lives1.get_height()-3))
                    screen.blit(lives2, (player2.rect.x+(10-(lives2.get_width()/2)),player2.rect.y-lives2.get_height()-3))
                    if player1.rect.x - player2.rect.x <= 0:
                        screen.blit(player1_clip, (player1.rect.x-5-player1_clip.get_width(),player1.rect.y+2))
                        screen.blit(gun0_image_right, (player1.rect.x+4,player1.rect.y+7))
                    elif player1.rect.x - player2.rect.x > 0:
                        screen.blit(player1_clip, (player1.rect.x+24,player1.rect.y+2))
                        screen.blit(gun0_image_left, (player1.rect.x-24,player1.rect.y+7))
                    if player2.rect.x - player1.rect.x <= 0:
                        screen.blit(player2_clip, (player2.rect.x-5-player2_clip.get_width(),player2.rect.y+2))
                        screen.blit(gun0_image_right, (player2.rect.x+4,player2.rect.y+7))
                    elif player2.rect.x - player1.rect.x > 0:
                        screen.blit(player2_clip, (player2.rect.x+24,player2.rect.y+2))
                        screen.blit(gun0_image_left, (player2.rect.x-24,player2.rect.y+7))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            player1.reset(startPos,player1,player2)
                            player2.reset(startPos,player1,player2)
                            player1.score += 1
                            player2.deaths+=1
                            blink_red = 0
                            blink_blue = 0
                        elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                            done = True
                pygame.display.flip()
        if slowmo:
            clock.tick(20)
        else:
            clock.tick(60)

    pygame.quit()
if __name__ == "__main__":
    main()