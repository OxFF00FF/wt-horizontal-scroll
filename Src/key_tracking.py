from pynput import keyboard, mouse

from Src.app.colors import *
from Src.app.logging_config import logger
from Src.padding import update_padding
from Src.utils import check_settings

alt_pressed = False


def on_key_press(key):
    global alt_pressed
    if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = True


def on_key_release(key, _):
    global alt_pressed
    if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = False
        return

    if not alt_pressed:
        return

    try:
        k = key.char
    except AttributeError:
        k = None

    if key == keyboard.Key.right or k == 'right':
        update_padding(direction='right')
    elif key == keyboard.Key.left or k == 'left':
        update_padding(direction='left')
    elif key == keyboard.Key.down or k == 'down':
        update_padding(reset=True)
    elif key == keyboard.Key.up or k == 'up':
        check_settings()
    else:
        logger.debug(f"{YELLOW}[⚠ ]{WHITE}  Неподдерживаемая комбинация: Alt + {k}")


def on_scroll(x, y, dx, dy):
    if not alt_pressed:
        return
    if dy > 0:
        # Scroll up
        update_padding(direction='left')
    elif dy < 0:
        # Scroll down
        update_padding(direction='right')


def keyboard_listener():
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as kl, mouse.Listener(on_scroll=on_scroll) as ml:
        kl.join()
        ml.join()
