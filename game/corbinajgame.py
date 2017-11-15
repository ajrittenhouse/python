import random
import pygame
from time import sleep

def createWindow():

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("LIXOR")

#============= Default Values =============#

	done = False

	loc_x = int(PLAY_AREA_WIDTH/2)
	loc_y = int(PLAY_AREA_HEIGHT/2)

	food_loc = None
	boost1_loc = None
	person_loc = None

	health = None

	time_passed = 0.0

	score_num = 0

#============= Main Loop =============#

	while not done:

		grid = createGrid(screen) #Create the grid

		if not food_loc: #Original item spaws
			food_loc = spawnFood(screen) #Create and return food location
			drawFood(screen, food_loc)

		if not boost1_loc:
			boost1_loc = spawnBoost1(screen) #Create and return food location
			drawBoost1(screen, boost1_loc)

		if not person_loc:
			person_loc = spawnPerson(screen)
			drawPerson(screen, person_loc)
		
		x = grid[loc_x][0]*CELL_SIZE+3 #Locations of person
		y = grid[loc_y][1]*CELL_SIZE+3 #Allows to use grid coords instead of pixels
		
		person_loc = (x, y) #initial person location

		movePerson(screen, person_loc, food_loc, boost1_loc) #Orig. person spawn

		if food_loc == person_loc: #If person loc and food loc are equal
			screen.fill(WHITE)
			food_loc = spawnFood(screen) #Create new food loc
			drawPerson(screen, person_loc)
			time_passed = 0.0 #Reset food meter if food is eaten			
			score_num += FOOD_SCORE #Increase score each time food is eaten
			updateScore(screen, score_num)


		if boost1_loc == person_loc: #If person loc and food loc are equal
			screen.fill(WHITE)
			boost1_loc = spawnBoost1(screen)
			drawPerson(screen, person_loc)
			score_num += STAR_SCORE #Increase score each time star is eaten
			updateScore(screen, score_num)

		updateScore(screen, score_num)

		time_passed += FOOD_EAT_SPEED #Higher number = faster health depreciation
		health = updateHealth(screen, time_passed)

#============= EVENT HANDLING =============#

		for event in pygame.event.get(): #Event listener
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				done = True

			if event.type == pygame.KEYDOWN: #Eventually add if conditions for walls
				if event.key == pygame.K_LEFT:
					if 1:	
						loc_x -= CELL_SIZE
				elif event.key == pygame.K_RIGHT:
					if 1:
						loc_x += CELL_SIZE					
				elif event.key == pygame.K_UP:
					if 1:
						loc_y -= 1
				elif event.key == pygame.K_DOWN:
					if 1:
						loc_y += 1

def createGrid(screen):

	grid = []

	rows = int(PLAY_AREA_WIDTH/CELL_SIZE) #Determine the number of columns and rows in grid
	cols = int(PLAY_AREA_HEIGHT/CELL_SIZE) 

	row = 0 #Used for creating cells
	col = 0 

	while row < rows: #Create each cell
		while col < cols:
			cell = (row, col)
			grid.append(cell)
			col += 1
		row += 1
		col = 0

	for cell in grid: #Draw the grid
		area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE) #Syntax (x, y locations, width, height of rect)
		pygame.draw.rect(screen, BLUE, area, 1)

	pygame.display.flip()

	return grid

def spawnPerson(screen):

	x = random.randrange(0, PLAY_AREA_WIDTH, CELL_SIZE)+3
	y = random.randrange(0, PLAY_AREA_HEIGHT, CELL_SIZE)+3

	return (x, y)

def drawPerson(screen, person_loc):

	screen.blit(person_img, (person_loc))

def movePerson(screen, person_loc, food_loc, boost1_loc): #Add all other functions for ddrawing items here
																# So when the person in moved, everything else reappears
	screen.fill(WHITE)

	drawPerson(screen, person_loc)
	drawFood(screen, food_loc)
	drawBoost1(screen, boost1_loc)

def spawnFood(screen):

	x = random.randrange(0, PLAY_AREA_WIDTH, CELL_SIZE)+3 #Could do this and other spawns through grid?
	y = random.randrange(0, PLAY_AREA_HEIGHT, CELL_SIZE)+3 #ie. xy = random.randint(len(grid)) then x = grid[xy][0] y = grid[xy][1]

	return (x, y)

def drawFood(screen, food_loc):

	screen.blit(food_img, (food_loc))

def spawnBoost1(screen):

	x = random.randrange(0, PLAY_AREA_WIDTH, CELL_SIZE)+3
	y = random.randrange(0, PLAY_AREA_HEIGHT, CELL_SIZE)+3

	return (x, y)

def drawBoost1(screen, boost1_loc):

	screen.blit(star_img, (boost1_loc))

def updateHealth(screen, time_passed):

	bar_length = 8.0 # Starting value - will decrease over time until food is eaten

	multiplier = bar_length-time_passed

	outer_bar_size = (3, SCREEN_HEIGHT+3-CELL_SIZE, CELL_SIZE*bar_length, CELL_SIZE-5) #Outer bar - uses bar_len
	bar_size = (3, SCREEN_HEIGHT+3-CELL_SIZE, CELL_SIZE*multiplier, CELL_SIZE-5)

	pygame.draw.rect(screen, BLUE, outer_bar_size, 1)
	pygame.draw.rect(screen, BLUE, bar_size, 0)

	if time_passed >= bar_length:
		gameOver(screen)

def updateScore(screen, score_num):

	score_text = FONT.render("Score: ", True, BLUE)
	screen.blit(score_text, (PLAY_AREA_WIDTH-104, PLAY_AREA_HEIGHT)) #Minus 124 to bring text to the Left

	score_num = str(score_num)

	score_amt = FONT.render(score_num, True, BLUE)
	screen.blit(score_amt, (PLAY_AREA_WIDTH-30, PLAY_AREA_HEIGHT))

def gameOver(screen):

	screen.fill(WHITE)
	gameover_text = FONT.render("GAME OVER!", True, BLUE)
	
	screen.blit(gameover_text, (SCREEN_WIDTH/2+1, SCREEN_HEIGHT/2)) #"Centered", but not really. Needs adjusting to center text

	pygame.display.flip()

	sleep(3)
	
	#mainMenu()
	exit() 

#===========================================================#
#================== Code Execution begins ==================# 
#===========================================================#

pygame.init()
clock = pygame.time.Clock() #Create game clock
clock.tick(30) #30 fps

#========== CREATE GLOBAL VARIABLES ==========#

CELL_SIZE = 31

SCREEN_WIDTH = 1302 #961
SCREEN_HEIGHT = 713 #Width+1 CELL for health, etc. bar

PLAY_AREA_WIDTH = SCREEN_WIDTH
PLAY_AREA_HEIGHT = SCREEN_HEIGHT-CELL_SIZE

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

FONT = pygame.font.SysFont('Arial', 24) #Size 24 b/c thats the size of images (looks good)

FOOD_EAT_SPEED = 0.01 #Higher number = faster food meter depreciations
FOOD_SCORE = 1
STAR_SCORE = 5

#========== LOAD FILES ==========#

person_img = pygame.image.load('person.png')
food_img = pygame.image.load('food.png')
star_img = pygame.image.load('star.png')

#========== INITIAL FUNCTION CALL ==========#

window = createWindow() #Create the main window

quit()

#============== NOTES ================#
#
#	When spawning item to screen, make sure to add 3 to center item
#
#	For walls, maybe check if x,y or person are in grid
#
#
#
#
#
#