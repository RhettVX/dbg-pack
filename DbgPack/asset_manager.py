from collections import ChainMap
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, ChainMap as ChainMapType, Union

from .abc import AbstractPack, AbstractAsset
from .loose_pack import LoosePack
from .pack1 import Pack1
from .pack2 import Pack2
from .hash import crc64


# TODO: calculate file type from asset header
# TODO: Filter by type or pack group
# TODO: option to lookup directly by name, no hash calc
# TODO: Apply namelist
# TODO: Calculate MD5 hash of unpacked assets while creating asset index
# TODO: Optimize pack reading


@dataclass
class AssetManager:
    packs: List[AbstractPack]
    assets: ChainMapType[int, AbstractAsset] = field(repr=False)

    @staticmethod
    def load_pack(path: Path):
        if path.is_file():
            if path.suffix == '.pack':
                return Pack1(path)
            elif path.suffix == '.pack2':
                return Pack2(path)
        else:
            return LoosePack(path)

    def export_pack2(self, name: str, outdir: Path, raw=False):
        Pack2.export(list(self.assets.values()), name, outdir, raw)

    def __init__(self, paths: List[Path]):
        self.packs = [AssetManager.load_pack(path) for path in paths]
        self.assets = ChainMap(*[p.assets for p in self.packs])

    def __len__(self):
        return len(self.assets)

    def __getitem__(self, item: Union[str, int]):
        try:
            if isinstance(item, str):
                return_asset = self.assets[crc64(item)]
                if return_asset:  # Set the asset name while we're here
                    return_asset.name = item

                return return_asset

            elif isinstance(item, int):
                return self.assets[item]
            else:
                raise KeyError

        except KeyError:
            print(f'[!!] Unable to find "{item}"')

    def __contains__(self, item):
        return item in self.assets

    def __iter__(self):
        return iter(self.assets.values())
