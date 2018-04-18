class Players:
	def __init__(self, player, tilelist, tilewidth, tileheight, units):
		additional_lira = player
		self.name = "Player" + str(player + 1)
		self.resources = {"lira": 2 + additional_lira, "gemstones": 0, "diamonds": 0, "fruit": 0, "fabric": 0, "spice": 0, "max_res": 2}
		self.gemstone_slots = [
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(400/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(605/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(810/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(1010/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(1215/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)], 
			[units.get("resource_p" + str(player + 1)).x + tilewidth*(1415/1605), units.get("resource_p" + str(player + 1)).y + tileheight*(770/1072)] 
		]
		self.units_stack = [self.name + "_merchant1", self.name + "_servant1", self.name + "_servant2", self.name + "_servant3", self.name + "_servant4"]
		self.location = tilelist[6].location

	def update_resources(self, resource, amount): #self, string, integer
		if resource == "diamonds" or resource == "fruit" or resource == "fabric" or resource == "spice":
			if (self.resources.get(resource) + amount) >= self.resources.get("max_res"):
				self.resources[resource] = self.resources.get("max_res");
			else:
				self.resources[resource] = self.resources.get(resource) + amount
		else:
			self.resources[resource] = self.resources.get(resource) + amount
		# elif resource == "max_res": #Cannot have more than 5 resources at a time
		# 	if self.resources[resource] < 5:
		# 		self.resources[resource] = self.resources.get(resource) + amount
		# 	else:
		# 		self.resources[resource] = 5;

	def update_gemstone_slots(self):
		self.gemstone_slots.pop(0)

	def update_location(self, location):
		self.location = location

class Tiles:
	def __init__(self, name, location, boardx, boardy, tilewidth, tileheight, tilegap):
		self.name = name
		self.tilenumbers = []
		self.location = location
		self.x = boardy + ((self.location[1] - 1) * (tilewidth + tilegap))
		self.y = boardx + ((self.location[0] - 1) * (tileheight + tilegap))
		self.players_present = []
		self.units_stack = []
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
			self.resources_price = ["diamonds", "fabric", "spice", "fruit", "winnow"]
			self.resources_queue = ["diamonds", "fabric", "spice", "fruit", "winnow"]
			self.gemstone_amount = 6

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
		self.resources_price.append(self.resources_queue[0])
		self.resources_price.sort()
		self.resources_queue.pop(0)

	def has_sufficient_resources(self, current_player):
		#print("resource price = ", self.resources_price)
		result = False
		nchoice = self.resources_price.count("choice")
		if (current_player.resources.get("diamonds") >= self.resources_price.count("diamonds")) and \
			(current_player.resources.get("fabric") >= self.resources_price.count("fabric")) and \
			current_player.resources.get("spice") >= self.resources_price.count("spice") and \
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
		#self.name = name
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.image_path = image_path

	#def update_name(self, newname):
	#	self.name = newname

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