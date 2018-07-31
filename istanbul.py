import sys
import time
import math
from random import randint
import pygame
from pygame.locals import *
from pygame import gfxdraw

from classes import Board, Players, Tiles, Object

windowtype = FULLSCREEN
framewidth = 1920			
frameheight = 1080
boardx = 25
boardy = 25
tilegap = 5
boardwidth = framewidth * (2/3)
boardheight = frameheight * (10/12)
tilewidth = (boardwidth - 3 * tilegap) / 4
tileheight = (boardheight - 3 * tilegap) / 4

p1_windowx = boardx + (4.2 * tilewidth) + (tilegap * 4)
p1_windowy = boardy + (0.5 * tileheight)
p1_windowwidth = 1.5 * tilewidth
p1_windowheight = boardy + tileheight
p2_windowx = p1_windowx
p2_windowy = boardy + (2.5 * tileheight)
p2_windowwidth = p1_windowwidth
p2_windowheight = p1_windowheight

black = (0, 0, 0)
white = (255, 255, 255)
offwhite = (255, 255, 204)
yellow = (255, 163, 26)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
background = (49, 49, 49)
background2 = (0, 68, 102)

def main():
	#board = Board(int(sys.argv[1]), 16)
	board = Board(2, 16)
	print("Playing Istanbul with", board.number_of_players, "players!")
	print("")

	tiles = {"great_mosque": [1, 1], "postal_office": [1, 2], "fabric_warehouse": [1, 3], "small_mosque": [1, 4], 
		"fruit_warehouse": [2, 1], "police_station": [2, 2],"fountain": [2, 3], "spice_warehouse": [2, 4], 
		"black_market": [3, 1], "caravansary": [3, 2], "small_market": [3, 3], "tea_house": [3, 4],
		"sultans_palace": [4, 1], "large_market": [4, 2], "wainwright": [4, 3], "gemstone_dealer": [4, 4]}
	tilelist = [Tiles(tile, tiles.get(tile), boardx, boardy, tilewidth, tileheight, tilegap) for tile in tiles]

	# Object template: Object(x, y, width, height, image_path)
	postalblock_1 = Object(tilelist[1].x + tilewidth*(191/1612), tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	postalblock_2 = Object(tilelist[1].x + tilewidth*(388/1612), tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	postalblock_3 = Object(tilelist[1].x + tilewidth*(584/1612), tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	postalblock_4 = Object(tilelist[1].x + tilewidth*(780/1612), tilelist[1].y + tileheight/1.7, tileheight/7.2, tileheight/7.2, "")
	resource_p1 = Object(p1_windowx + 3*tilegap, p1_windowy + 3*tilegap, p1_windowwidth - p1_windowwidth/5 - 6*tilegap, p1_windowheight - 6*tilegap, "images/resource2_1.png")
	resource_p2 = Object(p2_windowx + 3*tilegap, p2_windowy + 3*tilegap, p2_windowwidth - p2_windowwidth/5 - 6*tilegap, p2_windowheight - 6*tilegap, "images/resource2_2.png")
	resourceblock_1 = Object(resource_p1.x + resource_p1.width*(373/1604), resource_p1.y + resource_p1.height*(148/1074), resource_p1.width/15, resource_p1.width/15, "")
	resourceblock_2 = Object(resource_p1.x + resource_p1.width*(373/1604), resource_p1.y + resource_p1.height*(291/1074), resource_p1.width/15, resource_p1.width/15, "")
	resourceblock_3 = Object(resource_p1.x + resource_p1.width*(373/1604), resource_p1.y + resource_p1.height*(433/1074), resource_p1.width/15, resource_p1.width/15, "")
	resourceblock_4 = Object(resource_p1.x + resource_p1.width*(373/1604), resource_p1.y + resource_p1.height*(573/1074), resource_p1.width/15, resource_p1.width/15, "")
	resourceblock_5 = Object(resource_p2.x + resource_p2.width*(373/1604), resource_p2.y + resource_p2.height*(148/1074), resource_p2.width/15, resource_p2.width/15, "")
	resourceblock_6 = Object(resource_p2.x + resource_p2.width*(373/1604), resource_p2.y + resource_p2.height*(291/1074), resource_p2.width/15, resource_p2.width/15, "")
	resourceblock_7 = Object(resource_p2.x + resource_p2.width*(373/1604), resource_p2.y + resource_p2.height*(433/1074), resource_p2.width/15, resource_p2.width/15, "")
	resourceblock_8 = Object(resource_p2.x + resource_p2.width*(373/1604), resource_p2.y + resource_p2.height*(573/1074), resource_p2.width/15, resource_p2.width/15, "")

	# Coin- and text objects
	coin_p1 = Object(resource_p1.x + p1_windowwidth*(5/6), resource_p1.y + p1_windowheight*(1/5), resource_p1.width/6, resource_p1.width/6, "")
	coin_p2 = Object(resource_p2.x + p2_windowwidth*(5/6), resource_p2.y + p2_windowheight*(1/5), resource_p2.width/6, resource_p2.width/6, "")
	lira_1 = Object(resource_p1.x + p1_windowwidth*(5/6), resource_p1.y + p1_windowheight*(1/5), resource_p1.width/6, resource_p1.width/6, "")
	lira_2 = Object(resource_p2.x + p2_windowwidth*(5/6), resource_p2.y + p2_windowheight*(1/5), resource_p2.width/6, resource_p2.width/6, "")

	# Mosque Tiles
	gem_small_mosque1 = Object(tilelist[3].x, tilelist[3].y + tileheight - tileheight/8, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_small_mosque2 = Object(tilelist[3].x + tilewidth/15, tilelist[0].y + tileheight - tileheight/8, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_great_mosque1 = Object(tilelist[0].x, tilelist[0].y + tileheight - tileheight/8, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_great_mosque2 = Object(tilelist[0].x + tilewidth/15, tilelist[0].y + tileheight - tileheight/8, tileheight/8, tileheight/8, "images/gemstone_2.png")

	# Gemstone Dealer Gems
	gem_gemstone1 = Object(tilelist[15].x + tilewidth/3.4, tilelist[15].y + tileheight - tileheight/4.5, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone2 = Object(tilelist[15].x + tilewidth/2.5, tilelist[15].y + tileheight - tileheight/4.5, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone3 = Object(tilelist[15].x + tilewidth*(830/1609), tilelist[15].y + tileheight - tileheight/4.5, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone4 = Object(tilelist[15].x + tilewidth*(1000/1609), tilelist[15].y + tileheight - tileheight/4.5, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone5 = Object(tilelist[15].x + tilewidth*(1190/1609), tilelist[15].y + tileheight - tileheight/4.5, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone6 = Object(tilelist[15].x + tilewidth*(1365/1609), tilelist[15].y + tileheight - tileheight/4.5, tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone7 = Object(tilelist[15].x + tilewidth*(1365/1609), tilelist[15].y + tileheight*(658/1077), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone8 = Object(tilelist[15].x + tilewidth*(1365/1609), tilelist[15].y + tileheight*(478/1077), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_gemstone9 = Object(tilelist[15].x + tilewidth*(1365/1609), tilelist[15].y + tileheight*(298/1077), tileheight/8, tileheight/8, "images/gemstone_2.png")

	# Sultans Palace Gems
	gem_sultan1 = Object(tilelist[12].x + tilewidth*(650/1611), tilelist[12].y + tileheight*(840/1084), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_sultan2 = Object(tilelist[12].x + tilewidth*(830/1611), tilelist[12].y + tileheight*(840/1084), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_sultan3 = Object(tilelist[12].x + tilewidth*(1010/1611), tilelist[12].y + tileheight*(840/1084), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_sultan4 = Object(tilelist[12].x + tilewidth*(1190/1611), tilelist[12].y + tileheight*(840/1084), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_sultan5 = Object(tilelist[12].x + tilewidth*(1370/1611), tilelist[12].y + tileheight*(840/1084), tileheight/8, tileheight/8, "images/gemstone_2.png")
	gem_sultan6 = Object(tilelist[12].x + tilewidth*(1370/1611), tilelist[12].y + tileheight*(670/1084), tileheight/8, tileheight/8, "images/gemstone_2.png")

	# Market Tiles
	small_market_tiles = Object(tilelist[10].x + tilewidth*(322/1619), tilelist[10].y + tileheight*(330/1084), tilewidth/3.42, tileheight/1.78, "images/small_market_tile" + tilelist[10].merchandise[0].get("tilenumber") + ".png")
	large_market_tiles = Object(tilelist[13].x + tilewidth*(313/1612), tilelist[13].y + tileheight*(325/1079), tilewidth/3.35, tileheight/1.78, "images/large_market_tile" + tilelist[10].merchandise[0].get("tilenumber") + ".png")

	# End Turn Button and Text
	end_turn_button = Object(p1_windowx + ((p1_windowwidth - tilewidth)/2), tilelist[15].y + tileheight, tilewidth, tileheight/2, "images/buttonblue.png")
	end_turn_button_text = Object(p1_windowx + ((p1_windowwidth - tilewidth)/2), tilelist[15].y + tileheight, tilewidth, tileheight/2, "")

	units = {
		"postalblock_1": postalblock_1, "postalblock_2": postalblock_2, "postalblock_3": postalblock_3, "postalblock_4": postalblock_4,	
		"resource_p1": resource_p1, "resource_p2": resource_p2,
		"resourceblock_1": resourceblock_1, "resourceblock_2": resourceblock_2, "resourceblock_3": resourceblock_3, "resourceblock_4": resourceblock_4,
		"resourceblock_5": resourceblock_5, "resourceblock_6": resourceblock_6, "resourceblock_7": resourceblock_7, "resourceblock_8": resourceblock_8,
		"coin_p1": coin_p1, "coin_p2": coin_p2, "lira_1": lira_1, "lira_2": lira_2,
		"gem_small_mosque1": gem_small_mosque1, "gem_small_mosque2": gem_small_mosque2, "gem_great_mosque1": gem_great_mosque1, "gem_great_mosque2": gem_great_mosque2,
		"gem_gemstone1": gem_gemstone1, "gem_gemstone2": gem_gemstone2, "gem_gemstone3": gem_gemstone3, "gem_gemstone4": gem_gemstone4, 
		"gem_gemstone5": gem_gemstone5, "gem_gemstone6": gem_gemstone6, "gem_gemstone7": gem_gemstone7, "gem_gemstone8": gem_gemstone8, "gem_gemstone9": gem_gemstone9,
		"gem_sultan1": gem_sultan1, "gem_sultan2": gem_sultan2, "gem_sultan3": gem_sultan3,
		"gem_sultan4": gem_sultan4, "gem_sultan5": gem_sultan5, "gem_sultan6": gem_sultan6,
		"small_market_tiles": small_market_tiles, "large_market_tiles": large_market_tiles,
		"end_turn_button": end_turn_button, "end_turn_button_text": end_turn_button_text
	}

	playerlist = [Players(i, tilelist, tilewidth, tileheight, units) for i in range(0, board.number_of_players)]
	
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

	frame, font = setup_GUI(windowtype, framewidth, frameheight, boardwidth, boardheight, tilewidth, tileheight, tilegap, boardx, boardy, tilelist)
	draw_board(frame, tilelist)
	draw_units(frame, font, units, playerlist, board)
	mainloop_GUI(board, frame, font, tilelist, units, playerlist)
	
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

def setup_GUI(windowtype, framewidth, frameheight, boardwidth, boardheight, tilewidth, tileheight, tilegap, boardx, boardy, tilelist):
	global background
	pygame.init()
	frame = pygame.display.set_mode((framewidth, frameheight), windowtype)
	pygame.display.set_caption('Istanbul')
	frame.fill(background)

	pygame.font.init()
	font = pygame.font.SysFont('Comic Sans MS', int(framewidth/80))
	# w, h = pygame.display.get_surface().get_size()
	# print(f"windows width is {w}")
	# print(f"windows height is {h}")
	return frame, font
	
def draw_board(frame, tilelist):
	global background2
	global red
	for tile in tilelist:
		#print(tile.name)
		try:
			path = "images/" + tile.name + ".png"
			currenttile = pygame.image.load(path).convert()
		except:
			currenttile = pygame.image.load("images/spice_warehouse.png").convert()
			#print("except ", tile.name)
		#tilex = tile.coordinates[0]
		#tiley = tile.coordinates[1]
		#print("printing tile ", tile.name, "at x=", tilex, ", y=", tiley)
		currenttile = pygame.transform.smoothscale(currenttile, (int(tilewidth), int(tileheight)))
		frame.blit(currenttile, (tile.x, tile.y))

	draw_boxes(frame, "p1")
	draw_boxes(frame, "p2")
	draw_boxes(frame, "box")

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

def draw_boxes(frame, name):
	global background2
	global red

	if name == "box":
		try:
			currenttile = pygame.image.load("images/box.png").convert()
		except:
			currenttile = pygame.image.load("images/spice_warehouse.png").convert()
			print("Error retrieving tile image, using spice warehouse as a default.")
		currenttile = pygame.transform.smoothscale(currenttile, (int(tilewidth), int(tileheight - 5 * tilegap)))
		frame.blit(currenttile, (p1_windowx + ((p1_windowwidth - tilewidth)/2), p1_windowy + tileheight + 5 * tilegap))
	elif name == "p1":
		pygame.draw.rect(frame, background2, (p1_windowx, p1_windowy, p1_windowwidth, p1_windowheight)) #Player1 window
	else:
		pygame.draw.rect(frame, red, (p2_windowx, p2_windowy, p2_windowwidth, p2_windowheight)) #Player2 window

def draw_units(frame, font, units, playerlist, board):
	for name, unit in units.items():
		if "block" in name:
			#print("drawing block with name", name, "at ", unit.x, ",", unit.y)
			pygame.draw.rect(frame, offwhite, (unit.x, unit.y, unit.width, unit.height))
		elif "coin" in name:
			pygame.gfxdraw.aacircle(frame, int(unit.x), int(unit.y), int(unit.width/2), yellow)
			pygame.gfxdraw.filled_circle(frame, int(unit.x), int(unit.y), int(unit.width/2), yellow)
		elif "lira" in name:
			textsurface = font.render(str(playerlist[int(name.split("_")[1]) - 1].resources.get('lira')), False, black)
			if playerlist[int(name.split("_")[1]) - 1].resources.get('lira') < 10:
				frame.blit(textsurface, (unit.x - unit.width/7, unit.y - unit.height/3))
			else:
				frame.blit(textsurface, (unit.x - unit.width/4, unit.y - unit.height/3))
		elif "text" in name:
			textsurface = font.render("End Turn", False, white)
			frame.blit(textsurface, (unit.x + unit.width/3, unit.y + unit.height/3))
		else: #Shape loaded by image
			# print(f"unit image path is {unit.image_path} and board next player button is {board.next_player_button}")
			try:
				if name != "end_turn_button":
					currentunit = pygame.image.load(unit.image_path).convert_alpha()
				else:
					currentunit = pygame.image.load(board.next_player_button).convert_alpha()
			except:
				currentunit = pygame.image.load("images/spice_warehouse.png").convert()
				print("Error retrieving tile image, using spice warehouse as a default.")
			currentunit = pygame.transform.smoothscale(currentunit, (int(unit.width), int(unit.height)))
			#currentunit.set_colorkey((255, 255, 255))
			frame.blit(currentunit, (unit.x, unit.y))
		#print(f"I just drew unit {name}")

def mainloop_GUI(board, frame, font, tilelist, units, playerlist):
	global tilewidth
	global tileheight

	fps = 60
	fpsClock = pygame.time.Clock()

	while True: # main game loop
		for event in pygame.event.get():
			#print(event)

			if event.type == pygame.MOUSEBUTTONUP:
				clicked_tile, clicked_object = get_clicked_item(tilelist, units)
				print("You clicked on tile", clicked_tile)
				if clicked_object != "None":
					print("You clicked on object", clicked_object)


				if clicked_object == "end_turn_button":
					#print(f"player name is {playerlist[board.current_player].name}")
					print(f"{playerlist[board.current_player].name}'s turn was ended!")
					# if "1" in playerlist[board.current_player].name: # Player was is the current player
					# 	units.get("end_turn_button").update_image_path("images/buttonred.png")
					# else:
					# 	units.get("end_turn_button").update_image_path("images/buttonblue.png")
					
					board.set_nextplayer()
					draw_units(frame, font, units, playerlist, board)
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")

				elif clicked_tile == "postal_office": #Perform postal office action
					print("Performing postal office action")
					print("Current player is Player", board.current_player + 1)
					for key, value in tilelist[1].blocks[0].items():
						if value == 1:
							#print("You receive", key)
							if "lira" in key:
								playerlist[board.current_player].update_resources("lira", int(key.split("_")[1]))
							update_resource_blocks(board, playerlist, units, key, 1)

					print(playerlist[board.current_player].name, "now has", 
							playerlist[board.current_player].resources.get("lira"), "lira,", 
							playerlist[board.current_player].resources.get("fabric"), "fabric,", 
							playerlist[board.current_player].resources.get("spice"), "spice,", 
							playerlist[board.current_player].resources.get("diamonds"), "diamonds and", 
							playerlist[board.current_player].resources.get("fruit"), "fruit.")
					tilelist[1].move_postalblocks(tilelist[1].blocks)

					#for unit in units:
					for name, unit in units.items(): 
						if "postalblock" in name:

							if tilelist[1].blocks[0].get("fabric") == tilelist[1].blocks[0].get("lira_2_1") == tilelist[1].blocks[0].get("diamonds") == tilelist[1].blocks[0].get("lira_2_2") == 1:
								unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
							elif "postalblock_1" in name:
								if tilelist[1].blocks[0].get("fabric") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)
							elif "postalblock_2" in name:
								if tilelist[1].blocks[0].get("lira_2_1") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)
							elif "postalblock_3" in name:
								if tilelist[1].blocks[0].get("diamonds") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)
							elif "postalblock_4" in name:
								if tilelist[1].blocks[0].get("lira_2_2") == 1:
									unit.set_y(tilelist[1].y + tileheight/1.7 + tileheight/6)
								else:
									unit.set_y(tilelist[1].y + tileheight/1.7)

					board.set_nextplayer()
					draw_tile(frame, tilelist[1])
					draw_units(frame, font, units, playerlist, board)
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")

				elif clicked_tile == "fabric_warehouse": #Perform fabric warehouse action
					print("Performing fabric warehouse action")
					#print("Current player is Player", board.current_player + 1)
					
					playerlist[board.current_player].update_resources("fabric", int(playerlist[board.current_player].resources.get("max_res") - playerlist[board.current_player].resources.get("fabric")))
					
					draw_tile(frame, tilelist[2])
					update_resource_blocks(board, playerlist, units, "fabric", 0)
					draw_units(frame, font, units, playerlist, board)
					print(playerlist[board.current_player].name, "now has", playerlist[board.current_player].resources.get("lira"), "lira,", playerlist[board.current_player].resources.get("fabric"), "fabric,", playerlist[board.current_player].resources.get("spice"), "spice,", playerlist[board.current_player].resources.get("diamonds"), "diamonds and", playerlist[board.current_player].resources.get("fruit"), "fruit. The max amount of resources for this player is", playerlist[board.current_player].resources.get("max_res"))
					board.set_nextplayer()
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					draw_units(frame, font, units, playerlist, board)

				elif clicked_tile == "fruit_warehouse": #Perform fruit warehouse action
					print("Performing fruit warehouse action")
					#print("Current player is Player", board.current_player + 1)
					
					playerlist[board.current_player].update_resources("fruit", int(playerlist[board.current_player].resources.get("max_res") - playerlist[board.current_player].resources.get("fruit")))
					
					draw_tile(frame, tilelist[4])
					update_resource_blocks(board, playerlist, units, "fruit", 0)
					draw_units(frame, font, units, playerlist, board)
					print(playerlist[board.current_player].name, "now has", playerlist[board.current_player].resources.get("lira"), "lira,", playerlist[board.current_player].resources.get("fabric"), "fabric,", playerlist[board.current_player].resources.get("spice"), "spice,", playerlist[board.current_player].resources.get("diamonds"), "diamonds and", playerlist[board.current_player].resources.get("fruit"), "fruit. The max amount of resources for this player is", playerlist[board.current_player].resources.get("max_res"))
					board.set_nextplayer()
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					draw_units(frame, font, units, playerlist, board)

				elif clicked_tile == "spice_warehouse": #Perform spice warehouse action
					print("Performing spice warehouse action")
					print("Current player is Player", board.current_player + 1)
					
					playerlist[board.current_player].update_resources("spice", int(playerlist[board.current_player].resources.get("max_res") - playerlist[board.current_player].resources.get("spice")))
					
					draw_tile(frame, tilelist[7])
					update_resource_blocks(board, playerlist, units, "spice", 0)
					draw_units(frame, font, units, playerlist, board)
					print(playerlist[board.current_player].name, "now has", playerlist[board.current_player].resources.get("lira"), "lira,", playerlist[board.current_player].resources.get("fabric"), "fabric,", playerlist[board.current_player].resources.get("spice"), "spice,", playerlist[board.current_player].resources.get("diamonds"), "diamonds and", playerlist[board.current_player].resources.get("fruit"), "fruit. The max amount of resources for this player is", playerlist[board.current_player].resources.get("max_res"))
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					board.set_nextplayer()
					draw_units(frame, font, units, playerlist, board)

				elif clicked_tile == "black_market": #Perform Black Market action
					print("Performing black market action")
					print("Current player is Player", board.current_player + 1)

					option = 0
					display_message = "Please select an option: Press 1) fabric, 2) spice, 3) fruit"
					print(display_message)
					while not ((0 < option < 4) and (int(option))):
						option = get_keyboardinput(event)
						if not (0 < option < 4):
							print(display_message)
					if option == 1:
						draw_tile(frame, tilelist[8])
						update_resource_blocks(board, playerlist, units, "fabric", 1)
						draw_units(frame, font, units, playerlist, board)
					elif option == 2:
						draw_tile(frame, tilelist[8])
						update_resource_blocks(board, playerlist, units, "spice", 1)
						draw_units(frame, font, units, playerlist, board)
					else:
						draw_tile(frame, tilelist[8])
						update_resource_blocks(board, playerlist, units, "fruit", 1)
						draw_units(frame, font, units, playerlist, board)
					
					print("Rolling the dice to see if you win any diamonds...")
					dice_roll = roll_dice(board, frame, font, playerlist, tilelist, units) 
					if dice_roll > 10:
						print("Congratulations, you have won 3 diamonds!")
						#playerlist[board.current_player].update_resources("diamonds", 2)
						draw_tile(frame, tilelist[8])
						update_resource_blocks(board, playerlist, units, "diamonds", 3)
						draw_units(frame, font, units, playerlist, board) 
					elif dice_roll > 8:
						print("Congratulations, you have won 2 diamonds!")
						#playerlist[board.current_player].update_resources("diamonds", 2)
						draw_tile(frame, tilelist[8])
						update_resource_blocks(board, playerlist, units, "diamonds", 2)
						draw_units(frame, font, units, playerlist, board) 
					elif dice_roll > 6:
						print("Congratulations, you have won 1 diamond!")
						draw_tile(frame, tilelist[8])
						update_resource_blocks(board, playerlist, units, "diamonds", 1)
						draw_units(frame, font, units, playerlist, board) 
					else:
						print("Too bad, you receive no diamonds...")

					print(playerlist[board.current_player].name, "now has", playerlist[board.current_player].resources.get("lira"), "lira,", playerlist[board.current_player].resources.get("fabric"), "fabric,", playerlist[board.current_player].resources.get("spice"), "spice,", playerlist[board.current_player].resources.get("diamonds"), "diamonds and", playerlist[board.current_player].resources.get("fruit"), "fruit. The max amount of resources for this player is", playerlist[board.current_player].resources.get("max_res"))
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					board.set_nextplayer()
					draw_units(frame, font, units, playerlist, board)

				elif clicked_tile == "small_market": #Perform Small Market action
					print("Performing small_market market action")
					print("Current player is Player", board.current_player + 1)
					
					sold_resources = {"diamonds": 0, "fabric": 0, "spice": 0, "fruit": 0}
					display_message1 = "Please select an option: Press 1) diamonds, 2) fabric, 3) spice, 4) fruit"
					display_message2 = "Enter 0 if you want to stop selling resources"

					while clicked_object != "end_turn_button":
						if mouse_clicked():
							clicked_tile, clicked_object = get_clicked_item(tilelist, units)
							#print(f"Clicked object is \"{clicked_object}\"")

							diamonds_vendable = sold_resources.get("diamonds") < tilelist[10].merchandise[0].get("diamonds")
							fabric_vendable = sold_resources.get("fabric") < tilelist[10].merchandise[0].get("fabric")
							spice_vendable = sold_resources.get("spice") < tilelist[10].merchandise[0].get("spice")
							fruit_vendable = sold_resources.get("fruit") < tilelist[10].merchandise[0].get("fruit")

							if (clicked_object == "resourceblock_1" or clicked_object == "resourceblock_5") and playerlist[board.current_player].resources.get("diamonds") > 0 and diamonds_vendable:
								sold_resources["diamonds"] += 1
								update_resource_blocks(board, playerlist, units, "diamonds", -1)
							elif (clicked_object == "resourceblock_2" or clicked_object == "resourceblock_6") and playerlist[board.current_player].resources.get("fabric") > 0 and fabric_vendable:
								sold_resources["fabric"] += 1
								update_resource_blocks(board, playerlist, units, "fabric", -1)
							elif (clicked_object == "resourceblock_3" or clicked_object == "resourceblock_7") and playerlist[board.current_player].resources.get("spice") > 0 and spice_vendable:
								sold_resources["spice"] += 1
								update_resource_blocks(board, playerlist, units, "spice", -1)
							elif (clicked_object == "resourceblock_4" or clicked_object == "resourceblock_8") and playerlist[board.current_player].resources.get("fruit") > 0 and fruit_vendable:
								sold_resources["fruit"] += 1
								update_resource_blocks(board, playerlist, units, "fruit", -1)
							elif clicked_object == "None":
								print("\tTo sell a resource, please click on your slider block of the desired resource")
							else:
								if not (diamonds_vendable or fabric_vendable or spice_vendable or fruit_vendable):
									print("\tThe market doesn't allow this particular resource to be sold (anymore)")
								else:
									print("You do not have sufficient resources to sell that")
							print("\tSo far, you have sold", sum(sold_resources.values()), "resources")
							draw_units(frame, font, units, playerlist, board)
							pygame.display.update()

					reward = tilelist[10].reward_mapping(str(sum(sold_resources.values()))) # Sum of sold resources as string mapped to lira reward
					print("You have sold", str(sum(sold_resources.values())), "resources, rewarding you", reward, "lira!")
					print("")
					playerlist[board.current_player].update_resources("lira", reward)

					tilelist[10].switch_stack()
					units.get("small_market_tiles").update_image_path("images/small_market_tile" + tilelist[10].merchandise[0].get("tilenumber") + ".png")
					
					draw_tile(frame, tilelist[10])
					board.set_nextplayer()
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					draw_units(frame, font, units, playerlist, board)

				elif clicked_tile == "tea_house": #Perform teahouse action
					print("Performing tea house action, type in a number between 3-12 followed by an enter")
					bet = 1
					while not ((2 < bet < 13) and (int(bet))):
						bet = get_keyboardinput(event)
						if not (2 < bet < 13):
							print("Your bet must be between 3 and 12, please try again.")
					print("Your bet is", bet, "... Rolling the dice...")
					dice_roll = roll_dice(board, frame, font, playerlist, tilelist, units)
					if (dice_roll >= bet):
						messages = ["Congrats, you receive", bet, "lira!", "player", playerlist[board.current_player].name, " now has ", playerlist[board.current_player].resources.get('lira'), " lira"]
						playerlist[board.current_player].update_resources("lira", bet)
					else:
						messages = ["Too bad, you receive only 2 lira", "player", playerlist[board.current_player].name, " now has ", playerlist[board.current_player].resources.get('lira'), " lira"]
						playerlist[board.current_player].update_resources("lira", 2)
					draw_tile(frame, tilelist[11])
					draw_units(frame, font, units, playerlist, board)
					# time.sleep(1)
					for message in messages:
						print(messages)
					board.set_nextplayer()
					draw_units(frame, font, units, playerlist, board)
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
				
				elif clicked_tile == "wainwright": #Perform wainwright action
					print("Performing wainwright action")
					print("Current player is Player", board.current_player + 1)
					if playerlist[board.current_player].resources.get("lira") >= 7 and playerlist[board.current_player].resources.get("max_res") < 5:
						playerlist[board.current_player].update_resources("lira", -7)
						playerlist[board.current_player].update_resources("max_res", 1)
						#update resource image for this player
						#print("current player is", playerlist[board.current_player].name)
						if playerlist[board.current_player].name == "Player1": #Player 1
							units.get("resource_p1").update_image_path("images/resource" + str(playerlist[board.current_player].resources.get("max_res")) + "_1.png")
							print("Player 1 bought a cart extension")
						else: #Player 2
							units.get("resource_p2").update_image_path("images/resource" + str(playerlist[board.current_player].resources.get("max_res")) + "_2.png")
							print("Player 2 bought a cart extension")

						draw_tile(frame, tilelist[1])
						draw_units(frame, font, units, playerlist, board)
						board.set_nextplayer()
						draw_units(frame, font, units, playerlist, board)
					elif (not playerlist[board.current_player].resources.get("max_res") < 5):
						print(playerlist[board.current_player].name, "already has a full wainwright!")
					else:
						print("You do not have sufficient lira to buy a cart extension, you have", playerlist[board.current_player].resources.get("lira"), "lira.")
					print(playerlist[board.current_player].name, "now has", playerlist[board.current_player].resources.get("lira"), "lira,", playerlist[board.current_player].resources.get("fabric"), "fabric,", playerlist[board.current_player].resources.get("spice"), "spice,", playerlist[board.current_player].resources.get("diamonds"), "diamonds and", playerlist[board.current_player].resources.get("fruit"), "fruit. The max amount of resources for this player is", playerlist[board.current_player].resources.get("max_res"))
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")

				elif clicked_tile == "sultans_palace": #Perform Sultans Palace action
					print("Performing sultans palace's action")
					print("Current player is Player", board.current_player + 1)
					
					if (tile.has_sufficient_resources(playerlist[board.current_player])) and (tile.gemstone_amount > 0): #Player has sufficient resources to pay requirements
						for item in tilelist[12].resources_price:
							if item != "winnow":
								update_resource_blocks(board, playerlist, units, item, -1)
							else:
								# Then pay the resource(s) of choice (the winnow)
								sold = False
								while not sold: #Player has to pick a resource possession to continue
									display_message = "Now, please select your resource of choice to sell: Press 1) diamonds, 2) fabric, 3) spice, 4) fruit"
									option = prompt_input(event, display_message, [0, 5])
									if option == 1 and playerlist[board.current_player].resources.get("diamonds") > 0:
										update_resource_blocks(board, playerlist, units, "diamonds", -1)
										sold = True
									elif option == 2 and playerlist[board.current_player].resources.get("fabric") > 0:
										update_resource_blocks(board, playerlist, units, "fabric", -1)
										sold = True
									elif option == 3 and playerlist[board.current_player].resources.get("spice") > 0:
										update_resource_blocks(board, playerlist, units, "spice", -1)
										sold = True
									elif option == 4 and playerlist[board.current_player].resources.get("fruit") > 0:
										update_resource_blocks(board, playerlist, units, "fruit", -1)
										sold = True
									else:
										print("You do not have sufficient resources to sell that, select another resource")
							
						playerlist[board.current_player].update_resources("gemstones", 1)
						print(playerlist[board.current_player].name, "bought a gemstone!")
						
						units.get("gem_sultan" + str(7 - tilelist[12].gemstone_amount)).set_x(playerlist[board.current_player].gemstone_slots[0][0])
						units.get("gem_sultan" + str(7 - tilelist[12].gemstone_amount)).set_y(playerlist[board.current_player].gemstone_slots[0][1])
						playerlist[board.current_player].update_gemstone_slots()

						tile.increase_resources_price()
						tile.decrease_gemstone_amount()
						board.set_nextplayer()
					else:
						if tile.gemstone_amount == 0:
							print("The Sultan's palace ran out of gems, find another way to collect more gemstones!")
						else:
							print("You do not have sufficient resources to purchase a gemstone!")
					
					print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					draw_tile(frame, tilelist[12])
					draw_units(frame, font, units, playerlist, board)

				elif clicked_tile == "gemstone_dealer": #Perform gemstone dealer action
					print("Performing gemstone dealer action")
					print("Current player is Player", board.current_player + 1)
					if playerlist[board.current_player].resources.get("lira") >= tilelist[15].gemstone_price and tilelist[15].gemstone_amount > 0:
						playerlist[board.current_player].update_resources("lira", -(tilelist[15].gemstone_price))
						playerlist[board.current_player].update_resources("gemstones", 1)
						print(playerlist[board.current_player].name, "bought a gemstone!")
						units.get("gem_gemstone" + str(10 - tile.gemstone_amount)).set_x(playerlist[board.current_player].gemstone_slots[0][0])
						units.get("gem_gemstone" + str(10 - tile.gemstone_amount)).set_y(playerlist[board.current_player].gemstone_slots[0][1])
						playerlist[board.current_player].update_gemstone_slots()

						tilelist[15].increase_gemstone_price()
						tilelist[15].decrease_gemstone_amount()
						board.set_nextplayer()
						print("Next player's turn, go ahead", playerlist[board.current_player].name, "!")
					else:
						if tilelist[15].gemstone_amount == 0:
							print("The gemstone dealer ran out of gems, find another way to collect more gemstones!")
						else:
							print("You do not have sufficient resources to purchase a gemstone!")
					
					draw_tile(frame, tilelist[15])
					draw_units(frame, font, units, playerlist, board)
	
			if event.type == QUIT or (event.type is KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		pygame.display.update()
		fpsClock.tick(fps)

def update_resource_blocks(board, playerlist, units, name, amount):
	if "diamonds" in name:
		playerlist[board.current_player].update_resources("diamonds", amount)
		if board.current_player == 0:
			units.get("resourceblock_1").set_x(units.get("resource_p1").x + units.get("resource_p1").width*(375/1604) + (playerlist[board.current_player].resources.get("diamonds") * units.get("resource_p1").width*(185/1604)))
		else:
			units.get("resourceblock_5").set_x(units.get("resource_p2").x + units.get("resource_p2").width*(375/1604) + (playerlist[board.current_player].resources.get("diamonds") * units.get("resource_p2").width*(185/1604)))
	elif "fabric" in name:
		playerlist[board.current_player].update_resources("fabric", amount)
		if board.current_player == 0:
			units.get("resourceblock_2").set_x(units.get("resource_p1").x + units.get("resource_p1").width*(375/1604) + (playerlist[board.current_player].resources.get("fabric") * units.get("resource_p1").width*(185/1604)))
		else:
			units.get("resourceblock_6").set_x(units.get("resource_p2").x + units.get("resource_p2").width*(375/1604) + (playerlist[board.current_player].resources.get("fabric") * units.get("resource_p2").width*(185/1604)))
	elif "spice" in name:
		playerlist[board.current_player].update_resources("spice", amount)
		if board.current_player == 0:
			units.get("resourceblock_3").set_x(units.get("resource_p1").x + units.get("resource_p1").width*(375/1604) + (playerlist[board.current_player].resources.get("spice") * units.get("resource_p1").width*(185/1604)))
		else:
			units.get("resourceblock_7").set_x(units.get("resource_p2").x + units.get("resource_p2").width*(375/1604) + (playerlist[board.current_player].resources.get("spice") * units.get("resource_p2").width*(185/1604)))
	elif "fruit" in name:
		playerlist[board.current_player].update_resources("fruit", amount)
		if board.current_player == 0:
			units.get("resourceblock_4").set_x(units.get("resource_p1").x + units.get("resource_p1").width*(375/1604) + (playerlist[board.current_player].resources.get("fruit") * units.get("resource_p1").width*(186/1604)))
		else:
			units.get("resourceblock_8").set_x(units.get("resource_p2").x + units.get("resource_p2").width*(375/1604) + (playerlist[board.current_player].resources.get("fruit") * units.get("resource_p2").width*(186/1604)))

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
			if numbers_entered != "":
				option = int(numbers_entered)
			else:
				option = 3
			#print("option from get get_keyboardinput", option)

	return option

def get_clicked_item(tilelist, units):
	clicked_tile = "None"
	clicked_object = "None"
	pos_x = pygame.mouse.get_pos()[0]
	pos_y = pygame.mouse.get_pos()[1]
	for tile in tilelist:
		if pos_x > tile.x and pos_x < (tile.x + tilewidth) and pos_y > tile.y and pos_y < (tile.y + tileheight):
			clicked_tile = tile.name
			break
	for key, unit in units.items():
		if ("p1" not in key and "p2" not in key):
			if pos_x > unit.x and pos_x < (unit.x + unit.width) and pos_y > unit.y and pos_y < (unit.y + unit.height):
				clicked_object = key
				break
	return clicked_tile, clicked_object

def mouse_clicked():
	for event in pygame.event.get():
		#print(f"Nested Event: {event}")
		if event.type == pygame.MOUSEBUTTONUP:
			return True

def prompt_input(event, display_message, range):
	option = 0
	print(display_message)
	while not ((range[0] < option < range[1]) and (type(option) == int)):
		option = get_keyboardinput(event)
		if not (range[0] < option < range[1]):
			print(display_message)
	return option

def roll_dice(board, frame, font, playerlist, tilelist, units):
	global p1_windowx
	global p1_windowwidth
	global p1_windowy
	global tileheight
	global tilewidth
	global tilegap

	dice1_x = p1_windowx + ((p1_windowwidth - tilewidth)/2) + randint(int(tilewidth / 8), int(tileheight - 5 * tilegap)) #40, 220
	dice1_y = p1_windowy + tileheight + (5 * tilegap) + randint(int(tileheight / 9), int(tileheight / 2)) #25, 115
	dice2_x = p1_windowx + ((p1_windowwidth - tilewidth)/2) + randint(int(tilewidth / 8), int(tileheight - 5 * tilegap)) #40, 220
	dice2_y = p1_windowy + tileheight + (5 * tilegap) + randint(int(tileheight / 9), int(tileheight / 2)) #25, 115
	while (dice_offset(dice1_x, dice1_y, dice2_x, dice2_y)): #Replace the second die while they're overlapping
		dice2_x = p1_windowx + ((p1_windowwidth - tilewidth)/2) + randint(int(tilewidth / 8), int(tileheight))
		dice2_y = p1_windowy + tileheight + (5 * tilegap) + randint(int(tileheight / 9), int(tileheight / 2))

	# x_distance = 0.01
	# pause = 0.5
	# while x_distance < 5:
	dice1 = Object(dice1_x, dice1_y, tilewidth/5, tilewidth/5, "images/die1.png") # 40 <= x <= 220, 25 <= y <= 115
	randomnumber = randint(1, 6)
	dice1.update_image_path("images/die" + str(randomnumber) + ".png")
	image = pygame.image.load(dice1.image_path).convert()
	image = pygame.transform.smoothscale(image, (int(dice1.width), int(dice1.height)))
	
	dice2 = Object(dice2_x, dice2_y, tilewidth/5, tilewidth/5, "images/die1.png") # 40 <= x <= 220, 25 <= y <= 115
	randomnumber2 = randint(1, 6)
	dice2.update_image_path("images/die" + str(randomnumber2) + ".png")
	image2 = pygame.image.load(dice2.image_path).convert()
	image2 = pygame.transform.smoothscale(image2, (int(dice2.width), int(dice2.height)))

	#BEFORE blitting: draw background & all units, so the previous dice will be erased
	draw_boxes(frame, "box")
	draw_units(frame, font, units, playerlist, board)

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
