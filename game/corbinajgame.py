import random
import pygame
from time import sleep

def createWindow():

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("Lixor")
	playGame(screen)

#============= Default Values =============#

def playGame(screen):

	done = False

	menu_displayed = False
	restart = False

	loc_x = int(PLAY_AREA_WIDTH/2)
	loc_y = int(PLAY_AREA_HEIGHT/2)

	food_loc = None
	boost1_loc = None
	person_loc = None

	health = None

	time_passed = 0.0

	score_num = 0

#============= Main Loop =============#
	
	returns = createGrid(screen) #Create the grid
	grid = returns[0]
	rows = returns[1]
	cols = returns[2]

	filled_cells = createMaze(grid)

	filled_cells_pix = []

	for cell in filled_cells:
		filled_cells_pix.append((cell[0]*CELL_SIZE+3, cell[1]*CELL_SIZE+3))

	direction = 5

	while not done:

		moved = 0

		drawGrid(screen, grid, filled_cells)

		if not menu_displayed:  
			mainMenu(screen)
			menu_displayed = True

		if not food_loc: #Original item spaws
			food_loc = spawnFood(screen, filled_cells_pix) #Create and return food location
			drawFood(screen, food_loc)

		if not boost1_loc:
			boost1_loc = spawnBoost1(screen, filled_cells_pix) #Create and return food location
			drawBoost1(screen, boost1_loc)

		if not person_loc:
			person_loc = spawnPerson(screen)
			drawPerson(screen, person_loc)
		
		x = grid[loc_x][0]*CELL_SIZE+3 #Locations of person
		y = grid[loc_y][1]*CELL_SIZE+3 #Allows to use grid coords instead of pixels
		
		person_loc = (x, y)

		if person_loc in filled_cells_pix:
			movePerson(screen, person_loc, food_loc, boost1_loc) #Orig. person spawn
			moved = 1

		else:
			if direction == 0:
				loc_x += rows
			if direction == 1:
				loc_x -= rows
			if direction == 2:
				loc_y += 1
			if direction == 3:
				loc_y -= 1

			x = grid[loc_x][0]*CELL_SIZE+3
			y = grid[loc_y][1]*CELL_SIZE+3

		if food_loc == person_loc: #If person loc and food loc are equal
			screen.fill(WHITE)
			food_loc = spawnFood(screen, filled_cells_pix) #Create new food loc
			drawPerson(screen, person_loc)
			time_passed = 0.0 #Reset food meter if food is eaten			
			score_num += FOOD_SCORE #Increase score each time food is eaten
			updateScore(screen, score_num)


		if boost1_loc == person_loc: #If person loc and food loc are equal
			screen.fill(WHITE)
			boost1_loc = spawnBoost1(screen, filled_cells_pix)
			drawPerson(screen, person_loc)
			score_num += STAR_SCORE #Increase score each time star is eaten
			updateScore(screen, score_num)

		updateScore(screen, score_num)

		time_passed += FOOD_EAT_SPEED #Higher number = faster health depreciation
		restart = updateHealth(screen, time_passed, restart)

		if restart == True:
			menu_displayed = False
			break	

#============= EVENT HANDLING =============#
		

		for event in pygame.event.get(): #Event listener
	
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				done = True

			if moved == 1:	
				if event.type == pygame.KEYDOWN: #If key is pressed
					if event.key == pygame.K_LEFT:
						loc_x -= rows
						direction = 0
					elif event.key == pygame.K_RIGHT:
						loc_x += rows
						direction = 1			
					elif event.key == pygame.K_UP:
						loc_y -= 1
						direction = 2
					elif event.key == pygame.K_DOWN:
						loc_y += 1
						direction = 3

def createMaze(grid):

	div = float(CELL_SIZE)/(float(CELL_SIZE)-3)
	filled_cells = random.sample(grid, int(len(grid)/div))

	return filled_cells

def drawMaze(screen, filled_cells): #not used right now

	for cell in filled_cells: #Fill cells
		area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE) #Syntax (x, y locations, width, height of rect)
		pygame.draw.rect(screen, BLUE, area, 0)
	
def mainMenu(screen):


	clicked = None

	screen.fill(GREY)	

	button_text = FONT.render("Welcome to Lixor!", True, BLUE)
	screen.blit(button_text, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/3)) 

	button_text = FONT.render("Click anywhere to begin...", True, BLUE)
	screen.blit(button_text, (SCREEN_WIDTH/2-120, SCREEN_HEIGHT/2)) #"Centered", but not really. Needs adjusting to center text

	pygame.display.flip()

	while not clicked: #mouse_loc:
		for event in pygame.event.get(): #Event listener
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				exit()

			if event.type == pygame.MOUSEBUTTONUP:
				clicked = True
	
	screen.fill(GREY)
	button_text = FONT.render("3", True, BLUE)
	screen.blit(button_text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) #"Centered", but not really. Needs adjusting to center text
	pygame.display.flip()
	sleep(1)


	screen.fill(GREY)
	button_text = FONT.render("2", True, BLUE)
	screen.blit(button_text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) #"Centered", but not really. Needs adjusting to center text	
	pygame.display.flip()
	sleep(1)

	screen.fill(GREY)	
	button_text = FONT.render("1", True, BLUE)
	screen.blit(button_text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) #"Centered", but not really. Needs adjusting to center text
	pygame.display.flip()
	sleep(1)

	return True

def createGrid(screen):

	grid = []

	cols = int(PLAY_AREA_WIDTH/CELL_SIZE) #Determine the number of columns and rows in grid
	rows = int(PLAY_AREA_HEIGHT/CELL_SIZE) 

	row = 0 #Used for creating cells
	col = 0 

	while col < cols: #Create each cell
		while row < rows:
			cell = (col, row)
			grid.append(cell)
			row += 1
		col += 1
		row = 0

	return (grid, rows, cols)

def drawGrid(screen, grid, filled_cells):

	for cell in filled_cells: #grid: #Draw the grid
		area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE) #Syntax (x, y locations, width, height of rect)
		pygame.draw.rect(screen, WHITE, area, 1)

	for cell in grid:
		if cell not in filled_cells:
			area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE) #Syntax (x, y locations, width, height of rect)
			pygame.draw.rect(screen, BLUE, area, 0)

	pygame.display.flip()

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

def spawnFood(screen, filled_cells_pix):

	while True:

		x = random.randrange(0, PLAY_AREA_WIDTH, CELL_SIZE)+3 #Could do this and other spawns through grid?
		y = random.randrange(0, PLAY_AREA_HEIGHT, CELL_SIZE)+3 #ie. xy = random.randint(len(grid)) then x = grid[xy][0] y = grid[xy][1]

		if (x, y) in filled_cells_pix:
			return (x, y)

def drawFood(screen, food_loc):

	screen.blit(food_img, (food_loc))

def spawnBoost1(screen, filled_cells_pix):

	while True:

		x = random.randrange(0, PLAY_AREA_WIDTH, CELL_SIZE)+3
		y = random.randrange(0, PLAY_AREA_HEIGHT, CELL_SIZE)+3

		if (x, y) in filled_cells_pix:
			return (x, y)

def drawBoost1(screen, boost1_loc):

	screen.blit(star_img, (boost1_loc))

def updateHealth(screen, time_passed, restart):

	bar_length = 8.0 # Starting value - will decrease over time until food is eaten

	multiplier = bar_length-time_passed

	outer_bar_size = (3, SCREEN_HEIGHT+3-CELL_SIZE, CELL_SIZE*bar_length, CELL_SIZE-5) #Outer bar - uses bar_len
	bar_size = (3, SCREEN_HEIGHT+3-CELL_SIZE, CELL_SIZE*multiplier, CELL_SIZE-5)

	pygame.draw.rect(screen, BLUE, outer_bar_size, 1)
	pygame.draw.rect(screen, BLUE, bar_size, 0)

	if time_passed >= bar_length:
		screen.fill(WHITE)
		restart = gameOver(screen)

	return restart

def updateScore(screen, score_num):

	score_text = FONT.render("Score: ", True, BLUE)
	screen.blit(score_text, (PLAY_AREA_WIDTH-104, PLAY_AREA_HEIGHT)) #Minus 124 to bring text to the Left

	score_num = str(score_num)

	score_amt = FONT.render(score_num, True, BLUE)
	screen.blit(score_amt, (PLAY_AREA_WIDTH-30, PLAY_AREA_HEIGHT))

def gameOver(screen):

	screen.fill(WHITE)	

	restart_button_size = (SCREEN_WIDTH/2-CELL_SIZE*3, SCREEN_HEIGHT/2, CELL_SIZE*5, CELL_SIZE*2) #x3 and x5 for button rect size
	pygame.draw.rect(screen, BLUE, restart_button_size, 1) #Draw rectangle for button
	restart_button = pygame.Rect(restart_button_size) #Store button object

	restart_text = FONT.render("Restart", True, BLUE)
	screen.blit(restart_text, (SCREEN_WIDTH/2-45, SCREEN_HEIGHT/2+10)) #"Centered", but not really. Needs adjusting to center text

	pygame.display.flip()

	while True: #Pause until mouse
		for event in pygame.event.get(): #Event listener
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				exit()

			if event.type == pygame.MOUSEBUTTONUP:
				mouse_loc = pygame.mouse.get_pos() #Creates tuple of mouse loc on screen (x,y)

				if restart_button.collidepoint(mouse_loc): #Checks if mouse click was in button
					return True

				else:
					return False

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
GREY = (192, 192, 192)

FONT = pygame.font.SysFont('Arial', 24) #Size 24 b/c thats the size of images (looks good)

FOOD_EAT_SPEED = 0.01 #Higher number = faster food meter depreciations
FOOD_SCORE = 1
STAR_SCORE = 5

#========== LOAD FILES ==========#

person_img = pygame.image.load('person.png')
food_img = pygame.image.load('food.png')
star_img = pygame.image.load('star.png')

#========== INITIAL FUNCTION CALL ==========#

while True:

	window = createWindow() #Create the main window

quit()

#============== NOTES ================#
#
#	When spawning item to screen, make sure to add 3 to center item
#
#	For walls, maybe check if x,y or person are in grid
#
#	USE ROWS/COLS not CELL SIZE for mvmt
#
#
#
#