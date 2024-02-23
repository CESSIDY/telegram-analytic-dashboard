from dataclasses import dataclass


@dataclass
class ChannelLoaderModel:
    """
    if channel private and link contain '+' in the begin, then just remove it '+Ewa34r3fAWhjnv' -> 'Ewa34r3fAWhjnv'
    for 'id' just use 'hash' - https://t.me/hash
    """
    id: str
    private: bool

    def __init__(self, id: str, private: bool):
        self.id = id
        self.private = private
