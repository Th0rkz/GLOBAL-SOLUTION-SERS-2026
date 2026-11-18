**Global Solution 2026.2 | SERS | Ciência da Computação — FIAP**

**Integrantes:** _(Thor Correa Neto - 575726, Tales de Souza Jardins - 575080)_
**Integração** Com a disciplina de Pensamento Computacional e Automação em Python (código)
---

## 1. Problema

**Espaço comunitário:** Pontos de ônibus.

Pontos de ônibus costumam depender da rede elétrica para iluminação, painel informativo e carregamento de celular. Esses equipamentos funcionam em horários fixos, mesmo quando não há passageiros, o que gera **desperdício de energia**. Além disso, uma falta de energia deixa o ponto escuro e sem informação, o que afeta a segurança e a confiança no transporte público.

**Público beneficiado:** Passageiros do transporte público, principalmente nos horários de pico e à noite.

**(Alinhamento com ODS:** a meta 11.2 trata do acesso a transporte público seguro e sustentável. Há relação também com a ODS 7 (energia limpa e acessível) e a ODS 13 (ação contra a mudança do clima).)

**Ligação com o código:** o BUS NOW classifica cada ponto em prioridade ALTA, MÉDIA ou BAIXA com base na demanda de passageiros. O programa usa essa prioridade para estimar o uso de equipamentos como carregador USB, ligando a demanda por transporte ao consumo de energia.

## 2. Solução

Comparar três alternativas para a mesma necessidade energética (iluminação + painel informativo + carregador USB) em um período de referência de 30 dias:

| Alternativa | Descrição | Fonte |
|---|---|---|
| **A** | Rede convencional (linha de base) | Rede elétrica |
| **B** | LED com sensor de presença, ligado na rede | Rede elétrica |
| **C** | Painel fotovoltaico + bateria (híbrido, com rede de reserva) | **Renovável** |

### Diagrama de funcionamento

```
 Painel solar ─► Controlador/Bateria ─► Consumidores
 (fonte renovável)                      (LED, painel informativo, USB)
        │                                      │
        │                     Sensores (presença, consumo) e dados do BUS NOW
        ▼                                      ▼
   Rede elétrica  ───────────────►  Python 
   (reserva)                      prioridade + cálculos energéticos
                                               │
                                               ▼
                           CSV (indicadores_energia.csv) ─► Dashboard
```

## 3. Cálculos

Energia de cada equipamento: **E = (P × t) / 1000** (E em kWh, P em W, t em h/dia).

### 3.1 Premissas

| Premissa | Valor | Fontes |
|---|---|---|
| Horas de sol pleno (SP) | 4,5 h/dia | CRESESB |
| Rendimento do sistema solar (PR) | 0,75 | Literatura técnica |
| Tarifa de energia | R$ 0,90/kWh | ANEEL / distribuidora |
| Fator de emissão da rede | 0,06 kg CO₂e/kWh | MCTI |
| Módulo fotovoltaico | 400 Wp | Valor baseado em painéis comuns |
| Autonomia da bateria / DoD / eficiência | 2 dias / 80% / 90% | Valor baseado em painéis comuns |
| Cobertura solar (resto vem da rede) | 95% | Premissa |
| Custo de implantação A / B / C | R$ 3.000 / 4.500 / 12.000 | Orçamentos estimados|
| Manutenção A / B / C | R$ 300 / 200 / 250 por ano | Orçamentos estimados|

### 3.2 Equipamentos

| Equipamento | Potência | Horas/dia |
|---|---|---|
| Luminária convencional (A) | 70 W | 12 |
| Luminária LED com sensor (B e C) | 30 W | 12 × 0,65 = 7,8* |
| Painel informativo | 25 W | 18 |
| Carregador USB | 10 W | 8 (ALTA), 5 (MÉDIA) ou 3 (BAIXA), conforme o BUS NOW |

\* Com sensor, assume-se 50% do tempo com pessoas (100% da potência) e 50% sem (30% da potência): fator = 0,5 + 0,5 × 0,3 = 0,65.

### 3.3 Exemplo: ponto FIAP (prioridade MÉDIA)

- **A:** (70×12 + 25×18 + 10×5)/1000 = 1,34 kWh/dia → **40,2 kWh/mês**
- **B e C:** (30×7,8 + 25×18 + 10×5)/1000 = 0,734 kWh/dia → **22,0 kWh/mês**
- **Dimensionamento solar (C):** 0,734 / (4,5 × 0,75) = 0,22 kWp → **1 painel de 400 Wp**; bateria útil = 0,734 × 2 / (0,8 × 0,9) ≈ **2,0 kWh**

### 3.4 Resultados por ponto (projeções, por ponto de ônibus)

| Ponto (prioridade) | Alt. | Consumo (kWh/mês) | Economia da rede (kWh/mês) | Economia (R$/mês) | Renovável | CO₂e evitado (kg/ano) | Payback* |
|---|---|---|---|---|---|---|---|
| FIAP (MÉDIA) | A | 40,2 | 0 | 0 | 0% | 0 | — |
| | B | 22,0 | 18,2 (45%) | 24,70 | 0% | 13,1 | 5,1 anos |
| | C | 22,0 | 39,1 (97%) | 39,36 | 95% | 28,2 | 19,1 anos |
| Parque (BAIXA) | B | 21,4 | 18,2 (46%) | 24,70 | 0% | 13,1 | 5,1 anos |
| | C | 21,4 | 38,5 (97%) | 38,84 | 95% | 27,7 | 19,3 anos |
| Shopping (BAIXA) | B | 21,4 | 18,2 (46%) | 24,70 | 0% | 13,1 | 5,1 anos |
| | C | 21,4 | 38,5 (97%) | 38,84 | 95% | 27,7 | 19,3 anos |
| Metrô (ALTA) | B | 22,9 | 18,2 (44%) | 24,70 | 0% | 13,1 | 5,1 anos |
| | C | 22,9 | 40,0 (97%) | 40,13 | 95% | 28,8 | 18,7 anos |

\* Payback simples do custo extra de implantação em relação à alternativa A.

### 3.5 Comparação das alternativas

| Critério | A (convencional) | B (LED + sensor) | C (solar + bateria) |
|---|---|---|---|
| Economia de energia | Nenhuma | ~45% | ~97% da rede |
| Custo de implantação | Menor | Médio | Maior |
| Retorno financeiro | — | Mais rápido (~5 anos) | Lento (~19 anos) nas premissas atuais |
| Impacto ambiental | Maior | Reduzido | Menor (95% renovável) |
| Viabilidade técnica | Já existe | Simples | Exige espaço, insolação e manutenção da bateria |
| Benefício à comunidade | — | Menos desperdício | Ponto continua funcionando em queda de energia |

**Leitura dos resultados:** nas premissas adotadas, a alternativa B tem o melhor retorno financeiro, e a C tem o maior ganho ambiental e de resiliência (o ponto segue iluminado em falta de energia). A solução recomendada é **B como primeira etapa e C nos pontos onde a continuidade do serviço e a segurança são mais críticas**.

## 4. Indicadores do dashboard

| Indicador | Unidade |
|---|---|
| Consumo de energia | kWh/mês |
| Economia energética estimada | kWh/mês e % |
| Redução estimada de custos | R$/mês |
| Participação de energia renovável | % |
| Emissões evitadas estimadas | kg CO₂e/ano |
| Pontos de prioridade ALTA (do BUS NOW) | quantidade |

## 5 - Limitações

- Os valores de potência, custo, tarifa, fator de emissão e insolação são **estimativas**; os resultados são **projeções condicionadas às premissas**, não resultados garantidos.
- A prioridade do BUS NOW influencia apenas o carregador USB, que é o equipamento de menor consumo; por isso o consumo varia pouco entre os pontos.
- O fator do sensor de presença (50% do tempo com pessoas) é uma suposição, sem medição real.
- Não considera sombreamento, degradação dos painéis, vida útil da bateria, nem furto ou vandalismo.
- O payback é simples, sem inflação, reajuste de tarifa ou financiamento.
- Não é um projeto executivo de engenharia nem um orçamento comercial.
- A simulação usa apenas os dados cadastrados no programa (quantidade de pessoas e horário informados manualmente).

## 6 - Fontes
1. Surge PV. *Energia solar no estado de São Paulo* (irradiação de 4,5 a 4,8 kWh/m²/dia na capital). https://www.surgepv.com/pt/solar-compliance/brazil/estado/sao-paulo
2. CRESESB/CEPEL. *SunData — cálculo da irradiação solar diária média mensal.* https://cresesb.cepel.br/sundata/index.php
3. Enel Distribuição São Paulo. *Tarifa de Energia Elétrica* (Resolução Homologatória ANEEL nº 3.596/2026, válida a partir de 04/07/2026; B1 residencial: TUSD 472,42 R$/MWh e TE 316,96 R$/MWh). https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html
4. TRT-15. *Plano de Descarbonização — Programa Justiça Carbono Zero 2025* (cita o fator médio anual do SIN em 2023: 0,0385 tCO₂/MWh, dados do MCTI). https://trt15.jus.br/sites/portal/files/roles/institucional/gestao-estrategica/sustentabilidade/Plano%20de%20Descarboniza%C3%A7%C3%A3o%20-%20Programa%20Justi%C3%A7a%20Carbono%20Zero%20-%202025%20(2)_compressed.pdf
   Fatores oficiais mensais: MCTI/SIRENE, https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao
5. Canal Solar. *Emissões de CO₂ da geração elétrica sobem em abril, mostra MCTI* (jan–abr de 2025: 23,7; 24,8; 21,5 e 28,9 kg/MWh). https://canalsolar.com.br/emissoes-de-co₂-geracao-eletrica-mcti/
6. Normas.com.br. *A tecnologia LED usada na iluminação pública* (substituição de vapor de sódio de 70 W por LED). https://www.normas.com.br/visualizar/artigo-tecnico/2235/a-tecnologia-led-usada-na-iluminacao-publica
7. Prefeitura de Cotia. *Caderno de investimentos — Parque de Iluminação Pública + Inteligente* (luminárias LED de 30 W como o tipo mais numeroso). https://cotia.sp.gov.br/wp-content/uploads/2023/09/ed-anexo-16-–-caderno-de-investimentos.pdf
8. Wattuneed. *Bateria de lítio LiFePO₄ 12,8 V 100 Ah 1,28 kWh* (ficha de varejo europeu: DoD de até 90% e cerca de 3.000 ciclos em modelo comparável). https://www.wattuneed.com/es/bateria-litio/6750-bateria-de-litio-lifepo4-128-kwh-powerbrick-pb12100-128-v-100-ah-ip65-0712971137783.html
9. Cenário Energia. *Preço do watt-pico residencial recua 7% em um ano* (R$ 2,45/Wp, jun/2026). https://cenarioenergia.com.br/2026/06/09/preco-do-watt-pico-residencial-recua-7-em-um-ano-e-abre-janela-de-oportunidade-na-mmgd/
10. Calculadora do Mundo. *Valor do kWh por distribuidora 2026* (Enel SP: R$ 0,78938 sem impostos; cerca de R$ 1,02 com impostos a 300 kWh). https://www.calculadoradomundo.com.br/energia/tarifa-energia-por-distribuidora
11. Energia Livre Brasil. *Conta de luz em São Paulo* (Enel SP, B1 e B3 a R$ 0,79/kWh sem impostos). https://energialivrebrasil.com.br/cidade/sao-paulo
12. Prefeitura de Santa Cruz da Conceição/SP. *Estudo Técnico Preliminar — substituição de vapor de sódio por LED* (economia de até 60%). https://santacruzdaconceicao.sp.gov.br/wp-content/uploads/2025/04/ESTUDO-TECNICO-PRELIMINAR-LED-ORLA.pdf
13. DGABC. *Aneel aprova alta média de 10,18% para tarifas dos consumidores da Enel São Paulo* (reajuste de julho de 2026). https://www.dgabc.com.br/Noticia/4332348/aneel-aprova-alta-media-de-10-18-para-tarifas-dos-consumidores-da-enel-sao-paulo
14. ONU. *Objetivo de Desenvolvimento Sustentável 11* e *ODS 7* (metas 11.2 e 7.2).
