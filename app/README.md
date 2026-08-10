# Controle de Glicemia e Contagem de Carboidratos

Ferramenta pessoal para registrar refeições, glicemia (medidor Livre) e doses de
insulina, calcular sugestões de bolus/correção com base na sua prescrição, e
gerar relatórios (tempo no alvo, curva glicêmica, padrão diário) com
exportação dos dados.

## ⚠️ Aviso importante

Este projeto **não é um dispositivo médico e não substitui acompanhamento
médico**. Os cálculos aqui implementados apenas automatizam, com base nos
parâmetros que você configurou, a regra que **seu médico já prescreveu**.
Nenhum parâmetro clínico (razão I:C, fator de sensibilidade, metas, dose
basal) foi definido ou validado por um profissional de saúde através desta
ferramenta — eles devem ser sempre conferidos e ajustados com seu
endocrinologista. Em caso de hipoglicemia, hiperglicemia grave, cetose ou
qualquer emergência, siga a orientação médica e procure atendimento, não
esta ferramenta.

## Prescrição usada como referência (configurável em `backend/config.py` ou na tela "Configurações")

- Basal: Glargina, 16 UI, 1x/dia pela manhã
- Bolus: Fiasp, razão 1 UI : 20 g de carboidrato
- Fator de sensibilidade: 1 UI reduz ~50 mg/dL
- Meta de glicemia: 100 mg/dL (faixa alvo 70–180 mg/dL)
- Correção: a partir de 180 mg/dL, aplicar (glicemia − 100) ÷ 50 UI adicionais
- Abaixo de 100 mg/dL: reduzir a dose de bolus proporcionalmente
  (regra inferida — **confirme com seu médico** o critério exato de redução)

## Como rodar

```bash
cd app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```

Acesse http://localhost:5000

O banco de dados SQLite é criado automaticamente em `app/data/glicemia.db`
na primeira execução.

## Estrutura

```
app/
  backend/
    app.py         # servidor Flask (rotas de API e páginas)
    models.py       # schema do banco (SQLite) e acesso a dados
    calculator.py    # regras de cálculo de bolus/correção
    reports.py       # tempo no alvo, curva glicêmica, padrão diário, resumo
    config.py        # parâmetros padrão da prescrição
    cli.py           # registro de dados via linha de comando (sem servidor)
  frontend/
    templates/index.html
    static/app.js, style.css
  data/               # banco SQLite (não versionado)
```

## Registrando dados por texto, áudio ou foto

Você pode preencher os formulários na aba "Registrar" do app, **ou**
simplesmente descrever a refeição (por texto, áudio ou foto) nesta
conversa com o Claude — ele estima os carboidratos, calcula a sugestão de
dose e registra tudo automaticamente usando `backend/cli.py`, sem você
precisar abrir o navegador. A data/hora é usada automaticamente no
momento do registro, a menos que você informe um horário diferente
(registro retroativo).

Exemplos de uso direto do CLI:

```bash
python backend/cli.py refeicao --descricao "arroz, feijão, frango grelhado" --carboidratos_g 55 --origem foto
python backend/cli.py glicemia --valor_mgdl 142 --contexto pre_refeicao
python backend/cli.py calcular --carboidratos_g 55 --glicemia_atual_mgdl 142
python backend/cli.py dose --tipo bolus_refeicao --insulina Fiasp --unidades 2.8
```

## Exportação de dados

Na aba "Histórico", ou diretamente pelas rotas:
- `/api/export/refeicoes.csv`
- `/api/export/glicemias.csv`
- `/api/export/doses.csv`

## Relatórios disponíveis

- **Tempo no alvo (TIR)**: % de leituras abaixo, dentro e acima da faixa alvo.
- **Curva glicêmica diária**: leituras do dia plotadas em ordem cronológica.
- **Padrão diário**: média/mín/máx de glicemia por horário do dia, últimos 14 dias.
- **Resumo diário**: carboidratos totais, insulina total por tipo, estatísticas de glicemia.
