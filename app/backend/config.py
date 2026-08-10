"""Parâmetros clínicos usados nos cálculos de dose.

Estes valores devem refletir exatamente a prescrição do seu médico.
Sempre que a prescrição mudar, atualize aqui (ou via tela de configurações).
"""

PRESCRICAO_PADRAO = {
    # --- Basal (Glargina/Glargilin) ---
    "basal_insulina": "Glargina",
    "basal_dose_ui": 16,
    "basal_horario": "manhã",
    "meta_jejum_min_mgdl": 100,
    "meta_jejum_max_mgdl": 160,
    # correção da BASAL por glicemia de jejum (regra da receita, aplicada 1x/dia):
    # jejum < basal_correcao_jejum_baixo_mgdl  -> reduzir basal_correcao_ui
    # jejum > basal_correcao_jejum_alto_mgdl   -> aumentar basal_correcao_ui
    "basal_correcao_ui": 2,
    "basal_correcao_jejum_baixo_mgdl": 100,
    "basal_correcao_jejum_alto_mgdl": 160,

    # --- Bolus de refeição (Fiasp) ---
    "bolus_insulina": "Fiasp",
    # Método principal: contagem de carboidratos (escolhido pelo usuário/objetivo do projeto)
    "razao_ic_g_por_ui": 20,       # 1 UI cobre 20g de carboidrato
    "fator_sensibilidade_mgdl_por_ui": 50,  # 1 UI reduz ~50 mg/dL
    "meta_glicemia_mgdl": 100,
    "faixa_alvo_min_mgdl": 70,
    "faixa_alvo_max_mgdl": 180,
    "correcao_inicio_mgdl": 180,   # PENDENTE: receita usa 120 para a dose fixa; confirmar com o médico
    "correcao_reducao_abaixo_mgdl": 100,  # abaixo disso, reduzir dose de bolus

    # Método alternativo da receita (dose fixa, só para referência/comparação — não somar aos dois):
    "bolus_fixo_cafe_ui": 6,
    "bolus_fixo_almoco_ui": 4,
    "bolus_fixo_jantar_ui": 4,
    "bolus_fixo_gatilho_mgdl": 120,
}

# Medicações de uso contínuo (não entram no cálculo de insulina, só no checklist diário)
MEDICACOES_CONTINUAS = [
    {"nome": "Creon 25.000", "posologia": "1 cápsula via oral a cada refeição"},
    {"nome": "Rosuvastatina 20mg", "posologia": "1 comprimido via oral após o jantar"},
    {"nome": "Ezetimibe 10mg", "posologia": "1 comprimido via oral após o jantar"},
    {"nome": "Andractive Peyronie", "posologia": "1 cápsula via oral ao dia"},
]
