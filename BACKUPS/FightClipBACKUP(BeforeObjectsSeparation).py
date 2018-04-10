import pygame,pickle,objects,AI_logics
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

mapname="hard"
guns_allowed = True
startPos=[650,10,30,10]

platform_specs1 = pickle.load(open(mapname+".p","rb"))

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

def collisions():
    global blink_blue,blink_red
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
        if player1.rect.top<min(tp_collision_cords) and player1.change_y>0:
            player1.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
            player1.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.bottom)
        if player1.rect.top>max(tp_collision_cords) and player1.change_y<0:
            player1.rect.x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
            player1.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        player1.deaths+=1
    tp_collision_list = pygame.sprite.spritecollide(player2, tp_list, False)
    if len(tp_collision_list)<2 and len(tp_collision_list)!=0:
        for i in tp_collision_list:
            if i.tpdest=="spawn":
                player2.rect.x = int(startPos[0])
                player2.rect.y = int(startPos[1])
            else:
                player2.rect.x = int(i.tpdest.split(",")[0])
                player2.rect.y = int(i.tpdest.split(",")[1])
        player2.deaths+=1
    if len(tp_collision_list)>1:
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.top)
        if player2.rect.top<min(tp_collision_cords) and player2.change_y>0:
            player2.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
            player2.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.bottom)
        if player2.rect.top>max(tp_collision_cords) and player2.change_y<0:
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



class Block(pygame.sprite.Sprite):
    def __init__(self,color,x,y,width,height, char):
        super().__init__()
        self.color = color
        self.height = height
        self.width = width
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.char = char
        self.p = 0
        self.life = 0
        self.djump = 2
        self.direction = 1
        self.crouching = False
        self.tryStand = False
        self.b_timer = 0
        self.score = 0
        self.bt = 20
        self.clip = 7
        self.reload_t = 0
        self.reloading = False
        self.tpdest = ""
        self.been_shot = 0
        self.shot_push = 0
        self.shot_recovery = 0
        self.heal_timer = 0
        self.heal_respawn_time = 5
        self.deaths = 0
    def update(self):
        if self.char==1:
            self.image = pygame.Surface([self.width, self.height])
            self.image.fill(self.color)
            lives1 = font.render(str(player1.life), 1,MRED)
            lives2 = font.render(str(player2.life), 1,RBLUE)
            if guns_allowed:
                player1_wins = font.render(str(player1.score), 1,MRED)
                player2_wins = font.render(str(player2.score), 1,RBLUE)
            elif not guns_allowed:
                player1_wins = font.render(str(player1.deaths), 1,MRED)
                player2_wins = font.render(str(player2.deaths), 1,RBLUE)
            player1_clip = font.render(str(player1.clip), 1,GREY)
            player2_clip = font.render(str(player2.clip), 1,GREY)
            global player1_wins
            global player2_wins
            global lives1
            global lives2
            global player2_clip
            global player1_clip
            if self.tryStand:
                self.stand()
            if self.reloading and self.reload_t <175:
                self.reload_t += 1
                if self.reload_t >= 175:
                    self.reloading = False
                    self.clip = 7
                    print("RELOAD DONE")
                    self.reload_t = 0
                elif self.reload_t%25==0:
                    self.clip=int(self.reload_t/25)
                print("LOADING")
            if self.b_timer <self.bt:
                self.b_timer += 1
            self.grav()
            self.rect.y += self.change_y
            hit_list = pygame.sprite.spritecollide(self, p_list, False)
            for i in hit_list:
                if len(hit_list)<2:
                    if self.change_y > 0:
                        self.rect.bottom = i.rect.top
                        if self.djump < 2:
                            self.djump = 2
                    elif self.change_y < 0:
                        self.rect.top = i.rect.bottom
                    self.change_y = 0
            if len(hit_list)>1:
                hit_list_cord=[]
                for i in hit_list:
                    hit_list_cord.append(i.rect.top)
                if self.rect.top<min(hit_list_cord) and self.change_y>0:
                    self.rect.bottom=hit_list[hit_list_cord.index(min(hit_list_cord))].rect.top
                    self.change_y=0
                    if self.djump < 2:
                            self.djump = 2
                hit_list_cord=[]
                for i in hit_list:
                    hit_list_cord.append(i.rect.bottom)
                if self.rect.top>max(hit_list_cord) and self.change_y<0:
                    self.rect.top=hit_list[hit_list_cord.index(max(hit_list_cord))].rect.bottom
                    self.change_y=0
                """
                #PLAYERS COLLIDE
            if self.p==1:
                if pygame.sprite.collide_rect(player1, player2):
                    if self.change_y > 0:
                        self.rect.bottom = player2.rect.top
                        if self.djump < 2:
                            self.djump = 2
                    elif self.change_y < 0:
                        self.rect.top = player2.rect.bottom
                    self.change_y = 0
            elif self.p==2:
                if pygame.sprite.collide_rect(player2, player1):
                    if self.change_y > 0:
                        self.rect.bottom = player1.rect.top
                        if self.djump < 2:
                            self.djump = 2
                    elif self.change_y < 0:
                        self.rect.top = player1.rect.bottom
                    self.change_y = 0"""
            if self.been_shot == 0:
                self.rect.x += self.change_x
            elif self.been_shot > 0:
                if self.p == 1:
                    if self.rect.x - player2.rect.x <= 0:
                        self.shot_push += self.shot_recovery
                        self.been_shot-=1
                        self.rect.x += self.shot_push
                        if self.been_shot==0:
                            self.shot_push=0
                    if self.rect.x - player2.rect.x >0:
                        self.shot_push -= self.shot_recovery
                        self.been_shot-=1
                        self.rect.x += self.shot_push
                        if self.been_shot==0:
                            self.shot_push=0
                if self.p == 2:
                    if self.rect.x - player1.rect.x <= 0:
                        self.shot_push += self.shot_recovery
                        self.been_shot-=1
                        self.rect.x += self.shot_push
                        if self.been_shot==0:
                            self.shot_push=0
                    if self.rect.x - player1.rect.x >0:
                        self.shot_push -=self.shot_recovery
                        self.been_shot-=1
                        self.rect.x += self.shot_push
                        if self.been_shot==0:
                            self.shot_push=0
            hit_list = pygame.sprite.spritecollide(self, p_list, False)
            for i in hit_list:
                if self.been_shot!=0:
                    if self.shot_push>0:
                        self.rect.right = i.rect.left
                    if self.shot_push<0:
                        self.rect.left = i.rect.right
                elif self.been_shot==0:
                    if self.change_x > 0:
                        self.rect.right = i.rect.left
                    if self.change_x < 0:
                        self.rect.left = i.rect.right
                    """
                    #PLAYERS COLLIDE
            if self.p==1:
                if pygame.sprite.collide_rect(player1, player2):
                    if self.change_x > 0:
                        self.rect.right = player2.rect.left
                    elif self.shot_push>0 and self.been_shot>0:
                        self.rect.right = player2.rect.left
                    if self.change_x < 0:
                        self.rect.left = player2.rect.right
                    elif self.shot_push<0 and self.been_shot>0:
                        self.rect.left = player2.rect.right
            elif self.p==2:
                if pygame.sprite.collide_rect(player2, player1):
                    if self.change_x > 0:
                        self.rect.right = player1.rect.left
                    elif self.shot_push>0 and self.been_shot>0:
                        self.rect.right = player1.rect.left
                    if self.change_x < 0:
                        self.rect.left = player1.rect.right
                    elif self.shot_push<0 and self.been_shot>0:
                        self.rect.left = player1.rect.right"""
        elif self.char==2:
            AI_logics.playerAI(player1,player2)
            pass
        else:
            self.rect.x += self.change_x
            self.rect.y += self.change_y
    def grav(self):
        if self.change_y == 0 and self.char:
            self.change_y = 1
        elif self.change_y != 0 and self.char:
            self.change_y += 0.35
            if self.crouching:
                self.change_y += 0.20
    def jump(self):
        if self.char:
            self.rect.y += 2
            hit_list = pygame.sprite.spritecollide(self,p_list,False)
            self.rect.y -= 2
            if len(hit_list) >0 or self.djump > 0:
                self.change_y = -5.4
                self.djump -= 1
                print("jumped")
    def crouch(self):
        if self.char and not self.crouching:
            self.height = 20
            self.image = pygame.Surface([self.width, self.height])
            x = self.rect.x
            y = self.rect.y+20
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.crouching = True
            print(self.height)
            print("Crouching")
    def stand(self):
        if self.char:
            self.rect.y-= 20
            if len(pygame.sprite.spritecollide(self,p_list,False))==0:
                self.height = 40
                self.image = pygame.Surface([self.width, self.height])
                x = self.rect.x
                y = self.rect.y
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.crouching = False
                self.tryStand=False
                print("Standing")
            else:
                print("Tried standing")
                self.tryStand=True
                self.rect.y+=20
    def shoot(self):
        if guns_allowed:
            if self.char and self.p == 1 and self.b_timer == self.bt and self.clip > 0 and not self.reloading:
                if self.rect.x - player2.rect.x <= 0:
                    bullet = Block(GREY,self.rect.right,self.rect.y+10,8,3,False)
                    bullet.change_x = 17
                if self.rect.x - player2.rect.x > 0:
                    bullet = Block(GREY,self.rect.left,self.rect.y+9,8,3,False)
                    bullet.change_x = -17
                self.clip -= 1
                self.b_timer -= self.b_timer
                bullet1_list.add(bullet)
                all_sprites.add(bullet)
            if self.char and self.p == 2 and self.b_timer == self.bt and self.clip > 0 and not self.reloading:
                if self.rect.x - player1.rect.x <= 0:
                    bullet = Block(GREY,self.rect.right,self.rect.y+9,8,3,False)
                    bullet.change_x = 17
                if self.rect.x - player1.rect.x > 0:
                    bullet = Block(GREY,self.rect.left,self.rect.y+9,8,3,False)
                    bullet.change_x = -17
                self.clip -= 1
                self.b_timer -= self.b_timer
                bullet2_list.add(bullet)
                all_sprites.add(bullet)
    def reload(self):
        if self.clip<7:
            self.reloading = True
    def reset(self):
        if self.p == 1:
            player1.rect.x = int(startPos[0])
            player1.rect.y = int(startPos[1])
            player1.change_x = 0
            player1.change_y = 0
            player1.life = 6
            player1.clip = 7
            player1.been_shot = 0
        if self.p == 2:
            player2.rect.x = int(startPos[2])
            player2.rect.y = int(startPos[3])
            player2.change_x = 0
            player2.change_y = 0
            player2.life = 6
            player2.clip = 7
            player2.been_shot = 0

def keyPressed(key):
    keys=pygame.key.get_pressed()
    if keys[key]:
        return True
    else:
        return False

if len(platform_specs1[0])>=4:
    startPos=platform_specs1[0][:4]
player1 = Block(MRED,int(startPos[0]),int(startPos[1]),20,40,1)
player1.p = 1
player1.life = 6
all_sprites.add(player1)
player_list.add(player1)

player2 = Block(RBLUE,int(startPos[2]),int(startPos[3]),20,40,1)
player2.p = 2
player2.life = 6
all_sprites.add(player2)
player_list.add(player2)

try:guns_allowed = platform_specs1[0][4]
except:pass

for i in range(1,len(platform_specs1)):
    print(platform_specs1[i])
    if platform_specs1[i][0]=="white":
        platform_specs1[i][0]=WHITE
    if platform_specs1[i][0]=="black" or platform_specs1[i][0]=="grey":
        platform_specs1[i][0]=GREY
    if platform_specs1[i][0]=="yellow":
        platform_specs1[i][0]=TPYELLOW
    if platform_specs1[i][0]=="green":
        platform_specs1[i][0]=HEALGREEN
    platform = Block(platform_specs1[i][0],platform_specs1[i][1],platform_specs1[i][2],platform_specs1[i][3],platform_specs1[i][4],platform_specs1[i][5])
    all_sprites.add(platform)
    if platform_specs1[i][6]=="normal":p_list.add(platform)
    elif platform_specs1[i][6]=="killer":instaDeath_list.add(platform)
    elif platform_specs1[i][6]=="teleporter":
        tp_list.add(platform)
        platform.tpdest = platform_specs1[i][7]
    elif platform_specs1[i][6]=="healer":
        heal_list.add(platform)
        print("1")
        platform.heal_respawn_time = int(platform_specs1[i][7])
        print("2")

bullet_block = Block(BLACK, -30,0,20,500,False)
bb_list.add(bullet_block)
all_sprites.add(bullet_block)
bullet_block = Block(WHITE, 710,0,20,500,False)
bb_list.add(bullet_block)
all_sprites.add(bullet_block)


def main():
    global blink_red,blink_blue
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    icon=pygame.image.load("icon.png")
    pygame.display.set_caption("Fight Clip")
    gun0_image_right = pygame.image.load("gun0.gif").convert()
    gun0_image_right.set_colorkey(INVISCOL)
    gun0_image_left=pygame.transform.flip(gun0_image_right,True,False)
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
                    player1.jump()
                if event.key == pygame.K_PERIOD:
                    player1.shoot()
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
                    player2.jump()
                if event.key == pygame.K_s:
                    player2.crouch()
                if event.key == pygame.K_LESS:
                    player2.shoot()
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
                    player1.stand()
                if event.key == pygame.K_a and player2.change_x < 0:
                    player2.change_x = 0
                if event.key == pygame.K_d and player2.change_x > 0:
                    player2.change_x = 0
                if event.key == pygame.K_s:
                    player2.stand()
        collisions()
        screen.fill(BGGREY)
        all_sprites.update()
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
                if j.heal_timer<j.heal_respawn_time*60:
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
                            player1.reset()
                            player2.reset()
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
                            player1.reset()
                            player2.reset()
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