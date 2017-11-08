import random
import pygame

def createWindow():

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("LIXOR")

#============= Default Values =============#

	done = False

	loc_x = int(PLAY_AREA_WIDTH/2)
	loc_y = int(PLAY_AREA_HEIGHT/2)

	food_loc = None
	health = None

	moving = 0

	time_passed = 0.0

	score_num = 0

#============= Main Loop =============#

	while not done:

		grid = createGrid(screen)	

		x = grid[loc_x][0]*CELL_SIZE+3 #Locations of person
		y = grid[loc_y][1]*CELL_SIZE+3# Default is center - this is the spawn

		if not food_loc:
			food_loc = spawnFood(screen) #Create and return food location
			drawFood(screen, food_loc)

		person_loc = movePerson(screen, x, y, food_loc) #Orig. person spawn	

		if food_loc == person_loc: #If person loc and food loc are equal
			screen.fill(WHITE)
			food_loc = spawnFood(screen) #Create new food loc
			movePerson(screen, x, y, food_loc) #Draw the person again in the same spot
			time_passed = 0.0 #Reset food meter if food is eaten
			
			score_num += FOOD_SCORE #Increase score each time food is eaten
		
		updateScore(screen, score_num)

		time_passed += FOOD_EAT_SPEED #Higher number = faster health depreciation
		health = updateHealth(screen, time_passed)

#============= EVENT HANDLING =============#

		keys = pygame.key.get_pressed()

		for event in pygame.event.get(): #Event listener
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				done = True

			if keys[pygame.K_LEFT]:
				if loc_x >= CELL_SIZE:	#Set wall - if in last cell to left, do not move left any more
					loc_x -= CELL_SIZE
			elif keys[pygame.K_RIGHT]:
				if loc_x <= PLAY_AREA_WIDTH-CELL_SIZE: #Wall right 
					loc_x += CELL_SIZE
			elif keys[pygame.K_UP]: #Wall up
				if loc_y % CELL_SIZE != 0:
					loc_y -= 1
			elif keys[pygame.K_DOWN]: #Wall down
				if (loc_y+1) % CELL_SIZE != 0:
					loc_y += 1


def createGrid(screen):

	grid = []

	rows = int(PLAY_AREA_HEIGHT/CELL_SIZE) #Determine the number of columns and rows in grid
	cols = int(PLAY_AREA_WIDTH/CELL_SIZE) 

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

def movePerson(screen, x, y, food_loc):

	screen.fill(WHITE)
	screen.blit(person_img, (x, y))
	drawFood(screen, food_loc)

	return (x, y)

def spawnFood(screen):

	x = random.randrange(0, PLAY_AREA_WIDTH, CELL_SIZE)+3
	y = random.randrange(0, PLAY_AREA_HEIGHT, CELL_SIZE)+3

	return (x, y)

def drawFood(screen, food_loc):

	screen.blit(food_img, (food_loc))

def updateHealth(screen, time_passed):

	bar_length = 8.0 # Starting value - will decrease over time until food is eaten

	multiplier = bar_length-time_passed

	bar_size = (3, SCREEN_HEIGHT+3-CELL_SIZE, CELL_SIZE*multiplier, CELL_SIZE-5)

	pygame.draw.rect(screen, BLUE, bar_size, 0)

	if time_passed >= bar_length:
		quit()

def updateScore(screen, score_num):

	score_text = FONT.render("Score: ", True, BLUE)
	screen.blit(score_text, (PLAY_AREA_WIDTH-104, PLAY_AREA_HEIGHT)) #Minus 124 to bring text to the Left

	score_num = str(score_num)

	score_amt = FONT.render(score_num, True, BLUE)
	screen.blit(score_amt, (PLAY_AREA_WIDTH-42, PLAY_AREA_HEIGHT))

#===========================================================#
#================== Code Execution begins ==================# 
#===========================================================#

pygame.init()
clock = pygame.time.Clock() #Create game clock
clock.tick(30) #30 fps

#========== CREATE GLOBAL VARIABLES ==========#

SCREEN_WIDTH = 961 #961
SCREEN_HEIGHT = 992 #Width+1 CELL for health, etc. bar

PLAY_AREA_WIDTH = 961
PLAY_AREA_HEIGHT = 961

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CELL_SIZE = 31

FONT = pygame.font.SysFont('Arial', 24) #Size 24 b/c thats the size of images (looks good)

FOOD_EAT_SPEED = 0.002 #Higher number = faster food meter depreciations
FOOD_SCORE = 1

#========== LOAD FILES ==========#

person_img = pygame.image.load('person.png')
food_img = pygame.image.load('food.png')

#========== INITIAL FUNCTION CALL ==========#

screen = createWindow() #Create the main window

quit()

#============== NOTES ================#
#
#	When spawning item to screen, make sure to add 3 to center item
#
#
#
#
#
#
#
#
