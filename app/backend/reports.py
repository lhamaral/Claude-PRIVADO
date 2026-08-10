from collections import defaultdict
from statistics import mean, pstdev

from models import get_connection


def tempo_no_alvo(data_inicio: str, data_fim: str, faixa_min: int, faixa_max: int):
    """Time in Range (TIR) no período [data_inicio, data_fim] (YYYY-MM-DD)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT valor_mgdl FROM glicemias "
        "WHERE date(datahora) BETWEEN ? AND ?",
        (data_inicio, data_fim),
    ).fetchall()
    conn.close()

    valores = [r["valor_mgdl"] for r in rows]
    total = len(valores)
    if total == 0:
        return {
            "total_leituras": 0,
            "abaixo_pct": 0, "no_alvo_pct": 0, "acima_pct": 0,
            "media": None, "desvio_padrao": None,
        }

    abaixo = sum(1 for v in valores if v < faixa_min)
    acima = sum(1 for v in valores if v > faixa_max)
    no_alvo = total - abaixo - acima

    return {
        "total_leituras": total,
        "abaixo_pct": round(100 * abaixo / total, 1),
        "no_alvo_pct": round(100 * no_alvo / total, 1),
        "acima_pct": round(100 * acima / total, 1),
        "media": round(mean(valores), 1),
        "desvio_padrao": round(pstdev(valores), 1) if total > 1 else 0.0,
    }


def curva_glicemica_por_dia(data: str):
    """Todas as leituras de glicemia de um dia (YYYY-MM-DD), em ordem, para plotar a curva."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT datahora, valor_mgdl, contexto FROM glicemias "
        "WHERE date(datahora) = ? ORDER BY datahora",
        (data,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def padrao_diario(data_inicio: str, data_fim: str):
    """Agrupa leituras por hora do dia (0-23) para identificar padrões (ex: hiperglicemia recorrente após almoço)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT datahora, valor_mgdl FROM glicemias "
        "WHERE date(datahora) BETWEEN ? AND ?",
        (data_inicio, data_fim),
    ).fetchall()
    conn.close()

    por_hora = defaultdict(list)
    for r in rows:
        hora = int(r["datahora"][11:13])
        por_hora[hora].append(r["valor_mgdl"])

    return [
        {
            "hora": h,
            "media": round(mean(vs), 1),
            "min": min(vs),
            "max": max(vs),
            "n": len(vs),
        }
        for h, vs in sorted(por_hora.items())
    ]


def resumo_diario(data: str):
    conn = get_connection()
    carbs = conn.execute(
        "SELECT COALESCE(SUM(carboidratos_g), 0) AS total FROM refeicoes WHERE date(datahora) = ?",
        (data,),
    ).fetchone()["total"]

    insulina = conn.execute(
        "SELECT tipo, COALESCE(SUM(unidades), 0) AS total FROM doses_insulina "
        "WHERE date(datahora) = ? GROUP BY tipo",
        (data,),
    ).fetchall()

    glicemias = conn.execute(
        "SELECT valor_mgdl FROM glicemias WHERE date(datahora) = ? ORDER BY datahora",
        (data,),
    ).fetchall()
    conn.close()

    valores = [g["valor_mgdl"] for g in glicemias]
    return {
        "data": data,
        "carboidratos_totais_g": carbs,
        "insulina_por_tipo": {r["tipo"]: r["total"] for r in insulina},
        "insulina_total_ui": round(sum(r["total"] for r in insulina), 1),
        "glicemia_media": round(mean(valores), 1) if valores else None,
        "glicemia_min": min(valores) if valores else None,
        "glicemia_max": max(valores) if valores else None,
        "n_leituras": len(valores),
    }
