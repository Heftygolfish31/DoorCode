# Door Code Python
version = "0.1"

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
def kill():
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
  # Prepare resulting variables
  location = ""
  location_index = -1
  location_human_name = ""

  # List the contents of the doorsets folder
  doorsets_dir = os.listdir("./doorsets")

  # Ensure there are files in the doorsets folder
  assert len(doorsets_dir) > 0, "No doorsets availible."

  if "default" in doorsets_dir:
    # Get the supposed default location
    default_location = open("./doorsets/default", "r").readline()[:-1]
    # Check file exists
    if default_location not in doorsets_dir:
      print(f"{Colour.RED}Default not found.{Colour.END}")
    else:
      location = default_location
      location_index = doorsets_dir.index(location)
      location_human_name = open(f"./doorsets/{location}", "r").readline()[:-1]

      # Notify the user of the default option success
      print(f"{Colour.GREEN}'{location_human_name}' at '{location}' selected.{Colour.END}")
      return location

  # If there is a choice
  if len(doorsets_dir) > 1:
    print(f"{Colour.GREEN}Multiple locations found.{Colour.END}")
    # Index is also a valid option
    i = 1
    human_names = []
    for doorset in doorsets_dir:
      human_name = open(f"./doorsets/{doorset}", "r").readline()[:-1]
      human_names.append(human_name)
      print(f"{i}. {human_name} (saved as '{doorset}').")
      i += 1

    # User selected number or location or path
    user_location = input("Select a doorset: ")

    try:
      # File name inputted
      if user_location in doorsets_dir:
        location_index = doorsets_dir.index(user_location)
      # Human name inputted
      elif user_location in human_names:
        location_index = human_names.index(user_location)
      # Index inputted
      elif int(user_location) >= 1 and int(user_location) < i:
        location_index = int(user_location)-1
    except ValueError:
      pass

  else:
    location_index = 0


  if location_index > -1:
    print("{location

location_selection()
