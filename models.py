from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    id: int
    nom: str
    notes: List[float] = []  # Liste vide par défaut pour les notes

class Classe(BaseModel):
    id: int
    nom: str
    etudiants: List[Student] = [] # On stocke directement les objets étudiants ici