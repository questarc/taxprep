from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class AppConfig:
    app_name: str = "LLC Tax Prep Studio"
    supported_states: List[str] = ("MA", "NY", "CA", "TX", "FL")
    default_state: str = "MA"
    currency_symbol: str = "$"

CONFIG = AppConfig()
