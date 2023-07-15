from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class Hotel:
	name: str
	description: str
	best_for: dict[str]
	rooms: str
	location: dict[str: Union[str, list[int]]]
	individual_facilities: list[str]
	facilities_descriptions: dict[str, str]
	images: list[str]
	resort: Optional[str] = None
	slug: Optional[str] = None
	failed_reason: Optional[str] = None


@dataclass
class ScrapeFailHotel:
	name: str
	url: str
	failed_reason: str
