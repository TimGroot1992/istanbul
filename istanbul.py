import sys
import time
import math
from random import randint
import pygame
from pygame.locals import *

framewidth = 1500		
frameheight = 1000
boardx = 25
boardy = 25
tilegap = 5
boardwidth = framewidth * (2/3)
boardheight = frameheight * (10/12)
tilewidth = (boardwidth - 3 * tilegap) / 4
tileheight = (boardheight - 3 * tilegap) / 4
#print("TILEDWIDTH =", tilewidth)
#print("TILEHEIGHT =", tileheight)

p1_windowx = boardx + (4.2 * tilewidth) + (tilegap * 4)
p1_windowy = boardy + (0.5 * tileheight)
p1_windowwidth = 1.5 * tilewidth
p1_windowheight = boardy + tileheight
p2_windowx = p1_windowx
p2_windowy = boardy + (2.5 * tileheight)
p2_windowwidth = p1_windowwidth
p2_windowheight = p1_windowheight

black = (0, 0, 0)
white = (255, 255, 204)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
background = (49, 49, 49)
background2 = (0, 68, 102)

def main():
	board = Board(int(sys.argv[1]), 16)
	print("Playing Istanbul with", board.number_of_players, "players!")
	print("")

	tiles = {"great_mosque": [1, 1], "postal_office": [1, 2], "fabric_warehouse": [1, 3], "small_mosque": [1, 4], 
		"fruit_warehouse": [2, 1], "police_station": [2, 2],"fountain": [2, 3], "spice_warehouse": [2, 4], 
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

	postalblock_1 = Object("postalblock_1", tilelist[1].x + tilewidth/8.49, tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	postalblock_2 = Object("postalblock_2", tilelist[1].x + (tilewidth/8.49)*2, tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	postalblock_3 = Object("postalblock_3", tilelist[1].x + (tilewidth/8.49)*3, tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	postalblock_4 = Object("postalblock_4", tilelist[1].x + (tilewidth/8.49)*4, tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	units = [postalblock_1, postalblock_2, postalblock_3, postalblock_4]

	
	frame = setup_GUI(framewidth, frameheight, boardwidth, boardheight, tilewidth, tileheight, tilegap, boardx, boardy, tilelist)
	draw_board(frame, tilelist)
	draw_units(frame, units)
	
	mainloop_GUI(board, frame, tilelist, units, playerlist)
	

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
		#self.rubies = 0
		#self.diamonds = 0
		#self.fruit = 0
		#self.fabric = 0
		#self.spice = 0
		#self.max_res = 2
		self.resources = {"lira": 2 + additional_lira, "rubies": 0, "diamonds": 0, "fruit": 0, "fabric": 0, "spice": 0, "max_res": 2}
		self.units_stack = [self.name + "_merchant1", self.name + "_servant1", self.name + "_servant2", self.name + "_servant3", self.name + "_servant4"]
		self.location = location

	def update_resources(self, resource, amount): #self, string, integer
		if resource == "diamonds" or resource == "fruit" or resource == "fabric" or resource == "spice":
			if (self.resources.get(resource) + amount) >= self.resources.get("max_res"):
				self.resources[resource] = self.resources.get("max_res");
			else:
				self.resources[resource] = self.resources.get(resource) + amount
		else:
			self.resources[resource] = self.resources.get(resource) + amount

	def update_location(self, location):
		self.location = location


class Tiles:
	def __init__(self, name, location):
		global boardx
		global boardy
		global tilewidth
		global tileheight
		global tilegap

		self.name = name
		self.tilenumbers = []
		self.location = location
		self.x = (boardy + ((self.location[1] - 1) * (tilewidth + tilegap)))
		self.y = boardx + ((self.location[0] - 1) * (tileheight + tilegap))
		self.players_present = []
		self.units_stack = []
		if self.name == "postal_office":
			#self.blocks = {"fabric": 0, "lira_2_1": 0, "diamonds": 0, "lira_2_2": 0, "spice": 1, "lira_1_1": 1, "fruit": 1, "lira_1_2": 1}
			self.blocks = [
				{"fabric": 0, "lira_2_1": 0, "diamonds": 0, "lira_2_2": 0, "spice": 1, "lira_1_1": 1, "fruit": 1, "lira_1_2": 1}, 
				{"fabric": 1, "lira_2_1": 0, "diamonds": 0, "lira_2_2": 0, "spice": 0, "lira_1_1": 1, "fruit": 1, "lira_1_2": 1}, 
				{"fabric": 1, "lira_2_1": 1, "diamonds": 0, "lira_2_2": 0, "spice": 0, "lira_1_1": 0, "fruit": 1, "lira_1_2": 1},
				{"fabric": 1, "lira_2_1": 1, "diamonds": 1, "lira_2_2": 0, "spice": 0, "lira_1_1": 0, "fruit": 0, "lira_1_2": 1},
				{"fabric": 1, "lira_2_1": 1, "diamonds": 1, "lira_2_2": 1, "spice": 0, "lira_1_1": 0, "fruit": 0, "lira_1_2": 0}
				]
			
	def move_postalblocks(self, blocks):
		# if (blocks.get("spice") == blocks.get("lira_1_1") == blocks.get("fruit") == blocks.get("lira_1_2") == 0):
		# 	for value in blocks:
		# 		if value == 0:
		# 			value = 1
		# 		else:
		# 			value = 0
		# elif blocks.get("fruit") == 0:
		# 	blocks["lira_2_2"] = 1
		# 	blocks["lira_1_2"] = 0
		# elif blocks.get("lira_1_1") == 0:
		# 	blocks["diamonds"] = 1
		# 	blocks["fruit"] = 0
		# elif blocks.get("spice") == 0:
		# 	blocks["lira_2_1"] = 1
		# 	blocks["lira_1_1"] = 0
		# else:
		# 	blocks["fabric"] = 1
		# 	blocks["spice"] = 0
		blocks.append(blocks.pop(0))

	def update_players_present(self, player, action):
		if (action == "addition"):
			self.players_present.append(player)
		else: #deletion
			self.players_present.remove(player)

	def update_units_stack(self, player, unit):
		self.units_stack.append(unit)

	# def perform_action(self, bet, frame, tilelist):
	# 	print("Your bet is", bet, "... Rolling the dice...")
	# 	if self.name == "tea_house":
	# 		dice_roll = roll_dice(frame, tilelist)
	# 		if (dice_roll >= bet):
	# 			print("Congrats, you receive", bet, "lira!")
	# 			return bet
	# 		else:
	# 			print("Too bad, you receive only 2 lira")
	# 			return 2

class Object:
	def __init__(self, name, x, y, width, height, image_path):
		self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.image_path = image_path

	def update_name(self, newname):
		self.name = newname

	def set_x(self, newx):
		self.x = newx

	def set_y(self, newy):
		self.y = newy

	def set_x_rel(self, x):
		self.x = self.x + x

	def set_y_rel(self, y):
		self.y = self.y + y

	def update_image_path(self, image_path):
		self.image_path = image_path


class Board:
	def __init__(self, number_of_players, number_of_tiles):
		self.number_of_players = number_of_players
		self.number_of_tiles = number_of_tiles
		self.current_player = 0
		
	def set_nextplayer(self):
		if not (self.current_player + 1) > self.number_of_players - 1:
			self.current_player = self.current_player + 1
		else:
			self.current_player = 0


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

def setup_GUI(framewidth, frameheight, boardwidth, boardheight, tilewidth, tileheight, tilegap, boardx, boardy, tilelist):
	global background
	pygame.init()
	frame = pygame.display.set_mode((framewidth, frameheight), RESIZABLE) #FULLSCREEN
	pygame.display.set_caption('Istanbul')
	frame.fill(background)
	return frame
	
def draw_board(frame, tilelist):
	global background2
	global red

	for tile in tilelist:
		#print(tile.name)
		try:
			path = "images/" + tile.name + ".png"
			currenttile = pygame.image.load(path).convert()
			#print("try ", tile.name)
		except:
			currenttile = pygame.image.load("images/spice_warehouse.png").convert()
			#print("except ", tile.name)
		#tilex = tile.coordinates[0]
		#tiley = tile.coordinates[1]
		#print("printing tile ", tile.name, "at x=", tilex, ", y=", tiley)
		currenttile = pygame.transform.smoothscale(currenttile, (int(tilewidth), int(tileheight)))
		frame.blit(currenttile, (tile.x, tile.y))

	pygame.draw.rect(frame, background2, (p1_windowx, p1_windowy, p1_windowwidth, p1_windowheight)) #Player1 window
	pygame.draw.rect(frame, red, (p2_windowx, p2_windowy, p2_windowwidth, p2_windowheight)) #Player2 window

	box = pygame.image.load("images/box.png").convert()
	box = pygame.transform.smoothscale(box, (int(tilewidth), int(tileheight - 5*tilegap)))
	#print("BOXWIDTH = ", tilewidth)
	#print("BOXHEIGHT = ", tileheight - 5*tilegap)
	frame.blit(box, (p1_windowx + ((p1_windowwidth - tilewidth)/2), p1_windowy + tileheight + 5 * tilegap))

	#pygame.display.update()

def draw_tile(frame, tile):
	try:
		path = "images/" + tile.name + ".png"
		currenttile = pygame.image.load(path).convert()
		#print("try ", tile.name)
	except:
		currenttile = pygame.image.load("images/spice_warehouse.png").convert()
		print("Error retrieving tile image, using spice warehouse as a default.")
	currenttile = pygame.transform.smoothscale(currenttile, (int(tilewidth), int(tileheight)))
	frame.blit(currenttile, (tile.x, tile.y))

def draw_units(frame, units):
	for unit in units:
		if unit.image_path == "":
			pygame.draw.rect(frame, white, (unit.x, unit.y, unit.width, unit.height))

def mainloop_GUI(board, frame, tilelist, units, playerlist):
	global tilewidth
	global tileheight

	fps = 10
	fpsClock = pygame.time.Clock()
	#return frame
	#pygame.display.update()
	counter = 0
	while True: # main game loop
		for event in pygame.event.get():
			#pygame.event.wait()
			print(event)

			#Blit background
			#Update location of all units within a list
			#pygame.display.update(Unit list)

			if event.type == pygame.MOUSEBUTTONUP:
				mouseposition = pygame.mouse.get_pos()
				pos_x = mouseposition[0]
				pos_y = mouseposition[1]
				for tile in tilelist:
					if pos_x > tile.x and pos_x < (tile.x + tilewidth) and pos_y > tile.y and pos_y < (tile.y + tileheight):
						#print("you clicked on tile", tile.name)
						tilename = tile.name
						break
				if tile.name == "tea_house": #Perform teahouse action
					print("Performing tea house action, type in a number between 3-12 followed by an enter")
					bet = 1
					while not (2 < bet < 13):
						bet = get_keyboardinput(event)
						if not (2 < bet < 13):
							print("Your bet must be between 3 and 12, please try again.")
					print("Your bet is", bet, "... Rolling the dice...")
					dice_roll = roll_dice(frame, tilelist, units)
					if (dice_roll >= bet):
						print("Congrats, you receive", bet, "lira!")
						playerlist[board.current_player].update_resources("lira", bet)
						print("player", playerlist[board.current_player].name, " now has ", playerlist[board.current_player].resources.get('lira'), " lira")
					else:
						print("Too bad, you receive only 2 lira")
						playerlist[board.current_player].update_resources("lira", 2)
						print("player", playerlist[board.current_player].name, " now has ", playerlist[board.current_player].resources.get('lira'), " lira")
					board.set_nextplayer()
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
				elif tile.name == "postal_office": #Perform postal office action
					print("Performing postal office action")
					print("Current player is Player", board.current_player + 1)
					for key, value in tilelist[1].blocks[0].items():
						if value == 1:
							#print("You receive", key)
							if "lira" in key:
								playerlist[board.current_player].update_resources("lira", int(key.split("_")[1]))
							elif "fabric" in key:
								playerlist[board.current_player].update_resources("fabric", 1)
							elif "spice" in key:
								playerlist[board.current_player].update_resources("spice", 1)
							elif "diamonds" in key:
								playerlist[board.current_player].update_resources("diamonds", 1)
							elif "fruit" in key:
								playerlist[board.current_player].update_resources("fruit", 1)
					
					print(playerlist[board.current_player].name, "now has", playerlist[board.current_player].resources.get("lira"), "lira,", playerlist[board.current_player].resources.get("fabric"), "fabric,", playerlist[board.current_player].resources.get("spice"), "spice,", playerlist[board.current_player].resources.get("diamonds"), "diamonds and", playerlist[board.current_player].resources.get("fruit"), "fruit.")
					#print("Blocks now = ", tilelist[1].blocks)
					tilelist[1].move_postalblocks(tilelist[1].blocks)

					for unit in units:
						if "postalblock" in unit.name:

							if tilelist[1].blocks[0].get("fabric") == tilelist[1].blocks[0].get("lira_2_1") == tilelist[1].blocks[0].get("diamonds") == tilelist[1].blocks[0].get("lira_2_2") == 1 and "postalblock" in unit.name:
								unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
							elif "postalblock_1" in unit.name:
								if tilelist[1].blocks[0].get("fabric") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)
							elif "postalblock_2" in unit.name:
								if tilelist[1].blocks[0].get("lira_2_1") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)
							elif "postalblock_3" in unit.name:
								if tilelist[1].blocks[0].get("diamonds") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)
							elif "postalblock_4" in unit.name:
								if tilelist[1].blocks[0].get("lira_2_2") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)

					draw_tile(frame, tilelist[1])
					draw_units(frame, units)
					board.set_nextplayer()
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
				
			if event.type == QUIT or (event.type is KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		pygame.display.update()
		fpsClock.tick(fps)

def get_keyboardinput(event):
	enter_pressed = False
	numbers_entered = ""
	while not enter_pressed:
		pygame.event.wait()
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_0]:
			numbers_entered = numbers_entered + "0"
			print(numbers_entered)
		elif pressed[pygame.K_1]:
			numbers_entered = numbers_entered + "1"
			print(numbers_entered)
		elif pressed[pygame.K_2]:
			numbers_entered = numbers_entered + "2"
			print(numbers_entered)
		elif pressed[pygame.K_3]:
			numbers_entered = numbers_entered + "3"
			print(numbers_entered)
		elif pressed[pygame.K_4]:
			numbers_entered = numbers_entered + "4"
			print(numbers_entered)
		elif pressed[pygame.K_5]:
			numbers_entered = numbers_entered + "5"
			print(numbers_entered)
		elif pressed[pygame.K_6]:
			numbers_entered = numbers_entered + "6"
			print(numbers_entered)
		elif pressed[pygame.K_7]:
			numbers_entered = numbers_entered + "7"
			print(numbers_entered)
		elif pressed[pygame.K_8]:
			numbers_entered = numbers_entered + "8"
			print(numbers_entered)
		elif pressed[pygame.K_9]:
			numbers_entered = numbers_entered + "9"
			print(numbers_entered)
		elif pressed[pygame.K_RETURN]:
			enter_pressed = True
			#print("You pressed enter")
			bet = int(numbers_entered)
	return bet

def roll_dice(frame, tilelist, units):
	global p1_windowx
	global p1_windowwidth
	global p1_windowy
	global tileheight
	global tilewidth
	global tilegap

	dice1_x = p1_windowx + ((p1_windowwidth - tilewidth)/2) + randint(int(tilewidth / 8), int(tileheight)) #40, 220
	dice1_y = p1_windowy + tileheight + (5 * tilegap) + randint(int(tileheight / 9), int(tileheight / 2)) #25, 115
	dice2_x = p1_windowx + ((p1_windowwidth - tilewidth)/2) + randint(int(tilewidth / 8), int(tileheight))
	dice2_y = p1_windowy + tileheight + (5 * tilegap) + randint(int(tileheight / 9), int(tileheight / 2))
	while (dice_offset(dice1_x, dice1_y, dice2_x, dice2_y)): #Replace the second die while they're overlapping
		dice2_x = p1_windowx + ((p1_windowwidth - tilewidth)/2) + randint(int(tilewidth / 8), int(tileheight))
		dice2_y = p1_windowy + tileheight + (5 * tilegap) + randint(int(tileheight / 9), int(tileheight / 2))

	# x_distance = 0.01
	# pause = 0.5
	# while x_distance < 5:
	dice1 = Object("dice1", dice1_x, dice1_y, tilewidth/5, tilewidth/5, "images/die1.png") # 40 <= x <= 220, 25 <= y <= 115
	randomnumber = randint(1, 6)
	dice1.update_image_path("images/die" + str(randomnumber) + ".png")
	image = pygame.image.load(dice1.image_path).convert()
	image = pygame.transform.smoothscale(image, (int(dice1.width), int(dice1.height)))
	
	dice2 = Object("dice1", dice2_x, dice2_y, tilewidth/5, tilewidth/5, "images/die1.png") # 40 <= x <= 220, 25 <= y <= 115
	randomnumber2 = randint(1, 6)
	dice2.update_image_path("images/die" + str(randomnumber2) + ".png")
	image2 = pygame.image.load(dice2.image_path).convert()
	image2 = pygame.transform.smoothscale(image2, (int(dice2.width), int(dice2.height)))

	#BEFORE blitting: draw background & all units, so the previous dice will be erased
	draw_board(frame, tilelist)
	draw_units(frame, units)

	frame.blit(image, (dice1.x, dice1.y))
	frame.blit(image2, (dice2.x, dice2.y))
		# pygame.time.wait(int(pause))
		# pause = 0.5 + ((12.25 - math_velocity(x_distance)/ 12.25) * 1.5)
		# x_distance = x_distance + pause

	print("You have thrown", (randomnumber + randomnumber2))
	#pygame.display.update()
	return randomnumber + randomnumber2

def dice_offset(dice1_x, dice1_y, dice2_x, dice2_y):
	global tilewidth
	if (abs(dice1_x - dice2_x) < (tilewidth/5) and (abs(dice1_y - dice2_y) < (tilewidth/5))):
		return True
	else:
		return False

# def math_velocity(x):
# 	y = math.sqrt(150 - (math.pow(x, 3)))
# 	return y

if __name__ == '__main__':
  main()
