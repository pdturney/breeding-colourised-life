#
#
# Peter Turney, June 20, 2024
#
# colourised.py
#
#
# IMPORT
# ======
#
import golly
import colourised as colour
import numpy as np
import random as rand
import time
#
#
# PARAMETERS
# ==========
#
white  = 0
red    = 1
blue   = 2
#
#
# Variables for tracking growth.
#
red_growth    = 0
blue_growth   = 0
#
#
# FUNCTIONS
# =========
#
# Make a random seed matrix.
#
def make_seed_matrix(prob_red, prob_blue):
  # - seed_matrix size = 20 rows x 20 columns
  # - the Game of Life seems to prefer a density of
  #   about 0.3, so suggested probability setting is
  #   0.15 for prob_red and 0.15 for prob_blue
  # - rows and cols will be shifted by <-10, -10> so
  #   that the matrix is centered on the screen
  # - upper left  = <-10, -10>
  # - lower right = <+10, +10>
  rows = 20
  cols = 20
  # - each colour is assigned an ID number
  white  = 0
  red    = 1
  blue   = 2
  # - start with a matrix of zeros
  seed_matrix = np.zeros([rows, cols], dtype=int)
  for i in range(rows):
    for j in range(cols):
      # - 0 = loss, 1 = win
      # - assume loss for both red and blue
      red_state  = 0
      blue_state = 0
      # - flip a biased coin for red
      if (rand.random() < prob_red):
        red_state = 1
      # - flip a biased coin for blue
      if (rand.random() < prob_blue):
        blue_state = 1
      # - what if there is a tie between red and blue?
      if ((red_state == 1) and (blue_state == 1)):
        # - it's a tie, so flip a coin
        if (rand.random() < 0.5):
          red_state  = 0
          blue_state = 1
        else:
          red_state  = 1
          blue_state = 0
      # - we've broken the tie
      if (red_state == 1):
        # - red == 1
        seed_matrix[i, j] = red
      if (blue_state == 1):
        # - blue == 2
        seed_matrix[i, j] = blue
      # - if neither red nor blue was selected, then 
      #   seed_matrix[i, j] is zero, since the seed_matrix is
      #   initialized to zero (white)
  return seed_matrix
#
# Given seed matrix, write it on the Golly screen and let it grow.
#
def grow_matrix(seed_matrix, num_steps):
  #
  rule_name = "Immigration"                  # Immigration.rule
  max_dimension = ":T60,60"                  # Torus of 60 x 60
  golly.new(rule_name)                       # initialize cells
  golly.setrule(rule_name + max_dimension)   # infinite plane
  golly.autoupdate(True)                     # update screen
  # - colours
  white  = 0 # white,255,255,255
  red    = 1 # red,255,0,0
  blue   = 2 # blue,0,0,255
  golly.setcolors([white,255,255,255,red,255,0,0,blue,0,0,255])
  # - get seed_matrix size
  rows = len(seed_matrix)
  cols = len(seed_matrix[0])
  # - write seed_matrix in the center of Golly screen
  for i in range(rows):
    for j in range(cols):
      # - get the colour of this matrix cell
      colour = seed_matrix[i][j]
      # - write the colour on the Golly screen
      # - the matrix is 20 x 20, ranging from the top left
      #   at [0, 0] to the bottom right at [20, 20]
      # - to center the matrix, we subtract 10, so we have
      #   the top left at [-10, -10] and the bottom right
      #   at [+10, +10]
      golly.setcell(i - 10, j - 10, colour)
  # - run Golly until it grows to 60 x 60
  # - Golly is initialized at 20 x 20, so it needs to
  #   grow 40 steps in all four directions (up, down,
  #   left, right)
  # - Golly typically grows one half step each turn,
  #   so running for 80 steps should allow 60 x 60
  golly.run(num_steps)
  # - now make a box of 60 x 60 centered on the origin
  [left, top, width, height] = [-30, -30, 60, 60]
  # - read the 60 x 60 box into a matrix
  grown_matrix = np.zeros([height, width], dtype=int)
  for i in range(height):
    for j in range(width):
      grown_matrix[i][j] = golly.getcell(i + left, j + top)
  # - output the new grown_matrix
  return grown_matrix
#
# Given a seed matrix, randomly change a fraction of the seed.
#
def mutate_seed(seed_matrix, prob_mutation):
  # - each colour is assigned an ID number
  white  = 0
  red    = 1
  blue   = 2
  # - seed_matrix size = 20 rows x 20 columns
  # - get seed_matrix size
  rows = len(seed_matrix)
  cols = len(seed_matrix[0])
  new_matrix = np.zeros([rows, cols], dtype=int)
  for i in range(rows):
    for j in range(cols):
      # - change some cells
      if (rand.random() < prob_mutation):
        # - if currently red, then switch to blue or white
        if (seed_matrix[i][j] == red):
          if (rand.random() < 0.5):
            new_matrix[i][j] = blue
          else:
            new_matrix[i][j] = white
        # - if currently blue, then switch to red or white
        elif (seed_matrix[i][j] == blue):
          if (rand.random() < 0.5):
            new_matrix[i][j] = red
          else:
            new_matrix[i][j] = white
        # - if currently white, then switch to red or blue
        else: # - must be white
          assert (seed_matrix[i][j] == white)
          if (rand.random() < 0.5):
            new_matrix[i][j] = red
          else:
            new_matrix[i][j] = blue
      # - otherwise don't change
      else:
        new_matrix[i][j] = seed_matrix[i][j]
  # - output the new matrix
  return new_matrix         
#
#