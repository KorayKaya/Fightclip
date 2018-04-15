import pygame,gc,os

class Block(pygame.sprite.Sprite):
    def __init__(self,color,x,y,width,height,all_sprites):
        super().__init__()
        self.INVISCOL = (63,171,153)
        self.color = color
        self.height = height
        self.width = width
        self.image = pygame.Surface([self.width, self.height])
        if color!=None:
            self.image.fill(color)
        else:
            self.image.fill((0,0,0))
            self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)

class platform(Block):
    def __init__(self,color,x,y,width,height,all_sprites,p_list):
        Block.__init__(self,color,x,y,width,height,all_sprites)
        p_list.add(self)

class killer(Block):
    def __init__(self,color,x,y,width,height,all_sprites,instaDeath_list):
        Block.__init__(self,color,x,y,width,height,all_sprites)
        instaDeath_list.add(self)

class pictureBlock(pygame.sprite.Sprite):
    def __init__(self,picture,x,y,all_sprites):
        super().__init__()
        self.INVISCOL = (63,171,153)
        self.graphics_dir=os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
        self.image = pygame.image.load(self.graphics_dir+picture+".gif").convert()
        self.image.set_colorkey(self.INVISCOL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_sprites.add(self)

class bulletBlock(Block):
    def __init__(self,color,x,y,width,height,speed_x,speed_y,damage,all_sprites):
        Block.__init__(self,color,x,y,width,height,all_sprites)
        self.change_x = speed_x
        self.change_y = speed_y
        self.true_y = y
        self.true_x = x
        self.damage = damage
    def update(self):
        import FightClip
        self.true_y+=self.change_y
        self.rect.y=self.true_y
        self.true_x+=self.change_x
        self.rect.x=self.true_x
        if self.rect.x>2500 or self.rect.x<-1800 or self.rect.y>3100 or self.rect.y<-1000:
            self.kill()
            #print("bullet suicide")

class grenade(bulletBlock):
    def __init__(self,color,x,y,width,height,speed_x,speed_y,damage,all_sprites,grenade_list,explosion_timer):
        bulletBlock.__init__(self,color,x,y,width,height,speed_x,speed_y,damage,all_sprites)
        if self.color==None:
            self.graphics_dir=os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
            self.image = pygame.image.load(self.graphics_dir+"grenade.gif").convert()
            self.image.set_colorkey(self.INVISCOL)
            self.rect=self.image.get_rect()
            self.rect.x=x
            self.rect.y=y
        self.players_hurt=[]
        self.explosion_hitbox=None
        self.exploded=False
        self.explosion_timer=explosion_timer*60
        self.explosion_duration=20
        self.max_travel_time=6*60
        self.player_collision=False
        grenade_list.add(self)
    def update(self):
        pass
    def grenadePhysics(self,p_list,screen,all_sprites,player_list,exploding_grenades_list):
        import FightClip
        #Y MOVEMENT
        self.grav()
        self.true_y+=self.change_y
        self.rect.y=self.true_y
        grenade_hit_wall_list = pygame.sprite.spritecollide(self,p_list,False)
        if len(grenade_hit_wall_list)>0:
            if self.change_y>0:
                self.true_y=grenade_hit_wall_list[-1].rect.top-self.height
                self.rect.bottom=grenade_hit_wall_list[-1].rect.top
                self.change_y*=-0.55
                self.change_y+=0.56
                if self.change_y>0:
                    self.change_y=0
                self.change_x*=0.5
            elif self.change_y<0:
                self.change_y*=-0.9
                self.true_y=grenade_hit_wall_list[-1].rect.bottom
                self.rect.top=grenade_hit_wall_list[-1].rect.bottom
        #X MOVEMENT
        self.true_x+=self.change_x
        self.rect.x=self.true_x
        grenade_hit_wall_list = pygame.sprite.spritecollide(self,p_list,False)
        if len(grenade_hit_wall_list)>0:
            if self.change_x>0:
                self.true_x=grenade_hit_wall_list[-1].rect.left-self.width
                self.rect.right=self.rect.bottom=grenade_hit_wall_list[-1].rect.left
            elif self.change_x<0:
                self.true_x=grenade_hit_wall_list[-1].rect.right
                self.rect.left=grenade_hit_wall_list[-1].rect.right
            self.change_x*=-0.8
        #if self.color==None:
         #   screen.blit(self.grenade_image,(self.rect.x,self.rect.y))
        if -0.2<self.change_x<0.2 and self.change_y==0:
            self.explosion_timer-=1
        for i in player_list:
            if not self.player_collision:
                if pygame.sprite.collide_rect(self,i):
                    self.player_collision=True
        if self.explosion_timer<=0 and not self.exploded or self.player_collision and not self.exploded or self.max_travel_time==0 and not self.exploded:
            self.explode(all_sprites,exploding_grenades_list)
        if self.exploded:
            self.explosion_duration-=1
            if self.explosion_duration<=0:
                self.explosion_hitbox.kill()
                self.kill()
        if self.max_travel_time>0:
            self.max_travel_time-=1
        #print(self.change_x,self.change_y,self.explosion_timer)
        if self.rect.x>2500 or self.rect.x<-1800 or self.rect.y>3100 or self.rect.y<-1000:
            self.kill()
    def grav(self):
        if self.change_y==0:
            self.change_y=1
        elif self.change_y!=0:
            self.change_y += 0.35
    def explode(self,all_sprites,exploding_grenades_list):
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.exploded=True
        self.explosion_hitbox=Block((122,122,122),self.rect.center[0]-75,self.rect.center[1]-75,150,150,all_sprites)
        exploding_grenades_list.add(self)

class weaponBox(pictureBlock):
    def __init__(self,x,y,weapon,weapon_box_list,all_sprites,respawn_time):
        pictureBlock.__init__(self,weapon,x,y,all_sprites)
        self.weapon = weapon
        self.respawn_time = int(respawn_time)
        self.respawn_timer = int(respawn_time)*60
        weapon_box_list.add(self)
    def giveWeapon(self,player,draw_list,grenade_list):
        import FCweapons
        if player.currWeapon!=None:
            draw_list.remove(player.currWeapon)
        if self.weapon == "handGun":
            player.currWeapon = FCweapons.handGun(player,draw_list)
        if self.weapon == "assaultRifle":
            player.currWeapon = FCweapons.assaultRifle(player,draw_list)
        if self.weapon == "shotgun":
            player.currWeapon = FCweapons.shotgun(player,draw_list)
        if self.weapon == "lazerRifle":
            player.currWeapon = FCweapons.lazerRifle(player,draw_list)
        if self.weapon == "grenadeLauncher":
            player.currWeapon = FCweapons.grenadeLauncher(player,draw_list,grenade_list)
        if self.weapon == "katana":
            player.currWeapon = FCweapons.katana(player,draw_list)

class healBlock(Block):
    def __init__(self,color,x,y,width,height,respawn_time,all_sprites,heal_list):
        Block.__init__(self,color,x,y,width,height,all_sprites)
        self.respawn_time = respawn_time
        self.respawn_timer = respawn_time*60
        heal_list.add(self)

class teleporterBlock(Block):
    def __init__(self,color,x,y,width,height,destination,all_sprites,tp_list):
        Block.__init__(self,color,x,y,width,height,all_sprites)
        self.tpdest = destination
        tp_list.add(self)

class player(Block):
    def __init__(self,color,x,y,playerNR,all_sprites,player_list):
        Block.__init__(self,color,x,y,20,40,all_sprites)
        self.p = playerNR
        self.change_x = 0
        self.change_y = 0
        self.color = color
        self.color2 = (75,111,114)
        self.color3 = (97,121,75)
        self.life = 15
        self.djump = 2
        self.jump_number = 2
        self.crouching = False
        self.tryStand = False
        self.platform_under = None
        self.platform_under_timer = 30
        self.score = 0
        self.been_shot = 0
        self.shot_push = 0
        self.shot_recovery = 0
        self.deaths = 0
        self.currWeapon = None
        self.direction = 0
        self.walk_frame_timer = 0
        self.direction_enabled=True
        self.speed_coefficient_x=1
        self.speed_coefficient_y=1
        self.true_x=x
        self.true_y=y
        player_list.add(self)
    def update(self):
        self.image = pygame.Surface([self.width, self.height])
        if self.change_x!=0 and self.change_y==0 and not self.crouching:
            if self.walk_frame_timer==10:
                self.height-=4
                self.image = pygame.Surface([self.width, self.height])
                x = self.rect.x
                y = self.rect.y+4
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
            if self.walk_frame_timer==20:
                self.height+=4
                self.image = pygame.Surface([self.width, self.height])
                x = self.rect.x
                y = self.rect.y-4
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.walk_frame_timer=0
            self.walk_frame_timer+=1
        else:
            self.walk_frame_timer=0
            if self.crouching:
                if self.height!=20:
                    self.height = 20
                    self.image = pygame.Surface([self.width, self.height])
                    x = self.rect.x
                    y = self.rect.y
                    self.rect = self.image.get_rect()
                    self.rect.x = x
                    self.rect.y = y
            elif not self.crouching:
                if self.height!=40:
                    old_height=self.height
                    self.height = 40
                    self.image = pygame.Surface([self.width, self.height])
                    x = self.rect.x
                    y = self.rect.y-(40-old_height)
                    self.rect = self.image.get_rect()
                    self.rect.x = x
                    self.rect.y = y
        if self.life>21:
            self.image.fill((self.color[0]*0.3+(self.color[0]*0.7*21/15),self.color[1]*0.3+(self.color[1]*0.7*21/15),self.color[2]*0.3+(self.color[2]*0.7*21/15)))
        elif self.life>0:
            self.image.fill((self.color[0]*0.3+(self.color[0]*0.7*self.life/15),self.color[1]*0.3+(self.color[1]*0.7*self.life/15),self.color[2]*0.3+(self.color[2]*0.7*self.life/15)))
        else: self.image.fill((self.color[0]*0.3,self.color[1]*0.3,self.color[2]*0.3))
    def movement_and_collision(self,screen,p_list,player1,player2,player1_life,player2_life,guns_allowed,size,*args):
        self.grav()
        self.speed_coefficient_x=1
        self.speed_coefficient_y=1
        if self.crouching:
            self.speed_coefficient_x*=0.6
        try:
            self.speed_coefficient_x*=self.currWeapon.speed_coefficient_x
        except:pass
        try:
            self.speed_coefficient_y*=self.currWeapon.speed_coefficient_y
        except:pass
        self.platform_under_timer-=1
        if self.platform_under_timer==0:
            test_y=self.rect.bottom
            try:
                old_under_platform=self.platform_under
            except:print("none type obj")
            self.platform_under=None
            while test_y<self.rect.bottom+80 and self.platform_under==None:
                for i in p_list:
                    if i.rect.collidepoint(self.rect.x,test_y):
                        self.platform_under=i
                    elif i.rect.collidepoint(self.rect.right,test_y):
                        self.platform_under=i
                test_y+=1
            if self.platform_under==None:
                self.platform_under=old_under_platform
                #print("revived:",self.platform_under.rect.y)
            #print("platform under:", self.platform_under.rect.y)
            self.platform_under_timer=30
        self.rect.y += self.change_y
        hit_list = pygame.sprite.spritecollide(self, p_list, False)
        for i in hit_list:
            if len(hit_list)<2:
                if self.change_y > 0:
                    self.rect.bottom = i.rect.top
                    if self.djump < self.jump_number:
                        self.djump = self.jump_number
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
            if self.rect.bottom>max(hit_list_cord) and self.change_y<0:
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
            self.true_x += self.change_x*self.speed_coefficient_x
            self.rect.x = self.true_x
        elif self.been_shot > 0:
            if self.p == 1:
                if self.rect.x - player2.rect.x <= 0:
                    self.shot_push += self.shot_recovery
                    self.true_x += self.shot_push
                    self.rect.x = self.true_x
                    if self.been_shot==0:
                        self.shot_push=0
                if self.rect.x - player2.rect.x >0:
                    self.shot_push -= self.shot_recovery
                    self.true_x += self.shot_push
                    self.rect.x = self.true_x
                    if self.been_shot==0:
                        self.shot_push=0
            if self.p == 2:
                if self.rect.x - player1.rect.x <= 0:
                    self.shot_push += self.shot_recovery
                    self.true_x += self.shot_push
                    self.rect.x = self.true_x
                    if self.been_shot==0:
                        self.shot_push=0
                if self.rect.x - player1.rect.x >0:
                    self.shot_push -=self.shot_recovery
                    self.true_x += self.shot_push
                    self.rect.x = self.true_x
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
                    self.true_x = i.rect.left-(self.rect.right-self.rect.left)
                    self.rect.x = self.true_x
                if self.change_x < 0:
                    self.true_x = i.rect.right
                    self.rect.x = self.true_x
        if self.been_shot!=0:
            self.been_shot-=1
            """#PLAYERS COLLIDE
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
                    self.rect.left = player1.rect.right
            """
        if self.life>0 and self.direction_enabled:
            if self.p==1:
                if self.rect.x <= player2.rect.x:
                    self.direction = 1
                elif self.rect.x > player2.rect.x:
                    self.direction = 0
            elif self.p==2:
                if self.rect.x <= player1.rect.x:
                    self.direction = 1
                elif self.rect.x > player1.rect.x:
                    self.direction = 0
        if guns_allowed:
            if self.p==1:
                screen.blit(player1_life, (self.rect.x+(10-(player1_life.get_width()/2)),self.rect.y-player1_life.get_height()-3))
            elif self.p==2:
                screen.blit(player2_life, (self.rect.x+(10-(player2_life.get_width()/2)),self.rect.y-player2_life.get_height()-3))
        if self.rect.y>1400:
            self.life=0
        if self.tryStand:
            self.stand(p_list)
    def grav(self):
        if self.change_y == 0:
            self.change_y = 1
        elif self.change_y != 0:
            self.change_y += 0.35
            if self.crouching:
                self.change_y+=0.20
    def jump(self):
        if self.djump > 0:
            self.change_y = -5.7
            self.djump -= 1
            #print("jumped")
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
            #print("Crouching")
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
            #print("Standing")
        else:
            #print("Tried standing")
            self.tryStand=True
            self.rect.y+=20
    def reset(self,startPos,player1,player2,blink_red,blink_blue,bullet1_list,bullet2_list,startWeapon,draw_list,p_list,respawn_list):
        import FCweapons,FCobjects
        if self.p == 1:
            self.true_x = int(startPos[0])
            self.rect.y = int(startPos[1])
            blink_red=0
            for i in bullet1_list:
                i.kill()
        if self.p == 2:
            self.true_x = int(startPos[2])
            self.rect.y = int(startPos[3])
            blink_blue=0
        for i in bullet2_list:
                i.kill()
        if startWeapon=="handGun":
            draw_list.remove(self.currWeapon)
            self.currWeapon = FCweapons.handGun(self,draw_list)
        try:self.currWeapon.currentClip=self.currWeapon.clipSize
        except:print("no weapon to reset clip for, player",self.p)
        for obj in gc.get_objects():
            if isinstance(obj, FCweapons.lazerRifle):
                for i in obj.lazer_pictures_list:
                    i[2]=0
            if isinstance(obj,FCobjects.grenade):
                try:
                    obj.explosion_hitbox.kill()
                except:pass
                obj.kill()
        self.stand(p_list)
        self.change_x = 0
        self.change_y = 0
        self.life = 15
        self.been_shot = 0
        if self.p==1:
            for i in respawn_list:
                i.respawn_timer=0
        return blink_red,blink_blue


#Detta var experimentellt, funkade lite och kan eventuellt fixas. Just nu ar den lite
#forstord for jag forsokte fixa ett problem men skapade ett nytt problem samtidigt
class AIplayer(player):
    def __init__(self,x,y,all_sprites,player_list):
        self.color = (144,7,168)
        self.color2 = (75,111,114)
        self.color3 = (97,121,75)
        self.hit_wall = False
        self.wall = None
        self.platform_under = None
        self.target_x=None
        self.target_y=None
        self.target_platform = None
        self.final_target_platform = None
        self.walk_path = []
        self.path_platforms = []
        self.platform_blacklist = []
        self.path_update_timer = 60
        self.blacklist_timer = 480
        self.current_walk_path_index = 0
        self.find_path_timer = 30
        self.walking=False
        self.all_sprites = all_sprites
        player.__init__(self,self.color,x,y,2,all_sprites,player_list)
    def movement_and_collision(self,screen,p_list,player1,player2,player1_life,player2_life,guns_allowed,size):
        self.grav()
        if self.change_x==5 and self.crouching:
            self.change_x=3
        elif self.change_x==-5 and self.crouching:
            self.change_x=-3
        elif self.change_x==3 and not self.crouching:
            self.change_x=5
        elif self.change_x==-3 and not self.crouching:
            self.change_x=-5
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
            if self.rect.bottom>max(hit_list_cord) and self.change_y<0:
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
                    self.rect.x += self.shot_push
                    if self.been_shot==0:
                        self.shot_push=0
                if self.rect.x - player2.rect.x >0:
                    self.shot_push -= self.shot_recovery
                    self.rect.x += self.shot_push
                    if self.been_shot==0:
                        self.shot_push=0
            if self.p == 2:
                if self.rect.x - player1.rect.x <= 0:
                    self.shot_push += self.shot_recovery
                    self.rect.x += self.shot_push
                    if self.been_shot==0:
                        self.shot_push=0
                if self.rect.x - player1.rect.x >0:
                    self.shot_push -=self.shot_recovery
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
        if len(hit_list)>0:
            self.hit_wall=True
            self.wall=hit_list[0]
        else:self.hit_wall=False
        if self.been_shot!=0:
            self.been_shot-=1
            """#PLAYERS COLLIDE
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
                    self.rect.left = player1.rect.right
            """
        if self.life>0:
            if self.p==1:
                if self.rect.x <= player2.rect.x:
                    self.direction = 1
                elif self.rect.x > player2.rect.x:
                    self.direction = 0
            elif self.p==2:
                if self.rect.x <= player1.rect.x:
                    self.direction = 1
                elif self.rect.x > player1.rect.x:
                    self.direction = 0
        if guns_allowed:
            if self.p==1:
                screen.blit(player1_life, (self.rect.x+(10-(player1_life.get_width()/2)),self.rect.y-player1_life.get_height()-3))
            elif self.p==2:
                screen.blit(player2_life, (self.rect.x+(10-(player2_life.get_width()/2)),self.rect.y-player2_life.get_height()-3))
        if self.rect.y>1400:
            self.life=0
        if self.tryStand:
            self.stand(p_list)
    def AI_LOGIC(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list,size):
        if self.life>0:
            if self.final_target_platform!=player1.platform_under and player1.platform_under!=None and self.path_update_timer==0:
                print("PLAYER CHANGED PLATFORM",player1.rect.center[0],player1.rect.center[1])
                self.find_path_AI(player1.rect.center[0],player1.rect.center[1],size,all_sprites,p_list,player1.platform_under)
                self.path_update_timer=30
            print(self.path_update_timer)
            if self.path_update_timer>0:
                self.path_update_timer-=1
            self.walk_to_AI(player1.rect.center[0],player1.rect.center[1],p_list,size,all_sprites,player1)
            if self.hit_wall:
                if self.wall.rect.top-self.rect.bottom>-89 and self.change_y>=0:
                    self.jump()
            if self.rect.y+self.currWeapon.y_bullet_offset>player1.rect.top and self.rect.y+self.currWeapon.y_bullet_offset<player1.rect.bottom:
                if player1.rect.right<self.rect.left or player1.rect.left>self.rect.right:
                    if self.rect.x <= player1.rect.x:
                        testbullet = bulletBlock(self.color,self.rect.right,self.rect.y+self.currWeapon.y_bullet_offset,(player1.rect.x-self.rect.right),3,0,0,0,self.all_sprites)
                    if self.rect.x > player1.rect.x:
                        testbullet = bulletBlock(self.color,player1.rect.right,self.rect.y+self.currWeapon.y_bullet_offset,(self.rect.left-player1.rect.right),3,0,0,0,self.all_sprites)
                    bull_dis = pygame.sprite.spritecollide(testbullet,p_list,False)
                    testbullet.kill()
                    if len(bull_dis)==0:
                        self.currWeapon.shoot(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list)
            if self.currWeapon.currentClip==0 and self.currWeapon.reloadTimeFrames==0:
                self.currWeapon.reload()
            self.platform_under.image.fill((155,0,155))
        else:
            self.change_x=0
        try:self.target_platform.image.fill(255,0,0)
        except:pass
    def find_path_AI(self,x,y,size,all_sprites,p_list,final_target_platform):
        print("Destination:",x,y)
        for i in p_list:
            i.image.fill((255,255,255))
        test_y=self.rect.bottom
        old_platform_under=self.platform_under
        self.platform_under=None
        self.final_target_platform=final_target_platform
        while test_y<self.rect.bottom+80 and self.platform_under==None:
            for i in p_list:
                if i.rect.collidepoint(self.rect.x,test_y):
                    self.platform_under=i
                    print("found under",self.platform_under)
                elif i.rect.collidepoint(self.rect.right,test_y):
                    self.platform_under=i
                    print("found under",self.platform_under)
            test_y+=1
        if self.platform_under==None:
            self.platform_under=old_platform_under
        #FIND FINAL TARGET PLATFORM IF FINAL TARGET PLATFORM == NONE
        test_y=y
        while test_y<size[1] and self.final_target_platform==None:
            for i in p_list:
                if i.rect.collidepoint(x,test_y):
                    self.final_target_platform=i
                    self.final_target_platform.image.fill((0,255,0))
                    break
            test_y+=1
        #AFTER WE KNOW SELF PLATFORM UNDER AND FINAL TARGET PLATFORM WE FIND PATH
        self.walk_path=[]
        self.path_platforms=[]
        possible_paths=[]
        testing_path=[]
        testing_path_coords=[]
        all_paths=[]
        test_index=-1
        done=False
        try:
            if self.final_target_platform.rect.y<self.platform_under.rect.y:
                print("allo")
        except:print("final targe:", type(final_target_platform),"self under",type(self.platform_under))
        if self.final_target_platform==None:
            print("couldnt find a platform under player 1")
            done=True
        #IF FINAL TARGET IS UNDER SELF
        elif self.final_target_platform.rect.y>self.platform_under.rect.y:
            current_test_platform = self.platform_under
            while not done:
                #TEST LEFT
                detect_block = Block((1,1,1),current_test_platform.rect.x-20,current_test_platform.rect.y-40,20,(self.final_target_platform.rect.y+41-current_test_platform.rect.y),all_sprites)
                hit_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                detect_block.kill()
                platform_distances = []
                selected_platforms_list = []
                best_platform_left=None
                if len(hit_list)<=1:
                    if self.final_target_platform in hit_list:
                        print("final target in hit list left")
                        best_platform_left=self.final_target_platform
                if best_platform_left==None:
                    detect_block = Block((1,1,1),current_test_platform.rect.x-300,current_test_platform.rect.y,300,(self.final_target_platform.rect.y+1-current_test_platform.rect.y),all_sprites)
                    hit_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                    detect_block.kill()
                    for i in hit_list:
                        bad=False
                        if i.rect.y>self.final_target_platform.rect.y or i.rect.y<self.platform_under.rect.y:
                            bad=True
                        if i.rect.collidepoint(current_test_platform.rect.left,i.rect.y+1) and not bad:
                            print("(i.rect.y-current_test_platform.rect.y+41)=",str(int(i.rect.y-current_test_platform.rect.y+41)))
                            detect_block = Block((1,1,1),current_test_platform.rect.left-20,current_test_platform.rect.y-40,20,(i.rect.y-current_test_platform.rect.y+40),all_sprites)
                            check_fallable_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                            detect_block.kill()
                            if i in check_fallable_list:
                                print("found self in fallable list")
                            if len(check_fallable_list)>0:
                                bad=True
                        else:bad=True
                        if not bad:
                            platform_distances.append(i.rect.y)
                            selected_platforms_list.append(i)
                    if len(selected_platforms_list)>0:
                        best_platform_left = selected_platforms_list[platform_distances.index(max(platform_distances))]
                    else:best_platform_left=None
                #TEST RIGHT
                detect_block = Block((1,1,1),current_test_platform.rect.right,current_test_platform.rect.y-40,20,(self.final_target_platform.rect.y+41-current_test_platform.rect.y),all_sprites)
                hit_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                detect_block.kill()
                platform_distances = []
                selected_platforms_list = []
                best_platform_right=None
                if len(hit_list)<=1:
                    if self.final_target_platform in hit_list:
                        print("final target in hit list right")
                        best_platform_right=self.final_target_platform
                if best_platform_right==None:
                    detect_block = Block((1,1,1),current_test_platform.rect.right,current_test_platform.rect.y,300,(self.final_target_platform.rect.y+1-current_test_platform.rect.y),all_sprites)
                    hit_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                    detect_block.kill()
                    for i in hit_list:
                        bad=False
                        if i.rect.y>self.final_target_platform.rect.y or i.rect.y<self.platform_under.rect.y:
                            bad=True
                        if i.rect.collidepoint(current_test_platform.rect.left,i.rect.y+1) and not bad:
                            detect_block = Block((1,1,1),current_test_platform.rect.right,current_test_platform.rect.y-40,20,i.rect.y-current_test_platform.rect.y+41,all_sprites)
                            check_fallable_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                            detect_block.kill()
                            if len(check_fallable_list)>1:
                                bad=True
                        else:bad=True
                        if not bad:
                            platform_distances.append(i.rect.y)
                            selected_platforms_list.append(i)
                    if len(selected_platforms_list)>0:
                        best_platform_right = selected_platforms_list[platform_distances.index(max(platform_distances))]
                    else:best_platform_right=None
                left_distance_from_target=abs(x-current_test_platform.rect.left)
                right_distance_from_target=abs(x-current_test_platform.rect.right)
                if best_platform_right==None or right_distance_from_target>=left_distance_from_target:
                    self.walk_path.append([current_test_platform.rect.left-21,best_platform_left.rect.y-10])
                    current_test_platform=best_platform_left
                    print("appended left down")
                elif best_platform_left==None or left_distance_from_target>right_distance_from_target:
                    self.walk_path.append([current_test_platform.rect.right+21,best_platform_right.rect.y-10])
                    current_test_platform=best_platform_right
                    print("appended right down")
                else:
                    print("no path found down")
                    break
                if len(self.walk_path)>150:
                    print("walk path too long:",len(self.walk_path))
                    break
                if current_test_platform==self.final_target_platform:
                    print("found way down")
                    done=True
        #IF FINAL TARGET OVER SELF
        elif self.final_target_platform.rect.y<self.platform_under.rect.y:
            current_test_platform = self.final_target_platform
            #testing_path.append([x,y])
            closest_platform_left=None
            closest_platform_right=None
            closest_platform_under=None
            while not done:
                #TEST LEFT SIDE
                search_platform = Block((180,1,180),current_test_platform.rect.left-250,current_test_platform.rect.top,250,89,all_sprites)
                hit_list = pygame.sprite.spritecollide(search_platform,p_list,False)
                search_platform.kill()
                if len(hit_list)>0:
                    closest_platform_list=[]
                    selected_platforms_list=[]
                    for i in hit_list:
                        bad=False
                        if i in self.platform_blacklist:
                            print("found in blacklist",i.rect.right,i.rect.y)
                            bad=True
                        wall_detect_block = Block((1,1,1),i.rect.right-10,i.rect.y-40,50,40,all_sprites)
                        hit_list = pygame.sprite.spritecollide(wall_detect_block,p_list,False)
                        wall_detect_block.kill()
                        if len(hit_list)>0:
                            for j in hit_list:
                                if current_test_platform.rect.y-j.rect.y>89:
                                    print("found wall",i.rect.right,i.rect.y)
                                    bad=True
                                test_roof_x=j.rect.right
                                test_roof_y=j.rect.y
                                while test_roof_x<j.rect.right+30 and test_roof_y>j.rect.y-30 and not bad:
                                    for k in p_list:
                                        if k.rect.collidepoint(test_roof_x,test_roof_y):
                                            print("found roof",k.rect.x,k.rect.y)
                                            bad=True
                                            break
                                    test_roof_x+=1
                                    test_roof_y-=1
                        if i.rect.top>current_test_platform.rect.top and not bad:
                            i_x_dist=current_test_platform.rect.left-i.rect.right
                            i_y_dist=i.rect.y-current_test_platform.rect.y
                            if i_x_dist<=0:
                                i_x_dist=1
                            i_pythagoras_distance=(i_x_dist**2+i_y_dist**2)**0.5
                            closest_platform_list.append(i_pythagoras_distance)
                            selected_platforms_list.append(i)
                    if len(selected_platforms_list)>0:
                        closest_platform_left = selected_platforms_list[closest_platform_list.index(min(closest_platform_list))]
                        for i in selected_platforms_list:
                            if i!=closest_platform_left:
                                this_path = testing_path
                                this_path.append(i)
                                all_paths.append(this_path)
                        #CALCULATE LEFT DISTANCE
                        left_y_distance=closest_platform_left.rect.y-current_test_platform.rect.y
                        left_x_distance=current_test_platform.rect.left-closest_platform_left.rect.right
                        if left_x_distance<=0:
                            left_x_distance=1
                        left_pythagoras_distance=(left_x_distance**2+left_x_distance**2)**0.5
                    else:left_pythagoras_distance=100000
                else:left_pythagoras_distance=100000
                #TEST RIGHT SIDE
                search_platform = Block((1,1,1),current_test_platform.rect.right,current_test_platform.rect.top,250,89,all_sprites)
                hit_list = pygame.sprite.spritecollide(search_platform,p_list,False)
                search_platform.kill()
                if len(hit_list)>0:
                    closest_platform_list=[]
                    selected_platforms_list=[]
                    for i in hit_list:
                        bad=False
                        if i in self.platform_blacklist:
                            bad=True
                        #FIND IF THERE IS A WALL BETWEEN ME AND PLATFORM
                        wall_detect_block = Block((1,1,1),i.rect.left-60,i.rect.y-40,50,40,all_sprites)
                        hit_list = pygame.sprite.spritecollide(wall_detect_block,p_list,False)
                        wall_detect_block.kill()
                        if len(hit_list)>0:
                            for j in hit_list:
                                if current_test_platform.rect.y-j.rect.y>89:
                                    bad=True
                                #FIND ROOF TO WALL
                                test_roof_x=j.rect.left
                                test_roof_y=j.rect.y
                                while test_roof_x>j.rect.x-30 and test_roof_y>j.rect.y-30 and not bad:
                                    for k in p_list:
                                        if k.rect.collidepoint(test_roof_x,test_roof_y):
                                            bad=True
                                            break
                                    test_roof_x-=1
                                    test_roof_y-=1
                        if i.rect.top>=current_test_platform.rect.top and not bad:
                            i_x_dist=i.rect.left-current_test_platform.rect.right
                            i_y_dist=i.rect.y-current_test_platform.rect.y
                            if i_x_dist<=0:
                                i_x_dist=1
                            i_pythagoras_distance=(i_x_dist**2+i_y_dist**2)**0.5
                            closest_platform_list.append(i_pythagoras_distance)
                            selected_platforms_list.append(i)
                    if len(selected_platforms_list)>0:
                        closest_platform_right = selected_platforms_list[closest_platform_list.index(min(closest_platform_list))]
                        for i in selected_platforms_list:
                            if i!=closest_platform_right:
                                this_path = testing_path
                                this_path.append(i)
                                all_paths.append(this_path)
                        #CALCULATE RIGHT DISTANCE
                        right_y_distance=closest_platform_right.rect.y-current_test_platform.rect.y
                        right_x_distance=closest_platform_right.rect.left-current_test_platform.rect.right
                        if right_x_distance<=0:
                            right_x_distance=1
                        right_pythagoras_distance=(right_x_distance**2+right_y_distance**2)**0.5
                    else:right_pythagoras_distance=100000
                else:right_pythagoras_distance=100000
                under_pythagoras_distance=None
                closest_platform_under=None
                if right_pythagoras_distance==100000 and left_pythagoras_distance==100000:
                    detect_block = Block((1,1,1),current_test_platform.rect.x,current_test_platform.rect.bottom+40,current_test_platform.width,40,all_sprites)
                    hit_list = pygame.sprite.spritecollide(detect_block,p_list,False)
                    detect_block.kill()
                    closest_platform_list=[]
                    selected_platforms_list=[]
                    if len(hit_list)>0:
                        for i in hit_list:
                            if i.rect.y>current_test_platform.rect.y+40:
                                closest_platform_list.append(i.rect.y)
                                selected_platforms_list.append(i)
                        closest_platform_under = selected_platforms_list[closest_platform_list.index(min(closest_platform_list))]
                        under_pythagoras_distance = min(closest_platform_list)
                    else:under_pythagoras_distance=100000
                platform_choice=None
                print("left:",left_pythagoras_distance,"right:",right_pythagoras_distance)
                if closest_platform_under!=None and left_pythagoras_distance==100000 and right_pythagoras_distance==100000:
                    closest_platform=closest_platform_under
                    platform_choice="under"
                elif left_pythagoras_distance==100000 and right_pythagoras_distance==100000 and under_pythagoras_distance==100000:
                    print("no path found")
                    platform_choice="impossible"
                    break
                elif left_pythagoras_distance<right_pythagoras_distance:
                    print("chose left")
                    closest_platform=closest_platform_left
                    platform_choice="left"
                    if closest_platform_right!=None:
                        this_path = testing_path
                        this_path.append(closest_platform_right)
                        all_paths.append(this_path)
                elif left_pythagoras_distance>right_pythagoras_distance:
                    print("chose right")
                    closest_platform=closest_platform_right
                    platform_choice="right"
                    if closest_platform_left!=None:
                        this_path = testing_path
                        this_path.append(closest_platform_left)
                        all_paths.append(this_path)
                if platform_choice!="impossible":
                    if platform_choice=="under":
                        testing_path_coords.append([closest_platform.rect.center[0],closest_platform.rect.y-10])
                        testing_path.append(closest_platform)
                        current_test_platform=closest_platform
                        self.path_platforms.append(closest_platform)
                    elif platform_choice=="left":
                        print("appended left")
                        if left_x_distance==1:
                            testing_path.append(closest_platform)
                            testing_path_coords.append([current_test_platform.rect.left-1,closest_platform.rect.y-10])
                        else:
                            testing_path.append(closest_platform)
                            testing_path_coords.append([closest_platform.rect.right-10,closest_platform.rect.y-10])
                        current_test_platform=closest_platform
                        self.path_platforms.append(closest_platform)
                    elif platform_choice=="right":
                        print("appended right")
                        if right_x_distance==1:
                            testing_path.append(closest_platform)
                            testing_path_coords.append([current_test_platform.rect.right+1,closest_platform.rect.y-10])
                        else:
                            testing_path.append(closest_platform)
                            testing_path_coords.append([closest_platform.rect.left+10,closest_platform.rect.y-10])
                        try:current_test_platform=closest_platform
                        except:pass
                        self.path_platforms.append(closest_platform)
                    if self.final_target_platform==self.platform_under or closest_platform==self.platform_under:
                        if self.final_target_platform==self.platform_under or closest_platform==self.platform_under:
                            testing_path_coords.reverse()
                            testing_path_coords.append([x,y])
                            possible_paths.append(testing_path_coords)
                            print("appended successful path:")
                            print(testing_path_coords)
                        test_index+=1
                        print("test index:",test_index)
                        if test_index<len(all_paths):
                            print("success,trying next path")
                            testing_path=all_paths[test_index]
                            current_test_platform=testing_path[-1]
                        else:
                            print("success, no next path :(")
                            done=True
                    if platform_choice=="impossible":
                        test_index+=1
                        if test_index<len(all_paths):
                            print("impossible,trying next path")
                            testing_path=all_paths[test_index]
                            current_test_platform=testing_path[-1]
                        else:
                            print("impossible, no next path :(")
                            done=True
                else:self.walking=False
                print("current path:")
                print(testing_path_coords)
            all_distances=[]
            for path in possible_paths:
                total_distance=0
                for cord in path:
                    if path.index(cord)<len(path)-1:
                        x_dist=cord[0]-path[path.index(cord)+1][0]
                        y_dist=cord[1]-path[path.index(cord)+1][1]
                        distance=((x_dist**2)+(y_dist**2))**0.5
                        total_distance+=distance
                all_distances.append(total_distance)
            print("possible paths:\n")
            print(possible_paths)
            print("distances:\n")
            print(all_distances)
            if len(possible_paths)>0:
                self.walk_path=possible_paths[all_distances.index(min(all_distances))]
                self.path_platforms.append(self.final_target_platform)
        self.current_walk_path_index=0
        for i in self.path_platforms:
            i.image.fill((0,0,255))
        print(self.walk_path)
        self.target_platform=None
        self.target_x=None
        self.target_y=None
        self.change_x=0
    def blacklist_platform(self,x,y,size,all_sprites,p_list):
        #self.platform_blacklist.append(self.target_platform)
        self.current_walk_path_index=0
        self.blacklist_timer= 480
        try:
            self.target_platform.image.fill((20,20,20))
            print("blabklisted:",self.target_platform.rect.x,self.target_platform.rect.y)
        except:print("no target to fill")
        self.target_platform=None
        self.change_x=0
        print(x,y)
        self.find_path_AI(x,y,size,all_sprites,p_list,None)
    def walk_to_AI(self,x,y,p_list,size,all_sprites,player1):
        if self.life>0:
            if self.walk_path==[]:
                print("self path = [], searching for new")
                self.find_path_AI(x,y,size,all_sprites,p_list,None)
                self.walking=True
            elif not self.rect.collidepoint(self.walk_path[self.current_walk_path_index][0],self.walk_path[self.current_walk_path_index][1]):
                self.target_x=self.walk_path[self.current_walk_path_index][0]
                self.target_y=self.walk_path[self.current_walk_path_index][1]
                #FIND PLATFORM UNDER SELF
                test_y=self.rect.bottom
                old_platform_under=self.platform_under
                self.platform_under=None
                while test_y<self.rect.bottom+80 and self.platform_under==None:
                    for i in p_list:
                        if i.rect.collidepoint(self.rect.x,test_y):
                            self.platform_under=i
                        elif i.rect.collidepoint(self.rect.right,test_y):
                            self.platform_under=i
                    test_y+=1
                if self.platform_under==None:
                    self.platform_under=old_platform_under
                #FIND TARGET PLATFORM
                test_y=self.target_y
                while test_y<size[1] and self.target_platform==None:
                    for i in p_list:
                        if i.rect.collidepoint(self.target_x,test_y):
                            self.target_platform=i
                            break
                    test_y+=1
                if self.target_platform==None:
                    self.target_platform=self.platform_under
                self.target_platform.image.fill((255,0,0))
                if not self.walking:
                    self.walking=True
                if self.target_platform==self.platform_under:
                    if player1.rect.x-40>self.rect.x:self.change_x=5
                    elif player1.rect.x+40<self.rect.x:self.change_x=-5
                    else:self.change_x=0
                    if self.hit_wall:
                        if self.wall.rect.top-self.rect.bottom>-89 and self.change_y>=0:
                            self.jump()
                elif self.target_y>self.rect.bottom:
                    #IF TARGET IS UNDER ME
                    print("target under me")
                    if self.rect.bottom>self.target_platform.rect.y and self.change_y>=0:
                        self.jump()
                    if self.target_platform.rect.y>self.platform_under.rect.y:
                        print("tried walking down")
                        if self.target_x>self.rect.center[0]:
                            self.change_x=5
                            print("going right")
                        elif self.target_x<self.rect.center[0]:
                            self.change_x=-5
                            print("going left")
                        else:
                            self.change_x=0
                            print("stopped")
                    else:
                        print("passed block under")
                        if self.rect.x<self.target_x:self.change_x=5
                        elif self.rect.x>self.target_x:self.change_x=-5
                        else:self.change_x=0
                elif self.target_y<self.rect.bottom:
                    #IF TARGET IS OVER ME
                    #CHECK FOR ROOF
                    roof = None
                    test_y=self.rect.y
                    while test_y>self.rect.top-89 and roof==None:
                        for i in p_list:
                            if i.rect.collidepoint(self.rect.x,test_y):
                                roof=i
                                break
                        test_y-=1
                    #WALK TO TARGET PLATFORM CLOSEST SIDE (X) AND JUMP IF NO ROOF AND T PLATFORM IS CLOSE ENOUGH
                    if not self.target_platform.rect.left-10<=self.rect.right<=self.target_platform.rect.left and not self.target_platform.rect.right+10>=self.rect.left>=self.target_platform.rect.right:
                        if self.rect.right<self.target_platform.rect.left-10:
                            print("walking right to platform corner")
                            self.change_x=5
                            if roof==None or roof.rect.bottom<self.target_platform.rect.top-40:
                                if self.target_platform.rect.left-self.rect.right<250 and self.change_y>=0:
                                    self.jump()
                        elif self.rect.left>self.target_platform.rect.right+10:
                            print("walking left to platform corner")
                            self.change_x=-5
                            if roof==None or roof.rect.bottom<self.target_platform.rect.top-40:
                                if self.rect.left-self.target_platform.rect.right<250 and self.change_y>=0:
                                    self.jump()
                        elif self.rect.left<self.target_platform.rect.center[0] and self.rect.left>=self.target_platform.rect.left:
                            self.change_x=-5
                            print("inside out left")
                        elif self.rect.right>self.target_platform.rect.center[0] and self.rect.right<=self.target_platform.rect.right:
                            self.change_x=5
                            print("inside out right")
                        else:self.change_x=0
                    if self.target_platform.rect.left-10<=self.rect.right<=self.target_platform.rect.left or self.target_platform.rect.right+10>=self.rect.left>=self.target_platform.rect.right:
                        self.change_x=0
                        print("ready to jump")
                        if self.change_y>=0 and self.rect.bottom>=self.target_platform.rect.top:
                            self.jump()
                        if self.rect.bottom<self.target_platform.rect.top:
                            if x>self.rect.center[0]:
                                self.change_x=5
                            elif self.rect.center[0]>x:
                                self.change_x-5
                self.blacklist_timer-=1
                if self.blacklist_timer<=0 and self.target_platform!=None:
                    self.blacklist_platform(x,y,size,all_sprites,p_list)
            elif self.rect.collidepoint(self.walk_path[self.current_walk_path_index][0],self.walk_path[self.current_walk_path_index][1]):
                print("collided with point")
                self.blacklist_timer=480
                if self.target_platform!=None:
                    self.target_platform.image.fill((117,117,117))
                self.target_platform=None
                self.target_x=None
                self.target_y=None
                self.change_x=0
                if self.current_walk_path_index<len(self.walk_path)-1 and self.djump==2:
                    self.current_walk_path_index+=1
                elif self.current_walk_path_index>=len(self.walk_path)-1:
                    self.walking=False
                    self.walk_path=[]
                    self.platform_blacklist=[]
                    print("reached goal")

def main():
    pass

if __name__ == '__main__':
    main()
