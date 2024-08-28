# Door Code Python
version = "0.5"

# IMPORTS
# Import the os package for reading terminal data
import os
# Import the time package for sleeping
import time

# COLOURS
# ANSI codes used to format terminal text
class Colour:
	END="\033[0m"
	BOLD="\033[1m"
	UNDERLINE="\033[4m"
	RED="\033[31m"
	GREEN="\033[32m"
	YELLOW="\033[33m"
	CYAN="\033[36m"

# WELCOME
# Welcome the user on startup
def welcome():
	# The startup message identifying the program
	first_line = f"{Colour.UNDERLINE}*{Colour.END} {Colour.BOLD}{Colour.CYAN}Python Doorcode v{version}{Colour.END} {Colour.UNDERLINE}*{Colour.END}"
	print(f"{first_line}")

# CLEAR
# Clear the screen; start afresh
def clear(toWelcome=True):
	# One of my favorite Python one liners
	#  After reverse shells, of course
	os.system('cls' if os.name == 'nt' else 'clear')
	# If the `toWelcome` flag is set, the welcome message leads everything
	if toWelcome:
		welcome()

# COUNTDOWN
# Simulate a single-line animation to show a clock timeout, in seconds
def countdown(action, count=5):
	# Loop for the number of times to sleep by
	while count > 0:
		# Print the warning
		print(f"{Colour.RED}{action} in {Colour.BOLD}{count}{Colour.END}{Colour.RED} seconds...{Colour.END}", end="\r")
		# Sleep for one second
		time.sleep(1)
		# Decrement the counter
		count -= 1

# KILLER
# Kill the program and check first
def killer():
	# Are you sure?
	check = input(f"{Colour.BOLD}{Colour.RED}Kill the program? [Y/n]: {Colour.END}")
	# Yes, I'm sure
	if check.lower() in ["", "y", "yes"]:
		print(f"{Colour.GREEN}Goodbye!{Colour.END}")
		# Kill the program
		exit()
	# Neither
	elif check.lower() not in ["n", "no"]:
		print(f"{Colour.RED}Input not recognised.{Colour.END}")
		# Start the killer again
		killer()
	# No, continue the program

# SELECT A LOCATION
# Find and load the target location by file
def location_selection():

	# Make sure the locations directory exists
	assert os.path.exists("./locations")

	# Location Variables
	location = ""
	locations_dir = os.listdir("./locations") #because of the `assert` above, this cannot fail
	location_index = None
	location_human_name = ""
	locations_human_names = []

	# Open the locations directory
	assert len(locations_dir) > 0, f"{Colour.RED}No locations found.{Colour.END}"

	# Retrieve human names for each file
	for location in locations_dir:
		# Get the whole contents of the file
		location_contents = open(f"./locations/{location}", "r").readlines()
		# Check the file is formatted correctly
		if not location_contents[-1][-1] == "\n":
			# Write newline one-liner
			open(f"./locations/{location}", "a").write("\n")
		# Append the human name
		locations_human_names.append(location_contents[0][:-1])

	# If the default file exists but has a corrupted inside, don't use it
	if "default" in locations_dir:
		default_contents = open(f"./locations/default", "r").readline()[:-1]
		if default_contents not in locations_dir and not default_contents == "default":
			locations_human_names.remove(locations_dir.index("default"))
			locations_dir.remove("default")
		
	# If the default file is still listed, it must not be corrupted
	if "default" in locations_dir:
		# Locations found
		location_index = locations_dir.index(default_contents)
		print(f"{Colour.YELLOW}Default used.{Colour.END}")
	# There is only one file, use it
	elif len(locations_dir) == 1:
		location_index = 0
	else:
		print(f"{Colour.GREEN}{len(locations_human_names)} locations found:{Colour.END}")
		# List them
		i = 0
		for _ in locations_human_names:
			print(f"{i+1}. {Colour.YELLOW}{locations_human_names[i]}{Colour.END} (saved as {Colour.YELLOW}'{locations_dir[i]}{Colour.END})")
			i += 1
		# The user now chooses one
		choice = input(f"{Colour.BOLD}Select a location: {Colour.END}")

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
def search(location, target="", search_prompt="Enter a door ID: "):
	# Make sure the location you want to access does, in fact, exist
	assert os.path.exists(location), f"{Colour.RED}File ('{location}') does not exist.{Colour.END}"

	# Get the codes from the file at specified location
	file_contents = open(location, "r").readlines()
	# Get some data to do some end-user stuff
	human_name = file_contents[0][:-1]
	# Remove the human name so that it is not searchable
	file_contents.pop(0)

	# Declare the target
	if target == "":
		target = input(f"{Colour.BOLD}{search_prompt}{Colour.END}")

	# Check it for keywords
	if target.lower() in ["exit", "bye", "goodbye", "cya", "quit", "logout", "leave", "hwyl"]:
		killer()

	

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

	# Now we must handle the response
	#DEBUG
	# print(rooms)

	# There were results
	if len(rooms) > 0:
		# Result or results?
		if len(rooms) == 1:
			print(f"{Colour.GREEN}{Colour.BOLD}{len(rooms)}{Colour.END}{Colour.GREEN} result found for {human_name}.{Colour.END}")
		else:
			print(f"{Colour.GREEN}{Colour.BOLD}{len(rooms)}{Colour.END}{Colour.GREEN} results found for {human_name}.{Colour.END}")

		# Prepare the results
		max_id_len = 0
		max_code_len = 0
		for room in rooms:
			# Split up the room data
			room_type = room[0]
			room_id = room[1][0]
			room_code = room[1][1]
			# If this room ID is longer than the rest
			if len(room_id) > max_id_len:
				max_id_len = len(room_id)
			# If this room code is longer than the rest
			if len(room_code) > max_code_len:
				max_code_len = len(room_code)

		# Output the results
		last_type = ""
		for room in rooms:
			# Split up the room data
			room_type = room[0]
			room_id = room[1][0]
			room_code = room[1][1]
			# If this room is of a new type, print such
			if not room_type == last_type:
				print(f"{Colour.YELLOW}{room_type}{Colour.END}")
				last_type = room_type

			# Print the result
			print(f"{Colour.GREEN}{room_id}{Colour.END}:{Colour.CYAN}{room_code}{Colour.END}")

		# Be sure the user knows output has ended
		print(f"{Colour.RED}End of output.{Colour.END}")
		# Timeout
		countdown("Clearing", 5)
		# Clear the last output
		clear()

	# The search came up blank
	else:
		# Notify the user
		print(f"{Colour.RED}No results found.{Colour.END}")
		# Query if the user wants to try again
		if input(f"{Colour.BOLD}Try again? [Y/n]: {Colour.END}").lower() in ["", "y", "yes"]:
			# Keep the original call's arguments
			#  Phew, almost missed that!
			clear()
			return search(location, search_prompt=search_prompt)
		# If not, quit
		else:
			print(f"{Colour.GREEN}Goodbye!{Colour.END}")
			exit()



# Run on startup
if __name__ == "__main__":
	# Clear the screen and run the welcome message
	clear()
	# Prompt them for a location
	location = location_selection()
	# Search loop
	while True:
		# Search for a record in that location
		search(location)