import pygame,random,os

class firearm():
    def __init__(self,fireRateInFrames,reloadTime,player,clipSize,gun_image,x_offset,y_offset,y_bullet_offset,draw_list,bullet_speedx,bullet_speedy,bullet_damage):
        self.graphics_dir=os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
        self.image_right = pygame.image.load(self.graphics_dir+gun_image+".gif").convert()
        self.INVISCOL=(63,171,153)
        self.image_right.set_colorkey(self.INVISCOL)
        self.image_left = pygame.transform.flip(self.image_right,True,False)
        self.fireRateInFrames = fireRateInFrames
        self.fireRateFrames = 0
        self.clipSize = clipSize
        self.currentClip = clipSize
        self.reloadTime = reloadTime
        self.reloadTimeFrames = 0
        self.player = player
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.y_bullet_offset = y_bullet_offset
        self.bullet_speedx = bullet_speedx
        self.bullet_speedy = bullet_speedy
        self.bullet_damage = bullet_damage
        self.font = pygame.font.SysFont('Calibri', 20,True,False)
        self.GREY = (117,117,117)
        draw_list.append(self)
    def update(self,screen,**args):
        clip_render = self.font.render(str(self.currentClip), 1,self.GREY)
        if self.player.p==1:
            if self.player.direction == 1:
                screen.blit(clip_render, (self.player.rect.x-5-clip_render.get_width(),self.player.rect.y+2))
                screen.blit(self.image_right, (self.player.rect.x+self.x_offset,self.player.rect.y+self.y_offset))
            elif self.player.direction == 0:
                screen.blit(clip_render, (self.player.rect.x+24,self.player.rect.y+2))
                screen.blit(self.image_left, (self.player.rect.x-self.image_left.get_width()+(20-self.x_offset),self.player.rect.y+self.y_offset))
        elif self.player.p==2:
            if self.player.direction == 1:
                screen.blit(clip_render, (self.player.rect.x-5-clip_render.get_width(),self.player.rect.y+2))
                screen.blit(self.image_right, (self.player.rect.x+self.x_offset,self.player.rect.y+self.y_offset))
            elif self.player.direction == 0:
                screen.blit(clip_render, (self.player.rect.x+24,self.player.rect.y+2))
                screen.blit(self.image_left, (self.player.rect.x-self.image_left.get_width()+(20-self.x_offset),self.player.rect.y+self.y_offset))
        if self.reloadTimeFrames>0:
            self.reloadTimeFrames -= 1
            self.currentClip = int((self.reloadTime*60-self.reloadTimeFrames)/(self.reloadTime*60)*self.clipSize)
            if self.reloadTimeFrames==0:
                self.currentClip=self.clipSize
        if self.fireRateFrames>0:
            self.fireRateFrames-=1
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,*args):
        import FCobjects
        if guns_allowed and self.fireRateFrames == 0 and self.currentClip > 0 and self.reloadTimeFrames==0:
                if self.player.p == 1:
                    if player1.rect.x <= player2.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player1.rect.right,player1.rect.y+self.y_bullet_offset,8,3,self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    if player1.rect.x > player2.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player1.rect.left,player1.rect.y+self.y_bullet_offset,8,3,-1*self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    bullet1_list.add(bullet)
                elif self.player.p == 2:
                    if player2.rect.x <= player1.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player2.rect.right,player2.rect.y+self.y_bullet_offset,8,3,self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    if player2.rect.x > player1.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player2.rect.left,player2.rect.y+self.y_bullet_offset,8,3,-1*self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    bullet2_list.add(bullet)
                self.currentClip -= 1
                self.fireRateFrames = self.fireRateInFrames
    def reload(self):
        if self.reloadTimeFrames==0 and self.currentClip<self.clipSize:
            self.reloadTimeFrames=self.reloadTime*60

class handGun(firearm):
    def __init__(self,player,draw_list):
        firearm.__init__(self,25,1.7,player,8,"handgun",4,11,13,draw_list,20,0,2)

class assaultRifle(firearm):
    def __init__(self,player,draw_list):
        firearm.__init__(self,9,4,player,20,"assaultRifle",1,8,13,draw_list,20,0.5,1)

class shotgun(firearm):
    def __init__(self,player,draw_list):
        firearm.__init__(self,60,4,player,5,"shotgun",2,8,10,draw_list,15,0,2)
        self.bullets_per_shot = 5
        self.time_before_reload_frames = 0
    def update(self,screen,*args):
        clip_render = self.font.render(str(self.currentClip), 1,self.GREY)
        if self.player.direction==1:
            screen.blit(clip_render, (self.player.rect.x-5-clip_render.get_width(),self.player.rect.y+2))
            screen.blit(self.image_right, (self.player.rect.x+self.x_offset,self.player.rect.y+self.y_offset))
        elif self.player.direction==0:
            screen.blit(clip_render, (self.player.rect.x+24,self.player.rect.y+2))
            screen.blit(self.image_left, (self.player.rect.x-self.image_left.get_width()+(20-self.x_offset),self.player.rect.y+7))
        if self.reloadTimeFrames>0 and self.time_before_reload_frames==0:
            self.reloadTimeFrames -= 1
            self.currentClip = int((self.reloadTime*60-self.reloadTimeFrames)/(self.reloadTime*60)*self.clipSize)
            if self.reloadTimeFrames==0:
                self.currentClip=self.clipSize
        elif self.time_before_reload_frames>0:
            self.time_before_reload_frames-=1
        if self.fireRateFrames>0:
            self.fireRateFrames-=1
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,*args):
        import FCobjects
        if guns_allowed and self.fireRateFrames == 0 and self.currentClip > 0:
                if self.player.p == 1:
                    if player1.rect.x <= player2.rect.x:
                        for i in range(int((-self.bullets_per_shot)/2),int(self.bullets_per_shot-int((self.bullets_per_shot)/2))):
                            bullet = FCobjects.bulletBlock(GREY,player1.rect.right,player1.rect.y+self.y_bullet_offset,5,5,self.bullet_speedx,i*2,self.bullet_damage,all_sprites)
                            bullet1_list.add(bullet)
                    if player1.rect.x > player2.rect.x:
                        for i in range(int((-self.bullets_per_shot)/2),int(self.bullets_per_shot-int((self.bullets_per_shot)/2))):
                            bullet = FCobjects.bulletBlock(GREY,player1.rect.left,player1.rect.y+self.y_bullet_offset,5,5,-1*self.bullet_speedx,i*2,self.bullet_damage,all_sprites)
                            bullet1_list.add(bullet)
                elif self.player.p == 2:
                    if player2.rect.x <= player1.rect.x:
                        for i in range(int((-self.bullets_per_shot)/2),int(self.bullets_per_shot-int((self.bullets_per_shot)/2))):
                            bullet = FCobjects.bulletBlock(GREY,player2.rect.right,player2.rect.y+self.y_bullet_offset,5,5,self.bullet_speedx,i*2,self.bullet_damage,all_sprites)
                            bullet2_list.add(bullet)
                    if player2.rect.x > player1.rect.x:
                        for i in range(int((-self.bullets_per_shot)/2),int(self.bullets_per_shot-int((self.bullets_per_shot)/2))):
                            bullet = FCobjects.bulletBlock(GREY,player2.rect.left,player2.rect.y+self.y_bullet_offset,5,5,-1*self.bullet_speedx,i*2,self.bullet_damage,all_sprites)
                            bullet2_list.add(bullet)
                self.reloadTimeFrames=0
                self.currentClip -= 1
                self.fireRateFrames = self.fireRateInFrames
    def reload(self):
        if self.reloadTimeFrames==0 and self.currentClip<self.clipSize:
            self.reloadTimeFrames=self.reloadTime*60
            self.time_before_reload_frames = 60
            self.reloadTimeFrames=(self.reloadTime-((self.currentClip*self.reloadTime)/self.clipSize))*60


class lazerRifle(firearm):
    def __init__(self,player,draw_list):
        firearm.__init__(self,70,3,player,3,"lazerRifle",4,7,12,draw_list,0,0,2)
        self.lazer_pictures_list = []
        self.lazer_linger_time_frames = 100
        self.lazer_height = 4
        self.lazer_color = (255,255,255)
        self.timer=0
        self.timer_running=False
        self.damage_indicator_color=(1,1,1)
    def update(self,screen,*args):
        clip_render = self.font.render(str(self.currentClip), 1,self.GREY)
        if self.timer/40<3:
            if self.timer/40<1:
                damage_indicator_color=(73,252,97)
            elif self.timer/40<2:
                damage_indicator_color=(216,250,45)
            elif self.timer/40<3:
                damage_indicator_color=(250,137,45)
        else:damage_indicator_color=(245,20,20)
        if self.player.direction==1:
            if self.timer_running:
                pygame.draw.rect(screen, damage_indicator_color, [(self.player.rect.right+13),self.player.rect.y+self.y_bullet_offset-2,18,8])
            screen.blit(clip_render, (self.player.rect.x-5-clip_render.get_width(),self.player.rect.y+2))
            screen.blit(self.image_right, (self.player.rect.x+self.x_offset,self.player.rect.y+self.y_offset))
        elif self.player.direction==0:
            if self.timer_running:
                pygame.draw.rect(screen, damage_indicator_color, [(self.player.rect.x-31),self.player.rect.y+self.y_bullet_offset-2,18,8])
            screen.blit(clip_render, (self.player.rect.x+24,self.player.rect.y+2))
            screen.blit(self.image_left, (self.player.rect.x-self.image_left.get_width()+(20-self.x_offset),self.player.rect.y+7))
        if self.reloadTimeFrames>0:
            self.reloadTimeFrames -= 1
            self.currentClip = int((self.reloadTime*60-self.reloadTimeFrames)/(self.reloadTime*60)*self.clipSize)
            if self.reloadTimeFrames==0:
                self.currentClip=self.clipSize
        for i in self.lazer_pictures_list:
            if i[2]<=0:
                i[1].kill()
                self.lazer_pictures_list.remove(i)
            pygame.draw.rect(screen,(255,255,255),i[0])
            i[2]-=1
        if self.fireRateFrames>0:
            self.fireRateFrames-=1
        if self.timer_running:
            self.timer+=1
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list):
        if guns_allowed and self.fireRateFrames == 0 and self.currentClip > 0 and self.reloadTimeFrames==0:
            self.timer_running=True
    def release(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list):
        import FCobjects
        if self.timer/40<=3:
            if self.timer/40<1:
                self.bullet_damage=1
            elif self.timer/40<2:
                self.bullet_damage=2
            elif self.timer/40<3:
                self.bullet_damage=4
        else:self.bullet_damage=6
        if guns_allowed and self.fireRateFrames == 0 and self.currentClip > 0 and self.reloadTimeFrames==0:
            try:
                if self.player.p == 1:
                    if player1.rect.x <= player2.rect.x:
                        bullet = FCobjects.bulletBlock(self.lazer_color,player1.rect.right+15,player1.rect.y+self.y_bullet_offset,1500-(player1.rect.right+15),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                        bullet_picture = pygame.draw.rect(screen,self.lazer_color,[player1.rect.right+15,player1.rect.y+self.y_bullet_offset,1500-(player1.rect.right+15),self.lazer_height])
                    if player1.rect.x > player2.rect.x:
                        bullet = FCobjects.bulletBlock(self.lazer_color,-1500,player1.rect.y+self.y_bullet_offset,1500+(player1.rect.left-15),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                        bullet_picture = pygame.draw.rect(screen,self.lazer_color,[-1500,player1.rect.y+self.y_bullet_offset,1500+(player1.rect.left-15),self.lazer_height])
                    bull_dis = pygame.sprite.spritecollide(bullet,p_list,False)
                    if len(bull_dis)>0:
                        bullet.kill()
                        if player1.rect.x <= player2.rect.x:
                            bull_dis_x=[]
                            for i in bull_dis:
                                bull_dis_x.append(i.rect.left)
                            bullet = FCobjects.bulletBlock(self.lazer_color,player1.rect.right+15,player1.rect.y+self.y_bullet_offset,min(bull_dis_x)-(player1.rect.right+15),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                            bullet_picture = pygame.draw.rect(screen,self.lazer_color,[player1.rect.right+15,player1.rect.y+self.y_bullet_offset,min(bull_dis_x)-(player1.rect.right+15),self.lazer_height])
                        if player1.rect.x > player2.rect.x:
                            bull_dis_x=[]
                            for i in bull_dis:
                                bull_dis_x.append(i.rect.right)
                            bullet = FCobjects.bulletBlock(self.lazer_color,max(bull_dis_x),player1.rect.y+self.y_bullet_offset,(player1.rect.left-15)-max(bull_dis_x),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                            bullet_picture = pygame.draw.rect(screen,self.lazer_color,[max(bull_dis_x),player1.rect.y+self.y_bullet_offset,(player1.rect.left-15)-max(bull_dis_x),self.lazer_height])
                    bullet1_list.add(bullet)
                    self.lazer_pictures_list.append([bullet_picture,bullet,self.lazer_linger_time_frames])
                elif self.player.p == 2:
                    if player2.rect.x <= player1.rect.x:
                        bullet = FCobjects.bulletBlock(self.lazer_color,player2.rect.right+15,player2.rect.y+self.y_bullet_offset,1500-(player2.rect.right+15),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                        bullet_picture = pygame.draw.rect(screen,self.lazer_color,[player2.rect.right+15,player2.rect.y+self.y_bullet_offset,1500-(player2.rect.right+15),self.lazer_height])
                    if player2.rect.x > player1.rect.x:
                        bullet = FCobjects.bulletBlock(self.lazer_color,-1500,player2.rect.y+self.y_bullet_offset,1500+(player2.rect.left-15),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                        bullet_picture = pygame.draw.rect(screen,self.lazer_color,[-1500,player2.rect.y+self.y_bullet_offset,1500+(player2.rect.left-15),self.lazer_height])
                    bull_dis = pygame.sprite.spritecollide(bullet,p_list,False)
                    if len(bull_dis)>0:
                        bullet.kill()
                        if player2.rect.x <= player1.rect.x:
                            bull_dis_x=[]
                            for i in bull_dis:
                                bull_dis_x.append(i.rect.left)
                            bullet = FCobjects.bulletBlock(self.lazer_color,player2.rect.right+15,player2.rect.y+self.y_bullet_offset,min(bull_dis_x)-(player2.rect.right+15),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                            bullet_picture = pygame.draw.rect(screen,self.lazer_color,[player2.rect.right+15,player2.rect.y+self.y_bullet_offset,min(bull_dis_x)-(player2.rect.right+15),self.lazer_height])
                        if player2.rect.x > player1.rect.x:
                            bull_dis_x=[]
                            for i in bull_dis:
                                bull_dis_x.append(i.rect.right)
                            bullet = FCobjects.bulletBlock(self.lazer_color,max(bull_dis_x),player2.rect.y+self.y_bullet_offset,(player2.rect.left-15)-max(bull_dis_x),self.lazer_height,0,0,self.bullet_damage,all_sprites)
                            bullet_picture=pygame.draw.rect(screen,self.lazer_color,[max(bull_dis_x),player2.rect.y+self.y_bullet_offset,(player2.rect.left-15)-max(bull_dis_x),self.lazer_height])
                    bullet2_list.add(bullet)
                    self.lazer_pictures_list.append([bullet_picture,bullet,self.lazer_linger_time_frames])
            except:pass
            self.currentClip -= 1
            self.fireRateFrames = self.fireRateInFrames
            self.bullet_damage=2
            self.timer_running=False
            self.timer=0

class lazerPistol(firearm):
    def __init__(self,player,draw_list):
        firearm.__init__(self,40,3,player,6,"lazerRifle",4,7,13,draw_list,8,0,3)
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,*args):
        import FCobjects
        if guns_allowed and self.fireRateFrames == 0 and self.currentClip > 0 and self.reloadTimeFrames==0:
                if self.player.p == 1:
                    if player1.rect.x <= player2.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player1.rect.right,player1.rect.y+self.y_bullet_offset,80,3,self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    if player1.rect.x > player2.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player1.rect.left-80,player1.rect.y+self.y_bullet_offset,80,3,-1*self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    bullet1_list.add(bullet)
                elif self.player.p == 2:
                    if player2.rect.x <= player1.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player2.rect.right,player2.rect.y+self.y_bullet_offset,80,3,self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    if player2.rect.x > player1.rect.x:
                        bullet = FCobjects.bulletBlock(GREY,player2.rect.left-80,player2.rect.y+self.y_bullet_offset,80,3,-1*self.bullet_speedx,round(random.uniform(-self.bullet_speedy,self.bullet_speedy),3),self.bullet_damage,all_sprites)
                    bullet2_list.add(bullet)
                self.currentClip -= 1
                self.fireRateFrames = self.fireRateInFrames

class adminGun(lazerRifle):
    def __init__(self,player,draw_list):
        lazerRifle.__init__(self,player,draw_list)
        self.bullet_damage = 14
        self.clipSize = 1337
        self.currentClip = 1337
        self.fireRateInFrames = 10
        self.reloadTime = 0.5
        self.y_bullet_offset = -5
        self.lazer_color = (1,1,1)
        self.lazer_height = 40

class sniperRifle(firearm):
    def __init__(self,player,draw_list):
        firearm.__init__(self,80,4,player,4,"sniperRifle",2,8,14,draw_list,20,0,10)

class grenadeLauncher(firearm):
    def __init__(self,player,draw_list,grenade_list):
        firearm.__init__(self,40,5,player,5,"grenadeLauncher",3,13,16,draw_list,6,-10,5)
        self.grenade_list=grenade_list
        self.grenade_explosion_time=0.01
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,*args):
        import FCobjects
        if guns_allowed and self.fireRateFrames == 0 and self.currentClip > 0 and self.reloadTimeFrames==0:
                if self.player.p == 1:
                    if player1.rect.x <= player2.rect.x:
                        if player1.crouching:
                            grenade = FCobjects.grenade(None,player1.rect.x+36,player1.rect.y+self.y_bullet_offset-6,10,10,(self.bullet_speedx+player1.change_x*0.7)*0.7,self.bullet_speedy*0.5,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                        else:
                            grenade = FCobjects.grenade(None,player1.rect.x+36,player1.rect.y+self.y_bullet_offset,10,10,(self.bullet_speedx+player1.change_x*0.7),self.bullet_speedy,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                    if player1.rect.x > player2.rect.x:
                        if player1.crouching:
                            grenade = FCobjects.grenade(None,player1.rect.right-36,player1.rect.y+self.y_bullet_offset-6,10,10,(self.bullet_speedx*-1+player1.change_x*0.7)*0.7,self.bullet_speedy*0.5,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                        else:
                            grenade = FCobjects.grenade(None,player1.rect.right-36,player1.rect.y+self.y_bullet_offset,10,10,(self.bullet_speedx*-1+player1.change_x*0.7),self.bullet_speedy,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                elif self.player.p == 2:
                    if player2.rect.x <= player1.rect.x:
                        if player2.crouching:
                            grenade = FCobjects.grenade(None,player2.rect.x+36,player2.rect.y+self.y_bullet_offset-6,10,10,(self.bullet_speedx+player2.change_x*0.7)*0.7,self.bullet_speedy*0.5,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                        else:
                            grenade = FCobjects.grenade(None,player2.rect.x+36,player2.rect.y+self.y_bullet_offset,10,10,(self.bullet_speedx+player2.change_x*0.7),self.bullet_speedy,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                    if player2.rect.x > player1.rect.x:
                        if player2.crouching:
                            grenade = FCobjects.grenade(None,player2.rect.right-36,player2.rect.y+self.y_bullet_offset-6,10,10,(self.bullet_speedx*-1+player2.change_x*0.7)*0.7,self.bullet_speedy*0.5,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                        else:
                            grenade = FCobjects.grenade(None,player2.rect.right-36,player2.rect.y+self.y_bullet_offset,10,10,(self.bullet_speedx*-1+player2.change_x*0.7),self.bullet_speedy,self.bullet_damage,all_sprites,self.grenade_list,self.grenade_explosion_time)
                self.currentClip -= 1
                self.fireRateFrames = self.fireRateInFrames

class katana():
    def __init__(self,player,draw_list):
        self.animation_frame=0
        self.animation_frame_length=12
        self.fireRateInFrames=self.animation_frame_length+30
        self.fireRateFrames=0
        self.player=player
        self.graphics_dir=os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
        self.image_right = pygame.image.load(self.graphics_dir+"katana"+".gif").convert()
        self.INVISCOL=(63,171,153)
        self.image_right.set_colorkey(self.INVISCOL)
        self.image_left = pygame.transform.flip(self.image_right,True,False)
        self.x_offset=6
        self.y_offset=-18
        self.hitbox=None
        self.hit_direction=None
        self.hitbox_width=self.image_right.get_height()-13
        self.hitbox_height=14
        self.hitbox_y=4
        self.hitbox_x=0
        self.damage=3
        self.currentClip=1
        self.speed_coefficient_x=1
        self.speed_coefficient_y=1.2
        draw_list.append(self)
    def update(self,screen,**args):
        if self.player.change_y!=0:
            self.speed_coefficient_x=1.3
        else:
            self.speed_coefficient_x=1
        if self.animation_frame==0 and self.hitbox!=None:
            self.hitbox.kill()
            self.hitbox=None
            self.player.direction_enabled=True
        if self.player.direction == 1:
            if self.animation_frame==0:
                screen.blit(self.image_right, (self.player.rect.x+self.x_offset,self.player.rect.y+self.y_offset))
            elif self.animation_frame>0:
                frame_image=pygame.image.load(self.graphics_dir+"katana"+str(int((14-self.animation_frame)/2))+".gif").convert()
                frame_image.set_colorkey(self.INVISCOL)
                screen.blit(frame_image, (self.player.rect.x,self.player.rect.y+self.y_offset))
            if self.animation_frame>0 and self.hitbox!=None:
                self.hitbox.rect.x=self.player.rect.right+self.hitbox_x
                self.hitbox.rect.y=self.player.rect.y+self.hitbox_y
                self.animation_frame-=1
        elif self.player.direction == 0:
            if self.animation_frame==0:
                screen.blit(self.image_left, (self.player.rect.x-self.image_left.get_width()+(20-self.x_offset),self.player.rect.y+self.y_offset))
            elif self.animation_frame>0:
                frame_image=pygame.image.load(self.graphics_dir+"katana"+str(int((14-self.animation_frame)/2))+".gif").convert()
                frame_image.set_colorkey(self.INVISCOL)
                frame_image_left = pygame.transform.flip(frame_image,True,False)
                screen.blit(frame_image_left, (self.player.rect.right-frame_image_left.get_width(),self.player.rect.y+self.y_offset))
            if self.animation_frame>0 and self.hitbox!=None:
                self.hitbox.rect.right=self.player.rect.left-self.hitbox_x
                self.hitbox.rect.y=self.player.rect.y+self.hitbox_y
                self.animation_frame-=1
        if self.fireRateFrames>0:
            self.fireRateFrames-=1
    def shoot(self,guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list,*args):
        if self.fireRateFrames==0 and guns_allowed:
            import FCobjects
            try:self.hitbox.kill()
            except:pass
            if self.player.direction==1:
                self.hitbox=FCobjects.bulletBlock(None,self.player.rect.right,self.player.rect.y+self.hitbox_y,self.hitbox_width,self.hitbox_height,0,0,self.damage,all_sprites)
            elif self.player.direction==0:
                self.hitbox=FCobjects.bulletBlock(None,self.player.rect.left-self.hitbox_width,self.player.rect.y+self.hitbox_y,self.hitbox_width,self.hitbox_height,0,0,self.damage,all_sprites)
            if self.player.p==1:
                bullet1_list.add(self.hitbox)
            elif self.player.p==2:
                bullet2_list.add(self.hitbox)
            self.animation_frame=self.animation_frame_length
            self.fireRateFrames=self.fireRateInFrames
            self.player.direction_enabled=False
    def reload(self):
        pass

#class heavyHammer()

def main():
    pass

if __name__=="__main__":
    main()
