# Door Code Python
version = "0.2"

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


	if location_index == None:
		print("Location not recognised")
		return location_selection()

	# Update the function variables to match
	location = locations_dir[int(location_index)]
	location_human_name = locations_human_names[int(location_index)]
	# Notify the user
	print(f"{Colour.GREEN}{location_human_name}{Colour.END} (at '{location}') selected.")
	return location

location_selection()
