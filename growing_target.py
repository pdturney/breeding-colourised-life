#
#
# Peter Turney, May 15, 2024
#
# growing_target.py
#
# This program reads the file that had the highest
# score in the final population. The result is
# displayed by sending the information to Golly.
#
#
import golly
import pickle
import time
import targets as targ
#
# - make a torus
rule_name = "Immigration"     # - use Immigration rule
max_dimension = ":T60,60"     # - Torus of 60 x 60
golly.autoupdate(True)
golly.new(rule_name)
# - Immigration:T60,60 makes a torus of 60 x 60
# - a torus is finite, which means the live cells should
#   be packed more densely and uniformly, which is good
golly.setrule(rule_name + max_dimension)
#
data_file = open("top_result.bin", "rb")
data = pickle.load(data_file)
data_file.close()
[top_score, top_seed, top_adult] = data
#
# Write top_score in the bar at the top of the Golly window.
#
golly.show("score = " + str(top_score))
#
# Write the target in the Golly window.
#
golly.new("") # - clear the screen
white  = 0    # - white,255,255,255
red    = 1    # - red,255,0,0
blue   = 2    # - blue,0,0,255
golly.setcolors([white,255,255,255,red,255,0,0,blue,0,0,255])
matrix = targ.target_2()
# - show the seed growing in 3 steps
# - step 0 -- the initial state
targ.show_target(matrix)
# - steps: 50, 100
for step in range(2):
  time.sleep(10)
  golly.run(50)
#
#