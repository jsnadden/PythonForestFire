import pygame
import sys
import argparse
from Graph import *
from ForestFire import *

# read automaton parameters from command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--size", type=int, default=10, help="Specify automaton grid size", metavar="[value]")
parser.add_argument("-p", "--growth", type=float, default=0.1, help="Specify tree spawn rate", metavar="[value]")
parser.add_argument("-f", "--burn", type=float, default=0.001, help="Specify spontaneous ignition rate", metavar="[value]")
parser.add_argument("-r", "--rate", type=float, default=10, help="Specify automaton update rate (steps per second)", metavar="[value]")
args = parser.parse_args()
GRID_SIZE = min(args.size,800)
GROWTH_RATE = args.growth
IGNITION_RATE = args.burn
STEP_RATE = args.rate

# warn requested model size too large
if args.size > 800:
	print(f"(truncated to maximum allowed size)")

grid = Grid(GRID_SIZE, GRID_SIZE)
model = ForestFireModel(graph = grid, growthRate = GROWTH_RATE, ignitionRate = IGNITION_RATE)

# display parameters
WINDOW_WIDTH = WINDOW_HEIGHT = 800
CELL_SIZE = WINDOW_HEIGHT / GRID_SIZE
colours = { Status.empty : (139, 119, 101), Status.tree : (34, 139, 34), Status.burning : (255, 85, 0) }

# initialise pygame window (handles visualisation and timing)
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f"Forest fire model ({GRID_SIZE}x{GRID_SIZE} grid, p={GROWTH_RATE}, f={IGNITION_RATE})")
clock = pygame.time.Clock()

# main loop
while True:
	# poll/handle window events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	# draw current automaton state
	for y in range(GRID_SIZE):
		for x in range(GRID_SIZE):
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			colour = colours[model.state[(x,y)]]
			pygame.draw.rect(screen, colour, rect)

	# update automaton
	model.Step()

	# swap display buffers and wait for next frame
	pygame.display.flip()
	dt = clock.tick(STEP_RATE)
	#print(f"dt={dt}")