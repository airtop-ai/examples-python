
from typing import Optional

from prompts import Therapist
from pydantic import BaseModel


class State(BaseModel):
    urls: Optional[list[str]] = []
    therapists: Optional[list[Therapist]] = []
