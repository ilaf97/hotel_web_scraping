from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class Hotel:
	name: str
	description: str
	best_for: dict[str]
	rooms: str
	location: dict[str: Union[str, list[int]]]
	facilities: list[str]
	meals: str
	images: list[str]
	resort: Optional[str] = None
	failed_reason: Optional[str] = None

