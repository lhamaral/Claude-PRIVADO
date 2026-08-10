import csv
import io
from datetime import datetime, date, timedelta

from flask import Flask, request, jsonify, render_template, Response

import models
import reports
from calculator import calcular_dose
from config import PRESCRICAO_PADRAO

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)

models.init_db()
models.seed_config_if_empty(PRESCRICAO_PADRAO)


def _now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


# ---------- páginas ----------

@app.route("/")
def dashboard():
    return render_template("index.html")


# ---------- configuração ----------

@app.route("/api/config", methods=["GET"])
def api_get_config():
    return jsonify(models.get_config())


@app.route("/api/config", methods=["POST"])
def api_set_config():
    body = request.get_json(force=True)
    for chave, valor in body.items():
        models.set_config_value(chave, valor)
    return jsonify(models.get_config())


# ---------- calculadora ----------

@app.route("/api/calcular_dose", methods=["POST"])
def api_calcular_dose():
    body = request.get_json(force=True)
    carbs = float(body.get("carboidratos_g", 0))
    glicemia = int(body["glicemia_atual_mgdl"])
    cfg = models.get_config()
    sugestao = calcular_dose(carbs, glicemia, cfg)
    return jsonify(sugestao.__dict__)


# ---------- refeições ----------

@app.route("/api/refeicoes", methods=["GET"])
def api_listar_refeicoes():
    conn = models.get_connection()
    rows = conn.execute(
        "SELECT * FROM refeicoes ORDER BY datahora DESC LIMIT 200"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/refeicoes", methods=["POST"])
def api_criar_refeicao():
    body = request.get_json(force=True)
    conn = models.get_connection()
    cur = conn.execute(
        "INSERT INTO refeicoes (datahora, descricao, carboidratos_g, origem, observacoes) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            body.get("datahora") or _now(),
            body["descricao"],
            float(body["carboidratos_g"]),
            body.get("origem", "texto"),
            body.get("observacoes"),
        ),
    )
    conn.commit()
    novo_id = cur.lastrowid
    conn.close()
    return jsonify({"id": novo_id}), 201


# ---------- glicemias ----------

@app.route("/api/glicemias", methods=["GET"])
def api_listar_glicemias():
    conn = models.get_connection()
    rows = conn.execute(
        "SELECT * FROM glicemias ORDER BY datahora DESC LIMIT 200"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/glicemias", methods=["POST"])
def api_criar_glicemia():
    body = request.get_json(force=True)
    conn = models.get_connection()
    cur = conn.execute(
        "INSERT INTO glicemias (datahora, valor_mgdl, contexto, origem, observacoes) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            body.get("datahora") or _now(),
            int(body["valor_mgdl"]),
            body.get("contexto", "aleatoria"),
            body.get("origem", "medidor_livre"),
            body.get("observacoes"),
        ),
    )
    conn.commit()
    novo_id = cur.lastrowid
    conn.close()
    return jsonify({"id": novo_id}), 201


# ---------- doses de insulina ----------

@app.route("/api/doses", methods=["GET"])
def api_listar_doses():
    conn = models.get_connection()
    rows = conn.execute(
        "SELECT * FROM doses_insulina ORDER BY datahora DESC LIMIT 200"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/doses", methods=["POST"])
def api_criar_dose():
    body = request.get_json(force=True)
    conn = models.get_connection()
    cur = conn.execute(
        "INSERT INTO doses_insulina "
        "(datahora, tipo, insulina, unidades, refeicao_id, glicemia_id, observacoes) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            body.get("datahora") or _now(),
            body["tipo"],
            body["insulina"],
            float(body["unidades"]),
            body.get("refeicao_id"),
            body.get("glicemia_id"),
            body.get("observacoes"),
        ),
    )
    conn.commit()
    novo_id = cur.lastrowid
    conn.close()
    return jsonify({"id": novo_id}), 201


# ---------- relatórios ----------

@app.route("/api/relatorios/tempo_no_alvo")
def api_tempo_no_alvo():
    fim = request.args.get("fim") or date.today().isoformat()
    inicio = request.args.get("inicio") or (date.today() - timedelta(days=13)).isoformat()
    cfg = models.get_config()
    return jsonify(reports.tempo_no_alvo(
        inicio, fim, cfg["faixa_alvo_min_mgdl"], cfg["faixa_alvo_max_mgdl"]
    ))


@app.route("/api/relatorios/curva/<data_str>")
def api_curva(data_str):
    return jsonify(reports.curva_glicemica_por_dia(data_str))


@app.route("/api/relatorios/padrao_diario")
def api_padrao_diario():
    fim = request.args.get("fim") or date.today().isoformat()
    inicio = request.args.get("inicio") or (date.today() - timedelta(days=13)).isoformat()
    return jsonify(reports.padrao_diario(inicio, fim))


@app.route("/api/relatorios/resumo_diario/<data_str>")
def api_resumo_diario(data_str):
    return jsonify(reports.resumo_diario(data_str))


# ---------- exportação ----------

def _export_csv(nome_tabela, colunas):
    conn = models.get_connection()
    rows = conn.execute(f"SELECT * FROM {nome_tabela} ORDER BY datahora").fetchall()
    conn.close()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=colunas)
    writer.writeheader()
    for r in rows:
        writer.writerow({c: r[c] for c in colunas})

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={nome_tabela}.csv"},
    )


@app.route("/api/export/refeicoes.csv")
def export_refeicoes():
    return _export_csv(
        "refeicoes", ["id", "datahora", "descricao", "carboidratos_g", "origem", "observacoes"]
    )


@app.route("/api/export/glicemias.csv")
def export_glicemias():
    return _export_csv(
        "glicemias", ["id", "datahora", "valor_mgdl", "contexto", "origem", "observacoes"]
    )


@app.route("/api/export/doses.csv")
def export_doses():
    return _export_csv(
        "doses_insulina",
        ["id", "datahora", "tipo", "insulina", "unidades", "refeicao_id", "glicemia_id", "observacoes"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
