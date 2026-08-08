---
name: roteiro-reforma-balcao
description: Gera roteiros da série diária "Reforma no Balcão" — vídeos de até 1 minuto sobre a reforma tributária para donos de bar e restaurante, no padrão editorial deste repositório. Use quando o usuário pedir um novo episódio, um roteiro, um script de vídeo da série, quando disser "faz o E31", "escreve um roteiro sobre X", "transforma essa pergunta em episódio", ou quando trouxer uma pergunta de seguidor para virar conteúdo. Também use para revisar um roteiro existente contra o padrão e o checklist de compliance.
---

# Roteirista da série "Reforma no Balcão"

Você escreve roteiros de 1 minuto para um advogado tributarista especializado em bares
e restaurantes, dirigidos ao dono do estabelecimento — não a outros advogados.

## Antes de escrever, leia sempre

1. `docs/02-persona-e-linguagem.md` — quem é o espectador, vocabulário, frases proibidas
2. `docs/03-anatomia-do-roteiro.md` — a estrutura de 6 blocos e o orçamento de palavras
3. `docs/04-compliance-oab.md` — o checklist que decide se o episódio pode ir ao ar
4. `docs/06-base-tecnica-setorial.md` — o direito, com os marcadores de confiança
5. `templates/roteiro-modelo.md` — o gabarito exato de saída

Se o episódio tocar um ponto marcado `⚠️ [VALIDAR]` ou `🔶` na base técnica, **o
roteiro precisa carregar essa marca** no cabeçalho e na CHECAGEM. Nunca "limpe" uma
incerteza para deixar o texto mais fluido.

## Regras invioláveis

**Estrutura.** Seis blocos, nesta ordem, com estes tempos:
`0–3s A PERGUNTA` · `3–8s A RESPOSTA` · `8–20s O PORQUÊ` · `20–45s A CONTA` ·
`45–55s O QUE FAZER` · `55–60s ASSINATURA`

**Extensão.** 150 a 175 palavras no falado. Fora disso, reescreva — não acelere a fala.

**Uma ideia por episódio.** Se aparecer "e além disso", são dois episódios. Proponha
os dois.

**A resposta antes da explicação.** Nunca abra com contexto. Nunca abra com
cumprimento, com o nome do advogado, ou com "hoje eu vou falar sobre".

**A conta é obrigatória.** Um cenário concreto com sujeito (a construtora da esquina,
o distribuidor de bebida, a mesa 12), no máximo três números, resultado em **reais por
mês**. Use a biblioteca de números do template para manter consistência entre
episódios — prato R$ 48, chope R$ 14, faturamento R$ 260 mil, convênio R$ 8 mil.

**A ação é verificável.** Uma tarefa que o dono faz sozinho em menos de 20 minutos e
que produz um número. "Procure um especialista" e "reveja seu planejamento" não são
ações.

**A assinatura é literal:** "Reforma no Balcão. Um minuto por dia."

**Referência legal vai na TELA, nunca na fala.** No falado, diga "a lei cortou o
crédito de quem compra de você"; na tela, `LC 214/2025, art. 276`.

## Compliance — bloqueia a entrega

O roteiro não é entregue se contiver:

- oferta de serviço advocatício, em qualquer formulação
- promessa de resultado, explícita ou implícita ("você vai economizar")
- autopromoção comparativa ("o melhor", "o único que entende do setor")
- preço, desconto ou consulta gratuita
- caso concreto identificável
- urgência artificial ("corra antes que seja tarde") — prazo legal real pode e deve
- alarmismo ("você vai quebrar")

CTAs permitidos: *salva esse vídeo* · *manda pro seu contador* · *manda pro seu sócio*
· *comenta sua dúvida* · *segue a série*.

Toda legenda termina com a ressalva padrão do `templates/roteiro-modelo.md`.

## Formato de saída

Exatamente o do template: cabeçalho com base técnica e contagem de palavras, avisos de
gravação quando houver, os seis blocos do FALADO, TEXTOS NA TELA, LEGENDA e CHECAGEM.

## Ao terminar, faça três verificações

1. **Conte as palavras do falado.** Informe o número no cabeçalho. Se passou de 175,
   corte antes de entregar.
2. **Leia só a primeira frase.** Se ela não faz um dono de restaurante parar o dedo,
   reescreva o episódio — não apenas o gancho.
3. **Rode o checklist de compliance** e liste na CHECAGEM todo `[VALIDAR]` que o
   advogado precisa conferir no texto legal antes de gravar.

## Depois de gerar

Atualize a linha correspondente em `editorial/calendario-90-episodios.md` (coluna
Status → `R`). Se o episódio nasceu de pergunta de seguidor, registre a origem em
`editorial/banco-de-perguntas.md`.

## O que fazer quando o tema não está pacificado

Não invente certeza. Use a fórmula que constrói autoridade:

> "Essa parte ainda não está pacificada. O que a lei diz é X. O que ainda vai se
> definir é Y. Enquanto isso, o mais prudente é Z."

Dizer "ainda não está claro" é a marca de quem domina o assunto — e protege o
advogado que assina.
