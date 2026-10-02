# 03 - Contagem de estoque e checagem de validade (medicamentos, vacinas, insumos)

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Aviso sobre fontes

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy para gov.br e in.gov.br. Portanto **nenhuma afirmação factual abaixo foi verificada com URL**. Tudo que depende de norma, produto ou estudo está marcado como "não verificado" e deve ser conferido antes de uso. A análise de forma e de desenho é raciocínio de engenharia, não afirmação factual externa.

## 1. Soluções existentes

- Normas candidatas a conferir (não verificado, sem URL): RDC ANVISA 222/2018 (gerenciamento de resíduos de serviços de saúde, base do PGRSS); normas do CFMV sobre estabelecimentos veterinários e sobre registro/controle de medicamentos; regras do MAPA para produtos veterinários (vacinas, biológicos); legislação de controlados (Portaria SVS/MS 344/98, aplicável a psicotrópicos/entorpecentes de uso veterinário). Número exato, artigos e exigências (por exemplo, prazo de guarda de registros, temperatura de vacinas) não verificado.
- PIMS/ERP veterinários brasileiros em geral oferecem controle de estoque com lote e validade e alertas de vencimento (não verificado; checar com demonstração do fornecedor se o seu sistema tem relatório "a vencer em X dias" e entrada por lote).
- Planilhas com formatação condicional e leitura de código de barras são a alternativa comum de baixo custo (não verificado como prática de mercado; é conhecimento geral).
- Estudos sobre perdas por vencimento em clínicas veterinárias: não verificado, não encontrei fonte.

## 2. Forma recomendada: script/planilha (workflow determinístico simples)

Justificativa: o problema central é aritmético e de calendário (data de validade menos hoje, agrupamento por lote), sem ambiguidade de linguagem. LLM adiciona risco de alucinar datas/lotes e não agrega valor no cálculo. O gargalo real é a coleta física (contar prateleira e geladeira, ler lote), que nenhuma IA faz.

Desenho mínimo:
1. Planilha/CSV de estoque com colunas: item, categoria (medicamento, vacina, insumo, controlado), lote, validade, quantidade, local (prateleira/geladeira), origem (nota de entrada).
2. Script que lê o CSV, calcula dias para vencer e gera: lista 0-30, 31-60, 61-90 dias, vencidos; ordena por validade (PEPS/FEFO: o que vence primeiro sai primeiro).
3. Comparação sistema x contagem física: lista divergências de quantidade por item/lote.
4. Modelo de registro de descarte (item, lote, quantidade, data, responsável, destino conforme PGRSS da clínica).
5. Opcional depois: LLM apenas para extrair lote/validade de foto de rótulo ou NF-e, sempre com conferência humana. Não necessário no MVP.

Agente não se justifica. Integração direta com o PIMS só vale se o sistema exportar relatório ou tiver API (não verificado).

## 3. Humano no circuito, riscos

Validação humana obrigatória:
- Contagem física e leitura do lote/validade no frasco (fonte da verdade é o rótulo).
- Aprovação de ajuste de estoque (baixa por divergência) pelo responsável.
- Decisão e execução do descarte, e assinatura do registro. Descarte segue o PGRSS da clínica e a norma vigente (não verificado o texto).
- Controlados: contagem e baixa seguem escrituração própria exigida pela Portaria 344/98 (não verificado); a ferramenta não deve alterar esses registros, só sinalizar.
- Vacinas: cadeia de frio; item vencendo ou com excursão de temperatura é decisão do veterinário responsável.

Riscos:
- Clínico: usar produto vencido por falha de alerta; falso "ok" por data errada no cadastro. Mitigação: alerta conservador, conferência visual.
- Legal: descarte incorreto e registro inadequado (PGRSS/vigilância sanitária); controlados. Não verificado o detalhamento.
- LGPD: baixo; estoque não envolve dados de tutores/pacientes. Não usar lançamentos que citem paciente.
- Alucinação: nula no script determinístico; relevante só se se adicionar LLM/OCR (datas e lotes trocados). Mitigar com campo de confirmação e dupla leitura.

## 4. Pontuação

- Impacto: 3. Reduz perdas e risco de uso de vencidos, mas o ganho de tempo é moderado; o trabalho manual de contagem continua.
- Viabilidade: 5 para planilha/script; 2-3 para automatizar leitura de rótulos.
- Risco: 2 (clínico/legal baixo-moderado, controlado por conferência humana e por não tocar controlados).

## 5. MVP sem dados reais e sem serviços pagos

Cabe. Um script Python com CSV sintético (itens fictícios, lotes inventados, validades relativas a 2026-10-02) que gere as faixas 0-30/31-60/61-90/vencidos, divergências sistema x contagem e um modelo de registro de descarte. Sem integrações, sem API paga. Testável com casos de borda (validade hoje, mesmo item com dois lotes, quantidade zero, data inválida).
