import threading
from functools import partial

import keyboard

from Src.app.logging_config import logger
from Src.key_tracking import keyboard_listener, on_key_release
from Src.menu import create_icon
from Src.padding import update_padding
from Src.utils import check_settings, banner


def main():
    try:
        check_settings()
        update_padding(reset=True)

        threading.Thread(target=keyboard_listener, daemon=True).start()

        icon = create_icon()
        keyboard.on_release(partial(on_key_release, icon))
        icon.run()

    finally:
        update_padding(reset=True)
        check_settings()


if __name__ == "__main__":
    banner()
    logger.info('Tray started')
    main()
    logger.info('Tray stopped')
