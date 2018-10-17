from random import shuffle

class Players:
	def __init__(self, player, tilelist, tilewidth, tileheight, units, tokens):
		additional_lira = player
		self.player = "p" + str(player + 1)
		self.name = "Player" + str(player + 1)
		self.resources = {"lira": 50 + additional_lira, "gemstones": 0, "diamonds": 0, "fruit": 0, "fabric": 0, "spice": 0, "max_res": 2, "bonuses": []}
		self.gemstone_slots = [
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(400/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(605/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(810/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(1010/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(1215/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(1415/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)] 
		]
		if "Player1" in self.name:
			self.mosque_tile_slots = [
				[units.get("resource_p" + str(player + 1)).x + 0 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y - (tilewidth/3.06)],
				[units.get("resource_p" + str(player + 1)).x + 0.5 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y - (tilewidth/3.06)],
				[units.get("resource_p" + str(player + 1)).x + 1 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y - (tilewidth/3.06)],
				[units.get("resource_p" + str(player + 1)).x + 1.5 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y - (tilewidth/3.06)]
			]
		else:
			self.mosque_tile_slots = [
				[units.get("resource_p" + str(player + 1)).x + 0 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y + tileheight],
				[units.get("resource_p" + str(player + 1)).x + 0.5 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y + tileheight],
				[units.get("resource_p" + str(player + 1)).x + 1 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y + tileheight],
				[units.get("resource_p" + str(player + 1)).x + 1.5 * tilewidth/3.06, units.get("resource_p" + str(player + 1)).y + tileheight]
			]
		
		self.token_stack = []
		for i in range(1, 5): # Insert all assistants in a stack at start of the game
			self.token_stack.append(self.player + "_assistant_" + str(i))

	def update_resources(self, resource, amount): #self, string, integer
		if resource == "diamonds" or resource == "fruit" or resource == "fabric" or resource == "spice":
			if (self.resources.get(resource) + amount) >= self.resources.get("max_res"):
				self.resources[resource] = self.resources.get("max_res");
			else:
				self.resources[resource] = self.resources.get(resource) + amount
		else:
			self.resources[resource] = self.resources.get(resource) + amount

	def update_gemstone_slots(self):
		self.gemstone_slots.pop(0)

	def update_tile_stack(self):
		self.mosque_tile_slots.pop(0)

	def update_bonuses(self, name, bonus):
		self.resources.get("bonuses").insert(0, [name, bonus])

	def insert_token_stack(self, token_name):
		self.token_stack.append(token_name)

	def pop_token_stack(self):
		self.token_stack.pop(0)
	

class Tiles:
	def __init__(self, name, index, location, boardx, boardy, tilewidth, tileheight, tilegap):
		self.name = name
		self.index = index
		self.location = location
		self.x = boardy + ((self.location[1] - 1) * (tilewidth + tilegap))
		self.y = boardx + ((self.location[0] - 1) * (tileheight + tilegap))
		self.token_grid = {
							"p1_merchant": [self.x + (tilewidth / 4 + tilewidth / 24), self.y + (tileheight / 6)],
							"p1_assistant": [self.x + (tilewidth / 24) + tilegap, self.y + (tileheight / 6) * 2],
							"p1_prisoner": [self.x + (tilewidth / 4 + tilewidth / 24), self.y + (tileheight / 6) * 2],

							"p2_merchant": [self.x + (tilewidth / 2 + tilewidth / 24), self.y + (tileheight / 6)],
							"p2_assistant": [self.x + ((tilewidth / 4) * 3 + tilewidth / 24), self.y + (tileheight / 6) * 2],
							"p2_prisoner": [self.x + (tilewidth / 2 + tilewidth / 24), self.y + (tileheight / 6) * 2]
						  }

		if self.name == "postal_office":
			self.blocks = [
				{"fabric": 0, "lira_2_1": 0, "diamonds": 0, "lira_2_2": 0, "spice": 1, "lira_1_1": 1, "fruit": 1, "lira_1_2": 1}, 
				{"fabric": 1, "lira_2_1": 0, "diamonds": 0, "lira_2_2": 0, "spice": 0, "lira_1_1": 1, "fruit": 1, "lira_1_2": 1}, 
				{"fabric": 1, "lira_2_1": 1, "diamonds": 0, "lira_2_2": 0, "spice": 0, "lira_1_1": 0, "fruit": 1, "lira_1_2": 1},
				{"fabric": 1, "lira_2_1": 1, "diamonds": 1, "lira_2_2": 0, "spice": 0, "lira_1_1": 0, "fruit": 0, "lira_1_2": 1},
				{"fabric": 1, "lira_2_1": 1, "diamonds": 1, "lira_2_2": 1, "spice": 0, "lira_1_1": 0, "fruit": 0, "lira_1_2": 0}
				]
		if self.name == "gemstone_dealer":
			self.gemstone_price = 15
			self.gemstone_amount = 9
		if self.name == "sultans_palace":
			self.resources_price = ["diamonds", "fabric", "flavourspice", "fruit", "winnow"] # Called spice flavourspice so the sort puts it between fabric and fruit!
			self.resources_queue = ["diamonds", "fabric", "flavourspice", "fruit", "winnow"] # Winnow is resource of choice, named to be last alphabetically
			self.gemstone_amount = 6
		if self.name == "wainwright" or self.name == "small_mosque" or self.name == "great_mosque":
			self.gemstone_amount = 2
		if "small_mosque" in self.name:
			self.tile_stack = ["small_mosque_fabric_2", "small_mosque_fabric_4", "small_mosque_spice_2", "small_mosque_spice_4"]
		if "great_mosque" in self.name: 
			self.tile_stack = ["great_mosque_diamonds_2", "great_mosque_diamonds_4", "great_mosque_fruit_2", "great_mosque_fruit_4"]
		if self.name == "small_market":
			self.merchandise = [
				{"tilenumber": "1", "diamonds": 0, "fabric": 1, "spice": 3, "fruit": 1}, 
				{"tilenumber": "2", "diamonds": 1, "fabric": 1, "spice": 2, "fruit": 1},
				{"tilenumber": "3", "diamonds": 1, "fabric": 1, "spice": 1, "fruit": 2},
				{"tilenumber": "4", "diamonds": 0, "fabric": 1, "spice": 2, "fruit": 2},
				{"tilenumber": "5", "diamonds": 1, "fabric": 0, "spice": 2, "fruit": 2}
				]
			shuffle(self.merchandise)
		if self.name == "large_market":
			self.merchandise = [
				{"tilenumber": "1", "diamonds": 2, "fabric": 2, "spice": 1, "fruit": 0}, 
				{"tilenumber": "2", "diamonds": 2, "fabric": 1, "spice": 1, "fruit": 1},
				{"tilenumber": "3", "diamonds": 3, "fabric": 1, "spice": 0, "fruit": 1},
				{"tilenumber": "4", "diamonds": 3, "fabric": 1, "spice": 1, "fruit": 0},
				{"tilenumber": "5", "diamonds": 2, "fabric": 2, "spice": 0, "fruit": 1}
				]
			shuffle(self.merchandise)
			
	# Postal office functions
	def move_postalblocks(self, blocks):
		blocks.append(blocks.pop(0))

	# Gemstone dealer functions
	def increase_gemstone_price(self):
		self.gemstone_price = self.gemstone_price + 1

	def decrease_gemstone_amount(self):
		self.gemstone_amount = self.gemstone_amount - 1

	# Sultans Palace functions
	def increase_resources_price(self):
		if len(self.resources_queue) != 0:
			self.resources_price.append(self.resources_queue[0])
			self.resources_price.sort()
			self.resources_queue.pop(0)

	def has_sufficient_resources(self, current_player):
		result = False
		nchoice = self.resources_price.count("choice")
		if (current_player.resources.get("diamonds") >= self.resources_price.count("diamonds")) and \
			(current_player.resources.get("fabric") >= self.resources_price.count("fabric")) and \
			current_player.resources.get("spice") >= self.resources_price.count("flavourspice") and \
			current_player.resources.get("fruit") >= self.resources_price.count("fruit") and \
			self.has_leftover_choice(current_player):
			result = True
		return result

	def has_leftover_choice(self, current_player):
		result = False
		diamondsleft = current_player.resources.get("diamonds") - self.resources_price.count("diamonds")
		fabricleft = current_player.resources.get("fabric") - self.resources_price.count("fabric")
		spiceleft = current_player.resources.get("spice") - self.resources_price.count("spice")
		fruitleft = current_player.resources.get("fruit") - self.resources_price.count("fruit")
		if sum([diamondsleft, fabricleft, spiceleft, fruitleft]) >= self.resources_price.count("choice"):
			result = True
		return result

	# Market functions
	def switch_stack(self):
		self.merchandise = self.merchandise[1:] + self.merchandise[:1]
		#print("stack after switching = ", self.merchandise)

	def reward_mapping(self, amount): #Takes the amount of resources sold at the market as parm
		if self.name == "small_market":
			mapping_dict = {"0": 0, "1": 2, "2": 5, "3": 9, "4": 14, "5": 20}
		else: #Large market
			mapping_dict = {"0": 0, "1": 3, "2": 7, "3": 12, "4": 18, "5": 25}
		return mapping_dict.get(amount)

	# Mosque functions
	def update_tile_stack(self, name):
		self.tile_stack.remove(name)
	def get_stack_top(self, name): # In: small_mosque_fabric_4, Out: small_mosque_fabric_2 (top of stack beginning with small_mosque_1)
		for item in self.tile_stack:
			if name in item:
				return item

	# General functions
	def update_players_present(self, player, action):
		if (action == "addition"):
			self.players_present.append(player)
		else: #deletion
			self.players_present.remove(player)

	def update_units_stack(self, player, unit):
		self.units_stack.append(unit)

class Object:
	def __init__(self, x, y, width, height, image_path):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.image_path = image_path

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

class Token:
	def __init__(self, name, image_path, visibility, entry_fee, tile_number):
		self.name = name
		self.image_path = image_path
		self.visible = visibility
		self.entry_fee = entry_fee
		self.tile_number = tile_number

	def switch_visibility(self):
		#print(f"visibility before: {self.visible} for token {self.name}")
		self.visible = not self.visible
		#print(f"visibility after: {self.visible} for token {self.name}")

	def set_tile_number(self, tile_number):
		self.tile_number = tile_number

class Board:
	def __init__(self, number_of_players, number_of_tiles):
		self.number_of_players = number_of_players
		self.number_of_tiles = number_of_tiles
		self.current_player = 0
		self.next_player_button = "images/buttonblue.png"
		
	def set_nextplayer(self):
		if not (self.current_player + 1) > self.number_of_players - 1:
			self.current_player = self.current_player + 1
			self.next_player_button = "images/buttonred.png"
		else:
			self.current_player = 0
			self.next_player_button = "images/buttonblue.png"
		print(f"Next player's turn, go ahead Player{self.current_player + 1}!")

	def move_is_legal_distance(self, origin, destination): #Tile1, Tile2
		#print("move from is", move_from)
		#print("move to is", move_to)

		#x1, y1 = origin[0], origin[1]
		#x2, y2 = destination[0], destination[1]
		#xdist = abs(destination[0] - origin[0])
		#ydist = abs(destination[1] - origin[1])

		if ((abs(destination[0] - origin[0]) == 0 and (abs(destination[1] - origin[1]) == 1 or abs(destination[1] - origin[1]) == 2)) or 
			(abs(destination[1] - origin[1]) == 0 and (abs(destination[0] - origin[0]) == 1 or abs(destination[0] - origin[0]) == 2)) or 
			(abs(destination[0] - origin[0]) == abs(destination[1] - origin[1]) == 1)):
			return True
		else:
			return False

	def move_is_legal_cost(self, playerlist, tokens, destination_tile):
		fee = 0
		for token_name, token in tokens.items():
			#print(f"token image path is {token.image_path}, token tile number is {token.tile_number} and destination tile index is {destination_tile.index}")
			if token.entry_fee and (token.tile_number == destination_tile.index):
				fee += 2
		
		if playerlist[self.current_player].resources.get("lira") >= fee or destination_tile.name == "fountain":
			return True
		else:
			return False