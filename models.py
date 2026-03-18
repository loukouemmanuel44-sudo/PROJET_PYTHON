from pydantic import BaseModel, Field
from typing import List

class Student(BaseModel):
    id: int
    nom: str
    notes: List[float] = Field(default_factory=list)

class Classe(BaseModel):
    id: int
    nom: str
    etudiants: List[Student] = Field(default_factory=list)
