#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame 
from pygame.locals import *
import random # 파이프 길이 랜덤생성을 위한 라이브러리

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Oaia") # 창 타이틀

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# define colors
white = (255, 255, 255)


# 게임 변수들 정의
ground_scroll = 0
scroll_speed = 4
flying = False # 게임시작을 내가 원할 때 할 수 있도록 하기위한 변수 
game_over = False
pipe_gap = 150 # 파이프 사이의 간격 변수
pipe_frequency = 1500 # 단위 : milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


# 이미지 불러오기
bg = pygame.image.load("img/bgKopo.png") # 배경
groung_img = pygame.image.load("img/ground.png") # 땅 
button_img = pygame.image.load('img/restart.png') # 다시하기 버튼


def draw_text(text, font, text_col, x, y): # pygame은 텍스트출력 지원안하므로, 그려야함
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    

def reset_game(): # 게임 restart를 위한 reset 함수
    pipe_group.empty() # 파이프그룹을 비워준다.
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0 # 앞에 선언된 score은 global 변수이기 때문에 여기서 해봤자 영향이 없다.
    # 두개다 전역변수(global)로 해주거나, return score 해줘야 한다.
    return score


class Bird(pygame.sprite.Sprite): # pygame의 sprite 클래스 이용 (update & draw)
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0 # animation speed 조정
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
            
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0 # velocity
        self.clicked = False
        
    def update(self):
        
        if flying == True: # 게임 시작된 후 로직 구현
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768: # 땅 속으로 들어가지 않도록
                self.rect.y += int(self.vel) # float이므로 int로 캐스팅
        
        if game_over == False:
            # jump

            #keystate = pygame.key.get_pressed() # 스페이스바 누를 때
            #if keystate[pygame.K_SPACE] and self.clicked == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: 
                # .mouse.get_pressed는 작은 list를 생성함 -> 좌클릭[0]을 하면 (== 1은 클릭)
                self.clicked = True
                self.vel = -10 # -시 위로, +시 아래로
            if pygame.mouse.get_pressed()[0] == 0: # 마우스 누르고 있는 것 방지
                self.clicked = False


            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird (올라갈 땐 고개위로, 내려갈 땐 고개 아래로)
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2) # 반시계 방향임
        else: 
            self.image = pygame.transform.rotate(self.images[self.index], -90) # 반시계 방향임 (-90이면 앞으로 90도)
            # 땅에 떨어지면 박힙니다...

            
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) # (~, x축, y축)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
            
    def update(self):
        self.rect.x -= scroll_speed # 파이프 이동
        if self.rect.right < 0:
            self.kill() # 메모리를 위해 화면 넘어가면 kill
        
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        
        action = False # Trigger 역할
        
        # get mous position
        pos = pygame.mouse.get_pos() # [0]은 x coordinate, [1]은 y coordinate
        
        # check if mous is over the button
        if self.rect.collidepoint(pos): # 마우스가 버튼위에 있으면
            if pygame.mouse.get_pressed()[0] == 1: # 좌클릭을 하면
                action = True
        
        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
    
    
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy) # 그룹에 추가

# create restart button instance (//는 소수점버리고 정수부분만 구함)
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)


# Game Loop
run = True
while run:
    
    clock.tick(fps)
    
    # draw background
    screen.blit(bg, (0,0)) # 이미지 로딩위한 blit 함수
    
    bird_group.draw(screen) # sprite 안에 builtin된 function 중 하나
    bird_group.update()
    pipe_group.draw(screen)

    
    # draw the ground
    screen.blit(groung_img, (ground_scroll, 768))
    
    
    # check the score 
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right            and pass_pipe == False:
            pass_pipe = True
        # bird는 only one이므로 [0]고정, 왼쪽은 통과, 오른쪽은 아직
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1 # 오른쪽도 통과하면 스코어 + 1점
                pass_pipe = False # 초기화
    
    draw_text(str(score), font, white, int(screen_width / 2), 20) # score 생성
    
    
    # 파이프와 충돌구현
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True # groupcollide 함수 (True, False) 면 앞에 것이 충돌이 delete 됨.
    
    
    # check if bird has hit the ground
    if flappy.rect.bottom >= 768: # hit the ground
        game_over = True
        flying = False
    
    
    if game_over == False and flying == True:
        # generate new pipes        
        time_now = pygame.time.get_ticks() # 현재 시간
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-125, 125) # 랜덤 Number 생성
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
            
            
        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35 :
            ground_scroll = 0 # 땅이 계속 지나가는 것 처럼 보이게
            
        pipe_group.update()
        
    # check for game over and restart
    if game_over == True:
        if button.draw() == True: # 즉, 버튼을 눌렀을 때 return action -> True
            game_over = False
            score = reset_game() # return score (value of 0) 이므로
    
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 종료버튼(X) 누르면 종료
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False: 
            flying = True # 아무 마우스버튼 클릭 시 시작!
            
    pygame.display.update() # 업데이트를 해줘야 위 사항이 적용된다.
            
pygame.quit()

