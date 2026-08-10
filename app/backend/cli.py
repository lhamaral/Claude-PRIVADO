"""Utilitário de linha de comando para registrar dados sem precisar do servidor web
rodando — útil quando os dados chegam via conversa (texto/áudio/foto) e precisam
ser gravados diretamente no banco.

Exemplos:
    python cli.py refeicao --descricao "arroz, feijao, frango" --carboidratos_g 55 --origem foto
    python cli.py glicemia --valor_mgdl 142 --contexto pre_refeicao
    python cli.py dose --tipo bolus_refeicao --insulina Fiasp --unidades 2.8
    python cli.py calcular --carboidratos_g 55 --glicemia_atual_mgdl 142
"""

import argparse
from datetime import datetime

import models
from calculator import calcular_dose, calcular_dose_fixa, calcular_correcao_basal
from config import PRESCRICAO_PADRAO

models.init_db()
models.seed_config_if_empty(PRESCRICAO_PADRAO)


def _now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def cmd_refeicao(args):
    conn = models.get_connection()
    cur = conn.execute(
        "INSERT INTO refeicoes (datahora, descricao, carboidratos_g, origem, observacoes) "
        "VALUES (?, ?, ?, ?, ?)",
        (args.datahora or _now(), args.descricao, args.carboidratos_g, args.origem, args.observacoes),
    )
    conn.commit()
    print(f"Refeição registrada, id={cur.lastrowid}")
    conn.close()


def cmd_glicemia(args):
    conn = models.get_connection()
    cur = conn.execute(
        "INSERT INTO glicemias (datahora, valor_mgdl, contexto, origem, observacoes) "
        "VALUES (?, ?, ?, ?, ?)",
        (args.datahora or _now(), args.valor_mgdl, args.contexto, args.origem, args.observacoes),
    )
    conn.commit()
    print(f"Glicemia registrada, id={cur.lastrowid}")
    conn.close()


def cmd_dose(args):
    conn = models.get_connection()
    cur = conn.execute(
        "INSERT INTO doses_insulina "
        "(datahora, tipo, insulina, unidades, refeicao_id, glicemia_id, observacoes) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            args.datahora or _now(), args.tipo, args.insulina, args.unidades,
            args.refeicao_id, args.glicemia_id, args.observacoes,
        ),
    )
    conn.commit()
    print(f"Dose registrada, id={cur.lastrowid}")
    conn.close()


def cmd_calcular(args):
    cfg = models.get_config()
    sugestao = calcular_dose(args.carboidratos_g, args.glicemia_atual_mgdl, cfg)
    print(sugestao.detalhes)


def cmd_dosefixa(args):
    cfg = models.get_config()
    sugestao = calcular_dose_fixa(args.refeicao, args.glicemia_atual_mgdl, cfg)
    print(sugestao.detalhes)


def cmd_basal(args):
    cfg = models.get_config()
    sugestao = calcular_correcao_basal(args.glicemia_jejum_mgdl, cfg)
    print(sugestao.detalhes)


def cmd_medicacao(args):
    conn = models.get_connection()
    conn.execute(
        "INSERT INTO medicacoes_log (datahora, nome, observacoes) VALUES (?, ?, ?)",
        (args.datahora or _now(), args.nome, args.observacoes),
    )
    conn.commit()
    conn.close()
    print(f"Medicação registrada: {args.nome}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="comando", required=True)

    p_ref = sub.add_parser("refeicao")
    p_ref.add_argument("--descricao", required=True)
    p_ref.add_argument("--carboidratos_g", type=float, required=True)
    p_ref.add_argument("--origem", default="texto", choices=["texto", "audio", "foto"])
    p_ref.add_argument("--observacoes", default=None)
    p_ref.add_argument("--datahora", default=None, help="YYYY-MM-DDTHH:MM:SS (padrão: agora)")
    p_ref.set_defaults(func=cmd_refeicao)

    p_gli = sub.add_parser("glicemia")
    p_gli.add_argument("--valor_mgdl", type=int, required=True)
    p_gli.add_argument("--contexto", default="aleatoria",
                        choices=["jejum", "pre_refeicao", "pos_refeicao", "aleatoria", "antes_dormir"])
    p_gli.add_argument("--origem", default="medidor_livre")
    p_gli.add_argument("--observacoes", default=None)
    p_gli.add_argument("--datahora", default=None)
    p_gli.set_defaults(func=cmd_glicemia)

    p_dose = sub.add_parser("dose")
    p_dose.add_argument("--tipo", required=True, choices=["basal", "bolus_refeicao", "correcao"])
    p_dose.add_argument("--insulina", required=True, choices=["Glargina", "Fiasp"])
    p_dose.add_argument("--unidades", type=float, required=True)
    p_dose.add_argument("--refeicao_id", type=int, default=None)
    p_dose.add_argument("--glicemia_id", type=int, default=None)
    p_dose.add_argument("--observacoes", default=None)
    p_dose.add_argument("--datahora", default=None)
    p_dose.set_defaults(func=cmd_dose)

    p_calc = sub.add_parser("calcular")
    p_calc.add_argument("--carboidratos_g", type=float, default=0)
    p_calc.add_argument("--glicemia_atual_mgdl", type=int, required=True)
    p_calc.set_defaults(func=cmd_calcular)

    p_fixa = sub.add_parser("dosefixa", help="Referência da receita — não somar à contagem de carboidratos")
    p_fixa.add_argument("--refeicao", required=True, choices=["cafe", "almoco", "jantar"])
    p_fixa.add_argument("--glicemia_atual_mgdl", type=int, required=True)
    p_fixa.set_defaults(func=cmd_dosefixa)

    p_basal = sub.add_parser("basal", help="Correção da dose basal (Glargina) pela glicemia de jejum")
    p_basal.add_argument("--glicemia_jejum_mgdl", type=int, required=True)
    p_basal.set_defaults(func=cmd_basal)

    p_med = sub.add_parser("medicacao")
    p_med.add_argument("--nome", required=True)
    p_med.add_argument("--observacoes", default=None)
    p_med.add_argument("--datahora", default=None)
    p_med.set_defaults(func=cmd_medicacao)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
