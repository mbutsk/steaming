from __future__ import annotations

from typing import TextIO

import vdf

from dataclasses import dataclass


@dataclass
class NonSteamGame:
    app_id: int
    name: str
    exe_path: str
    start_dir: str
    icon_path: str
    launch_options: str
    is_hidden: bool
    last_play_time: int

    @classmethod
    def from_dict(cls, data: dict) -> NonSteamGame:
        return NonSteamGame(
            app_id=data["appid"],
            name=data["AppName"],
            exe_path=data["Exe"],
            start_dir=data["StartDir"],
            icon_path=data["icon"],
            launch_options=data["LaunchOptions"],
            is_hidden=data["IsHidden"],
            last_play_time=data["LastPlayTime"],
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

    def add_to_library(self, fp: TextIO):
        shortcuts = vdf.binary_load(fp)
        shortcuts["shortcuts"][str(self.app_id)] = self.to_dict()
        vdf.dump(shortcuts, fp)
