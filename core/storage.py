from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

BASE_DIR = Path(".data")
BASE_DIR.mkdir(exist_ok=True)

def _file_for(key: str) -> Path:
    return BASE_DIR / f"{key}.json"

def save_model(key: str, model: BaseModel) -> None:
    path = _file_for(key)
    path.write_text(model.model_dump_json(indent=2), encoding="utf-8")

def load_model(key: str, model_cls: Type[T]) -> Optional[T]:
    path = _file_for(key)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return model_cls.model_validate(data)
