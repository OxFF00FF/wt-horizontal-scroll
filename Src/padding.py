import json

from Src.app.colors import *
from Src.app.config import app_config
from Src.app.logging_config import logger
from Src.utils import format_padding, parse_padding


def update_padding(direction=None, reset=False):
    with open(app_config.SETTINGS_JSON_PATH, "r", encoding='utf-8') as f:
        data = json.load(f)

    try:
        if reset:
            padding = app_config.DEFAULT_PADDING.copy()
            direction_symbol = "⭮"
        else:
            padding_str = data["profiles"]["defaults"]["padding"]
            padding = parse_padding(padding_str)

            if direction == 'right':
                padding[0] -= 50
                padding[2] += 50
                direction_symbol = "→"
            elif direction == 'left':
                # Защита от лишнего шага влево (выход за дефолт)
                if padding[0] >= app_config.DEFAULT_PADDING[0] and padding[2] <= app_config.DEFAULT_PADDING[2]:
                    logger.debug(f"{LIGHT_BLUE}[🔒 ]{WHITE}  Уже в начальном положении: {format_padding(padding)}")
                    return

                padding[0] += 50
                padding[2] -= 50
                direction_symbol = "←"
            else:
                logger.error(f"{RED}[! ]{WHITE}  Неизвестное направление")
                return

        formatted = format_padding(padding)
        data["profiles"]["defaults"]["padding"] = formatted

        with open(app_config.SETTINGS_JSON_PATH, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        logger.debug(f"{LIGHT_GREEN}[✔ ]{WHITE}  {direction_symbol} {formatted}")

    except Exception as e:
        logger.error(f"{LIGHT_RED}[✘ ]{WHITE}  Ошибка обновления padding: {e}")
