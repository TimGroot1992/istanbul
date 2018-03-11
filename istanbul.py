import sys
import random
import pygame
from pygame.locals import *

def main():
	board = Board(int(sys.argv[1]), 16)
	print("Playing Istanbul with", board.number_of_players, "players!")
	print("")

	tiles = {"great_mosque": [1, 1], "post_office": [1, 2], "fabric_warehouse": [1, 3], "small_mosque": [1, 4], 
		"fruit_warehouse": [2, 1], "police station": [2, 2],"fountain": [2, 3], "spice_warehouse": [2, 4], 
		"black_market": [3, 1], "caravansary": [3, 2], "small_market": [3, 3], "tea_house": [3, 4],
		"sultans_palace": [4, 1], "large_market": [4, 2], "wainwright": [4, 3], "gemstone_dealer": [4, 4]}
	tilelist = [Tiles(tile, tiles.get(tile)) for tile in tiles]
	playerlist = [Players(i, tilelist[6].location) for i in range(0, board.number_of_players)]
	

	for player in playerlist:
		print("Money for", player.name, "is", player.resources.get("lira"), "lira.")
	
	#Initiate fountain for all players
	currenttile = tilelist[6] #Fountain
	for i in range(0, len(playerlist)):
		currenttile.update_players_present(playerlist[i].name, "addition")
		for unit in playerlist[i].units_stack:
			currenttile.update_units_stack(playerlist[i].name, unit)
	
	print("Tile with name", currenttile.name, "has the following players present:", currenttile.players_present, ". The following units are present here:", currenttile.units_stack)
	
	print("player 1 location is", playerlist[0].location)
	playerlist[0].update_location(tilelist[3].location)
	print("player 1 location is now", playerlist[0].location)
	
	setup_GUI(tilelist)

	#Teahouse action
	'''
	reward = tilelist[11].perform_action()
	print("reward is", reward)
	playerlist[0].update_resources("lira", reward)
	print(playerlist[0].name, "now has", playerlist[0].resources.get("lira"), "lira!")
	'''
	#print(move_islegal(playerlist[0], tilelist[6], tilelist[15]))


	''' game logic
	while game hasnt ended:
		for player in players
			move merchant (not to self, not diagonally)
			if servant present, add stack
			if not, drop to do action (optionally), else turn ends

			pay other merchant (player) if present
				if you cannot pay & location != fountain -> turn ends
				if neutral merchant, pay bank & throw dice to move to new tile

			do tile action

			do family members, get 3 lira or 1 bonus card
			optionally: do governor, smuggler action	
	'''
	

class Players:
	def __init__(self, player, location):
		additional_lira = player
		name = player + 1
		self.name = "Player" + str(name)
		self.rubies = 0
		self.diamonds = 0
		self.fruit = 0
		self.fabric = 0
		self.spice = 0
		self.max_res = 3
		self.resources = {"lira": 2 + additional_lira, "rubies": 0, "diamonds": 0, "fruit": 0, "fabric": 0, "spice": 0, "max_res": 3}
		self.units_stack = [self.name + "_merchant1", self.name + "_servant1", self.name + "_servant2", self.name + "_servant3", self.name + "_servant4"]
		self.location = location

	def update_resources(self, resource, amount): #self, string, integer
		self.resources[resource] = self.resources.get(resource) + amount;

	def update_location(self, location):
		self.location = location


class Tiles:
	def __init__(self, name, location):
		self.name = name
		self.tilenumbers = []
		self.location = location
		self.players_present = []
		self.units_stack = []

	#def get_location(self, location):
	#	return location

	def update_players_present(self, player, action):
		if (action == "addition"):
			self.players_present.append(player)
		else: #deletion
			self.players_present.remove(player)

	def update_units_stack(self, player, unit):
		self.units_stack.append(unit)

	def perform_action(self):
		if self.name == "tea_house":
			print("Performing tea house action...")
			number = 1
			while not(2 < number < 13):
				number = int(input("Fill in a number between 3-12: "))
			print("You picked number", number, ", rolling the dices...")
			dice_roll = random.randint(3,12)
			print("You threw %s" %dice_roll)
			if (dice_roll >= number):
				print("Congrats, you receive", number, "lira!")
				return number
			else:
				print("Too bad, you receive only 2 lira")
				return 2



class Board:
	def __init__(self, number_of_players, number_of_tiles):
		self.number_of_players = number_of_players
		self.number_of_tiles = number_of_tiles
		#self.current_player_location = {}
		#for i in range(0, number_of_players):
		#	self.current_player_location["Player" + str(i + 1)] = []
			#print("HERE:", self.current_player_location)

def move_islegal(player, move_from, move_to): #Tile1, Tile2
	print("move from is", move_from.location)
	print("move to is", move_to.location)
	#x1, y1 = move_from.location[0], move_from.location[1]
	#x2, y2 = move_to.location[0], move_to.location[1]
	#xdist = abs(move_to.location[0] - move_from.location[0])
	#ydist = abs(move_to.location[1] - move_from.location[1])
	if ((abs(move_to.location[0] - move_from.location[0]) == 0 and (abs(move_to.location[1] - move_from.location[1]) == 1 or abs(move_to.location[1] - move_from.location[1]) == 2)) or 
		(abs(move_to.location[1] - move_from.location[1]) == 0 and (abs(move_to.location[0] - move_from.location[0]) == 1 or abs(move_to.location[0] - move_from.location[0]) == 2)) or 
		(abs(move_to.location[0] - move_from.location[0]) == abs(move_to.location[1] - move_from.location[1]) == 1)):
		return True
	else:
		return False


def setup_GUI(tilelist):
	pygame.init()
	framewidth = 1600	
	frameheight = 1000
	frame = pygame.display.set_mode((framewidth, frameheight), RESIZABLE)
	pygame.display.set_caption('Istanbul')

	boardwidth = framewidth * (2/3)
	boardheight = frameheight * (2/3)
	tilegap = 10
	boardx = (framewidth / 12) - (tilegap * 4)
	boardy = (frameheight / 12)

	#tilewidth = (boardwidth / 4) - tilegap
	#tileheight = (boardheight / 4) - tilegap
	tilewidth= (boardwidth - 3 * tilegap) / 4
	tileheight= (boardheight - 3 * tilegap) / 4

	black = (0, 0, 0)
	white = (255, 255, 255)
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	background = (49, 49, 49)
	background2 = (0, 68, 102)
	frame.fill(background)

	# wallpaper = pygame.image.load("images/wallpaper2.png")
	# # guy = pygame.transform.smoothscale(box, (int(framewidth - boardx), int(frameheight - (boardy + (tileheight + tilegap) * 4 ))))
	# frame.blit(wallpaper, (0, 0))

	for tile in tilelist:
		try:
			path = "images/" + tile.name + ".png"
			currenttile = pygame.image.load(path)
			#print("try ", tile.name)
		except:
			currenttile = pygame.image.load("images/spice_warehouse.png")
			#print("except ", tile.name)
		tilex = boardy + ((tile.location[1] - 1) * (tilewidth + tilegap))
		tiley = boardx + ((tile.location[0] - 1) * (tileheight + tilegap))
		#print("printing tile ", tile.name, "at x=", tilex, ", y=", tiley)
		currenttile = pygame.transform.smoothscale(currenttile, (int(tilewidth), int(tileheight)))
		frame.blit(currenttile, (tilex, tiley))

	box = pygame.image.load("images/box.png")
	box = pygame.transform.smoothscale(box, (int(tilewidth), int(tileheight)))
	frame.blit(box, (boardx + ((tilewidth + tilegap / 2) * 4 + tilewidth / 2), boardy + (tileheight * 1.5 + (tilegap / 2))))

	# pygame.draw.rect(frame, background2, (boardx + tilegap / 2, boardy + (tileheight + tilegap) * 4, 
	# 	framewidth - boardx, frameheight - (boardy + (tileheight + tilegap) * 4 )))

	# guyonthebox = pygame.image.load("images/guyonthebox.png")
	# guy = pygame.transform.smoothscale(box, (int(framewidth - boardx), int(frameheight - (boardy + (tileheight + tilegap) * 4 ))))
	# frame.blit(guyonthebox, (boardx + tilegap / 2, boardy + (tileheight + tilegap) * 4))

	p1_windowx = boardx + (0.5 * tilewidth) - tilegap
	p1_windowy = boardy + boardheight + (tilegap * 2)
	p1_windowwidth = 1.5 * tilewidth + tilegap
	p1_windowheight = boardy + tileheight
	pygame.draw.rect(frame, background2, (p1_windowx, p1_windowy, p1_windowwidth, p1_windowheight)) #Player1 window

	p2_windowx = boardx + (2 * tilewidth) + tilegap
	p2_windowy = boardy + boardheight + (tilegap * 2) 
	p2_windowwidth = p1_windowwidth
	p2_windowheight = p1_windowheight
	pygame.draw.rect(frame, red, (p2_windowx, p2_windowy, p2_windowwidth, p2_windowheight)) #Player1 window

	# resource2 = pygame.image.load("images/resource2.png")
	# resource2 = pygame.transform.smoothscale(resource2, (int(tilewidth), int(tileheight)))
	# frame.blit(resource2, (boardx + (0.5 * tilewidth) - tilegap, boardy + boardheight + tilegap * 2, 1.5 * tilewidth, boardy + tileheight))


	while True: # main game loop
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()


if __name__ == '__main__':
  main()
