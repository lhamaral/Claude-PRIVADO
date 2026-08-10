"""Parâmetros clínicos usados nos cálculos de dose.

Estes valores devem refletir exatamente a prescrição do seu médico.
Sempre que a prescrição mudar, atualize aqui (ou via tela de configurações).
"""

PRESCRICAO_PADRAO = {
    "basal_insulina": "Glargina",
    "basal_dose_ui": 16,
    "basal_horario": "manhã",
    "bolus_insulina": "Fiasp",
    "razao_ic_g_por_ui": 20,       # 1 UI cobre 20g de carboidrato
    "fator_sensibilidade_mgdl_por_ui": 50,  # 1 UI reduz ~50 mg/dL
    "meta_glicemia_mgdl": 100,
    "faixa_alvo_min_mgdl": 70,
    "faixa_alvo_max_mgdl": 180,
    "correcao_inicio_mgdl": 180,   # a partir daqui passa a corrigir
    "correcao_reducao_abaixo_mgdl": 100,  # abaixo disso, reduzir dose de bolus
}
