from fastapi import FastAPI
from models import Student, Classe

app = FastAPI()

# Base de données en mémoire
base_classes = []

#  GESTION DES CLASSES 

@app.post("/classes")
def creer_classe(nouvelle_classe: Classe):
    for c in base_classes:
        if c.id == nouvelle_classe.id:
            return {"erreur": "Cette classe existe deja"}
    
    base_classes.append(nouvelle_classe)
    return {"message": "Classe cree avec succes"}

@app.get("/classes")
def afficher_classes():
    return base_classes

# GESTION DES ÉTUDIANTS 

@app.post("/classes/{classe_id}/etudiants")
def ajouter_un_etudiant_dans_une_classe(classe_id: int, etudiant: Student):
    for c in base_classes:
        if c.id == classe_id:
            for e in c.etudiants:
                if e.id == etudiant.id:
                    return {"erreur": "Cet etudiant existe deja dans cette classe"}
            
            c.etudiants.append(etudiant)
            return {"message": f"Etudiant {etudiant.nom} ajoute a la classe {c.nom}"}
    
    return {"erreur": "Classe introuvable"}

# NOTES ET STATISTIQUES

@app.post("/etudiants/{etudiant_id}/notes")
def ajouter_une_note(etudiant_id: int, note: float):
    for c in base_classes:
        for e in c.etudiants:
            if e.id == etudiant_id:
                e.notes.append(note)
                return {"message": f"Note {note} ajoutee a {e.nom}"}
    return {"erreur": "Etudiant introuvable"}

@app.get("/etudiants/{etudiant_id}/moyenne")
def moyenne_etudiant(etudiant_id: int):
    for c in base_classes:
        for e in c.etudiants:
            if e.id == etudiant_id:
                if len(e.notes) == 0:
                    return {"moyenne": 0, "message": "Aucune note pour le moment"}
                
                moyenne = sum(e.notes) / len(e.notes)
                return {"nom": e.nom, "moyenne": moyenne}
    return {"erreur": "Etudiant introuvable"}

@app.get("/statistiques")
def statistiques_generales():
    total_eleves = sum(len(c.etudiants) for c in base_classes)
    
    return {
        "nombre_total_classes": len(base_classes),
        "nombre_total_etudiants": total_eleves
    }

@app.delete("/classes/{classe_id}")
def supprimer_une_classe(classe_id: int):
    for c in base_classes:
        if c.id == classe_id:
            base_classes.remove(c)
            return {"message": "Classe supprimee"}
    return {"erreur": "Classe introuvable"}
