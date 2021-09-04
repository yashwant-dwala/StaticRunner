import random
import sys
import time
import pygame
from pygame.locals import *  



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
SKYBLUE = (0, 150, 200)
BLUE = (0, 0, 255)               # set up the colors
SILVER = (192,192,192)
DARKGRAY = (169,169,169)
GRAY = (128,128,128)
LIGHTGRAY= (211,211,211)


# global_variables for the game Setup
Fps=30
ScreenWidth=1080
ScreenHeight=720
pygame.init()
pygame.display.set_caption('STATIC_RUNNER By @yashwant dwala')
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))


Game_Sprites={} # images
Game_Sounds={} # sounds
Ground_Layers =[]


 # Game variables
PlayerX =0
PlayerY =0
stageData = None  # for to - Fro Motion
isGrounded = False
isPlayerMid = False
jump =False
GAME_OVER =False
isCollided =False
idleData = None
jumpheight =0
Player_Total_height =0
Player_Total_width = 0
Total_Page = 10
Current_Page = 1
player_Speed = 0




class Display:
	def GAMEOVER():
		''' GAME OVER'''
		font2=pygame.font.SysFont(None, 68, bold=False, italic=True)
		text1 = font2.render(f"Thank You", True, WHITE,GRAY) 
		# text2 = font2.render('GAME OVER', True, WHITE,GRAY)
		textRect = text1.get_bounding_rect(min_alpha = 10)
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = screen.get_rect().centery -200
		# text2Rect = text2.get_bounding_rect(min_alpha = 10)
		# text2Rect.centerx = screen.get_rect().centerx 
		# text2Rect.centery = screen.get_rect().centery -160
		screen.blit(text1, textRect)
		# screen.blit(text2, text2Rect)

	def Loading():
		i=0
		Game_Sounds['intro'].play()
		while True:
			if i>=100:
				return
			i+=random.randrange(1,10)
			font2=pygame.font.SysFont(None, 68, bold=False, italic=True)                # set up fonts
			text1 = font2.render('STATIC RUNNER', True, WHITE,GREEN) 
			textRect = text1.get_bounding_rect(min_alpha = 10)
			textRect.centerx = screen.get_rect().centerx             # set up the text
			textRect.centery = screen.get_rect().centery

			skip_task_font=pygame.font.SysFont(None,18,bold=False,italic=False)
			Skip_text=skip_task_font.render("( Press 'TAB' to SKIP )",False,BLACK,GREEN)
			S_T_rect=Skip_text.get_bounding_rect(min_alpha=10)
			S_T_rect.centerx = 445
			S_T_rect.centery = 10

			loading_task_font=pygame.font.SysFont(None, 30,bold=True,italic=False)
			if i<101:
				loading_text=loading_task_font.render(f"Loading...({i}%)",False,BLACK,GREEN)
			L_rect=Skip_text.get_bounding_rect(min_alpha=10)
			L_rect.x = 20
			L_rect.centery = 360

			time.sleep(0.3)
			screen.fill(GREEN)
			pygame.draw.polygon(screen, SILVER, ((250,10), (200, 40), (200, 140), (240, 140), (240, 160),  (220,160),(220,170),(280,170),(280,160),(260,160),(260,140),(300,140),(300,40)))
			pygame.draw.polygon(screen, DARKGRAY, ((250,20),(220, 40), (220, 140), (240, 140), (240, 160),  (220,160),(220,170),(280,170),(280,160),(260,160),(260,140),(280,140),(280,40)))
			pygame.draw.polygon(screen, BLACK, ((250, 20),(240, 140),(240, 160),(220,160),(220,170),(280,170),(280,160),(260,160),(260,140)))
			pygame.draw.line(screen,BLACK,(250,170),(250,190),20)
			pygame.draw.line(screen, WHITE, (20, 380), (int(f"{i*4+50}"), 380), 6)
			pygame.draw.line(screen, BLACK, (20, 380), (int(f"{i*4+50}"), 380), 4)
			pygame.draw.line(screen,BLACK,(160,230),(340,230),10)

			pygame.draw.ellipse(screen, BLACK, (210, 210, 80, 30),15)
			pygame.draw.circle(screen, BLACK, (250, 200), 40, 20)
			
			screen.blit(text1, textRect)
			screen.blit(Skip_text, S_T_rect)
			screen.blit(loading_text, L_rect)
			pygame.display.update()	
			fpsclock.tick(Fps)	
			for event in pygame.event.get():
				if event.type==KEYDOWN and event.key==K_TAB:
					Game_Sounds['intro'].stop()
					Game_Sounds['tabs'].play()
					return

				elif event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
					pygame.QUIT
					sys.exit()

	def welcomeScreen():
		BaseY = ScreenHeight - Game_Sprites['Base'].get_height()
		while True:
			for event in pygame.event.get():
				if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
					pygame.quit
					sys.exit()
				if event.type==KEYDOWN and event.key==K_TAB:
					return
					
				else:
						screen.blit(Game_Sprites['Background'],(-100,-120))
						screen.blit(Game_Sprites['Base'],(-100,BaseY))
						screen.blit(Game_Sprites['msg'],(100,160))
						pygame.display.update()
						fpsclock.tick(Fps)

	def Cliff_End():
		basey=ScreenHeight-Game_Sprites['base'].get_height()

		offset =Game_Sprites['grass'].get_width()
		xitem =[0,basey-Game_Sprites['grass'].get_height()-10,3*offset]
		physics.AddToGroundLayers(xitem)
		
		screen.blit(Game_Sprites['base'],(0,basey))
		screen.blit(Game_Sprites['rock'],(0,ScreenHeight-Game_Sprites['base'].get_height()-Game_Sprites['rock'].get_height()))
		screen.blit(Game_Sprites['rock'],(Game_Sprites['rock'].get_width(),ScreenHeight-Game_Sprites['base'].get_height()-Game_Sprites['rock'].get_height()))
		screen.blit(Game_Sprites['rock'],(Game_Sprites['rock'].get_width()*2,ScreenHeight-Game_Sprites['base'].get_height()-Game_Sprites['rock'].get_height()))
		screen.blit(Game_Sprites['grass'],(0,ScreenHeight-Game_Sprites['base'].get_height()-Game_Sprites['rock'].get_height()))
		screen.blit(Game_Sprites['grass'],(Game_Sprites['rock'].get_width(),ScreenHeight-Game_Sprites['base'].get_height()-Game_Sprites['rock'].get_height()))
		screen.blit(Game_Sprites['grass'],(Game_Sprites['rock'].get_width()*2,ScreenHeight-Game_Sprites['base'].get_height()-Game_Sprites['rock'].get_height()))

	def FullBase():
		global ScreenHeight
		offset =Game_Sprites['Base'].get_width()
		basey = ScreenHeight - Game_Sprites['Base'].get_height()
		xitem = [-100,basey + 10,offset]
		physics.AddToGroundLayers(xitem)
		screen.blit(Game_Sprites['Base'], (-100,basey))

	def Stage(page,dataX):
		global Ground_Layers,stageData,player_Speed
		Ground_Layers = []
		offset =0
		pageNext = page+1
		pagePrev = page-1
		
		if page == 1 or pagePrev == page:
			offset =1
			font2=pygame.font.SysFont(None, 68, bold=False, italic=True)
			text1 = font2.render(f"START..", True, WHITE) 
			textRect = text1.get_bounding_rect(min_alpha = 10)
			textRect.centerx = screen.get_rect().centerx
			textRect.centery = screen.get_rect().centery -200

			screen.blit(Game_Sprites['Background'],(-100,-120))
			Player.Display_Player_Profile()
			screen.blit(text1, textRect)
			Hurdle.Pipe(500, 400, "green")
			Display.FullBase()		
		
		if page ==2 or pageNext == page or pagePrev == page:
			offset =2
			screen.blit(Game_Sprites['Background'],(-100,-120))
			Player.Display_Player_Profile()
			Hurdle.CompleteBlockTile(600,500,2)
			Hurdle.RockTile(300,200,2)
			Hurdle.Pipe(200, 500, "blue")
			Display.Cliff_End()
		
		if page ==3 or pageNext == page or pagePrev == page:
			offset = 3
			screen.blit(Game_Sprites['Background'],(-100,-120))
			Player.Display_Player_Profile()
			Display.Cliff_End()
			Hurdle.CompleteBlockTile(700,500,1)
		
		if page ==4 or pageNext == page or pagePrev == page:
			offset =4
			screen.blit(Game_Sprites['Background'],(-100,-120))
			Player.Display_Player_Profile()
			Display.FullBase()
			if dataX == None:
				dataX = physics.To_Fro_Motion(50,300, False, 300)
				Hurdle.CompleteBlockTile(int(dataX['x']),500,2)
			else:
				dataX = physics.To_Fro_Motion(int(dataX['x']),300,bool(dataX['forward']),300)
				Hurdle.CompleteBlockTile(int(dataX['x']),500,2)
			return dataX
		
		else:
			pass
			# Display.GAMEOVER()


class Player:

	def Display_Player(playerX,playerY,facing_right):
		global idle,Player_Total_height,Player_Total_width,player_Speed,idleData,isGrounded
		chestx = playerX
		chesty = playerY
		legy = playerY + Game_Sprites['player_chest'].get_height() - 10
		if facing_right:
			legx = playerX + 10
			if player_Speed ==0 and isGrounded:
				if idleData ==None:
					idleData = physics.To_Fro_Motion(chesty, playerY+2, None, 2)
					chesty = idleData['x']
				else:
					idleData = physics.To_Fro_Motion(idleData['x'], playerY+2, idleData['forward'], 2)
					chesty = idleData['x']
			else:
				chesty = playerY

			screen.blit(pygame.transform.scale(Game_Sprites['player_chest'], (75,70)),(chestx,chesty))
			screen.blit(pygame.transform.scale(Game_Sprites['player_leg'], (75,80)),(legx,legy))
		else:
			legx = playerX - 10
			if player_Speed ==0 and isGrounded:
				if idleData ==None:
					idleData = physics.To_Fro_Motion(chesty, playerY+2, None, 2)
					chesty = idleData['x']
				else:
					idleData = physics.To_Fro_Motion(idleData['x'], playerY+2, idleData['forward'], 2)
					chesty = idleData['x']

			chest = pygame.transform.flip(Game_Sprites['player_chest'], True, False)
			leg = pygame.transform.flip(Game_Sprites['player_leg'], True, False)
			screen.blit(pygame.transform.scale(chest, (75,70)),(chestx,chesty))
			screen.blit(pygame.transform.scale(leg, (75,80)),(legx,legy))
		pygame.display.update()
		fpsclock.tick(Fps)

	def Display_Player_Profile():
		pygame.draw.line(screen, WHITE, (30, 34), (200, 34), 15)
		pygame.draw.line(screen, RED, (30, 50), (250, 50), 20)
		pygame.draw.circle(screen, GRAY, (30, 30), 33, 0)
		screen.blit(Game_Sprites['player_Profile'],(5,5))


class physics:
	def linearCollision():
		global Ground_Layers,PlayerX,PlayerY,Player_Total_width,Player_Total_height,isCollided
		for layer in Ground_Layers:
			if len(layer) == 4:
				if (PlayerX+Player_Total_width >= int(layer[0]) and PlayerX <= int(layer[0])+int(layer[2])):
					if PlayerY + int(Player_Total_height/3)  >= int(layer[1]):
						if PlayerY + Player_Total_height <= int(layer[1])+int(layer[3]):
							if not isCollided:
								Game_Sounds['damage'].play()
							isCollided=True
							break
			else:
				isCollided=False

	def Gravity():
		canStand =False
		gravity = 20
		global PlayerY,isGrounded,Player_Total_height,Ground_Layers,Player_Total_width
		Player_Total_height = Game_Sprites['Players'][0].get_height()
		Player_Total_width = Game_Sprites['Players'][0].get_width()
		player_mid = int(Game_Sprites['Players'][0].get_width()/2)

		for layer in Ground_Layers:
			if (PlayerX+player_mid >= int(layer[0]) and PlayerX+player_mid <= int(layer[0])+int(layer[2])) and PlayerY + Player_Total_height <= int(layer[1]+10) and PlayerY + Player_Total_height > int(layer[1])-10:
				canStand =True
				if not isGrounded:
					Game_Sounds['hit'].play()
					isGrounded =True

		if not jump and not canStand:
			isGrounded = False
			PlayerY += gravity			
		
	def Jump():
		global PlayerY,isGrounded,jump,jumpheight
		force =-20
		MaxJumpHeight = int(-ScreenHeight/6)
		if jump and PlayerY > 0 and jumpheight>=MaxJumpHeight: 
			PlayerY += jumpheight
		else:
			jumpheight=0
			jump = False
			return

	def To_Fro_Motion(coordinate,about,forward,rangeOfMotion):
		if forward == None:
			forward = True
		speed = 2
		X = coordinate
		f_motion = forward
		min = about - rangeOfMotion
		max = about + rangeOfMotion
		if f_motion:
			if X < max:
				if X < min:
					X = min 
				X +=speed
				return {"x":X,"forward":True}
			elif X>=max:
				f_motion=False
				return {"x":X,"forward":False}
		else:
			if X > min:
				if X > max:
					X = max 
				X -= speed
				return {"x":X,"forward":False}
			elif X<=min:
				f_motion=True
				return {"x":X,"forward":True}

	def AddToGroundLayers(itemx):
		match =False
		global Ground_Layers
		if Ground_Layers == None: 
			Ground_Layers.append(itemx)
		else:
			for item in Ground_Layers:
				if item == itemx:
					match =True
			if not match:
				 Ground_Layers.append(itemx)

	def Relative_motion(xCoord,yCoord):
		global PlayerY,PlayerX,player_Speed
		if player_Speed >0 or player_Speed <0:
			xCoord = xCoord-PlayerX
			yCoord = yCoord-PlayerY 
		return [xCoord,yCoord]  # FAALTU HAI


class Extra:
	def getRandomObstacles():
		"""   GENERATES RANDOM PIPES    """
		pipeheight=Game_Sprites['pipe'].get_height()
		# offset=30+ScreenHeight/3
		offset=(ScreenHeight/3)*2 
		pipey=random.randrange(int(offset),ScreenHeight-100)
		pipex=ScreenWidth+10
		pipe=[{'x':pipex,'y':pipey}] 

		return pipe   

	def Move_and_Display_Pipe():
		newpipe1=getRandomObstacles()
		newpipe2=getRandomObstacles()
		lowerpipes=[ {'x':ScreenWidth+200,'y':newpipe1[0]['y'] },{'x':ScreenWidth+200+(ScreenWidth/2),'y':newpipe2[0]['y']}]
		
		pipeVel =-4

		for  lowerpipe in lowerpipes:
			lowerpipe['x'] += pipeVel

		if 0< lowerpipes[0]['x'] <5:
			newpipe=getRandomPipe()
			lowerpipes.append(newpipe)

		if lowerpipes[0]['x'] < -Game_Sprites['pipe'].get_width():
			lowerpipes.pop(0)

		for lp in lowerpipes:
			screen.blit(Game_Sprites['pipe'],(lp['x'],lp['y']))


class Hurdle:
	def CompleteBlockTile(x,y,no_of_tile):
		offset =Game_Sprites['rock'].get_width()
		xitem =[x,y,no_of_tile*offset]        # use [] only else order will be incorrect
		physics.AddToGroundLayers(xitem)
		for n in range(no_of_tile):
			screen.blit(Game_Sprites['rock'], (x+n*offset,y))
			screen.blit(Game_Sprites['grass'],(x+n*offset,y))
				
	def RockTile(x,y,no_of_tile):
  		offset =Game_Sprites['rock'].get_width()
  		xitem =[x,y,no_of_tile*offset]
  		physics.AddToGroundLayers(xitem)
  		for n in range(no_of_tile):
	  		screen.blit(Game_Sprites['rock'], (x+n*offset,y))

	def Pipe(x,y,color):
	 	global Ground_Layers
	 	width =100
	 	height = 300
	 	xitem = [x,y,width,height]
	 	Ground_Layers.append(xitem)
	 	if color == "green":
	 		screen.blit(pygame.transform.scale(Game_Sprites['pipe'], (width,height)), (x,y))
	 	else:
	 		screen.blit(pygame.transform.scale(Game_Sprites['pipe2'], (width,height)), (x,y))



def makePlayerParent(moving_Coord,static_Coord):
	global PlayerX,PlayerY,Player_Total_height,Ground_Layers
	platform_size =0
	for l in Ground_Layers:
		if int(l[0]) == moving_Coord:
			platform_size = int(l[2])
	if PlayerX >=moving_Coord and PlayerX <= moving_Coord + platform_size and PlayerY + Player_Total_height <= static_Coord+10 and PlayerY + Player_Total_height > static_Coord-10:
		print("Climbed")
		offset = moving_Coord - PlayerX
		PlayerX = moving_Coord + offset





def main_game():
	global PlayerY,isGrounded,PlayerX,jump,jumpheight,Current_Page,GAME_OVER,player_Speed,Player_Total_height,Player_Total_width,idle,isPlayerMid
	Fps=30

	BaseY = ScreenHeight - Game_Sprites['Base'].get_height()

	jumptime =0
	playerMaxVelY = -ScreenHeight/4
	playerVelY = playerMaxVelY
	playerMaxVelY=10
	playerJumped=False 
	facing_right=True
	Bird_right = True
	canRun = True
	Data = None
	Crr_Point = 0 
	while True:
		for event in pygame.event.get():
			if event.type==KEYDOWN and (event.key==K_SPACE) and isGrounded:
				Game_Sounds['jump'].play()
				isGrounded =False
				jump =True
				playerJumped=True
			# if event.type==KEYDOWN and (event.key==K_SPACE) and playerJumped and not isGrounded:
			# 	jumptime =0
			# 	jumpheight =0
			# 	jump = True
			# 	playerJumped=False

			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				pygame.quit
				sys.exit()

			elif event.type==KEYDOWN and (event.key==K_TAB):
				Game_Sounds['back_music'].stop()
				Game_Sounds['tabs'].play()
				return

			elif event.type==KEYDOWN and (event.key==K_LEFT):
				player_Speed = -20
				facing_right=False
			elif event.type==KEYDOWN and (event.key==K_RIGHT):
				facing_right=True
				player_Speed = 20
			elif event.type == KEYUP and ( event.key == K_LEFT or event.key == K_RIGHT):
				player_Speed = 0


		if jump:
			if jumptime < 5:
				jumptime += 1
				jumpheight += -20
			else:
				jump = False
			physics.Jump()
		else:
			jumptime =0
			jumpheight =0
			physics.Gravity()

		physics.linearCollision()
		if not isCollided : # and not isPlayerMid  For  parallax effect
			PlayerX += player_Speed
		elif isCollided and facing_right:
			PlayerX +=-30
			if player_Speed <= 0:
				PlayerX += player_Speed
		elif isCollided and not facing_right:
			PlayerX +=30
			if player_Speed >=0:
				PlayerX += player_Speed

		
		if PlayerX >= ScreenWidth - Player_Total_width and Current_Page <= Total_Page:
			PlayerX =0	
			Current_Page +=1

		# #  For Parallelax effect
		# if player_Speed >0 and PlayerX >= int(ScreenWidth/2):
		# 	isPlayerMid = True
		# 	Current_Page +=1
		# if player_Speed <0 and PlayerX + Player_Total_width <= int(ScreenWidth/2):
		# 	isPlayerMid = True
		# 	Current_Page -=1

		if PlayerX + Player_Total_width <= 0 and Current_Page >1:
			PlayerX = ScreenWidth - Player_Total_width	
			Current_Page -=1
				
		if PlayerY + Player_Total_height >= ScreenHeight  or Current_Page == Total_Page:
			if not GAME_OVER:
				Game_Sounds['back_music'].stop()
				Game_Sounds['damage'].play()
				Game_Sounds['gameover'].play()
			GAME_OVER =True

		Display.Stage(Current_Page,Data)
		if Current_Page > 1:
			if Data ==None:
				Data = physics.To_Fro_Motion(PlayerX, 300,None,200)
				if bool(Data['forward']):
					screen.blit(Game_Sprites['Birds'][0],(int(Data['x']),120))   
				else:
					screen.blit(Game_Sprites['Birds'][1],(int(Data['x']),120))
			else:
				Data = physics.To_Fro_Motion(int(Data['x']), 300,bool(Data['forward']),200)
				if bool(Data['forward']):
					screen.blit(Game_Sprites['Birds'][0],(int(Data['x']),120))
				else:
					screen.blit(Game_Sprites['Birds'][1],(int(Data['x']),120))    # bird display

		if GAME_OVER:
			Display.GAMEOVER()

		Player.Display_Player(PlayerX,PlayerY,facing_right)
		pygame.display.update()
		fpsclock.tick(Fps)
		
						
	


if __name__ == '__main__':
	pygame.init()  # initializes all pygame modules
	fpsclock=pygame.time.Clock()  # control the rendring of max fps frames	
	Game_Sprites['numbers']=((pygame.image.load('Sprites/0.png').convert_alpha()),
		(pygame.image.load('Sprites/1.png').convert_alpha()),
		(pygame.image.load('Sprites/2.png').convert_alpha()),
		(pygame.image.load('Sprites/3.png').convert_alpha()),
		(pygame.image.load('Sprites/4.png').convert_alpha()),
		(pygame.image.load('Sprites/5.png').convert_alpha()),
		(pygame.image.load('Sprites/6.png').convert_alpha()),
		(pygame.image.load('Sprites/7.png').convert_alpha()),
		(pygame.image.load('Sprites/8.png').convert_alpha()),
		(pygame.image.load('Sprites/9.png').convert_alpha()),
		)

	Game_Sprites['Players']=(pygame.image.load("Sprites/Player 75-150.png").convert_alpha(),
		pygame.transform.flip(pygame.image.load("Sprites/Player 75-150.png").convert_alpha(), True, False),
		)
	Game_Sprites['Birds']=(pygame.image.load("Sprites/bird.png").convert_alpha(),
		pygame.transform.flip(pygame.image.load("Sprites/bird.png").convert_alpha(), True, False),
		)
	Game_Sprites['player_Profile']=pygame.image.load("Sprites/LifeProfile 50-50.png").convert_alpha()
	Game_Sprites['player_chest']=pygame.image.load("Sprites/chest.png").convert_alpha()
	Game_Sprites['player_leg']=pygame.image.load("Sprites/leg pixel.png").convert_alpha()
	Game_Sprites['Background']=pygame.image.load('Sprites/Background 1280-1080.png').convert_alpha()
	Game_Sprites['base']=pygame.image.load('Sprites/Base 500-30.png').convert_alpha()
	Game_Sprites['Base']=pygame.image.load('Sprites/CompleteBase 1280-100.png').convert_alpha()
	Game_Sprites['msg']=pygame.image.load('Sprites/msg.png').convert_alpha()
	Game_Sprites['rock']=pygame.image.load('Sprites/RockTile 200-70.png').convert_alpha()
	Game_Sprites['grass']=pygame.image.load('Sprites/GrassTile 200-50.png').convert_alpha()
	Game_Sprites['topGrass']=pygame.image.load('Sprites/TopGrassTile 200-50.png').convert_alpha()
	Game_Sprites['pipe']=pygame.image.load('Sprites/pipe.png').convert_alpha()
	Game_Sprites['Pipe']=pygame.image.load("Sprites/pipe2 120-300.png").convert_alpha()
	Game_Sprites['pipe2']=pygame.image.load('Sprites/pipe2.png').convert_alpha()

	# pygame.mixer.init()
	Game_Sounds['damage']=pygame.mixer.Sound('Sounds/take hit.wav')
	Game_Sounds['gameover']=pygame.mixer.Sound('Sounds/gameover.wav')
	Game_Sounds['tabs']=pygame.mixer.Sound('Sounds/changing tab.wav')
	Game_Sounds['hit']=(pygame.mixer.Sound('Sounds/quick punch.wav'))
	Game_Sounds['intro']=(pygame.mixer.Sound('Sounds/intro.wav'))
	Game_Sounds['land']=pygame.mixer.Sound('Sounds/jump.wav')
	Game_Sounds['jump']=(pygame.mixer.Sound('Sounds/quick jump.wav'))
	Game_Sounds['back_music']=(pygame.mixer.Sound('Sounds/selection waiting.wav'))

	Display.Loading()
	while(True):
		Display.welcomeScreen() 
		Game_Sounds['tabs'].play()
		Game_Sounds['back_music'].set_volume(0.3)	
		Game_Sounds['back_music'].play(-1)
		main_game()