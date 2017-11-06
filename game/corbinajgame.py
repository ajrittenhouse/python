import random
import pygame

def createWindow():

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("LIXOR")

	screen.fill(WHITE)
	pygame.display.update()

	done = False

	loc_x = int(SCREEN_WIDTH/2)
	loc_y = int(SCREEN_HEIGHT/2)

	food_loc = None

	moving = 0

	while not done: #MAIN LOOP - ALL FUNCTION CALLS SHOULD OCCUR HERE	
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

		keys = pygame.key.get_pressed()

		for event in pygame.event.get(): #Event listener
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				done = True

			if keys[pygame.K_LEFT]:
				if loc_x >= CELL_SIZE:	#Set wall - if in last cell to left, do not move left any more
					loc_x -= CELL_SIZE
			elif keys[pygame.K_RIGHT]:
				if loc_x <= SCREEN_WIDTH-CELL_SIZE: #Wall right 
					loc_x += CELL_SIZE
			elif keys[pygame.K_UP]: #Wall up
				if loc_y % CELL_SIZE != 0:
					loc_y -= 1
			elif keys[pygame.K_DOWN]: #Wall down
				if (loc_y+1) % CELL_SIZE != 0:
					loc_y += 1

def createGrid(screen):

	grid = []

	rows = int(SCREEN_HEIGHT/CELL_SIZE) #Determine the number of columns and rows in grid
	cols = int(SCREEN_WIDTH/CELL_SIZE) 

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
		area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
		pygame.draw.rect(screen, WHITE, area, 1)

	pygame.display.flip()

	return grid

def movePerson(screen, x, y, food_loc):

	screen.fill(WHITE)
	screen.blit(person_img, (x, y))
	drawFood(screen, food_loc)

	return (x, y)

def spawnFood(screen):

	x = random.randrange(0, SCREEN_WIDTH, CELL_SIZE)+3
	y = random.randrange(0, SCREEN_HEIGHT, CELL_SIZE)+3

	return (x, y)

def drawFood(screen, food_loc):

	screen.blit(food_img, (food_loc))

#===========================================================#
#===========================================================#
#===========================================================#

pygame.init()
clock = pygame.time.Clock() #Create game clock
clock.tick(30) #30 fps

#========== CREATE GLOBAL VARIABLES ==========#

SCREEN_WIDTH = 961
SCREEN_HEIGHT = 961

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CELL_SIZE = 31

#========== LOAD FILES ==========#

person_img = pygame.image.load('person.png')
food_img = pygame.image.load('food.png')

#========== INITIAL FUNCTION CALL ==========#

screen = createWindow() #Create the main window

quit()

#============== NOTES ==========================#
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