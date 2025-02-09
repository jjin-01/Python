# Jina Ryu 30090141 Assignment 2
# getting simple graphics to use graphic functions
from SimpleGraphics import *


# function and input for users to pick a background colour and fore colour. No colours allowed other than listed.
def choose_colours():
    while True:
        background_colour = str(
            input("What color do you want to use for the background? (black, white, blue, or green) "))
        if background_colour in ["black", "white", "blue", "green"]:
            break
        else:
            print(f"{background_colour} is not a valid option. ")

    while True:
        foreground_colour = str(
            input("What color do you want to use for the foreground? (black, white, blue, or green) "))
        if foreground_colour in ["black", "white", "blue", "green"] and background_colour != foreground_colour:
            break
        elif background_colour == foreground_colour:
            print("Your foreground color can't be the same as your background color. ")
        else:
            print(f"{foreground_colour} is not a valid option. ")

    return background_colour, foreground_colour


# start coordinate input. It should be in between 0 and 800.
def get_coordinates():
    while True:
        coordinate_x = int(input("Enter the starting x-coordinate: "))
        if 0 <= coordinate_x <= 800:
            break
        else:
            print("Coordinates must be between 0 and 800.")

    while True:
        coordinate_y = int(input("Enter the starting y-coordinate: "))
        if 0 <= coordinate_y <= 800:
            break
        else:
            print("Coordinates must be between 0 and 800.")

    return coordinate_x, coordinate_y


# getting coordinate inputs after the start coordinate input

def get_next_coordinates():
    while True:
        coordinate_x_next = int(input("Enter the next x-coordinate: "))
        if 0 <= coordinate_x_next <= 800:
            break
        else:
            print("Coordinates must be between 0 and 800.")

    while True:
        coordinate_y_next = int(input("Enter the next y-coordinate: "))
        if 0 <= coordinate_y_next <= 800:
            break
        else:
            print("Coordinates must be between 0 and 800.")

    return coordinate_x_next, coordinate_y_next


# drawing a line with the coordinate
def draw_line(x1, y1, x2, y2, color):
    setColor(color)
    line(x1, y1, x2, y2)


# main function
def main():
    background_colour, foreground_colour = choose_colours()
    background(background_colour)
    setFill(foreground_colour)
    # getting the name of the shape from the drawer
    shape_name = str(input("What is the Shape? "))
    # print 10 lines after the shape, so it doesn't reveal the shape to the guesser
    print("\n" * 10)
    # counts the points that are seen. Start with 1 since start coordinate counts as 1st point.
    points_seen = 1

    x_start, y_start = get_coordinates()
    x_prev, y_prev = x_start, y_start

    while True:
        # choosing to guess or continue with more points to be seen
        choice = input("Do you want to 1) guess the shape or 2) get the next point? ")
        # choice 1 will guess the shape and tell whether that is correct or incorrect shape.
        if choice == '1':
            # Guess the picture
            guess = str(input("Ok, what do you think it is? "))
            if guess == shape_name:
                print(f"Fantastic! You got it after seeing {points_seen} points.")
                break
            else:
                print(f"Nope, it's not {guess}. Better luck next time!")
                break
        # choice 2 will continue with the next coordinate points
        elif choice == '2':
            points_seen = points_seen + 1
            x_next, y_next = get_next_coordinates()
            draw_line(x_prev, y_prev, x_next, y_next, foreground_colour)
            x_prev, y_prev = x_next, y_next

            if (x_next, y_next) == (x_start, y_start):
                print(f"Game Over. It was a {shape_name}. ")
                break


# calling a function
main()
