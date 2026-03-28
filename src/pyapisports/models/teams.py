from dataclasses import dataclass


@dataclass
class Team:
    id: int
    name: str
    code: str
    country: str
    founded: int
    national: bool
    logo: str
