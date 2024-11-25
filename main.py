import logging
from src.schedule.removeMember import RemoveMember
from src.config import Config
from src.sqlite import SQLite
from src.bcz import BCZ



config = Config()
logger = config.logger
sqlite = SQLite(config)
bcz = BCZ(config)


removeMember = RemoveMember(config, sqlite, bcz)