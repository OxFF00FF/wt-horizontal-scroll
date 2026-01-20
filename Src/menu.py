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
            "⚙️ Изменить шаг смещения...",
            Menu(
                MenuItem(f"✔️  Текущий шаг: {app_config.STEP}", None, enabled=False),
                MenuItem("➕ Увеличить шаг (10)", increase_step),
                MenuItem("➖ Уменьшить шаг (10)", decrease_step),
            )
        ),
        MenuItem('⏩  Смещение вправо (Alt + Right)', None),
        MenuItem('⏪  Смещение влево (Alt + Left)', None),
        MenuItem('↩️  Сбросить (Alt + Down)', lambda icon, item: update_padding(reset=True)),
        MenuItem(f"{'❌  Отключить' if app_config.LINE_WRAP else '✅  Включить'} (Alt + Up)", toggle_line_wrap),
        MenuItem(
            "ℹ️  Путь до конфига WT",
            Menu(
                MenuItem(f"Конфиг: {basename(settings_file)}", lambda icon, item: os.startfile(settings_file)),
                MenuItem(f"Папка: {basename(settings_dir)}", lambda icon, item: os.startfile(settings_dir)),
            )
        ),
        MenuItem('❌  Выход (Alt + Q)', lambda icon, item: icon.stop())
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
