from pynput import keyboard, mouse
from pynput.keyboard import Key

from Src.app.colors import *
from Src.app.logging_config import logger
from Src.menu import get_icon
from Src.padding import update_padding
from Src.utils import check_settings

alt_pressed = False


def on_key_press(key):
    global alt_pressed
    if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = True


def on_key_release(key, _):
    global alt_pressed

    if key == Key.alt_l or key == Key.alt_r:
        alt_pressed = False
        logger.debug(f"[🔒]  {key} {LIGHT_YELLOW}Ignored{WHITE}")
        return

    try:
        k = key.char
    except AttributeError:
        k = None

    if alt_pressed and k is None and key not in (Key.up, Key.down, Key.left, Key.right):
        return

    logger.debug(f"[🔒 ]  {k} ({_}) {LIGHT_YELLOW}Ignored{WHITE}")

    # Alt + стрелки / Alt + Up / Alt + Down
    if alt_pressed:
        if key == Key.right or k == 'right':
            update_padding(direction='right')
        elif key == Key.left or k == 'left':
            update_padding(direction='left')
        elif key == Key.down or k == 'down':
            update_padding(reset=True)
        elif key == Key.up or k == 'up':
            check_settings()
        elif k == 'q' or k == 'й':
            icon = get_icon()
            icon.stop()

        else:
            logger.debug(f"{YELLOW}[⚠ ]{WHITE}  Unsuported combination: Alt + {k}")


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
