import json


class Config:
    default_config_path = 'config.json'

    def __init__(self, config_path=None) -> None:
        self._config_path = config_path or self.default_config_path
        self._conf = {}
        
    def load(self) -> dict:
        with open(self._config_path, 'r') as file:
            self._conf = json.load(file)
    
    def __getitem__(self, index):
        return self._conf[index]

    def __repr__(self):
        return repr(self._conf)