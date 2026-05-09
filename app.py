from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Conexão com MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
colecao = db["formulario"]


# ──────────────────────────────────────────────
# READ — Listar todos os registros
# ──────────────────────────────────────────────
@app.route("/")
def index():
    registros = list(colecao.find())
    for r in registros:
        r["_id"] = str(r["_id"])
    return render_template("index.html", registros=registros)


# ──────────────────────────────────────────────
# CREATE — Exibir formulário e salvar
# ──────────────────────────────────────────────
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()

        erros = []
        if not nome:
            erros.append("Nome é obrigatório.")
        if not email:
            erros.append("E-mail é obrigatório.")
        if not telefone:
            erros.append("Telefone é obrigatório.")

        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("form.html", acao="novo",
                                   dados={"nome": nome, "email": email, "telefone": telefone})

        colecao.insert_one({"nome": nome, "email": email, "telefone": telefone})
        flash("Registro criado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("form.html", acao="novo", dados={})


# ──────────────────────────────────────────────
# UPDATE — Exibir formulário de edição e salvar
# ──────────────────────────────────────────────
@app.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        flash("ID inválido.", "erro")
        return redirect(url_for("index"))

    registro = colecao.find_one({"_id": oid})
    if not registro:
        flash("Registro não encontrado.", "erro")
        return redirect(url_for("index"))

    registro["_id"] = str(registro["_id"])

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()

        erros = []
        if not nome:
            erros.append("Nome é obrigatório.")
        if not email:
            erros.append("E-mail é obrigatório.")
        if not telefone:
            erros.append("Telefone é obrigatório.")

        if erros:
            for e in erros:
                flash(e, "erro")
            return render_template("form.html", acao="editar",
                                   dados={"_id": id, "nome": nome, "email": email, "telefone": telefone})

        colecao.update_one({"_id": oid}, {"$set": {"nome": nome, "email": email, "telefone": telefone}})
        flash("Registro atualizado com sucesso!", "sucesso")
        return redirect(url_for("index"))

    return render_template("form.html", acao="editar", dados=registro)


# ──────────────────────────────────────────────
# DELETE — Remover registro
# ──────────────────────────────────────────────
@app.route("/deletar/<id>", methods=["POST"])
def deletar(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        flash("ID inválido.", "erro")
        return redirect(url_for("index"))

    resultado = colecao.delete_one({"_id": oid})
    if resultado.deleted_count:
        flash("Registro excluído com sucesso!", "sucesso")
    else:
        flash("Registro não encontrado.", "erro")
    return redirect(url_for("index"))


# ──────────────────────────────────────────────
# API JSON (bonus)
# ──────────────────────────────────────────────
@app.route("/api/registros")
def api_registros():
    registros = list(colecao.find())
    for r in registros:
        r["_id"] = str(r["_id"])
    return jsonify(registros)


if __name__ == "__main__":
    app.run()