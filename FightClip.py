"""
Jag ska definitivt rensa texten och kommentera mer, men detta far duga for nu
Python 3.4.3
Koray M Kaya
"""
import pygame,pickle,FCobjects,FCweapons,FCcosmetics, os
pygame.init()

mapname="space"

#Deklarera farger
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (117,117,117)
BGGREY = (51,51,51)
DARKGREY = (10,10,10)
MRED = (173,16,16)
RBLUE = (0,0,179)
RGREEN = (32,179,16)
TPYELLOW = (229,237,0)
HEALGREEN = (13,189,19)
ALPHA = (75,111,114)
BETA = (97,121,75)
INVISCOL = (63,171,153)

#Deklarera fonten sa att jag kan skriva score etc
font = pygame.font.SysFont('Calibri', 20,True,False)

#Olika installningar som man kan andra

#map_dir="C:\\Users\\ab43324\\Desktop\\FunktionellaProjekt\\FightClip\\MAPS\\"
#graphics_dir="C:\\Users\\ab43324\\Desktop\\FunktionellaProjekt\\FightClip\\GRAPHICS\\"
dir_path = os.path.dirname(os.path.realpath(__file__))
map_dir= dir_path+"\\MAPS\\"
graphics_dir= dir_path+"\\GRAPHICS\\"
guns_allowed = True
startWeapon = "handGun"
map_info = pickle.load(open(map_dir+str(mapname)+".p","rb"))

#Har forsoker jag ge mappen en stor lek och spelaren en start position, om banan inte har dessa installningar
#anvands standardinstallningarna
try:size=map_info[0][5]
except:size = (1280,720)
try:startPos=map_info[0][:4]
#De tva forsta startpos galler player1 och de 2 sista galler player2
except:startPos=[650,10,30,10]

#Har deklareras alla grupper som jag behover
respawn_list = []
p_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
bb_list = pygame.sprite.Group()
instaDeath_list = pygame.sprite.Group()
tp_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
heal_list = pygame.sprite.Group()
bullet1_list = pygame.sprite.Group()
bullet2_list = pygame.sprite.Group()
grenade_list = pygame.sprite.Group()
exploding_grenades_list = pygame.sprite.Group()
weapon_box_list = pygame.sprite.Group()
draw_list=[]

#Denna funktion updaterar alla Graphical User Interface:n, spelarnas liv, magasin och vinster.
def GUIUpdates():
    if guns_allowed:
        player1_life = font.render(str(player1.life), 1,MRED)
        player1_clip = font.render(str(player1.currWeapon.currentClip), 1,GREY)
        player1_wins = font.render(str(player1.score), 1,MRED)
        try:
            player2_life = font.render(str(player2.life), 1,RBLUE)
            player2_clip = font.render(str(player2.currWeapon.currentClip), 1,GREY)
            player2_wins = font.render(str(player2.score), 1,RBLUE)
        except:pass
        #Om man anvander AI blir AI spelaren player2 darfor behover man hamta informationen fran en annan plats
        try:
            player2_life = font.render(str(AIplayer.life), 1,RBLUE)
            player2_clip = font.render(str(AIplayer.currWeapon.currentClip), 1,GREY)
            player2_wins = font.render(str(AIplayer.score), 1,RBLUE)
        except:pass
    elif not guns_allowed:
        #Om vapen inte ar tillatna blir vissa installningar orelevanta och far
        #att halla skarmen clean kan de lamnas blanka
        player1_life = None
        player1_clip = None
        player1_wins = font.render(str(player1.deaths), 1,MRED)
        player2_life = None
        player2_clip = None
        try:player2_wins = font.render(str(player2.deaths), 1,RBLUE)
        except:pass
        try:player2_wins = font.render(str(AIplayer.deaths), 1,RBLUE)
        except:pass
    try:
        return player1_wins,player2_wins,player1_life,player2_life,player2_clip,player1_clip
    except:
        return player1_wins,player2_wins

def bulletCollisions(blink_red,blink_blue):
    #Kollar alla bullet-player kollisioner, lagg marke till att man inte kan skadas av sina egna
    #bullets, forutom granater. Dessutom gor den sa skarmen blinkar rott/blott nar man skadas
    for item in bullet1_list:
        bull_dis = pygame.sprite.spritecollide(item,p_list,False)
        for i in bull_dis:
            item.kill()
    for item in bullet2_list:
        bull_dis = pygame.sprite.spritecollide(item,p_list,False)
        for i in bull_dis:
            item.kill()
    for i in exploding_grenades_list:
        explosion_hitlist = pygame.sprite.spritecollide(i.explosion_hitbox,player_list,False)
        for player in explosion_hitlist:
            if player not in i.players_hurt:
                player.life-=i.damage
                if player==player1:
                    if blink_red==0:
                        blink_red=4
                player.been_shot=20
                if player.rect.x>i.rect.x:
                    player.shot_push = 17
                    player.shot_recovery=17/20
                elif player.rect.x<i.rect.x:
                    player.shot_push = -17
                    player.shot_recovery=-17/20
                player.change_y=-9
                i.players_hurt.append(player)
    coll_list = pygame.sprite.spritecollide(player1, bullet2_list, True)
    for i in coll_list:
        if blink_red == 0:
            blink_red = 4
        player1.life -= i.damage
        player1.been_shot = 30
        if player1.rect.x - player2.rect.x < 0:
            player1.shot_push = -4
            player1.shot_recovery = 4/30
            if player1.change_x==-5:
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
            elif player1.change_x==-5:
                player1.been_shot = 20
                player1.shot_push = 2
                player1.shot_recovery = 2/20
        if player1.change_y==0:
            player1.change_y = -2
    coll_list = pygame.sprite.spritecollide(player2, bullet1_list, True)
    for i in coll_list:
        if blink_blue == 0:
            blink_blue = 4
        player2.life -= i.damage
        player2.been_shot = 30
        if player2.rect.x - player1.rect.x < 0:
            player2.shot_push = -4
            player2.shot_recovery = 4/30
            if player2.change_x==-5:
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
            elif player2.change_x==-5:
                player2.been_shot = 20
                player2.shot_push = 2
                player2.shot_recovery = 2/20
        if player1.change_y==0:
            player2.change_y = -2
    return blink_blue,blink_red

def collisions():
    #instad ar killerblocken som dodar en direkt
    instad_list = pygame.sprite.spritecollide(player1, instaDeath_list,False)
    for i in instad_list:
        player1.life=0
    instad_list = pygame.sprite.spritecollide(player2, instaDeath_list,False)
    for i in instad_list:
        player2.life=0
    #Kollar om spelaren har rort nagon vapenbox
    weapon_box_coll = pygame.sprite.spritecollide(player1, weapon_box_list,False)
    for i in weapon_box_coll:
        i.giveWeapon(player1,draw_list,grenade_list)
        i.kill()
        respawn_list.append(i)
    weapon_box_coll = pygame.sprite.spritecollide(player2, weapon_box_list,False)
    for i in weapon_box_coll:
        i.giveWeapon(player2,draw_list,grenade_list)
        i.kill()
        respawn_list.append(i)
    #Nar spelaren kolliderar med teleporter, denna ar lite mer komplicerad for ibland kan
    #spelaren rora flera teleportorer samtidigt och darfor har jag en algoritm for att valja
    #en godtycklig
    tp_collision_list = pygame.sprite.spritecollide(player1, tp_list, False)
    if len(tp_collision_list)<2 and len(tp_collision_list)!=0:
        for i in tp_collision_list:
            if i.tpdest=="spawn":
                player1.true_x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.true_x = int(i.tpdest.split(",")[0])
                player1.rect.y = int(i.tpdest.split(",")[1])
        player1.deaths+=1
    if len(tp_collision_list)>1:
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.top)
        tp_collision_cords.sort()
        if tp_collision_cords[0]==tp_collision_cords[1]:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player1.true_x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.rect.x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        elif player1.rect.top<tp_collision_cords[0] and player1.change_y>0:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player1.true_x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.true_x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.bottom)
        tp_collision_cords.sort()
        if tp_collision_cords[-1]==tp_collision_cords[-2]:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player1.true_x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.true_x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        elif player1.rect.top>max(tp_collision_cords) and player1.change_y<0:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player1.true_x = int(startPos[0])
                player1.rect.y = int(startPos[1])
            else:
                player1.true_x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player1.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        player1.deaths+=1
    tp_collision_list = pygame.sprite.spritecollide(player2, tp_list, False)
    if len(tp_collision_list)==1:
        for i in tp_collision_list:
            if i.tpdest=="spawn":
                player2.true_x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.true_x = int(i.tpdest.split(",")[0])
                player2.rect.y = int(i.tpdest.split(",")[1])
        player2.deaths+=1
    if len(tp_collision_list)>1:
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.top)
        tp_collision_cords.sort()
        if tp_collision_cords[0]==tp_collision_cords[1]:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player2.true_x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.true_x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        elif player2.rect.top<min(tp_collision_cords) and player2.change_y>0:
            if tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest=="spawn":
                player2.true_x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.true_x=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(min(tp_collision_cords))].tpdest.split(",")[1])
        tp_collision_cords=[]
        for i in tp_collision_list:
            tp_collision_cords.append(i.rect.bottom)
        tp_collision_cords.sort()
        if tp_collision_cords[-1]==tp_collision_cords[-2]:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player2.true_x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.true_x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        elif player2.rect.top>max(tp_collision_cords) and player2.change_y<0:
            if tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest=="spawn":
                player2.true_x = int(startPos[2])
                player2.rect.y = int(startPos[3])
            else:
                player2.true_x=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[0])
                player2.rect.y=int(tp_collision_list[tp_collision_cords.index(max(tp_collision_cords))].tpdest.split(",")[1])
        player2.deaths+=1
    #Nar man ror ett health block sa ger den liv
    heal_collision_list = pygame.sprite.spritecollide(player1, heal_list, False)
    for i in heal_collision_list:
        player1.life+=2
        i.kill()
        respawn_list.append(i)
    heal_collision_list = pygame.sprite.spritecollide(player2, heal_list, False)
    for i in heal_collision_list:
        player2.life+=2
        i.kill()
        respawn_list.append(i)

#Enkel funktion for att se om en key ar nedtryckt
def keyPressed(key):
    keys=pygame.key.get_pressed()
    if keys[key]:
        return True
    else:
        return False

#Oppnar banan som man laddade in tidigare, den laser av pickle filen och far reda pa blockens egenskaper
#sedan skapar den blocken
def loadMap():
    #print(map_info[0])
    try:guns_allowed = map_info[0][4]
    except:pass
    for i in range(1,len(map_info)):
        print(map_info[i])
        if map_info[i][0]=="white":
            map_info[i][0]=WHITE
        elif map_info[i][0]=="black" or map_info[i][0]=="grey":
            map_info[i][0]=GREY
        elif map_info[i][0]=="yellow":
            map_info[i][0]=TPYELLOW
        elif map_info[i][0]=="green":
            map_info[i][0]=HEALGREEN
        if map_info[i][5]=="normal":
            platform = FCobjects.platform(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4],all_sprites,p_list)
        elif map_info[i][5]=="killer":
            platform = FCobjects.killer(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4],all_sprites,instaDeath_list)
        elif map_info[i][5]=="teleporter":
            platform = FCobjects.teleporterBlock(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4],map_info[i][6],all_sprites,tp_list)
        elif map_info[i][5]=="healer":
            platform = FCobjects.healBlock(map_info[i][0],map_info[i][1],map_info[i][2],map_info[i][3],map_info[i][4],int(map_info[i][6]),all_sprites,heal_list)
        elif map_info[i][5]=="weapon":
            platform = FCobjects.weaponBox(map_info[i][1],map_info[i][2],map_info[i][7],weapon_box_list,all_sprites,map_info[i][6])

player1 = FCobjects.player(MRED,int(startPos[0]),int(startPos[1]),1,all_sprites,player_list)
player2 = FCobjects.player(RBLUE,int(startPos[2]),int(startPos[3]),2,all_sprites,player_list)
#player1.life=999999
#player2 = FCobjects.AIplayer(int(startPos[2]),int(startPos[3]),all_sprites,player_list)
#player2.life=999999

def main():
    screen = pygame.display.set_mode(size)
    fullscreen = False
    icon=pygame.image.load(graphics_dir+"icon.gif")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Fight Clip")
    if guns_allowed:
        if startWeapon=="handGun":
            player1.currWeapon=FCweapons.handGun(player1,draw_list)
            player2.currWeapon=FCweapons.handGun(player2,draw_list)
    blink_red = 0
    blink_blue = 0
    loadMap()
    quit_timer=30
    done = False
    slowmo=False
    round_end = False
    clock = pygame.time.Clock()
    while not done:
        if player1.life>0:
            if keyPressed(pygame.K_k):
                player1.crouch()
            if keyPressed(pygame.K_m):
                if guns_allowed:
                    player1.currWeapon.shoot(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list)
        if player2.life>0:
            if keyPressed(pygame.K_s):
                player2.crouch()
            if keyPressed(pygame.K_LESS):
                if guns_allowed:
                    player2.currWeapon.shoot(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list)
        if keyPressed(pygame.K_SPACE):
            slowmo=True
        else:
            slowmo=False
        if keyPressed(pygame.K_ESCAPE):
            quit_timer-=1
        else: quit_timer=30
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if not fullscreen:
                        pygame.display.set_mode(size,pygame.FULLSCREEN)
                        fullscreen = True
                    elif fullscreen:
                        pygame.display.set_mode(size)
                        fullscreen = False
                if player2.life<=0 or player1.life<=0:
                        if event.key == pygame.K_y:
                            round_end = False
                            blink_red,blink_blue=player1.reset(startPos,player1,player2,blink_red,blink_blue,bullet1_list,bullet2_list,startWeapon,draw_list,p_list,respawn_list)
                            blink_red,blink_blue=player2.reset(startPos,player1,player2,blink_red,blink_blue,bullet1_list,bullet2_list,startWeapon,draw_list,p_list,respawn_list)
                        if event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                            done=True
                if player1.life>0:
                    if event.key == pygame.K_m:
                        if guns_allowed and player1.currWeapon.currentClip==0:
                            player1.currWeapon.reload()
                    if event.key == pygame.K_j:
                        player1.change_x = -5
                    if event.key == pygame.K_l:
                        player1.change_x = 5
                    if event.key == pygame.K_i:
                        player1.jump()
                    if event.key == pygame.K_o:
                        if guns_allowed:
                            player1.currWeapon.reload()
                if player2.life>0:
                    if event.key == pygame.K_LESS:
                        if guns_allowed and player2.currWeapon.currentClip==0:
                            player2.currWeapon.reload()
                    if event.key == pygame.K_a:
                        player2.change_x = -5
                    if event.key == pygame.K_d:
                        player2.change_x = 5
                    if event.key == pygame.K_LSHIFT:
                        player2.jump()
                    if event.key == pygame.K_s:
                        player2.crouch()
                    if event.key == pygame.K_w:
                        if guns_allowed:
                            player2.currWeapon.reload()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j and player1.change_x < 0:
                    player1.change_x = 0
                if event.key == pygame.K_l and player1.change_x > 0:
                    player1.change_x = 0
                if player1.life>0:
                    if event.key == pygame.K_k:
                        player1.stand(p_list)
                if event.key == pygame.K_a and player2.change_x < 0:
                    player2.change_x = 0
                if event.key == pygame.K_d and player2.change_x > 0:
                    player2.change_x = 0
                if player2.life>0:
                    if event.key == pygame.K_s:
                        player2.stand(p_list)
                if event.key == pygame.K_LESS:
                    if type(player2.currWeapon).__name__=="lazerRifle":
                        player2.currWeapon.release(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list)
                if event.key == pygame.K_m:
                    if type(player1.currWeapon).__name__=="lazerRifle":
                        player1.currWeapon.release(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list)
        blink_blue,blink_red=bulletCollisions(blink_red,blink_blue)
        collisions()
        if player1.life>0 and player2.life>0:
            screen.fill(BGGREY)
        else: screen.fill(DARKGREY)
        try:
            player1_wins,player2_wins,player1_life,player2_life,player2_clip,player1_clip = GUIUpdates()
        except:
            player1_wins,player2_wins = GUIUpdates()
        all_sprites.update()
        player1.movement_and_collision(screen,p_list,player1,player2,player1_life,player2_life,guns_allowed,size)
        player2.movement_and_collision(screen,p_list,player1,player2,player1_life,player2_life,guns_allowed,size)
        if type(player2).__name__=="AIplayer":player2.AI_LOGIC(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list,size)
        all_sprites.draw(screen)
        player_list.draw(screen)
        screen.blit(player1_wins, ((size[0]/2)+50,size[1]-19))
        screen.blit(player2_wins, ((size[0]/2)-50,size[1]-19))
        for i in grenade_list:
            i.grenadePhysics(p_list,screen,all_sprites,player_list,exploding_grenades_list)
        for i in draw_list:
            i.update(screen)
        if len(respawn_list)>0:
            for j in respawn_list:
                if int(j.respawn_timer)>0:
                    j.respawn_timer -= 1
                else:
                    if type(j).__name__=="healBlock":
                        heal_list.add(j)
                    if type(j).__name__=="weaponBox":
                        weapon_box_list.add(j)
                    all_sprites.add(j)
                    j.respawn_timer=j.respawn_time*60
                    respawn_list.remove(j)
        if player1.life<=0:
            player1.life = 0
            q = font.render("Royal wins, wanna play again bruh?",1,RBLUE)
            screen.blit(q,((size[0]/2)-(q.get_width()/2),size[1]/3))
            if not round_end:
                player2.score+=1
            round_end=True
        if player2.life<=0:
            player2.life = 0
            q = font.render("Ruby wins, wanna play again bruh?",1,MRED)
            screen.blit(q,((size[0]/2)-(q.get_width()/2),size[1]/3))
            if not round_end:
                player1.score+=1
            round_end=True
        if not player1.life==0 or not player2.life==0:
            if not done:
                if blink_red > 0:
                    pygame.draw.rect(screen, MRED, [0,0,size[0],size[1]])
                    blink_red-=1
                if blink_blue > 0:
                    pygame.draw.rect(screen, RBLUE, [0,0,size[0],size[1]])
                    blink_blue-=1
        pygame.display.flip()
        if quit_timer<=0:
            done=True
        try:
            if slowmo or player2.life<=0 or player1.life<=0:
                clock.tick(20)
            else:
                clock.tick(60)
        except:clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
