from flask import Blueprint, request, jsonify, render_template
from app import db
from models import Electeur, Candidat, Vote

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/electeurs', methods=['POST'])
def create_electeur():
    data = request.json
    electeur = Electeur(nom=data['nom'], email=data['email'], mot_de_passe="")
    electeur.set_password(data['mot_de_passe'])
    db.session.add(electeur)
    db.session.commit()
    return jsonify({"id": electeur.id})

@main.route('/candidats', methods=['GET'])
def get_candidats():
    candidats = Candidat.query.all()
    return jsonify([{"id": c.id, "nom": c.nom} for c in candidats])

@main.route('/candidats', methods=['POST'])
def create_candidat():
    data = request.json
    candidat = Candidat(nom=data['nom'])
    db.session.add(candidat)
    db.session.commit()
    return jsonify({"id": candidat.id})

@main.route('/vote', methods=['POST'])
def voter():
    data = request.json
    vote_existant = Vote.query.filter_by(electeur_id=data['electeur_id']).first()
    if vote_existant:
        return jsonify({"erreur": "Cet électeur a déjà voté"}), 400
    vote = Vote(
        electeur_id=data['electeur_id'],
        candidat_id=data['candidat_id']
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify({"message": "Vote enregistré"})

@main.route('/resultats', methods=['GET'])
def resultats():
    candidats = Candidat.query.all()
    result = []
    for c in candidats:
        nb_votes = Vote.query.filter_by(candidat_id=c.id).count()
        result.append({"candidat": c.nom, "votes": nb_votes})
    return jsonify(result)