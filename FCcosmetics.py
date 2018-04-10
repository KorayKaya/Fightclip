import pygame,os

class cosmetic():
    def __init__(self,hat_image,x_offset,y_offset,player,screen,draw_list):
        self.INVISCOL = (63,171,153)
        self.graphics_dir= os.path.dirname(os.path.realpath(__file__))+"\\GRAPHICS\\"
        self.hat_image_right = pygame.image.load(self.graphics_dir+hat_image+".gif").convert()
        self.hat_image_right.set_colorkey(self.INVISCOL)
        self.hat_image_left = pygame.transform.flip(self.hat_image_right,True,False)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.screen = screen
        self.player = player
        draw_list.append(self)
    def update(self,*args):
        if self.player.direction==1:
            self.screen.blit(self.hat_image_right, (self.player.rect.x+self.x_offset,self.player.rect.y+self.y_offset))
        elif self.player.direction==0:
            self.screen.blit(self.hat_image_left, (self.player.rect.right-(self.hat_image_left.get_width()+self.x_offset),self.player.rect.y+self.y_offset))

class sunglasses(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"sunglasses",0,0,player,screen,draw_list)

class goldenFedora(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"goldenFedora",-4,-9,player,screen,draw_list)
class whiteFedora(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"whiteFedora",-5,-11,player,screen,draw_list)
class blondePonytail(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"blondePonytail",-5,-7,player,screen,draw_list)
class crazyHat(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"crazyHat",-14,-89,player,screen,draw_list)
class chairHat(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"chairHat",-19,-19,player,screen,draw_list)
class test(cosmetic):
    def __init__(self,player,screen,draw_list):
        cosmetic.__init__(self,"katana",8,-20,player,screen,draw_list)


def main():
    pass

if __name__ == '__main__':
    main()
