from SimpleGame.simplegame import *
from random import choice

BEAT_DIRECTIONS = ['up', 'down', 'left', 'right']
ZONES= ['orange', 'pink', 'blue']
STREAMS = ['stream1', 'stream2', 'stream3']

game_ended = False
game_started = False
frame_counter = 0
# Use the following list to keep track of all your beats.
beatList = []

score = 0
scoreElement = create_element("blackbox", (50, 50))
timeLeft = 3

tap_images = ['tap', 'tap-active']

timerElement = create_element('timer', (WIDTH - 50, 50))
dir_arrow = create_element("arrow-key", (WIDTH / 2, HEIGHT - 50))

readyElement = create_element('text-ready', (WIDTH / 2, HEIGHT / 2 - 100))
spaceBarElement = create_element('space-bar', (WIDTH / 2, HEIGHT / 2 + 50))
tapElement = create_element(tap_images[0], (WIDTH / 2 + 70, HEIGHT / 2 + 50))
tapElement['isTapped'] = False
timeupElement = create_element('text-timeup', (WIDTH / 2, HEIGHT / 2))

flag = False


def draw_widgets():
    draw_element(scoreElement)
    draw_text_on_screen(str(score), (50, 50))
    draw_element(timerElement)
    draw_text_on_screen(str(timeLeft), (WIDTH - 50, 50))
    draw_element(dir_arrow)


def draw():
    """
    - Called automatically everytime there's a change in the screen
    - Do not include any operations other than drawing inside this function.
    - The only allowed statements/functions are the ones that have draw_ in the name like
    draw_background_image(), draw_element(), etc
    """
    # You may set different background for each step!
    global flag
    draw_background("background4")

    if not game_started:
        draw_element(readyElement)
        draw_element(spaceBarElement)
        draw_element(tapElement)
    elif game_ended:
        if flag:
            draw_text_on_screen(timeupElement)
        else:
            draw_text_on_screen(f'SCORE\n{score}', (WIDTH / 2, HEIGHT / 2), lineheight=1.2, ocolor='lightseagreen',
                                owidth=1.5, color="white", fontsize=100)
    else:
        # What you want to show *during* the game goes here. e.g. beats, timer, etc
        draw_widgets()
        for beat in beatList:
            draw_element(beat)

BEAT_GENERATION_INTERVAL = 60



def update():
    """
    - Called automatically 60 times per second (every 1/60th of a second) to
    maintain a smooth frame rate of 60 fps.
    - Ideal for game logic e.g. moving objects, updating score, and checking game conditions.
    """
    global frame_counter, game_ended, timeLeft, score
    frame_counter += 1
    if frame_counter % 60 == 0 and not game_ended:
        timeLeft -= 0.10
        play_sound_clip('tick')
        if timeLeft <= 0:
            end_game()

    if not game_started:
        # Game logic if any *before* the game starts.
        pass
    elif game_ended:
        # Game logic if any *after* the game ends.
        pass
    else:
        # Game logic if any *during* the game.
        for beat in beatList:
            if beat['isMoving']:
                move_by_offset(beat, (0, 3))

        # Generate beats at regular intervals
        if frame_counter % BEAT_GENERATION_INTERVAL == 0:
            generate_beat()


def get_lowest_beat():
    """
    Determine the lowest beat on the screen.
    """
    lowest_beat = None
    lowest_y = float('inf')  # Initialize with positive infinity

    for beat in beatList:
        # Compare the Y-coordinate of the beat
        if beat['y'] > lowest_y:
            lowest_y = beat['y']
            lowest_beat = beat

    return lowest_beat

def on_key_down(key):
    """
    Called when a key is pressed on the keyboard.
    - Do not use this function for game logic.

    Parameters:
    - key: An integer representative of the key that was pressed.
    In order to get a str value of the key pressed, use get_key() instead.
    """
    global score

    key_pressed = get_key_pressed(key)
    if key_pressed == 'space' and not game_started:
        start_game()

    if key_pressed in BEAT_DIRECTIONS:
        if key_pressed == 'right':
            rotate_by(dir_arrow, 450)
        if key_pressed == 'left':
            rotate_by(dir_arrow, 630)
        if key_pressed == "up":
            rotate_by(dir_arrow, 360)
        if key_pressed == "down":
            rotate_by(dir_arrow, -180)

    if key_pressed in BEAT_DIRECTIONS:
        for beat in beatList:
            if beat['isMoving'] and beat['direction'] == key_pressed:
                score += 1
                beatList.remove(beat)  # Remove the beat when scored
                play_sound_clip('hit1')
                break  # Stop iterating if a beat is scored


def start_game():
    # user-defined function
    # only put logic that'll happen once when the game starts
    global game_started
    game_started = True
    manage_background_music('winter', 'play')
    generate_beat()


def end_game():
    """
    - Called when the game ends (when the timer reaches 0 seconds).
    - You can add game-over logic here, such as displaying the final score or resetting the game.
    """
    global game_ended
    game_ended = True
    # Additional game-over logic can be added here, such as displaying the final score.
    print("Game Over! Final Score:", score)


def generate_beat():
    """
    Function to generate a beat with a random orientation and assign it to a random stream.
    After creating the beat, it adds it to the 'beatList'.
    """
    global beatList
    # Randomly select a direction for the beat
    direction = choice(BEAT_DIRECTIONS)

    # Randomly select a stream for the beat
    stream = choice(STREAMS)

    # Calculate initial position based on the chosen stream
    if stream == 'stream1':
        initial_position = (WIDTH / 4, 0)
    elif stream == 'stream2':
        initial_position = (WIDTH / 2, 0)
    elif stream == 'stream3':
        initial_position = (WIDTH * 3 / 4, 0)

    # Create the beat element
    beat = create_element('arrow-orange', initial_position)
    if direction == 'up':
        rotate_by(beat, 0)
    elif direction == 'down':
        rotate_by(beat, 180)
    elif direction == 'left':
        rotate_by(beat, -90)
    elif direction == 'right':
        rotate_by(beat, 90)
    beat['direction'] = direction
    beat['isMoving'] = True
    beat['stream'] = stream  # Assign the beat to a random stream
    beatList.append(beat)


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # DO NOT REMOVE THIS LINE!! # # # # # # # #
run_game()
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
