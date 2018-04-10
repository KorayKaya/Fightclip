import pygame
from FCobjects import player

class AIPlayer(player):
    def __init__(self,color,x,y,playerNR,all_sprites,player_list):
        player.__init__(self,color,x,y,playerNR,all_sprites,player_list)
    def AIupdate(player1,player2):
        if player1.rect.y<(self.rect.y+10) or player1.rect.bottom>(self.rect.y+10):
                self.currWeapon.shoot(guns_allowed,player1,player2,GREY,bullet1_list,bullet2_list,all_sprites,screen,p_list)



def main():
    pass

if __name__ == '__main__':
    main()