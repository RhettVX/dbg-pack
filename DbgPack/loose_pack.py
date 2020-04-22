from dataclasses import dataclass
from typing import Dict
from pathlib import Path
from os import walk

from .abc import AbstractPack
from .loose_asset import LooseAsset
from .hash import crc64


@dataclass
class LoosePack(AbstractPack):
    name: str
    path: Path

    asset_count: int
    assets: Dict[int, LooseAsset]

    def __init__(self, path: Path):
        super().__init__(path)

        self.assets = {}
        for root, _, files in walk(self.path):
            for file in files:
                asset = LooseAsset(name=file, path=self.path)
                self.assets[asset.name_hash] = asset

    def __repr__(self):
        return super().__repr__()

    def __len__(self):
        return super().__len__()

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __iter__(self):
        return iter(self.assets.values())

    def __contains__(self, item):
        super().__contains__(item)
