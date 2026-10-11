# Reforma no Balcão — guia para sessões do Claude Code

Este repositório **não é um projeto de código**: não há `package.json`, dependências,
build, testes ou linter. É a fábrica de conteúdo da série diária "Reforma no Balcão"
(vídeos verticais de 45–60s sobre a reforma tributária, para donos de bar e restaurante).
Não é necessário instalar nada para trabalhar aqui — sessões remotas (web/app) sobem
prontas para uso.

## Antes de gerar ou revisar um roteiro

Use a skill `.claude/skills/roteiro-reforma-balcao/SKILL.md` (`/roteiro-reforma-balcao`).
Ela já indica a ordem de leitura obrigatória em `docs/`. Não escreva um roteiro sem
seguir esse fluxo — o padrão editorial e o compliance da OAB (Provimento 205/2021,
`docs/04-compliance-oab.md`) dependem disso.

## Mapa rápido

- `docs/` — estratégia editorial, persona, anatomia do roteiro, compliance, produção, base técnica (com marcadores `[VALIDAR]`)
- `editorial/` — calendário dos 90 episódios e banco de perguntas de seguidores
- `roteiros/bloco-NN.md` — roteiros prontos, 5 episódios por bloco
- `templates/` — gabarito de roteiro e de legenda
- `producao/` — checklists de gravação e assets visuais

## Regra que nunca se quebra

Um ponto marcado `⚠️ [VALIDAR]` ou `🔶` na base técnica (`docs/06-base-tecnica-setorial.md`)
tem que carregar essa marca no roteiro também. Nunca "limpar" uma incerteza jurídica para
deixar o texto mais fluido.
