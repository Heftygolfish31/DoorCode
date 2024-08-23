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
  # Prepared result variable
  location = ""
  # List the contents of the doorsets folder
  doorsets_directory = os.listdir("./doorsets")

  # Fail if no doorsets availible
  assert len(doorsets_directory) > 0, "No doorset files availible."

  # If a default is preloaded
  if "default" in doorsets_directory:
    # The default file should only contain one line with a filename
    default_location = open("./doorsets/default", "r").readline()[:-1]
    # Check file stored in default actually exists
    if default_location not in doorsets_directory:
      print(f"{Colour.RED}Default not found.{Colour.END}")
      os.remove("./doorsets/default")
      # Start the selection process again
      location_selection()
    # It does actually exist
    else:
      location = default_location

  # If there is a choice
  elif len(doorsets_directory) > 1:
    print(f"{Colour.GREEN}Multiple locations found.{Colour.END}")
    i = 1
    doorsets_human_names = []
    for doorset in doorsets_directory:
      # The first line of the file should be the human name to identify its contents
      doorset_human_name = open(f"./doorsets/{doorset}", "r").readline()[:-1]
      doorsets_human_names.append(doorset_human_name)
      print(f"{i}. {doorset_human_name} (saved as '{doorset}').")
      i += 1

    # User selected number or location or path
    user_location = input("Select a doorset: ")

    # Check location input valid
    location_index = -1

    # File name inputted
    if user_location in doorsets_directory:
      location_index = doorsets_directory.index(user_location)
    # Human name inputted
    elif user_location in doorsets_human_names:
      location_index = doorsets_human_names.index(user_location)
    else:
      try:
        # Index inputted
        if int(user_location) >= 1 and int(user_location) < i:
          location_index = int(user_location)-1
      except ValueError:
        pass

    # If the location index is still the placeholder value, the input was not recognised
    if location_index == -1:
      print(f"{Colour.RED}Input not recognised.{Colour.END}")
      location_selection()

    # Select the location filename
    location = doorsets_directory[location_index]

  # There is only one file and its not the default file
  else:
    location = doorsets_directory[0]

  human_name = open(f"./doorsets/{location}", "r").readline()[:-1]
  print(f"{Colour.GREEN}'{human_name}' at '{location}' selected.{Colour.END}")
  return location

location_selection()
