import pygame
import random

def createGrid(screen):

	screen.fill(WHITE)

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

#	for cell in grid: #Draw the grid
#		area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE) #Syntax (x, y locations, width, height of rect)
#		pygame.draw.rect(screen, BLUE, area, 1)
#
	#pygame.display.flip()

	return (grid, rows, cols)

def createMaze(screen, grid, rows, cols):

	screen.fill(WHITE)

	checked_cells = []
	filled_cells = []

	first_cell = random.randint(0, len(grid))

	checked_cells.append(grid[first_cell]) #add first cell to filled cells
	filled_cells.append(grid[first_cell]) #add first cell to filled cells

	current_cell = first_cell #set the current cell to the first cell
 
	while len(checked_cells) != len(grid): #loop until every cell has been checked

		for event in pygame.event.get(): #Event listener
			if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
				done = True

		next_cell_sel = random.randint(0,3) #select random bordering cell

		if next_cell_sel == 0: #left
			next_cell = current_cell-rows
			if next_cell-1 in range(0, len(grid)) and next_cell+1 in range(0,len(grid)): #CHECK
				if grid[next_cell-1] and grid[next_cell+1] not in filled_cells: #if above and below next cell are empty
					if next_cell-rows+1 in range(0,len(grid)) and next_cell-rows-1 in range(0,len(grid)): #CHECK
						if grid[next_cell-rows+1] and grid[next_cell-rows-1] not in filled_cells: #diagonal check left
							if next_cell+rows+1 in range(0,len(grid)) and next_cell+rows-1 in range(0,len(grid)): #CHECK	
								if grid[next_cell+rows+1] and grid[next_cell+rows-1] not in filled_cells: #diagonal check right	
									filled_cells.append(grid[next_cell])
									checked_cells.append(grid[next_cell])

		elif next_cell_sel == 1: #up
			next_cell = current_cell-1
			if next_cell-rows in range(0,len(grid)) and next_cell+rows in range(0,len(grid)): #CHECK
				if grid[next_cell-rows] and grid[next_cell+rows] not in filled_cells: #if above and below next cell are empty
					if next_cell-rows+1 in range(0,len(grid)) and next_cell-rows-1 in range(0,len(grid)): #CHECK
						if grid[next_cell-rows+1] and grid[next_cell-rows-1] not in filled_cells: #diagonal check left		
							if next_cell+rows+1 in range(0,len(grid)) and next_cell+rows-1 in range(0,len(grid)): #CHECK
								if grid[next_cell+rows+1] and grid[next_cell+rows-1] not in filled_cells: #diagonal check right
									filled_cells.append(grid[next_cell])
									checked_cells.append(grid[next_cell])

		elif next_cell_sel == 2: #right
			next_cell = current_cell+rows
			if next_cell-1 in range(0,len(grid)) and next_cell+1 in range(0,len(grid)):
				if grid[next_cell-1] and grid[next_cell+1] not in filled_cells: #if above and below next cell are empty
					if next_cell+rows+1 in range(0,len(grid)) and next_cell+rows-1 in range(0,len(grid)):					
						if grid[next_cell-rows+1] and grid[next_cell-rows-1] not in filled_cells: #diagonal check left		
							if next_cell+rows+1 in range(0,len(grid)) and next_cell+rows-1 in range(0,len(grid)): #CHECK
								if grid[next_cell+rows+1] and grid[next_cell+rows-1] not in filled_cells: #diagonal check right
									filled_cells.append(grid[next_cell])
									checked_cells.append(grid[next_cell])

		elif next_cell_sel == 3: #down
			next_cell = current_cell+1
			if next_cell-rows in range(0,len(grid)) and next_cell+rows in range(0,len(grid)):
				if grid[next_cell-rows] and grid[next_cell+rows] not in filled_cells: #if above and below next cell are empty
					if next_cell-rows+1 in range(0,len(grid)) and next_cell-rows-1 in range(0,len(grid)):	
						if grid[next_cell-rows+1] and grid[next_cell-rows-1] not in filled_cells: #diagonal check left		
							if next_cell+rows+1 in range(0,len(grid)) and next_cell+rows-1 in range(0,len(grid)): #CHECK
								if grid[next_cell+rows+1] and grid[next_cell+rows-1] not in filled_cells: #diagonal check right
									filled_cells.append(grid[next_cell])
									checked_cells.append(grid[next_cell])
		current_cell = next_cell

	for cell in filled_cells: #Fill cells
		area = (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE) #Syntax (x, y locations, width, height of rect)
		pygame.draw.rect(screen, BLUE, area, 0)
	
		pygame.display.flip()



CELL_SIZE = 31

SCREEN_WIDTH = 1302 #961
SCREEN_HEIGHT = 713 #Width+1 CELL for health, etc. bar

PLAY_AREA_WIDTH = SCREEN_WIDTH
PLAY_AREA_HEIGHT = SCREEN_HEIGHT-CELL_SIZE

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

pygame.init()
clock = pygame.time.Clock() #Create game clock
clock.tick(30) #30 fps

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("LIXOR")

done = False

returns = createGrid(screen)
grid = returns[0]
rows = returns[1]
cols = returns[2]

createMaze(screen, grid, rows, cols)

while not done:

	for event in pygame.event.get(): #Event listener
		if event.type == pygame.QUIT: #If "x" is clicked, program is clsoed
			done = True


