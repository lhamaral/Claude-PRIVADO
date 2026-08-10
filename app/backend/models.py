import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "glicemia.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS config (
    chave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS refeicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datahora TEXT NOT NULL,
    descricao TEXT NOT NULL,
    carboidratos_g REAL NOT NULL,
    origem TEXT NOT NULL DEFAULT 'texto',
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS glicemias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datahora TEXT NOT NULL,
    valor_mgdl INTEGER NOT NULL,
    contexto TEXT NOT NULL DEFAULT 'aleatoria',
    origem TEXT NOT NULL DEFAULT 'medidor_livre',
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS medicacoes_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datahora TEXT NOT NULL,
    nome TEXT NOT NULL,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS doses_insulina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datahora TEXT NOT NULL,
    tipo TEXT NOT NULL,          -- basal | bolus_refeicao | correcao
    insulina TEXT NOT NULL,      -- Glargina | Fiasp
    unidades REAL NOT NULL,
    refeicao_id INTEGER,
    glicemia_id INTEGER,
    observacoes TEXT,
    FOREIGN KEY (refeicao_id) REFERENCES refeicoes(id),
    FOREIGN KEY (glicemia_id) REFERENCES glicemias(id)
);
"""


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def seed_config_if_empty(defaults: dict):
    conn = get_connection()
    cur = conn.execute("SELECT COUNT(*) AS n FROM config")
    if cur.fetchone()["n"] == 0:
        conn.executemany(
            "INSERT INTO config (chave, valor) VALUES (?, ?)",
            [(k, str(v)) for k, v in defaults.items()],
        )
        conn.commit()
    conn.close()


def get_config():
    conn = get_connection()
    rows = conn.execute("SELECT chave, valor FROM config").fetchall()
    conn.close()
    cfg = {}
    for r in rows:
        v = r["valor"]
        try:
            v = float(v) if "." in v else int(v)
        except ValueError:
            pass
        cfg[r["chave"]] = v
    return cfg


def set_config_value(chave: str, valor):
    conn = get_connection()
    conn.execute(
        "INSERT INTO config (chave, valor) VALUES (?, ?) "
        "ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor",
        (chave, str(valor)),
    )
    conn.commit()
    conn.close()
