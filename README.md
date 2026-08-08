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
| **Regra de ouro** | Uma decisão por bloco. Uma pergunta por episódio. Uma conta. Uma ação. |

## O princípio de organização

**A série não é um curso sobre a reforma. É um programa de decisões.**

Conteúdo organizado por tema ensina. Conteúdo organizado por decisão faz agir — e só
quem age percebe que precisa de ajuda técnica.

Cada bloco de cinco episódios nasce de **uma decisão concreta que o empresário tem de
tomar**, ordenada por prioridade real: prazo legal em curso primeiro, depois
pré-requisito, depois prazo de virada, depois maturação longa.

Dentro do bloco, os episódios seguem sempre a mesma progressão:

| Ep | Papel | O que entrega |
|---|---|---|
| 1 | **A DECISÃO** | O que está em jogo, qual o prazo, quem decide |
| 2 | **O QUE SABER** | A regra que governa a decisão |
| 3 | **O QUE SABER** | A exceção ou armadilha que muda a leitura |
| 4 | **O SEU NÚMERO** | O dado da própria casa que tira a decisão do genérico |
| 5 | **A ATITUDE** | O que fazer, com quem, até quando |

O bloco só está completo quando o espectador **sabe o que decidir, tem o número para
decidir, e sabe qual é o próximo movimento.**

## As seis decisões do primeiro ciclo

| Bloco | A decisão | Prazo |
|---|---|---|
| [1](roteiros/bloco-01.md) | Optar ou não pelo regime regular de IBS/CBS | **Setembro/2026** |
| [2](roteiros/bloco-02.md) | Arrumar o cadastro fiscal da operação | Antes de 01/2027 |
| [3](roteiros/bloco-03.md) | O que substitui o regime especial de ICMS | **31/12/2026** |
| [4](roteiros/bloco-04.md) | O que fazer com a carteira de clientes PJ | Antes que o cliente decida |
| [5](roteiros/bloco-05.md) | Preço e composição de cardápio para 2027 | Janeiro/2027 |
| [6](roteiros/bloco-06.md) | Como preparar o caixa para o split payment | 2027 |

O bloco 2 vem antes do 3 e do 4 de propósito: enquanto o cadastro estiver errado, todos
os números levantados nos outros blocos estarão errados também.

---

## Como usar este repositório

### Para gravar amanhã

1. Abra o roteiro do bloco em [`roteiros/`](roteiros/).
2. Leia o bloco **FALADO** — já está no tempo certo (150 a 175 palavras).
3. Grave. Use os **TEXTOS NA TELA** como legenda queimada.
4. Publique com a **LEGENDA** que acompanha o roteiro.
5. Marque o episódio no [calendário](editorial/calendario-90-episodios.md).

### Para produzir novos episódios

- O padrão está em [`templates/roteiro-modelo.md`](templates/roteiro-modelo.md).
- A skill em [`.claude/skills/roteiro-reforma-balcao/`](.claude/skills/roteiro-reforma-balcao/SKILL.md)
  gera episódios no formato: peça `/roteiro-reforma-balcao E31`, ou descreva a decisão e
  ela monta o bloco inteiro.
- O estoque de perguntas está em [`editorial/banco-de-perguntas.md`](editorial/banco-de-perguntas.md).

---

## Mapa dos arquivos

```
docs/
  01-estrategia-editorial.md    Arquitetura por decisão, prioridade, funil
  02-persona-e-linguagem.md     Quem é o Seu Marcelo. O que falar e o que nunca falar
  03-anatomia-do-roteiro.md     A estrutura de 60 segundos e os papéis dentro do bloco
  04-compliance-oab.md          Provimento 205/2021 — checklist antes de publicar
  05-producao-e-distribuicao.md Gravação, edição, plataformas, reaproveitamento
  06-base-tecnica-setorial.md   O direito por trás da série + o que validar antes de falar

editorial/
  calendario-90-episodios.md    18 decisões mapeadas, 6 totalmente roteirizadas
  banco-de-perguntas.md         Perguntas reais do setor, agrupadas por tema

roteiros/
  bloco-01.md ... bloco-06.md   30 roteiros prontos para gravar

templates/
  roteiro-modelo.md             O gabarito
  legenda-modelo.md             Legenda, hashtags e CTA
```

---

## Estado do conteúdo (agosto de 2026)

A série nasce num momento raro: **estamos dentro do ano-teste**. As alíquotas de CBS
(0,9%) e IBS (0,1%) já aparecem nos documentos fiscais, a regulamentação saiu em abril
(Decreto nº 12.955/2026 e Resolução CGIBS nº 6/2026), e há **uma decisão com prazo em
setembro de 2026** — a opção do Simples Nacional pelo regime regular de IBS/CBS.

É por isso que o bloco 1 é o que é: existe uma escolha vencendo agora, e o público-alvo
majoritariamente não sabe disso.

> ⚠️ **Leia antes de gravar:** [`docs/06-base-tecnica-setorial.md`](docs/06-base-tecnica-setorial.md)
> marca com `[VALIDAR]` cada ponto que depende de conferência no texto legal ou que
> ainda está em disputa. Os roteiros repetem essas marcas. Nenhum episódio marcado como
> bloqueante vai ao ar sem a conferência — a assinatura é sua.
