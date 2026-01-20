import os
from os.path import basename, dirname

from PIL import Image
from pystray import Icon, MenuItem, Menu

from Src.app.config import app_config
from Src.app.logging_config import logger
from Src.padding import update_padding
from Src.utils import check_settings

_icon_instance = None


def increase_step(icon):
    app_config.STEP += 10
    logger.debug(f"⚙️ Увеличен шаг смещения: {app_config.STEP}")
    icon.menu = create_menu()
    icon.update_menu()


def decrease_step(icon):
    if app_config.STEP > 10:
        app_config.STEP -= 10
        logger.debug(f"⚙️ Уменьшен шаг смещения: {app_config.STEP}")
        icon.menu = create_menu()
        icon.update_menu()


def toggle_line_wrap(icon):
    check_settings()
    icon.menu = create_menu()
    icon.update_menu()


def create_menu():
    settings_file = app_config.SETTINGS_JSON_PATH
    settings_dir = dirname(settings_file)

    return Menu(
        MenuItem(
            "⚙️ Change shift step...",
            Menu(
                MenuItem(f"✔️  Current step: {app_config.STEP}", None, enabled=False),
                MenuItem("➕ Increase step (10)", increase_step),
                MenuItem("➖ Decrease step (10)", decrease_step),
            )
        ),
        MenuItem('⏩  Shift right (Alt + Right)', None),
        MenuItem('⏪  Shift left (Alt + Left)', None),
        MenuItem('↩️  Reset (Alt + Down)', lambda icon, item: update_padding(reset=True)),
        MenuItem(f"{'❌  Disable' if app_config.LINE_WRAP else '✅  Enable'} (Alt + Up)", toggle_line_wrap),
        MenuItem(
            "ℹ️  Path to WT config",
            Menu(
                MenuItem(f"Config: {basename(settings_file)}", lambda icon, item: os.startfile(settings_file)),
                MenuItem(f"Directory: {basename(settings_dir)}", lambda icon, item: os.startfile(settings_dir)),
            )
        ),
        MenuItem('❌  Quit (Alt + Q)', lambda icon, item: icon.stop())
    )


def create_icon():
    """Создаёт объект Icon и сохраняет его для дальнейшего доступа."""
    global _icon_instance
    if _icon_instance is None:
        image = Image.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon', 'ICO.png'))
        _icon_instance = Icon("WT_horizontal_scroll", image, "WT Horizontal Scroll", create_menu())
    return _icon_instance


def get_icon():
    """Возвращает уже созданный объект Icon, если он существует."""
    if _icon_instance is None:
        raise RuntimeError("Icon ещё не создан. Сначала вызовите create_icon().")
    return _icon_instance
