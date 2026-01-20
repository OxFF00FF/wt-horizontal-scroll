import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    STEP: int = 50
    DEFAULT_PADDING: list
    SETTINGS_JSON_PATH: str = os.path.join(os.path.dirname(os.environ.get('APPDATA')), 'Local', 'Packages', 'Microsoft.WindowsTerminal_8wekyb3d8bbwe', 'LocalState', 'settings.json')
    LINE_WRAP: bool
    DEBUG: bool

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.config'))


app_config: Config = Config()
