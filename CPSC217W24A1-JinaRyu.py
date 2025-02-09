# Assignment 01 Jina Ryu 30090141 This codes takes user input for (x,y) coordinate for boat and sun and draws them
# with the prompted value of x,y position.
# There are sky, seagulls, clouds, and ocean. They are not movable objects.


from SimpleGraphics import *  # import SimpleGraphics

background("pale turquoise")  # background colour

setColor("blue4")  # blue ocean using rectangle
rect(0, 400, 800, 400)

setColor("white")
line(50, 100, 75, 75, 100, 100, 125, 75, 150,100)  # a seagull using a line
line(100,150, 110, 130, 120,150, 130,130, 140,150)  # a baby seagull

setColor("white")  # two white clouds
ellipse(310, 150, 200, 50)
ellipse(540, 50, 100, 50)

boat_x_pos = float(input("Please enter x-position value of the boat: "))  # user input for x,y of boat
boat_y_pos = float(input("Please enter y-position value of the boat: "))

# boat using pieslice function and x,y from user input
setColor("brown")
pieSlice(boat_x_pos, boat_y_pos, 300, 150, 0, -180)

Sun_x_pos = int(input("Please enter x-position value of the sun: "))  # input of x and y from the user (sun)
Sun_y_pos = int(input("Please enter y-position value of the sun: "))

setColor("yellow")  # yellow sun using ellipse and input
ellipse(Sun_x_pos, Sun_y_pos, 100, 100)


