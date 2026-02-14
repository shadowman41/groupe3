from flask import Flask, render_template, request, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   
        database="login"
    )

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM personne WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and user[0]==password:
            return " Connexion réussie "
        else:
            flash(" Identifiants incorrects")

    return render_template("formulaire.html")

if __name__ == "__main__":
    app.run(port=5003)
