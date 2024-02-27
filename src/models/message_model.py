from dataclasses import dataclass, field
from typing import ByteString
from datetime import datetime


@dataclass(frozen=True, order=True)
class EmojiLoaderModel:
    emoticon: ByteString = field()
    count: int = field(compare=False, hash=False, repr=True)


@dataclass
class MessageLoaderModel:
    id: int
    chat_id: int
    message: str
    views: int
    forwards: int
    replies: int
    emojis: list[EmojiLoaderModel]
    date: datetime
