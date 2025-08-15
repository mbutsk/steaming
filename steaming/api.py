import os
import random
import time
from dataclasses import dataclass, field

import requests

from . import config, steamutils, exceptions

import tmdb


@dataclass
class Manager:
    config_path: str
    games: list[steamutils.NonSteamGame] = field(default_factory=list)

    @classmethod
    def build(cls, config_path: str):
        config_path = os.path.expanduser(
            config_path.format(steamid=config.STEAM_ID)
        )
        shortcuts_path = os.path.join(config_path, "shortcuts.vdf")
        with open(shortcuts_path, "rb+") as fp:
            return cls(
                config_path=config_path,
                games=steamutils.NonSteamGame.list_from_vdf(fp),
            )

    def add_movie(
        self,
        title: str,
        url: str,
        icon_path: str = "",
        movie: "tmdb.Movie.Movie | None" = None,
    ):
        app_id = app_id = -next(
            x
            for x in iter(lambda: random.randint(int(1e8), 999999999), None)
            if -x not in self.games
        )
        game = steamutils.NonSteamGame(
            app_id,
            title,
            "echo",
            "",
            icon_path,
            config.OPEN_URL_COMMAND.format(url=url) + r" & %command%",
            int(time.time()),
        )
        self.games.append(game)
        game.add_to_library(os.path.join(self.config_path, "shortcuts.vdf"))

        if movie:
            image_url = movie.get('full-size cover url')

            if not image_url:
                raise exceptions.NoPosterException()

            save_path = os.path.join(
                self.config_path, "grid", f"{game.grid_hash}_hero.png"
            )
            img_data = requests.get(image_url).content
            with open(save_path, "wb") as f:
                f.write(img_data)
