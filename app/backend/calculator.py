"""Calculadora de bolus e correção de insulina rápida.

Implementa exatamente as regras informadas pelo usuário/prescrição médica:
- Bolus de refeição = carboidratos_g / razao_ic
- Correção (glicemia alta) = (glicemia - meta) / fator_sensibilidade,
  aplicada a partir de `correcao_inicio_mgdl`.
- Redução (glicemia baixa) = (correcao_reducao_abaixo - glicemia) / fator_sensibilidade,
  subtraída do bolus de refeição quando a glicemia pré-refeição está abaixo
  de `correcao_reducao_abaixo_mgdl`. Esta parte é uma inferência a partir da
  descrição do usuário e deve ser confirmada com o médico assistente.
"""

from dataclasses import dataclass


@dataclass
class SugestaoDose:
    bolus_refeicao_ui: float
    correcao_ui: float
    total_ui: float
    detalhes: str


def calcular_dose(
    carboidratos_g: float,
    glicemia_atual_mgdl: int,
    cfg: dict,
) -> SugestaoDose:
    razao_ic = cfg["razao_ic_g_por_ui"]
    meta = cfg["meta_glicemia_mgdl"]
    sensibilidade = cfg["fator_sensibilidade_mgdl_por_ui"]
    inicio_correcao = cfg["correcao_inicio_mgdl"]
    limite_reducao = cfg["correcao_reducao_abaixo_mgdl"]

    bolus = round(carboidratos_g / razao_ic, 1) if carboidratos_g else 0.0
    correcao = 0.0
    detalhes = [f"Bolus refeição: {carboidratos_g}g ÷ {razao_ic} = {bolus} UI"]

    if glicemia_atual_mgdl >= inicio_correcao:
        correcao = round((glicemia_atual_mgdl - meta) / sensibilidade, 1)
        detalhes.append(
            f"Correção (glicemia {glicemia_atual_mgdl} ≥ {inicio_correcao}): "
            f"({glicemia_atual_mgdl} - {meta}) ÷ {sensibilidade} = +{correcao} UI"
        )
    elif glicemia_atual_mgdl < limite_reducao:
        reducao = round((limite_reducao - glicemia_atual_mgdl) / sensibilidade, 1)
        correcao = -reducao
        detalhes.append(
            f"Redução (glicemia {glicemia_atual_mgdl} < {limite_reducao}): "
            f"-{reducao} UI do bolus [confirme esta regra com seu médico]"
        )

    total = max(0.0, round(bolus + correcao, 1))
    detalhes.append(f"Total sugerido: {total} UI")

    return SugestaoDose(
        bolus_refeicao_ui=bolus,
        correcao_ui=correcao,
        total_ui=total,
        detalhes=" | ".join(detalhes),
    )
