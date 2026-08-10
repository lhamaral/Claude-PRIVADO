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

Baseada na receita de Dr. Severino de Almeida (CREMEB 6175, RQE 4003 —
Cliendi Prev Endocrinologia), 06/08/2026.

- **Basal**: Glargina (Glargilin), 16 UI, 1x/dia antes do café da manhã.
  Meta de jejum: 100–160 mg/dL.
- **Correção da basal** (regra separada, 1x/dia, pela glicemia de JEJUM):
  jejum < 100 → reduzir 2 UI (14 UI) · jejum > 160 → aumentar 2 UI (18 UI).
- **Bolus (Fiasp)** — dois métodos estão na receita:
  - *Contagem de carboidratos* (método usado como principal neste app,
    por ser o objetivo do projeto e o método recomendado pela SBD para
    quem faz múltiplas aplicações diárias): razão 1 UI : 20 g de carboidrato.
  - *Dose fixa* (alternativa da receita para refeições padronizadas, só
    exibida como referência/comparação — **não some as duas**): 6 UI no
    café, 4 UI no almoço, 4 UI no jantar, se glicemia > 120 mg/dL.
- **Fator de sensibilidade**: 1 UI reduz ~50 mg/dL. Exemplo da receita:
  glicemia 250 → 3 UI ((250−100)÷50), consistente com meta 100.
- Faixa alvo geral (uso diário, TIR): 70–180 mg/dL (conforme você descreveu).

### ⚠️ Pendente de confirmação com o médico

- **Gatilho de correção do bolus por contagem de carboidratos**: a receita
  usa 120 mg/dL para a dose fixa; você descreveu 180–200 mg/dL para a
  contagem de carboidratos. O app usa 180 mg/dL por padrão
  (`correcao_inicio_mgdl`) — confirme qual valor vale para o seu caso.
- **Redução do bolus quando a glicemia pré-refeição está baixa** (abaixo de
  100 mg/dL): a receita não detalha essa regra para o Fiasp (só para a
  basal). O app aplica `(100 − glicemia) ÷ 50` como redução do bolus, mas
  isso é uma inferência, não algo escrito na receita — confirme com o médico.

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
python backend/cli.py basal --glicemia_jejum_mgdl 168
python backend/cli.py dosefixa --refeicao almoco --glicemia_atual_mgdl 135
python backend/cli.py medicacao --nome "Creon 25.000"
```

## Exportação de dados

Na aba "Histórico", ou diretamente pelas rotas:
- `/api/export/refeicoes.csv`
- `/api/export/glicemias.csv`
- `/api/export/doses.csv`
- `/api/export/medicacoes.csv`

## Medicações contínuas

A receita também lista medicações não relacionadas à glicemia, com um
checklist diário na aba "Registrar": Creon 25.000 (a cada refeição),
Rosuvastatina 20mg + Ezetimibe 10mg (após o jantar), Andractive Peyronie
(1x/dia). A lista está em `backend/config.py` (`MEDICACOES_CONTINUAS`).

## Relatórios disponíveis

- **Tempo no alvo (TIR)**: % de leituras abaixo, dentro e acima da faixa alvo.
- **Curva glicêmica diária**: leituras do dia plotadas em ordem cronológica.
- **Padrão diário**: média/mín/máx de glicemia por horário do dia, últimos 14 dias.
- **Resumo diário**: carboidratos totais, insulina total por tipo, estatísticas de glicemia.
