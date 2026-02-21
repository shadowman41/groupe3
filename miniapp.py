from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
app.secret_key = "secret123"

# Configuration SQLAlchemy MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:stsdevpassword@stsohiodb.cjgwc262s6im.us-east-2.rds.amazonaws.com:3306/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Base pour les modèles
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Modèle Personne (crée la table automatiquement)
class Personne(db.Model):
    __tablename__ = 'personne'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Requête SQLAlchemy (sécurisée automatiquement)
        user = Personne.query.filter_by(username=username).first()
        
        if user and user.password == password:
            return "Connexion réussie"
        else:
            flash("Identifiants incorrects")

    return render_template("formulaire.html")

# Route pour créer les tables (une seule fois)
@app.route("/create_tables")
def create_tables():
    with app.app_context():
        db.create_all()
    return "Tables créées !"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crée les tables au démarrage
    app.run(port=5003, debug=True)
