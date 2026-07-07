from flask import Flask, jsonify, render_template, make_response, send_from_directory
from db import inserir_senha, proxima_senha, chamar_senha, ultima_chamada, listar_tickets, limpar_tickets
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# A pasta "mp3" está ao lado da pasta "backend" (não dentro dela), por isso
# indicamos ao Flask onde ela está e sob que URL a deve servir.
# Resultado: o ficheiro backend/../mp3/som.mp3 fica acessível em /mp3/som.mp3
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "..", "mp3"),
    static_url_path="/mp3"
)

# A pasta "imagens" também está ao lado da pasta "backend".
# Flask só permite configurar UMA pasta estática "default" (a de cima, para o mp3),
# por isso servimos a pasta "imagens" através de uma rota própria.
IMAGENS_DIR = os.path.join(BASE_DIR, "..", "imagens")

@app.route("/imagens/<path:filename>")
def imagens(filename):
    return send_from_directory(IMAGENS_DIR, filename)


# Pasta "css" -- esta já está DENTRO da pasta "backend" (é código da aplicação,
# ao contrário do mp3/imagens que são ficheiros fornecidos por ti).
CSS_DIR = os.path.join(BASE_DIR, "css")

@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(CSS_DIR, filename)


# Página da máquina touch
@app.route("/")
def home():
    return render_template("index.html")


# Página do painel da TV
@app.route("/painel")
def painel():
    return render_template("painel.html")


# Emitir senha (G ou P)
@app.route("/emitir/<tipo>", methods=["POST"])
def emitir(tipo):
    tipo = tipo.upper()
    if tipo not in ("G", "P"):
        return jsonify({"erro": "Tipo inválido"}), 400

    codigo = inserir_senha(tipo)
    return jsonify({"codigo": codigo})


# Ver a próxima senha pendente (não usada no painel)
@app.route("/proxima", methods=["GET"])
def proxima():
    senha = proxima_senha()
    if not senha:
        return jsonify({"codigo": None, "mensagem": "Sem senhas pendentes"}), 200

    id_senha, codigo = senha
    return jsonify({"id": id_senha, "codigo": codigo})


# Chamar a próxima senha
@app.route("/chamar", methods=["POST"])
def chamar():
    senha = proxima_senha()
    if not senha:
        # Devolvemos sempre a chave "codigo" (a None) para o frontend
        # nunca ter de lidar com "undefined".
        return jsonify({"codigo": None, "mensagem": "Sem senhas para chamar"}), 200

    id_senha, codigo = senha
    chamar_senha(id_senha)
    return jsonify({"id": id_senha, "codigo": codigo})


# Última senha chamada (usada pelo painel da TV)
@app.route("/ultima_chamada", methods=["GET"])
def ultima_chamada_route():
    codigo = ultima_chamada()
    response = make_response(jsonify({"codigo": codigo}))
    # Garante que o browser/painel nunca fica com uma resposta antiga em cache
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


# --- Endpoints de diagnóstico / gestão (úteis durante os testes) ---

@app.route("/debug/tickets", methods=["GET"])
def debug_tickets():
    """Lista todos os tickets e o seu estado. Útil para verificar o que está na BD."""
    tickets = listar_tickets()
    return jsonify([
        {"id": t[0], "tipo": t[1], "numero": t[2], "codigo": t[3],
         "estado": t[4], "ordem_chamada": t[5]}
        for t in tickets
    ])


@app.route("/debug/limpar", methods=["POST"])
def debug_limpar():
    """Apaga todas as senhas. Usar para reiniciar o sistema (ex: início de dia)."""
    limpar_tickets()
    return jsonify({"mensagem": "Todas as senhas foram apagadas"})


if __name__ == "__main__":
    app.run(debug=True)