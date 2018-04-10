import pygame
class Block(pygame.sprite.Sprite):
    def __init__(self,color,x,y,width,height):
        super().__init__()
        self.color = color
        self.height = height
        self.width = width
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class bulletBlock(Block):
    def __init__(self,color,x,y,width,height):
        Block.__init__(self,color,x,y,width,height)
        self.change_x = 0
        self.change_y = 0
    def update(self):
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y

class healBlock(Block):
    def __init__(self,color,x,y,width,height,respawn_time):
        Block.__init__(self,color,x,y,width,height)
        self.heal_timer = 0
        self.heal_respawn_time = respawn_time

class teleporterBlock(Block):
    def __init__(self,color,x,y,width,height,destination):
        Block.__init__(self,color,x,y,width,height)
        self.tpdest = destination

class player(Block):
    def __init__(self,color,x,y,playerNR):
        Block.__init__(self,color,x,y,20,40)
        self.p = playerNR
        self.change_x = 0
        self.change_y = 0
        self.life = 6
        self.djump = 2
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
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
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
    def movement_and_collision(self,p_list,player1,player2):
        self.grav()
        self.rect.y += self.change_y
        hit_list = pygame.sprite.spritecollide(self, p_list, False)
        if self.tryStand:
            self.stand(p_list)
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
    def grav(self):
        if self.change_y == 0:
            self.change_y = 1
        elif self.change_y != 0:
            self.change_y += 0.35
            if self.crouching:
                self.change_y += 0.20
    def jump(self,p_list):
        self.rect.y += 2
        hit_list = pygame.sprite.spritecollide(self,p_list,False)
        self.rect.y -= 2
        if len(hit_list) >0 or self.djump > 0:
            self.change_y = -5.4
            self.djump -= 1
            print("jumped")
    def crouch(self):
        if not self.crouching:
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
    def stand(self,p_list):
        self.rect.y-= 20
        if len(pygame.sprite.spritecollide(self,p_list,False))==0:
            self.crouching = False
            self.tryStand=False
            self.height = 40
            self.image = pygame.Surface([self.width, self.height])
            x = self.rect.x
            y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            print("Standing")
        else:
            print("Tried standing")
            self.tryStand=True
            self.rect.y+=20
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites):
        if guns_allowed:
            if self.p == 1 and self.b_timer == self.bt and self.clip > 0 and not self.reloading:
                if self.rect.x - player2.rect.x <= 0:
                    bullet = bulletBlock(GREY,self.rect.right,self.rect.y+10,8,3)
                    bullet.change_x = 17
                if self.rect.x - player2.rect.x > 0:
                    bullet = bulletBlock(GREY,self.rect.left,self.rect.y+9,8,3)
                    bullet.change_x = -17
                self.clip -= 1
                self.b_timer -= self.b_timer
                bullet1_list.add(bullet)
                all_sprites.add(bullet)
            if self.p == 2 and self.b_timer == self.bt and self.clip > 0 and not self.reloading:
                if self.rect.x - player1.rect.x <= 0:
                    bullet = bulletBlock(GREY,self.rect.right,self.rect.y+9,8,3)
                    bullet.change_x = 17
                if self.rect.x - player1.rect.x > 0:
                    bullet = bulletBlock(GREY,self.rect.left,self.rect.y+9,8,3)
                    bullet.change_x = -17
                self.clip -= 1
                self.b_timer -= self.b_timer
                bullet2_list.add(bullet)
                all_sprites.add(bullet)
    def reload(self):
        if self.clip<7:
            self.reloading = True
    def reset(self,startPos,player1,player2):
        if self.p == 1:
            player1.rect.x = int(startPos[0])
            player1.rect.y = int(startPos[1])
        if self.p == 2:
            player2.rect.x = int(startPos[2])
            player2.rect.y = int(startPos[3])
        self.change_x = 0
        self.change_y = 0
        self.life = 6
        self.reloading = False
        self.clip = 7
        self.been_shot = 0

def main():
    pass

if __name__ == '__main__':
    main()
