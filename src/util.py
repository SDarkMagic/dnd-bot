import json
import pathlib

class Config:
    def __init__(self, config_path='config.json'):
        self.path = config_path
        self.data = self._load()
        self.asset_path = pathlib.Path(__file__).parent.parent / 'assets'
        return

    def _load(self):
        with open(self.path, 'rt') as config_raw:
            return json.loads(config_raw.read())