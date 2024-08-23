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

	# # Default to whatever is stored in the "default" file
	# if "default" in locations_dir and open(f"./locations/{location}", "r").readline()[:-1] in locations_human_names:
	# 	# Assign the relavent information
	# 	location_index = locations_dir.index("default")
	# 	location = locations_dir[location_index]
	# 	location_human_name = locations_human_names[location_index]
	# 	print(f"{Colour.GREEN}'{location_human_name}'{Colour.END} (saved as '{Colour.GREEN}{location}{Colour.END}') selected.")
	# 	return location
	# else:
	# 	# If default was corrupted, don't use or count it.
	# 	if "default" in locations_dir:
	# 		locations_human_names.remove(locations_dir.index("default"))
	# 		locations_dir.remove("default")

	# 	if len(locations_dir) == 2:
	# 		location = locations_dir[0]
	# 		location_human_name = locations_human_names[0]
	# 		print(f"{Colour.GREEN}'{location_human_name}'{Colour.END} (saved as '{Colour.GREEN}{location}{Colour.END}') selected.")
	# 		return location
	# 	else:
	# 		print(f"Multiple ")

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








	# # Prepare resulting variables
	# location = ""
	# location_index = None
	# location_human_name = ""

	# # List the contents of the doorsets folder
	# doorsets_dir = os.listdir("./doorsets")

	# # Ensure there are files in the doorsets folder
	# assert len(doorsets_dir) > 0, "No doorsets availible."

	# # Retrive human names for each file
	# human_names = []
	# for doorset in doorsets_dir:
	# 	# Store the first line / the human name
	# 	human_name = open(f"./doorsets/{doorset}", "r").readline()[:-1]

	# 	# If the default is found
	# 	if doorset == "default" and human_name not in ["", "default"]:
	# 		# The first line of the default only holds a path
	# 		location_index = doorsets_dir.index(human_name)

	# 	else:
	# 		human_names.append(human_name)

	# # A location has not been selected yet
	# if location_index == None:
	# 	# Mutiple options for locations
	# 	if len(human_names) > 1:
	# 		print(f"{len(human_names)} locations found:")
	# 		# List them
	# 		possible_location_index = 0
	# 		for _ in human_names:
	# 			print(f"{possible_location_index+1}. {Colour.YELLOW}{human_names[possible_location_index]}{Colour.END} (saved as '{doorsets_dir[possible_location_index]})")
	# 			possible_location_index += 1
	# 		# The user now chooses one
	# 		choice = input("Select a location: ")

	# 		try:
	# 			# File name inputted
	# 			if choice in doorsets_dir:
	# 				location_index = doorsets_dir.index(choice)
	# 			# Human name inputted
	# 			elif choice in human_names:
	# 				location_index = human_names.index(choice)
	# 			# Index inputted
	# 			elif int(choice) >= 1 and int(choice) < possible_location_index:
	# 				location_index = int(choice)-1
	# 			# That choice doesn't fit any pattern
	# 			else:
	# 				print("Location not recognised")
	# 				return location_selection()
	# 		except ValueError:
	# 			pass
	# 	# Only one option for a location
	# 	else:
	# 		location_index = 0

	# # If saved default
	# if "default" in doorsets_dir:
	# 	# Get the supposed default location
	# 	default_location = open("./doorsets/default", "r").readline()[:-1]
	# 	# Check file exists
	# 	if default_location not in doorsets_dir:
	# 		print(f"{Colour.RED}Default not found.{Colour.END}")

	# 		# If there is a choice
	# 		if len(doorsets_dir) > 1:
	# 			print(f"{Colour.GREEN}Multiple locations found.{Colour.END}")
	# 			# Index is also a valid option
	# 			i = 1
	# 			human_names = []
	# 			for doorset in doorsets_dir:
	# 				human_name = open(f"./doorsets/{doorset}", "r").readline()[:-1]
	# 				human_names.append(human_name)
	# 				print(f"{i}. {human_name} (saved as '{doorset}').")
	# 				i += 1

	# 			# User selected number or location or path
	# 			user_location = input("Select a doorset: ")

	# 			try:
	# 				# File name inputted
	# 				if user_location in doorsets_dir:
	# 					location_index = doorsets_dir.index(user_location)
	# 				# Human name inputted
	# 				elif user_location in human_names:
	# 					location_index = human_names.index(user_location)
	# 				# Index inputted
	# 				elif int(user_location) >= 1 and int(user_location) < i:
	# 					location_index = int(user_location)-1
	# 			except ValueError:
	# 				pass

	# 	else:
	# 		location_index = doorsets_dir.index(location)
		

	# Update the function variables to match
	location = locations_dir[int(location_index)]
	location_human_name = locations_human_names[int(location_index)]
	# Notify the user
	print(f"{Colour.GREEN}{location_human_name}{Colour.END} (at '{location}') selected.")
	return location

location_selection()
