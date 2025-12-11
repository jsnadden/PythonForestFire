import sys
import os
import argparse
import csv
import json
import hashlib
from datetime import datetime

import pygame
import numpy as np
import matplotlib.pyplot as plt

from Graph import *
from ForestFire import *

# parse/handle command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--size", type=int, default=10, help="Specify automaton grid size", metavar="[value]")
parser.add_argument("-p", "--growth", type=float, default=0.1, help="Specify tree spawn rate", metavar="[value]")
parser.add_argument("-f", "--burn", type=float, default=0.001, help="Specify spontaneous ignition rate", metavar="[value]")
parser.add_argument("-r", "--rate", type=float, default=10, help="Specify automaton update rate (steps per second)", metavar="[value]")
parser.add_argument("-o", "--stats", action="store_true", help="Enable statistical output on app exit")
args = parser.parse_args()

GROWTH_RATE = args.growth
IGNITION_RATE = args.burn
STEP_RATE = args.rate
GRID_SIZE = min(args.size,800)
if args.size > 800:
	print(f"(truncated to maximum allowed size)")
CELL_COUNT = GRID_SIZE ** 2
PARAMS_DESCRIPTION = f"{GRID_SIZE}x{GRID_SIZE} grid, p={GROWTH_RATE}, f={IGNITION_RATE}"
print(f"Running Drossel–Schwabl forest fire simulation ({PARAMS_DESCRIPTION})")
OUTPUT_STATS = args.stats

# initialise automaton
grid = Grid(GRID_SIZE, GRID_SIZE)
model = ForestFireModel(graph = grid, growthRate = GROWTH_RATE, ignitionRate = IGNITION_RATE)

# initialise statistics
treeDensities = []

# initialise pygame and display parameters
WINDOW_WIDTH = WINDOW_HEIGHT = 800
CELL_SIZE = WINDOW_HEIGHT / GRID_SIZE
colours = { Status.empty : (139, 119, 101), Status.tree : (34, 139, 34), Status.burning : (255, 85, 0) }
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f"Drossel–Schwabl Forest Fire Model ({PARAMS_DESCRIPTION})")
clock = pygame.time.Clock()

# main loop
running = True
while running:
	# poll/handle window events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	if not running:
		break

	# draw current automaton state
	for y in range(GRID_SIZE):
		for x in range(GRID_SIZE):
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			colour = colours[model.CurrentState()[(x,y)]]
			pygame.draw.rect(screen, colour, rect)

	# record tree count
	treeDensities.append(model.TreeCount() / CELL_COUNT)

	# update automaton
	model.Step()

	# swap display buffers and wait for next frame
	pygame.display.flip()
	clock.tick(STEP_RATE)

pygame.quit()

if OUTPUT_STATS:
	# create output directory
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	hashObject = hashlib.md5(PARAMS_DESCRIPTION.encode())
	hashTrunc= hashObject.hexdigest()[:6]
	outputDir = "./output/" + timestamp + "_" + hashTrunc + "/"
	os.makedirs(outputDir, exist_ok=True)

	# output simulation metadata
	metadata = {
		"grid_size" : GRID_SIZE,
		"growth_rate": GROWTH_RATE,
		"ignition_rate" : IGNITION_RATE,
		"generations" : model.StepCount()
	}
	with open(outputDir + "meta.json", "w+") as metafile:
		json.dump(metadata, metafile, indent = 2)

	# output time series data
	columnNames = "tree_density" # NOTE: single string, comma-separated, no spaces
	data = np.column_stack([treeDensities])
	np.savetxt(outputDir + "data.csv", data, delimiter=",", header=columnNames, comments="")

	# plot time series data
	plt.plot(data[:, 0], label="tree density")
	plt.legend()
	plt.show()

