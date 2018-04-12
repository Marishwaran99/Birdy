import pygame,random
pygame.init()
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
white=(255,255,255)
orange=(255,128,0)
black=(0,0,0)
dw=500
dh=500
screen=pygame.display.set_mode([dw,dh])
pygame.display.set_caption("Birdy")
clock=pygame.time.Clock()
#--------------sounds-------------------------------
scoresound=pygame.mixer.Sound('point.wav')
hitsound=pygame.mixer.Sound('hit.wav')
wingsound=pygame.mixer.Sound('wing.wav')
#-------------------images-----------------------------------
bbirdimg=[ pygame.image.load('bb'+str(i)+'.png') for i in range(1,4)]
ybirdimg=[ pygame.image.load('yb'+str(i)+'.png') for i in range(1,4)]
rbirdimg=[ pygame.image.load('rb'+str(i)+'.png') for i in range(1,4)]
bottompipeimg=pygame.image.load('bottompipe.png')
nightbg=pygame.image.load('bg1.png')
daybg=pygame.image.load('bg2.png')
base=pygame.image.load('base.png')
daybgicon=pygame.image.load('daybg.png')
nightbgicon=pygame.image.load('nightbg.png')
bw,bh=nightbg.get_rect().size
basew,baseh=base.get_rect().size
#--------------------------pipe-y positions----------------
pipelist=[[205-40,205+40],[200-40,200+40],[190-40,190+40],[185-40,185+40],[180-40,180+40],[175-40,175+40],
          [170-40,170+40],[165-40,165+40],[160-40,160+40],[155-40,155+40],[145-40,145+40],[140-40,140+40],
          [135-40,135+40],[130-40,130+40],[127-40,127+40],[90-40,90+40],[95-40,95+40],[100-40,100+40],
          [105-40,105+40],[110-40,110+40],[115-40,115+40],[120-40,120+40],[127-40,127+40],
          [300-40,300+40],[335-40,335+40],[330-40,330+40],[325-40,325+40],[320-40,320+40],
          [315-40,315+40],[310-40,310+40],[305-40,305+40],[300-40,300+40],[295-40,295+40],
          [280-40,280+40],[275-40,275+40],[270-40,270+40],[265-40,265+40],[260-40,260+40],
          [255-40,255+40],[250-40,250+40],[245-40,245+40],[240-40,240+40],[235-40,235+40],
          [230-40,230+40],[225-40,225+40],[220-40,220+40],[215-40,215+40],[210-40,210+40]]
class Bird(pygame.sprite.Sprite):
   def __init__(self,game):
      super().__init__()
      self.game=game
      if self.game.choice=='red':
         self.image=rbirdimg[0]
         self.deadimg=pygame.transform.flip(rbirdimg[0],0,1)
      elif self.game.choice=='blue':
         self.image=bbirdimg[0]
         self.deadimg=pygame.transform.flip(bbirdimg[0],0,1)
      elif self.game.choice=='yellow':
         self.image=ybirdimg[0]
         self.deadimg=pygame.transform.flip(ybirdimg[0],0,1)
      self.rect=self.image.get_rect()
      self.rect.x=200
      self.rect.y=250
      self.vy=0
      self.flycount=0
      self.hit=0
   def update(self):
      self.vy=2
      keys=pygame.key.get_pressed()
      if not self.hit:
         if keys[pygame.K_SPACE]:
            self.vy=-2
            wingsound.play()
            if self.flycount+1<15:
               if self.game.choice=='red':
                  self.image=rbirdimg[self.flycount//5]
               elif self.game.choice=='blue':
                  self.image=bbirdimg[self.flycount//5]
               elif self.game.choice=='yellow':
                  self.image=ybirdimg[self.flycount//5]
               self.flycount+=1
            else:
               self.flycount=0
      self.rect.y+=self.vy
      hits=pygame.sprite.spritecollideany(self,self.game.pipesprites,0)
      if hits:
         self.game.gameover=1
         self.vy=10
         self.rect.y+=self.vy
         for tpipe in self.game.toppipes:
            tpipe.vx=0
         for bpipe in self.game.bottompipes:
            bpipe.vx=0
         self.image=self.deadimg           
         if self.rect.bottom>=dh-baseh/2+8:
            hitsound.play()
            self.rect.bottom=dh-baseh/2+8
            self.game.over()
         self.hit=1

      if self.rect.bottom>=dh-baseh/2:
         self.rect.bottom=dh-baseh/2         
      if self.rect.top<=0:
         self.rect.top=0
class Toppipe(pygame.sprite.Sprite):
   def __init__(self,x,y,game):
      super().__init__()
      self.game=game
      self.image=pygame.transform.flip(bottompipeimg,0,1)
      self.rect=self.image.get_rect()
      self.rect.x=x
      self.rect.bottom=y
      self.vx=2
   def update(self):
      if not self.game.gameover:
         self.rect.x-=self.vx
class Bottompipe(pygame.sprite.Sprite):
   def __init__(self,x,y,game):
      super().__init__()
      self.game=game
      self.image=bottompipeimg
      self.rect=self.image.get_rect()
      self.rect.x=x
      self.rect.y=y
      self.vx=2
   def update(self):
      if not self.game.gameover:
         self.rect.x-=self.vx
class Game:
   def __init__(self):
      self.bg=daybg
      self.bgx=0
      self.bgx1=bw
      self.basex=0
      self.basex1=basew
      self.gameover=0
      self.x1=500
      self.y1=pipelist[0][0]
      self.x2=500
      self.y2=pipelist[0][1]
      self.score=0
      self.menuselectpos=200
      self.xcharacterselectpos=144
      self.ycharacterselectpos=144
      self.choice='red'
      self.bg=daybg
      self.w=45
      self.h=40
      self.gapsize=50
      self.flycount=0
   def message(self,text,x,y,size,color):
      self.font=pygame.font.SysFont('show card gothic',size)
      msgtxt=self.font.render(text,1,color)
      msgrect=msgtxt.get_rect()
      msgrect.x,msgrect.y=x,y
      screen.blit(msgtxt,(msgrect.x,msgrect.y))
   def pause(self):
      wait =1
      startscreen=0
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
               if event.key==pygame.K_ESCAPE:
                  startscreen=1
                  wait=0
         self.message("Paused",200,dh/3,30,orange)
         self.message("Press  Enter  to  Continue",50,250,30,orange)
         self.message("Press Esacpe to go to menu",40,325,30,orange)
         pygame.display.update()
      if startscreen:
         self.start()
   def menu(self):      
      if self.menuselectpos<=200:
         self.menuselectpos=200
      if self.menuselectpos>=200+75+75:
         self.menuselectpos=200+75+75
      self.message("Start",190,200,40,orange)
      self.message("Select",185,275,40,orange)
      self.message("Help",200,275+75,40,orange)
      pygame.draw.rect(screen,red,(175,self.menuselectpos-20,150,70),2)
   def characterchoose(self):
      wait=True
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYUP:
               if event.key==pygame.K_LEFT:
                   self.xcharacterselectpos-=100
               if event.key==pygame.K_RIGHT:
                   self.xcharacterselectpos+=100
               if event.key==pygame.K_UP:                 
                   self.ycharacterselectpos=144
                   self.xcharacterselectpos=144
                   self.w=45
                   self.h=40
               if event.key==pygame.K_DOWN:
                   self.xcharacterselectpos=150
                   self.ycharacterselectpos=340
                   self.w=100
                   self.h=100
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN and self.xcharacterselectpos==144:
                  self.choice='yellow'
               if event.key==pygame.K_RETURN and self.xcharacterselectpos==144+100:
                  self.choice='blue'
               if event.key==pygame.K_RETURN and self.xcharacterselectpos==144+100+100:
                  self.choice='red'
               if event.key==pygame.K_RETURN and self.ycharacterselectpos==340 and self.xcharacterselectpos==150:
                  self.bg=daybg
               if event.key==pygame.K_RETURN and self.ycharacterselectpos==340 and self.xcharacterselectpos==150+100:
                  self.bg=nightbg
               if event.key==pygame.K_ESCAPE:
                  wait=0
         if self.xcharacterselectpos<=144:
            self.xcharacterselectpos=144
         if self.xcharacterselectpos>=144+100+100:
            self.xcharacterselectpos=144+100+100
         if self.ycharacterselectpos>=150:
            if self.xcharacterselectpos<=150:
               self.xcharacterselectpos=150
            if self.xcharacterselectpos>=150+100:
               self.xcharacterselectpos=250
         screen.fill(white)
         self.message('Press Escape to go back to menu',80,10,20,blue)
         self.message('Choose any character',75,90,30,blue)
         self.message('Choose Day or Night',75,250,30,blue)
         if self.flycount+1<24:
               screen.blit(ybirdimg[self.flycount//8],(150,150))
               screen.blit(bbirdimg[self.flycount//8],(250,150))
               screen.blit(rbirdimg[self.flycount//8],(350,150))
               self.flycount+=1
         else:
               self.flycount=0         
         screen.blit(daybgicon,(150,340))
         screen.blit(nightbgicon,(250,340))
         pygame.draw.rect(screen,blue,(self.xcharacterselectpos,self.ycharacterselectpos,self.w,self.h),4)
         pygame.display.update()
   def helpscreen(self):
      wait=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_ESCAPE:
                  wait=0
         screen.fill(white)
         self.message('Use Space bar to move up',75,100,30,green)
         self.message('Use Enter key to Pause',75,200,30,green)
         pygame.display.update()
   def start(self):
      wait=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYUP:
               if event.key==pygame.K_DOWN:
                   self.menuselectpos+=75
               if event.key==pygame.K_UP:
                   self.menuselectpos-=75            
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN and self.menuselectpos==200:
                  wait=0
               elif event.key==pygame.K_RETURN and self.menuselectpos==200+75:
                  self.characterchoose()
               elif event.key==pygame.K_RETURN and self.menuselectpos==200+75+75:
                  self.helpscreen() 
         self.bgx-=2
         self.bgx1-=2
         if self.bgx<bw*-1:
            self.bgx=bw
         if self.bgx1<bw*-1:
            self.bgx1=bw
         screen.blit(self.bg,(self.bgx,0))
         screen.blit(self.bg,(self.bgx1,0))
         self.message("BIRDY",190,100,40,orange)
         self.menu()
         pygame.display.update()
      self.new()
   def pipegenerate(self):
      self.toppipes=pygame.sprite.Group()
      self.bottompipes=pygame.sprite.Group()
      self.gapsize=random.randint(50,325)
      x=random.randint(500,550)
      y=random.choice(pipelist)
      y1=y[0]
      y2=y[1]
      self.toppipe=Toppipe(x,y1,self)
      self.bottompipe=Bottompipe(x,y2,self)
      self.toppipes.add(self.toppipe)
      self.bottompipes.add(self.bottompipe)
      self.pipesprites.add(self.bottompipe)
      self.pipesprites.add(self.toppipe)
   def new(self):
      self.bgx=0
      self.bgx1=bw
      self.basex=0
      self.basex1=basew
      self.gameover=0
      self.x1=500
      self.y1=pipelist[0][0]
      self.x2=500
      self.y2=pipelist[0][1]
      self.score=0
      self.gameover=0
      self.player_sprite=pygame.sprite.Group()
      self.bird=Bird(self)
      self.pipesprites=pygame.sprite.Group()
      self.toppipes=pygame.sprite.Group()
      self.bottompipes=pygame.sprite.Group()
      self.toppipe=Toppipe(self.x1,self.y1,self)
      self.bottompipe=Bottompipe(self.x2,self.y2,self)
      self.toppipes.add(self.toppipe)
      self.bottompipes.add(self.bottompipe)
      self.pipesprites.add(self.bottompipe)
      self.pipesprites.add(self.toppipe)
      self.player_sprite.add(self.bird)  
   def event(self):
      for event in pygame.event.get():
         if event.type==pygame.QUIT:
            pygame.quit()
            quit()
         if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  self.pause()
   def over(self):
      wait =1
      startscreen=0
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
               if event.key==pygame.K_ESCAPE:
                  startscreen=1
                  wait=0
         self.message("Game  Over",175,dh/3,30,orange)
         self.message("Press  Enter  to  Play  Again",40,250,30,orange)
         self.message("Press Esacpe to go to menu",40,325,30,orange)
         pygame.display.update()
      if startscreen:
         self.start()
      else:
         self.new()
   def update(self):      
      if self.toppipe.rect.x<self.gapsize and self.bottompipe.rect.x<self.gapsize:
         self.pipegenerate()
         if not self.gameover:
            self.score+=1
            wingsound.stop()
            scoresound.play()
      self.player_sprite.update()
      self.pipesprites.update()
   def draw(self):
      if not self.gameover:
         self.bgx-=2
         self.bgx1-=2
         if self.bgx<=bw*-1:
            self.bgx=bw
         if self.bgx1<bw*-1:
            self.bgx1=bw
         self.basex-=2
         self.basex1-=2
         if self.basex<=basew*-1:
            self.basex=basew
         if self.basex1<=basew*-1:
            self.basex1=basew
         screen.blit(self.bg,(self.bgx,0))
         screen.blit(self.bg,(self.bgx1,0))
         self.pipesprites.draw(screen)
         screen.blit(base,(self.basex,dh-baseh/2))
         screen.blit(base,(self.basex1,dh-baseh/2))
         self.player_sprite.draw(screen)
         self.message("Score:"+str(self.score),50,50,30,orange)
      else:
         screen.blit(self.bg,(self.bgx,0))
         screen.blit(self.bg,(self.bgx1,0))
         self.pipesprites.draw(screen)
         screen.blit(base,(self.basex,dh-baseh/2))
         screen.blit(base,(self.basex1,dh-baseh/2))
         self.player_sprite.draw(screen)
         self.message("Score:"+str(self.score),50,50,30,orange)
   def run(self):      
      while 1:
         clock.tick(60)
         self.event()
         self.update()
         self.draw()   
         pygame.display.flip()
g=Game()
while g.run:
   g.start()
   g.new()
   g.run()
