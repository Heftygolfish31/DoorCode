# Door Code Python
version = "0.3"

# IMPORTS
# Import the os package for reading terminal data
import os
# Import the time package for sleeping
import time

# COLOURS
class Colour:
	END="\033[0m"
	RED="\033[31m"
	GREEN="\033[32m"
	YELLOW="\033[33m"

# KILLER
# Kill the program and check first
def killer():
	# Are you sure?
	check = input(f"{Colour.RED}Kill the program? [Y/n]:{Colour.END}")
	# Yes, I'm sure
	if check.lower() in ["", "y", "yes"]:
		print(f"{Colour.GREEN}Goodbye!{Colour.END}")
		exit()
	# Neither
	elif check.lower() not in ["n", "no"]:
		print(f"{Colour.RED}Input not recognised.{Colour.END}")
		killer()
	# No, continue the program

# SELECT A LOCATION
# Find and load the target location by file
def location_selection():

	# Location Variables
	location = ""
	locations_dir = os.listdir("./locations")
	location_index = None
	location_human_name = ""
	locations_human_names = []

	# Open the locations directory
	assert len(locations_dir) > 0, "No locations found."

	# Retrieve human names for each file
	for location in locations_dir:
		locations_human_names.append(open(f"./locations/{location}", "r").readline()[:-1])

	# If the default file exists but has a corrupted inside, don't use it
	if "default" in locations_dir:
		default_contents = open(f"./locations/default", "r").readline()[:-1]
		if default_contents not in locations_dir and not default_contents == "default":
			locations_human_names.remove(locations_dir.index("default"))
			locations_dir.remove("default")
		
	# If the default file is still listed, it must not be corrupted
	if "default" in locations_dir:
		location_index = locations_dir.index("default")
	# There is only one file, use it
	elif len(locations_dir) == 1:
		location_index = 0
	else:
		print(f"Multiple locations found.")
		print(f"{len(locations_human_names)} locations found:")
		# List them
		i = 0
		for _ in locations_human_names:
			print(f"{i+1}. {Colour.YELLOW}{locations_human_names[i]}{Colour.END} (saved as {Colour.YELLOW}'{locations_dir[i]}{Colour.END})")
			i += 1
		# The user now chooses one
		choice = input("Select a location: ")

		# Just came back from dental surgery.
		#   Have never wanted donner more than right now.
		#    - S

		try:
			# File name inputted
			if choice in locations_dir:
				location_index = locations_dir.index(choice)
			# Human name inputted
			elif choice in locations_human_names:
				location_index = locations_human_names.index(choice)
			# Index inputted
			elif int(choice) >= 1 and int(choice) <= i:
				location_index = int(choice)-1
		except ValueError:
			pass

	# Missed all the checks
	if location_index == None:
		print("Location not recognised.")
		return location_selection()

	# Update the function variables to match
	location = locations_dir[int(location_index)]
	location_human_name = locations_human_names[int(location_index)]
	# Notify the user
	print(f"{Colour.GREEN}{location_human_name}{Colour.END} (at '{location}') selected.")
	return f"./locations/{location}"


# SEARCH FOR A ROOM
# Load the location information and find the target
def search(location, target):
	# Make sure the location you want to access does, in fact, exist
	assert os.path.exists(location), f"File ('{location}') does not exist."

	# Get the codes from the file at specified location
	file_contents = open(location, "r").readlines()
	# Get some data to do some end-user stuff
	human_name = file_contents[0]


	# Find the target
	rooms = []
	room_type = "UNKNOWN:"
	exact_match = False
	for room in file_contents:
		# Make a raw copy of the record
		raw_room = room
		# Split the record into managable chunks
		room = room[:-1].split(",")

		# Check! Is this record a label?
		if len(room) == 1 and room[0][-1] == ":":
			# If it is, update the room type
			room_type = room[0]
			# This is a new section to the file, find another exact match
			exact_match = False
			# Skip to the next record: it can't be a label and a room code!
			continue

		# I sit in my room listening to 'Wait' by C418...
		#  It is dark and the light is calming...
		#   Why must all the best feelings come at 22:23?
		#    - S

		# If its a copy, don't bother
		if [room_type, room] in rooms:
			continue

		# If an exact match hasn't been found yet,
		#  and the target is a substring of this room,
		#   and it's not entierly a duplicate
		if not exact_match and target in room[0]:
			# If the 'exact' match has been found
			if target == room[0]:

				# Kill all rooms with this type that don't match exactly
				dead_rooms = []
				# Collect all the rooms which aren't exact
				for dead_room in rooms:
					# If the room type is a copy, 
					if dead_room[0] == room_type:
						dead_rooms.append(dead_room)
				# Remove them all from the rooms
				for dead_room in dead_rooms:
					rooms.remove(dead_room)

				# We have found an exact match
				#  Don't stop until a new type is found
				exact_match = True

			# Add the room to the results list
			rooms.append([room_type, room])

	print(rooms)

search(location_selection(), input("> "))