from dataclasses import dataclass


@dataclass
class Clip:
    id: str
    url: str
    embed_url: str
    broadcaster_id: str
    broadcaster_name: str
    creator_id: str
    creator_name: str
    video_id: str
    game_id: str
    language: str
    title: str
    view_count: int
    created_at: str
    thumbnail_url: str
    duration: float = 0.0
    clip_id: int = 0
    vod_offset: int = 0
