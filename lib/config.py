import os
from pathlib import Path


def get_or_create_default_config_dir():
    config_dir = os.path.join(str(Path.home()), ".tie")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    return config_dir
