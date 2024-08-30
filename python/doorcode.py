# Door Code Python
VERSION = "1.1"

# IMPORTS
# Import the os package for reading terminal data
import os
# Import the time package for sleeping
import time

# GLOBALS
LOCATION_HUMAN_NAME = ""
LOCATION = ""

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
	first_line = f"{Colour.UNDERLINE}*{Colour.END} {Colour.BOLD}{Colour.CYAN}Python Doorcode v{VERSION}{Colour.END} {Colour.UNDERLINE}*{Colour.END}"
	print(first_line)
	# Location slot
	if not LOCATION_HUMAN_NAME == "":
		second_line = f"| {Colour.CYAN}Location: {Colour.GREEN}{LOCATION_HUMAN_NAME}{Colour.END}"
		print(second_line)


# CLEAR
# Clear the screen; start afresh
def clear(toWelcome=True):
	# ANSI 
	print("\033c", end="")
	# If the `toWelcome` flag is set, the welcome message leads everything
	if toWelcome:
		welcome()

# COUNTDOWN
# Simulate a single-line animation to show a clock timeout, in seconds
def countdown(action, count=5):
	# Loop for the number of times to sleep by
	while count > 0:
		# Second or seconds?
		s_in_seconds = "s"
		if count == 1:
			s_in_seconds = ""
		# Print the warning
		print(f"{Colour.RED}{action} in {Colour.BOLD}{count}{Colour.END}{Colour.RED} second{s_in_seconds}...{Colour.END}", end="\r")
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
		clear(False)
		print(f"{Colour.GREEN}Goodbye!{Colour.END}")
		# Kill the program
		exit()
	# Neither yes nor no
	elif check.lower() not in ["n", "no"]:
		print(f"{Colour.RED}Input not recognised.{Colour.END}")
		# Start the killer again
		killer()
	# No, continue the program

# SELECT A LOCATION
# Find and load the target location by file
def location_selection(useDefault=True):
	# Prepare the global location details
	global LOCATION_HUMAN_NAME
	global LOCATION

	# Make sure the locations directory exists
	assert os.path.exists("./locations"), f"{Colour.RED}Python Doorcode v{VERSION} misconfigured: './locations/' directory missing"

	# Location Variables
	locations_dir = os.listdir("./locations") #because of the `assert` above, this cannot fail
	location_index = None
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
		# Remove the default option on the condition that:
		# - the contents of default is not a valid location
		#  OR 
		# - the contents is default
		if default_contents not in locations_dir or default_contents == "default" or not useDefault:
			locations_human_names.pop(locations_dir.index("default"))
			locations_dir.remove("default")
		
	# If the default file is still listed, it must not be corrupted
	if "default" in locations_dir and useDefault:
		# Locations found
		location_index = locations_dir.index(default_contents)
		print(f"{Colour.YELLOW}Default used.{Colour.END}")
	# There is only one file, use it
	elif len(locations_dir) == 1:
		location_index = 0
	else:
		# Announce the list
		print(f"{Colour.GREEN}{Colour.BOLD}Locations:{Colour.END}")

		# List them
		i = 0
		for _ in locations_human_names:
			print(f"{i+1}. {Colour.YELLOW}{locations_human_names[i]}{Colour.END} (saved as {Colour.YELLOW}'{locations_dir[i]}'{Colour.END})")
			i += 1

		# Count them
		print(f"{Colour.GREEN}{Colour.BOLD}{len(locations_human_names)}{Colour.END}{Colour.GREEN} locations found:{Colour.END}")
		# The user now chooses one
		choice = input(f"{Colour.BOLD}Select a location: {Colour.END}")

		# Just came back from dental surgery.
		#   Have never wanted pizza more than right now.
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
	LOCATION = locations_dir[int(location_index)]
	LOCATION_HUMAN_NAME = locations_human_names[int(location_index)]
	# Notify the user
	clear()
	print(f"{Colour.GREEN}{LOCATION_HUMAN_NAME}{Colour.END} (at '{LOCATION}') selected.")
	return f"./locations/{LOCATION}"

# SWITCHER
# Facilitate switching locations
def switcher():
	# Get the current location human name
	global LOCATION_HUMAN_NAME
	# Are you sure?
	check = input(f"{Colour.BOLD}{Colour.GREEN}Switch locations?{Colour.END} [Y/n]: ")
	# Yes, I'm sure
	if check.lower() in ["", "y", "yes"]:
		clear()
		# Select a location the same way you chose a starting one
		location_selection(False)
		return True
	# No, continue
	return False

# SEARCH FOR A ROOM
# Load the location information and find the target
def search(target="", search_prompt="Enter a door ID: "):
	# Make sure the location you want to access does, in fact, exist
	assert os.path.exists(f"./locations/{LOCATION}"), f"{Colour.RED}File ('./locations/{LOCATION}') does not exist.{Colour.END}"

	# Get the codes from the file at specified location
	file_contents = open(f"./locations/{LOCATION}", "r").readlines()
	# Get some data to do some end-user stuff
	# Remove the human name so that it is not searchable
	file_contents.pop(0)

	# Declare the target
	if target == "":
		target = input(f"{Colour.BOLD}{search_prompt}{Colour.END}")

	# Check it for keywords
	# The user may want to leave
	if target.lower() in ["exit", "bye", "goodbye", "cya", "quit", "logout", "leave"]:
		clear()
		killer()
	# The user may want to switch locations
	elif target.lower() in ["switch", "location", "change"]:
		clear()
		if switcher():
			return
	# The user may want help
	# elif target.lower() in ["help", "?"]:
		# helper()

	# Find the target
	rooms = []
	room_type = "UNKNOWN:"
	exact_match = False
	for room in file_contents:
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
		if not exact_match and target.lower() in room[0].lower():
			# If the 'exact' match has been found
			if target.lower() == room[0].lower():

				#TODO: Make this even a little bit nicer
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

	# There were results
	if len(rooms) > 0:
		# Result or results?
		if len(rooms) == 1:
			print(f"{Colour.GREEN}{Colour.BOLD}{len(rooms)}{Colour.END}{Colour.GREEN} result found for {LOCATION_HUMAN_NAME}.{Colour.END}")
		else:
			print(f"{Colour.GREEN}{Colour.BOLD}{len(rooms)}{Colour.END}{Colour.GREEN} results found for {LOCATION_HUMAN_NAME}.{Colour.END}")

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
		print(f"{Colour.RED}No results found for {Colour.BOLD}'{target}'{Colour.END}{Colour.RED}.{Colour.END}")
		# Try again after a timeout
		countdown("Continuing", 2)
		clear()



# Run on startup
if __name__ == "__main__":
	try:
		# Clear the screen and run the welcome message
		clear()
		# Prompt them for a location
		location_selection()
		# Search loop
		while True:
			# Search for a record in that location
			search()
		
	# Someone pressed Ctrl + C !!
	#  How scandalous!
	#   - S
	except KeyboardInterrupt:
		clear(False)
		print(f"{Colour.RED}* Python Doorcode v{VERSION} killed by keyboard interrupt.")
		exit()