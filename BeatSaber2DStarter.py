from SimpleGame.simplegame import *
from random import choice
import sys

BEAT_DIRECTIONS = ['up', 'down', 'left', 'right']
LEFT_BEAT_DIRECTIONS=['w', 'a', 's', 'd']
VISIBLE = 'visible'
SPEED = 5   # DO NOT CHANGE

generation_speed = 0.6
frame_counter = 0
score = 0
songName = 'believer'

game_ended = False
game_started = False
startScreenElements = {}
playScreenElements = {}
endScreenElements = {}

beatList = []

def start_screen_setup():
    startScreenElements['ready'] = create_element('text-ready', (WIDTH / 2, HEIGHT / 2 - 100))
    startScreenElements['space'] = create_element('space-bar', (WIDTH / 2, HEIGHT / 2 + 50))
    startScreenElements['tap'] = create_element('tap-active', (WIDTH / 2 + 70, HEIGHT / 2 + 50))
    startScreenElements['tap'][VISIBLE] = True
    schedule_callback_every(toggle_tap, .5)

def end_screen_setup():
    global game_ended
    game_ended = True
    endScreenElements['timeup'] = create_element('text-timeup', (WIDTH / 2, HEIGHT / 2))
    endScreenElements['timeup'][VISIBLE] = True
    schedule_callback_after(hide_timeup, 1)


def game_screen_setup():
    global game_started
    game_started = True
    cancel_callback_schedule(toggle_tap)
    playScreenElements['score'] = create_element('star2', (30, 30))
    playScreenElements['keyboard'] = create_element('keyboard_arrows', (WIDTH / 2, HEIGHT - 60))
    playScreenElements['keyboard']['base'] = 'keyboard_arrows_'
    playScreenElements['go'] = create_element('text-go', (WIDTH / 2, HEIGHT / 2))
    playScreenElements['go'][VISIBLE] = True
    schedule_callback_after(hide_go, .5)



def hide_go():
    playScreenElements['go'][VISIBLE] = False

def hide_timeup():
    endScreenElements['timeup'][VISIBLE] = False

def toggle_tap():
    startScreenElements['tap'][VISIBLE] = not startScreenElements['tap'][VISIBLE]



def draw():
    """
    - Called automatically everytime there's a change in the screen
    - Do not include any operations other than drawing inside this function.
    - The only allowed statements/functions are the ones that have draw_ in the name like
    draw_background_image(), draw_element(), etc
    """
    global flag
    # You may set different background for each step!
    draw_background('background4')

    if not game_started:
        # What you want to show *before* the game starts goes here. eg 'Press Space to Start!'
        for gameElement in startScreenElements.values():
            if VISIBLE not in gameElement or gameElement[VISIBLE]:
                draw_element(gameElement)
    elif game_ended:
        # What you want to show *after* the game ends goes here. eg 'You Scored x Beats!'
        for gameElement in endScreenElements.values():
            if VISIBLE not in gameElement or gameElement[VISIBLE]:
                draw_element(gameElement)
            else:
                draw_text_on_screen(f'SCORE\n{score}', (WIDTH / 2, HEIGHT / 2), lineheight=1.2, ocolor='lightseagreen', owidth=1.5, color="white", fontsize=100)
    else:
        # What you want to show *during* the game goes here. e.g. beats, timer, etc
        draw_text_on_screen(f'{score}', (70, 32), color='yellow', fontsize=40)

        for gameElement in playScreenElements.values():
            if VISIBLE not in gameElement or gameElement[VISIBLE]:
                draw_element(gameElement)

        for beat in beatList:
            draw_element(beat)



def update():
    """
    - Called automatically 60 times per second (every 1/60th of a second) to
    maintain a smooth frame rate of 60 fps.
    - Ideal for game logic e.g. moving objects, updating score, and checking game conditions.
    """
    # The frame counter keeps track of which frame we're on, this can be helpful for
    # operations that are time sensitive. You may also use the callback functions instead of
    # using the frame_counter.

    global frame_counter, game_ended, score
    frame_counter += 1

    # Uncomment the following line and see what happens when you run the program
    # print(f'{frame_counter/60:.1f}')

    if not game_started:
        # Game logic if any *before* the game starts.
        pass

    elif game_ended:
        # Game logic if any *after* the game ends.
        pass
    else:
        # Game logic if any *during* the game.
        # move it 5 pixels down
        for beat in beatList:
            if beat['moving']:
                move_by_offset(beat, (0, SPEED))
                if get_position(beat, 'bottom') >= HEIGHT:
                    beat['moving'] = False
                    beat['scoreStatus'] = 'miss'
            elif beat['scoreStatus']:
                if beat['scoreStatus'] == 'hit':
                    score += 1
                score_beat(beat)


def on_key_down(key):
    """
    Called when a key is pressed on the keyboard.
    - Do not use this function for game logic.

    Parameters:
    - key: An integer representative of the key that was pressed.
    In order to get a str value of the key pressed, use get_key() instead.
    """

    key_pressed = get_key_pressed(key)
    if key_pressed == 'space' and not game_started:
        start_game()
        return

    lowest_beat = find_lowest_moving_beat()
    if not game_ended and lowest_beat and key_pressed in BEAT_DIRECTIONS:
        lowest_beat['moving'] = False
        change_image(playScreenElements['keyboard'], playScreenElements['keyboard']['base'] + lowest_beat['direction'])
        schedule_callback_after(keyboardArrowChangeBack, .1)
        if lowest_beat['direction'] == key_pressed:
            lowest_beat['scoreStatus'] = 'hit'
        else:
            lowest_beat['scoreStatus'] = 'miss'
    if key in LEFT_BEAT_DIRECTIONS:
        key_pressed = LEFT_BEAT_DIRECTIONS[key]
        stream = 'left'
    elif key in BEAT_DIRECTIONS:
        key_pressed = BEAT_DIRECTIONS[key]
        stream = 'right'
    else:
        return

    lowest_beat = find_lowest_moving_beat()
    if not game_ended and lowest_beat and lowest_beat['stream'] == stream:
        lowest_beat['moving'] = False
        change_image(playScreenElements['keyboard'], playScreenElements['keyboard']['base'] + lowest_beat['direction'])
        schedule_callback_after(keyboardArrowChangeBack, .1)
        if lowest_beat['direction'] == key_pressed:
            lowest_beat['scoreStatus'] = 'hit'
        else:
            lowest_beat['scoreStatus'] = 'miss'

    if key_pressed in BEAT_DIRECTIONS:
        if key_pressed == 'right':
            rotate_by(keyboard_arrows, 450)
        if key_pressed == 'left':
            rotate_by(keyboard_arrows, 630)
        if key_pressed == "up":
            rotate_by(keyboard_arrows, 360)
        if key_pressed == "down":
            rotate_by(keyboard_arrows, -180)

    if key_pressed in BEAT_DIRECTIONS:
        for beat in beatList:
            if beat['isMoving'] and beat['direction'] == key_pressed:
                score += 1
                beatList.remove(beat)  # Remove the beat when scored
                play_sound_clip('hit1')
                break  # Stop iterating if a bea


def keyboardArrowChangeBack():
    change_image(playScreenElements['keyboard'], playScreenElements['keyboard']['base'][:-1])


def score_beat(beat):
    status = beat['scoreStatus']
    beat['scoreStatus'] = ''
    direction = beat['direction']
    change_image(beat, direction + '-' + status)
    schedule_callback_after(remove_lowest_beat, .2)


def remove_lowest_beat():
    if beatList:
        beatList.pop(0)


def find_lowest_moving_beat():
    for beat in beatList:
        if beat['moving']:
            return beat
    return None



def start_game():
    # user-defined function
    # only put logic that'll happen once when the game starts
    game_screen_setup()
    manage_background_music(songName, 'play')
    manage_background_music(songName, 'change-volume', volume=0.3)
    schedule_callback_every(generate_beat, generation_speed)


def end_game():
    # user-defined function
    cancel_callback_schedule(generate_beat)
    end_screen_setup()
    beatList.clear()
    manage_background_music(songName, 'stop')


def generate_beat():
    # user-defined function
    beatDirection = choice(BEAT_DIRECTIONS)
    side = choice([-1, 1])
    beat = create_element(beatDirection + '-beat', centerPos=(WIDTH / 2 + side*150, 0))
    beat['side'] = side
    beat['moving'] = True
    beat['scoreStatus'] = ''
    beat['direction'] = beatDirection
    beatList.append(beat)



# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # DO NOT REMOVE THIS LINE!! # # # # # # # #
start_screen_setup()
run_game()
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
