import random
import time
from dataclasses import dataclass, field

from . import config, steamutils


@dataclass
class Manager:
    shortcuts_path: str
    games: list[steamutils.NonSteamGame] = field(default_factory=list)

    @classmethod
    def build(cls, shortcuts_path: str):
        with open(shortcuts_path, "rb+") as fp:
            return cls(
                shortcuts_path=shortcuts_path,
                games=steamutils.NonSteamGame.list_from_vdf(fp),
            )

    def add_movie(self, title: str, icon_path: str, url: str):
        app_id = app_id = -next(
            x
            for x in iter(lambda: random.randint(int(1e8), 999999999), None)
            if -x not in self.games
        )
        game = steamutils.NonSteamGame(
            app_id,
            title,
            "",
            "",
            icon_path,
            config.OPEN_URL_COMMAND.format(url=url),
            int(time.time()),
        )
        self.games.append(game)
        game.add_to_library(self.shortcuts_path)
