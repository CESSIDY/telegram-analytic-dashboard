from dataclasses import dataclass


@dataclass
class ChannelLoaderModel:
    """
    if channel private and link contain '+' in the begin, then just remove it '+Eywa34cr3fAWhjnv' -> 'Eywa34cr3fAWhjnv'
    for 'id' just use 'hash' - https://t.me/hash
    """
    id: str

    def __init__(self, id: str):
        self.id = id
