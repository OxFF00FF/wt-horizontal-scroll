import json
import os
import shutil
from pathlib import Path

from pyfiglet import figlet_format, parse_color

from Src.app.colors import *
from Src.app.config import app_config
from Src.app.logging_config import logger


def banner():
    os.system('cls')

    # standard, slant, cybermedium, ansi_shadow
    create_banner([
        ['WT ', WHITE, 'standard'],
        ['Horizontal', LIGHT_YELLOW, 'slant'],
        ['Scroll', LIGHT_RED, 'slant']
    ], show=True)


def parse_padding(padding_str):
    return [int(x.strip()) for x in padding_str.split(',')]


def format_padding(padding_list):
    return ', '.join(f'{x:06d}' if x >= 0 else f'{x:07d}' for x in padding_list)


def backup_file(filepath):
    filepath = Path(filepath)
    backup_path = filepath.with_suffix(filepath.suffix + '.bak')
    if os.path.exists(backup_path):
        return
    shutil.copy2(filepath, backup_path)
    return backup_path


def check_settings():
    user_wt_settings = app_config.SETTINGS_JSON_PATH

    if not os.path.exists(user_wt_settings):
        logger.error(f"{LIGHT_RED}[!]{WHITE}  Файл не найден: {user_wt_settings}")
        exit()

    backup_file(user_wt_settings)
    with open(user_wt_settings, "r", encoding='utf-8') as f:
        data = json.load(f)

    app_config.LINE_WRAP = not app_config.LINE_WRAP
    logger.debug(f"Horizontal scrolling is {LIGHT_GREEN}Working{WHITE}" if app_config.LINE_WRAP else f"Horizontal scrolling is {LIGHT_RED}Stopped{WHITE}")

    if app_config.LINE_WRAP:
        for profile in data["profiles"]['list']:
            profile.pop('padding', None)
    else:
        for profile in data["profiles"]['list']:
            profile['padding'] = 10

    with open(user_wt_settings, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def get_figlet_text(text, font=None, colors=":", **kwargs):
    ansi_colors = parse_color(colors)
    figlet_text = figlet_format(text, font, **kwargs)

    if ansi_colors:
        figlet_text = ansi_colors + figlet_text + RESET

    return figlet_text


def create_banner(words_and_colors, version=None, show=False):
    lines = []
    result = ""

    for (text, color, font) in words_and_colors:
        # Создание ASCII арта для каждого слова из переданного списка
        ascii_art_word = get_figlet_text(text, font, width=200)

        # Разделение арта на список линий
        word_lines = ascii_art_word.splitlines()
        lines.append([color + word_line for word_line in word_lines])

    # Склеиваем построчно
    for line_group in zip(*lines):
        result += "  ".join(line_group) + "\n"

    # Добавляем версию к последней строке
    if version:
        result_lines = result.splitlines()
        result_lines[-1] += f"{WHITE}{version}\n"
        result = "\n".join(result_lines)

    if show:
        print(f"\n{result}{WHITE}")

    return result
