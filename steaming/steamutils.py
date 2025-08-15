from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO

import vdf


@dataclass
class NonSteamGame:
    app_id: int
    name: str
    exe_path: str
    start_dir: str
    icon_path: str
    launch_options: str
    last_play_time: int
    is_hidden: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> NonSteamGame:
        return NonSteamGame(
            app_id=data["appid"],
            name=data["AppName"],
            exe_path=data["Exe"],
            start_dir=data["StartDir"],
            icon_path=data["icon"],
            launch_options=data["LaunchOptions"],
            last_play_time=data["LastPlayTime"],
            is_hidden=data["IsHidden"],
        )

    @classmethod
    def list_from_vdf(cls, fp: TextIO) -> list[NonSteamGame]:
        raw_games = [
            value
            for number, value in vdf.binary_load(fp)
            .get("shortcuts", {})
            .items()
        ]

        return [cls.from_dict(game) for game in raw_games]

    def to_dict(self) -> dict:
        return {
            "appid": self.app_id,
            "AppName": self.name,
            "Exe": self.exe_path,
            "StartDir": self.start_dir,
            "icon": self.icon_path,
            "ShortcutPath": "",
            "LaunchOptions": self.launch_options,
            "IsHidden": int(self.is_hidden),
            "AllowDesktopConfig": 1,
            "AllowOverlay": 1,
            "OpenVR": 0,
            "Devkit": 0,
            "DevkitGameID": "",
            "DevkitOverrideAppID": 0,
            "LastPlayTime": self.last_play_time,
            "FlatpakAppID": "",
            "tags": {},
        }

    def add_to_library(self, shortcuts_path: TextIO):
        with open(shortcuts_path, "rb") as fp:
            shortcuts = vdf.binary_load(fp)
        games = shortcuts.setdefault("shortcuts", {})

        if games:
            indices = list(map(int, games.keys()))
            new_index = str(max(indices) + 1)
        else:
            new_index = "0"

        games[new_index] = self.to_dict()

        with open(shortcuts_path, "wb") as fp:
            vdf.binary_dump(shortcuts, fp)

    @property
    def grid_hash(self):
        return self.app_id & 0xFFFFFFFF
