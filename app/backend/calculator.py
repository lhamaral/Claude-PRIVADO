"""Calculadora de bolus e correção de insulina rápida, e de correção da basal.

MÉTODO PRINCIPAL — contagem de carboidratos (escolhido porque é o objetivo
declarado do projeto, e é o método "avançado" indicado pela Sociedade
Brasileira de Diabetes para quem faz múltiplas aplicações diárias em esquema
basal-bolus):
- Bolus de refeição = carboidratos_g / razao_ic
- Correção (glicemia alta) = (glicemia - meta) / fator_sensibilidade,
  aplicada a partir de `correcao_inicio_mgdl`.
- Redução (glicemia baixa) = (correcao_reducao_abaixo - glicemia) / fator_sensibilidade,
  subtraída do bolus de refeição quando a glicemia pré-refeição está abaixo
  de `correcao_reducao_abaixo_mgdl`. Esta parte é uma inferência a partir da
  descrição do usuário e deve ser confirmada com o médico assistente.

  PENDENTE DE CONFIRMAÇÃO: a receita médica usa 120 mg/dL como gatilho para a
  dose FIXA de Fiasp, enquanto o usuário descreveu 180-200 mg/dL como início
  da correção na contagem de carboidratos. Mantido o valor mais conservador
  (180) por padrão em `correcao_inicio_mgdl`, mas confirme com o médico.

MÉTODO ALTERNATIVO DA RECEITA — dose fixa (6 UI café / 4 UI almoço / 4 UI
jantar, se glicemia > 120), indicado pela SBD para quem NÃO faz contagem de
carboidratos (refeições padronizadas). `sugestao_dose_fixa` só existe para
referência/comparação — não deve ser somado à contagem de carboidratos.

CORREÇÃO DA BASAL (Glargina) — regra separada e explícita da receita, aplicada
uma vez ao dia com base na glicemia de JEJUM (antes da própria dose basal):
jejum < 100 → reduzir 2 UI (14 UI); jejum > 160 → aumentar 2 UI (18 UI).
"""

from dataclasses import dataclass


@dataclass
class SugestaoDose:
    bolus_refeicao_ui: float
    correcao_ui: float
    total_ui: float
    detalhes: str


@dataclass
class SugestaoDoseFixa:
    dose_ui: float
    aplicar: bool
    detalhes: str


@dataclass
class SugestaoBasal:
    dose_base_ui: float
    ajuste_ui: float
    dose_final_ui: float
    detalhes: str


def calcular_dose_fixa(refeicao: str, glicemia_atual_mgdl: int, cfg: dict) -> SugestaoDoseFixa:
    """Dose fixa da receita, por referência. `refeicao`: 'cafe' | 'almoco' | 'jantar'."""
    doses = {
        "cafe": cfg["bolus_fixo_cafe_ui"],
        "almoco": cfg["bolus_fixo_almoco_ui"],
        "jantar": cfg["bolus_fixo_jantar_ui"],
    }
    gatilho = cfg["bolus_fixo_gatilho_mgdl"]
    dose = doses[refeicao]
    aplicar = glicemia_atual_mgdl > gatilho
    detalhes = (
        f"Dose fixa ({refeicao}): {dose} UI, aplicável se glicemia > {gatilho} "
        f"(atual: {glicemia_atual_mgdl} → {'aplicar' if aplicar else 'não aplicar'})"
    )
    return SugestaoDoseFixa(dose_ui=dose, aplicar=aplicar, detalhes=detalhes)


def calcular_correcao_basal(glicemia_jejum_mgdl: int, cfg: dict) -> SugestaoBasal:
    base = cfg["basal_dose_ui"]
    ajuste_ui = cfg["basal_correcao_ui"]
    baixo = cfg["basal_correcao_jejum_baixo_mgdl"]
    alto = cfg["basal_correcao_jejum_alto_mgdl"]

    if glicemia_jejum_mgdl < baixo:
        ajuste = -ajuste_ui
        motivo = f"jejum {glicemia_jejum_mgdl} < {baixo} → reduzir {ajuste_ui} UI"
    elif glicemia_jejum_mgdl > alto:
        ajuste = ajuste_ui
        motivo = f"jejum {glicemia_jejum_mgdl} > {alto} → aumentar {ajuste_ui} UI"
    else:
        ajuste = 0.0
        motivo = f"jejum {glicemia_jejum_mgdl} dentro de {baixo}-{alto} → manter dose"

    final = max(0.0, base + ajuste)
    return SugestaoBasal(
        dose_base_ui=base,
        ajuste_ui=ajuste,
        dose_final_ui=final,
        detalhes=f"Basal: {base} UI base | {motivo} | Dose final: {final} UI",
    )


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
