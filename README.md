# Reforma no Balcão

**Série diária de 1 minuto sobre a reforma tributária, para donos de bar e restaurante.**

Este repositório é a *fábrica* da série: estratégia, persona, base técnica, calendário
editorial, roteiros prontos para gravar e o padrão para produzir os próximos.

---

## O que é a série

| Item | Definição |
|---|---|
| **Nome** | Reforma no Balcão |
| **Assinatura** | "Reforma no Balcão. Um minuto por dia." |
| **Formato** | Vídeo vertical 9:16, 45 a 60 segundos |
| **Cadência** | 1 episódio por dia útil (seg a sex) |
| **Voz** | Advogado tributarista, especialista no setor, falando como quem senta na mesa do dono |
| **Regra de ouro** | Uma pergunta real por episódio. Uma resposta. Uma conta. Uma ação. |

Alternativas de nome, caso queira testar: *Comanda da Reforma*, *Tributo à Mesa*,
*Reforma na Praça*. A escolha está justificada em [`docs/01-estrategia-editorial.md`](docs/01-estrategia-editorial.md).

---

## Como usar este repositório

### Para gravar amanhã

1. Abra o roteiro da semana em [`roteiros/`](roteiros/).
2. Leia o bloco **FALADO** — ele já está no tempo certo (150 a 170 palavras).
3. Grave. Use os **TEXTOS NA TELA** como legenda queimada.
4. Publique com a **LEGENDA** que acompanha o roteiro.
5. Marque o episódio como publicado no [calendário](editorial/calendario-90-episodios.md).

### Para produzir novos episódios

- O padrão está em [`templates/roteiro-modelo.md`](templates/roteiro-modelo.md).
- Há uma skill do Claude Code em [`.claude/skills/roteiro-reforma-balcao/`](.claude/skills/roteiro-reforma-balcao/SKILL.md):
  peça `/roteiro-reforma-balcao E31` e ela gera o próximo episódio já no formato,
  com a checagem de conformidade da OAB embutida.
- O estoque de perguntas cruas está em [`editorial/banco-de-perguntas.md`](editorial/banco-de-perguntas.md).

---

## Mapa dos arquivos

```
docs/
  01-estrategia-editorial.md    Posicionamento, promessa, arco da série, funil
  02-persona-e-linguagem.md     Quem é o Seu Marcelo. O que falar e o que nunca falar
  03-anatomia-do-roteiro.md     A estrutura de 60 segundos, bloco a bloco
  04-compliance-oab.md          Provimento 205/2021 — checklist antes de publicar
  05-producao-e-distribuicao.md Gravação, edição, plataformas, reaproveitamento
  06-base-tecnica-setorial.md   O direito por trás da série + o que validar antes de falar

editorial/
  calendario-90-episodios.md    18 semanas mapeadas, 6 primeiras totalmente roteirizadas
  banco-de-perguntas.md         Perguntas reais do setor, agrupadas por tema

roteiros/
  semana-01.md ... semana-06.md 30 roteiros prontos para gravar

templates/
  roteiro-modelo.md             O gabarito
  legenda-modelo.md             Legenda, hashtags e CTA
```

---

## Estado do conteúdo (agosto de 2026)

A série nasce num momento raro: **estamos dentro do ano-teste**. As alíquotas de
CBS (0,9%) e IBS (0,1%) já aparecem nos documentos fiscais, a regulamentação saiu em
abril (Decreto nº 12.955/2026 e Resolução CGIBS nº 6/2026), e há **decisões com prazo
em setembro de 2026** — a opção do Simples Nacional pelo regime regular de IBS/CBS.

Ou seja: o público-alvo tem uma decisão concreta a tomar nas próximas semanas.
A Semana 1 da série foi escrita em cima disso.

> ⚠️ **Leia antes de gravar:** [`docs/06-base-tecnica-setorial.md`](docs/06-base-tecnica-setorial.md)
> marca com `[VALIDAR]` cada ponto que depende de conferência no texto legal ou que
> ainda está em disputa. Os roteiros repetem essas marcas. Nenhum episódio vai ao ar
> sem a conferência — a assinatura é sua.
