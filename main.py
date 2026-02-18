from fastapi import FastAPI
from models import Student, Classe

app = FastAPI()

# Nos listes de stockage (comme tes listes de comptes)
base_classes = []

# --- GESTION DES CLASSES ---

@app.post("/classes")
def creer_classe(nouvelle_classe: Classe):
    # Vérifier si la classe existe déjà (Fonctionnalité Bonus)
    for c in base_classes:
        if c.id == nouvelle_classe.id:
            return {"erreur": "Cette classe existe deja"}
    
    base_classes.append(nouvelle_classe)
    return {"message": "Classe cree avec succes"}

@app.get("/classes")
def afficher_classes():
    return base_classes

# --- GESTION DES ÉTUDIANTS ---

@app.post("/classes/{classe_id}/etudiants")
def ajouter_un_etudiant_dans_une_classe(classe_id: int, etudiant: Student):
    for c in base_classes:
        if c.id == classe_id:
            # Empêcher les doublons par ID (Fonctionnalité Bonus)
            for e in c.etudiants:
                if e.id == etudiant.id:
                    return {"erreur": "Cet etudiant existe deja dans cette classe"}
            
            c.etudiants.append(etudiant)
            return {"message": f"Etudiant {etudiant.nom} ajoute a la classe {c.nom}"}
    
    return {"erreur": "Classe introuvable"}

# --- FONCTIONNALITÉS SUPPLÉMENTAIRES (POUR LA MEILLEURE NOTE) ---

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
                
                # Calcul simple de la moyenne
                total = sum(e.notes)
                moyenne = total / len(e.notes)
                return {"nom": e.nom, "moyenne": moyenne}
    return {"erreur": "Etudiant introuvable"}

@app.get("/statistiques")
def statistiques_generales():
    total_eleves = 0
    for c in base_classes:
        total_eleves += len(c.etudiants)
    
    return {
        "nombre_total_classes": len(base_classes),
        "nombre_total_etudiants": total_eleves
    }

@app.delete("/classes/{classe_id}")
def supprimer_une_classe(classe_id: int):
    for i in range(len(base_classes)):
        if base_classes[i].id == classe_id:
            base_classes.pop(i)
            return {"message": "Classe supprimee"}
    return {"erreur": "Classe introuvable"}