# Reforma Tributária e os Documentos Fiscais Eletrônicos

## Guia técnico sobre o impacto da EC 132/2023 e da LC 214/2025 na emissão de notas e documentos fiscais no Brasil

---

## 1. Panorama geral da reforma

A Emenda Constitucional 132/2023, regulamentada principalmente pela Lei Complementar 214/2025, substitui cinco tributos sobre consumo (PIS, Cofins, IPI, ICMS e ISS) por um modelo de **IVA dual**:

| Tributo novo | Esfera | Substitui | Órgão gestor |
|---|---|---|---|
| **CBS** – Contribuição sobre Bens e Serviços | Federal | PIS + Cofins (+ parte do IPI, gradualmente) | Receita Federal |
| **IBS** – Imposto sobre Bens e Serviços | Estadual + Municipal | ICMS + ISS | Comitê Gestor do IBS (CG-IBS) |
| **IS** – Imposto Seletivo | Federal | Parte do IPI (bens nocivos à saúde/meio ambiente) | Receita Federal |

Características centrais que afetam diretamente os documentos fiscais:

- **Não cumulatividade plena** – crédito amplo sobre praticamente todas as aquisições (bens, serviços, ativos), calculado "por fora" e destacado item a item.
- **Tributação no destino** – o imposto pertence ao local de consumo, não mais ao de origem, exigindo identificação precisa do destinatário em cada documento.
- **Cálculo "por fora" e transparência** – o valor do tributo deve aparecer destacado no documento fiscal e, futuramente, no cupom/recibo entregue ao consumidor final ("Imposto Transparente").
- **Split Payment** – mecanismo de recolhimento automático do IBS/CBS no momento da liquidação financeira da operação.
- **Cashback / devolução** – devolução de parte do IBS/CBS a famílias de baixa renda, o que exige vincular CPF ao documento fiscal.

---

## 2. Cronograma de transição (o que muda e quando)

| Ano | O que acontece nos documentos fiscais |
|---|---|
| **2026** | Fase de testes: CBS a 0,9% e IBS a 0,1% (alíquotas simbólicas, sem aumento de carga). Empresas já precisam **destacar CBS e IBS no XML** das notas, mesmo pagando pouco ou nada (compensável com PIS/Cofins). Ambiente Nacional (ADN) entra em operação para o IBS. |
| **2027** | CBS passa a valer "para valer", substituindo PIS/Cofins definitivamente. IPI é reduzido a zero para a maioria dos produtos (exceto os fabricados na Zona Franca de Manaus). Imposto Seletivo (IS) começa a incidir. |
| **2029–2032** | Transição gradual do IBS: ICMS e ISS caem progressivamente (redução de ~1/10 ao ano) enquanto o IBS sobe na mesma proporção. Os documentos fiscais precisam **conviver com tributos antigos e novos simultaneamente**, exigindo dupla apuração. |
| **2033** | Extinção completa de ICMS e ISS. Sistema definitivo: CBS + IBS + IS operando plenamente, com alíquota de referência fixada por resolução do Senado. |

Ou seja: **entre 2026 e 2032 os sistemas emissores de documentos fiscais terão que operar em modo híbrido**, calculando e destacando tributos antigos e novos ao mesmo tempo.

---

## 3. Quais documentos fiscais são afetados

Praticamente todo o parque de documentos fiscais eletrônicos (DF-e) do SPED passa por revisão de leiaute:

- **NF-e (modelo 55)** – notas de venda entre empresas (B2B) e operações com produtos.
- **NFC-e (modelo 65)** – cupom fiscal eletrônico ao consumidor final.
- **NFS-e (Nota Fiscal de Serviços Eletrônica)** – até então municipal e fragmentada em milhares de leiautes diferentes; passa a ter um **padrão nacional obrigatório**, com adesão ao Ambiente de Dados Nacional (ADN) da NFS-e.
- **CT-e (Conhecimento de Transporte Eletrônico)** e **CT-e OS**.
- **MDF-e (Manifesto Eletrônico de Documentos Fiscais)**.
- **NF3-e (Nota Fiscal de Energia Elétrica Eletrônica)**.
- **NFCom** (telecomunicações), já em processo de implantação, também recebe os novos grupos tributários.

A Nota Técnica 2023.001 (e as subsequentes, como a NT 2025.002 do Confaz/Sped) definem oficialmente os novos campos que passam a compor o XML desses documentos.

---

## 4. Novos grupos e campos no leiaute (XML)

O leiaute atual (baseado nos grupos ICMS, PIS, COFINS, IPI) recebe **grupos totalmente novos**, que convivem com os antigos durante a transição:

### 4.1 Grupo `IBSCBS`
Novo bloco de tributação, presente em cada item da nota, contendo, entre outros:

- **`CST` novo** – Código de Situação Tributária específico do IBS/CBS (ex.: 000 tributação integral, 200 alíquota reduzida, 400 imunidade, 500 suspensão, 800/900 outros).
- **`cClassTrib`** – Código de Classificação Tributária, que detalha o *enquadramento* dentro do CST (ex.: cesta básica, saúde, educação, Simples Nacional, Zona Franca de Manaus).
- Base de cálculo, alíquotas de IBS (parte estadual + parte municipal) e de CBS, valores destacados separadamente.
- **Grupo de crédito presumido / diferimento / redução de base**, quando aplicável.
- **`cBenef`** – código de benefício fiscal, obrigatório sempre que houver incentivo, similar ao já usado hoje no ICMS.

### 4.2 Grupo `IS` (Imposto Seletivo)
Aplicável apenas a produtos específicos (cigarros, bebidas alcoólicas, veículos poluentes, bens minerais extraídos, apostas). Traz CST, base de cálculo e alíquota próprias.

### 4.3 Grupo de Split Payment
Campos que identificam o **arranjo de pagamento** usado na operação (cartão, Pix, boleto etc.) e o valor de IBS/CBS que será retido automaticamente pela instituição financeira/liquidante no momento do pagamento.

### 4.4 Totalizadores
Novos totais de nota: `vIBS`, `vCBS`, `vIS`, além dos totais tradicionais (`vICMS`, `vPIS`, `vCOFINS`, `vIPI`), que coexistem durante a fase de transição.

---

## 5. Split Payment: o recolhimento acontece "dentro" da transação

É a mudança mais disruptiva do ponto de vista operacional:

1. O emitente registra a nota fiscal normalmente, com os valores de IBS e CBS destacados.
2. No momento da **liquidação financeira** (pagamento via Pix, cartão, boleto, TED), a instituição de pagamento **separa automaticamente** a parcela referente a IBS/CBS e a repassa diretamente ao Comitê Gestor do IBS e à Receita Federal.
3. O vendedor recebe **líquido** de tributo, semelhante ao que hoje ocorre com retenções de cartão de crédito.
4. Isso exige que o documento fiscal esteja **vinculado eletronicamente à transação de pagamento**, com correlação entre chave de acesso da NF-e/NFS-e e o identificador da transação financeira.
5. Regras de exceção estão previstas para operações sem intermediação financeira eletrônica (ex.: dinheiro em espécie), que seguirão apuração tradicional.

**Implicação prática:** ERPs e adquirentes/PSPs (processadoras de pagamento) precisarão trocar informações em tempo real com o emissor do documento fiscal — um nível de integração que hoje não existe.

---

## 6. NFS-e Nacional: o fim da fragmentação municipal

Hoje existem mais de 5.000 leiautes municipais de nota fiscal de serviço. A reforma cria:

- Um **padrão nacional único** de NFS-e, gerido pelo Comitê Gestor do IBS em conjunto com a RFB e o Comitê Gestor da NFS-e (já em funcionamento desde 2022 via convênio ENCAT/CONFAZ).
- **Ambiente de Dados Nacional (ADN)** centralizando emissão, armazenamento e distribuição de eventos.
- Migração obrigatória dos municípios para o padrão nacional dentro do cronograma da reforma (a adesão já vem ocorrendo progressivamente desde 2023, mas se torna compulsória).
- Fim, na prática, dos sistemas próprios municipais isolados — o prestador de serviço emitirá pelo mesmo ambiente nacional, independentemente da cidade.

---

## 7. Cashback e identificação do consumidor

Para viabilizar a devolução de parte do IBS/CBS a famílias de baixa renda (especialmente sobre energia elétrica, água, gás e botijão de gás — e depois ampliável), o documento fiscal de consumo (NFC-e, NF3-e, contas de consumo) precisará:

- Vincular o **CPF do consumidor** de forma mais consistente do que hoje (atualmente opcional na maioria dos estados).
- Estruturar campos para o **cálculo automático do valor a devolver**, que será processado por sistemas do governo federal a partir dos dados dos próprios documentos fiscais eletrônicos.

---

## 8. Créditos e não cumulatividade plena

Diferente do modelo atual (crédito físico, restrito a determinadas categorias de insumo), o novo modelo adota **crédito financeiro amplo**:

- Em regra, **todo IBS/CBS pago numa aquisição gera crédito**, inclusive sobre bens de uso e consumo e ativo imobilizado (com poucas exceções, como uso/consumo pessoal).
- O crédito só é validado se o **fornecedor efetivamente recolheu o tributo** — o que reforça a importância da qualidade e da tempestividade da informação no documento fiscal eletrônico (rastreabilidade ponta a ponta via ADN).
- Documentos com CST/cClassTrib incorretos podem travar o crédito do destinatário — o que eleva a criticidade da parametrização tributária dentro do ERP.

---

## 9. Impactos práticos para empresas e escritórios

1. **ERP e sistemas emissores** precisarão de atualização profunda: novos grupos tributários, novos códigos (CST/cClassTrib/cBenef), cálculo dual (tributos antigos + novos) durante toda a transição 2026-2032.
2. **Cadastro de produtos e serviços** precisa ser revisado para reclassificação conforme as novas regras (cesta básica nacional, alíquota reduzida em 60% para saúde/educação, imunidades, Simples Nacional híbrido).
3. **Parametrização fiscal** ganha peso decisivo: erro de CST/cClassTrib pode gerar autuação ou bloqueio de crédito do cliente.
4. **Integração financeira** (split payment) exige comunicação entre ERP, meio de pagamento e o documento fiscal emitido — projeto de TI multidisciplinar, não apenas fiscal.
5. **Empresas do Simples Nacional** têm regras próprias (podem optar por apurar IBS/CBS "por fora" ou manter o regime unificado), o que também se reflete em campos específicos no documento.
6. **Obrigatoriedade em fases-piloto já em 2026** — mesmo com alíquota simbólica, a obrigação de emitir com os novos grupos já vale para todos os contribuintes, exigindo teste em ambiente de homologação da SEFAZ/RFB/ADN ao longo de 2025-2026.
7. **Treinamento de equipes fiscais e contábeis** é urgente diante da convivência de dois sistemas tributários por até 7 anos.

---

## 10. Recomendações imediatas

- Mapear, junto ao fornecedor de ERP, o cronograma de atualização dos módulos fiscais para os novos grupos `IBSCBS` e `IS`.
- Iniciar a reclassificação de produtos/serviços conforme o novo sistema de CST/cClassTrib assim que a tabela oficial (Anexo da LC 214/2025 e notas técnicas do Confaz) estiver consolidada.
- Testar a emissão em ambiente de homologação assim que disponibilizado pela SEFAZ do estado e pela RFB (piloto 2026).
- Revisar contratos com adquirentes/PSPs para entender como o split payment será operacionalizado tecnicamente.
- Acompanhar a regulamentação complementar do Comitê Gestor do IBS (resoluções, convênios e manuais técnicos), pois diversos detalhes operacionais ainda serão publicados ao longo de 2026.

---

*Documento elaborado como análise técnica geral sobre a Reforma Tributária (EC 132/2023 e LC 214/2025) e seus impactos na emissão de documentos fiscais eletrônicos no Brasil. Recomenda-se acompanhamento contínuo, pois a regulamentação infralegal (convênios, ajustes SINIEF, notas técnicas) ainda está em evolução.*
