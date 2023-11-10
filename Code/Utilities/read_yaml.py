from typing import LiteralString

import yaml

def load_yaml_content(yaml_route : LiteralString) -> dict:
    """
    Return some content from a yaml file.
    
    Parameters:
    -----------
    - `yaml_route` : `LiteralString`
        A path to the yaml file to read.
    """
    with open(yaml_route, 'r', encoding='utf-8') as fd:
        return yaml.load(fd, Loader=yaml.FullLoader)