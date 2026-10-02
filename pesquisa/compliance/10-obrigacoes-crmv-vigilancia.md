# Compliance: obrigações do estabelecimento perante CRMV e vigilância

Data: 2026-10-02

## Aviso de verificação
Nesta execução o WebFetch ao site do CFMV foi bloqueado (egress) e o orçamento de WebSearch estava esgotado. Portanto **nenhuma afirmação factual externa foi verificada**. Tudo abaixo sobre normas, prazos, taxas e produtos está marcado "não verificado". Única referência dada (não lida): https://www.cfmv.gov.br/wp-content/uploads/2022/05/Resolucao1275_ComentadaFinal.pdf (Res. CFMV 1.275/2019 comentada; atualizações posteriores: não verificado).

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com controle de vencimento de licenças: não verificado.
- Estudos ou artigos sobre automação desse tema: não verificado.
- Alternativa genérica conhecida: agenda/planilha de vencimentos com lembretes (Google Calendar, Excel); não é produto específico, sem fonte.
- Os requisitos (certificado de regularidade, RT, alvará sanitário, validade e periodicidade) variam por CRMV regional e por município/estado; conferir no regional e na vigilância local. Não verificado.

## 2. Forma recomendada: script/planilha (workflow determinístico simples)
Registro de obrigações (documento, órgão, número, emissão, validade, responsável, custo, link do arquivo) com alertas em 90/60/30/15 dias antes do vencimento, mais checklist de fiscalização. Sem IA generativa no caminho crítico.
Justificativa: o problema é de calendário e guarda de documentos, não de interpretação. Um LLM só agregaria valor opcional em tarefas laterais (rascunhar ofício de resposta a notificação, a partir de modelo), sempre revisado. Agente autônomo não se justifica: risco de alucinar norma/prazo e baixo ganho.
Forma: **script/planilha**.

## 3. Human-in-the-loop e riscos
- O RT/sócio valida: cada data cadastrada contra o documento original, qualquer resposta a fiscalização antes do envio, pagamentos e protocolos.
- Legal/CFMV: assinatura e responsabilidade são do RT; a ferramenta não deve emitir nem protocolar nada por conta própria. Exigências normativas devem ser confirmadas na norma vigente (não verificado).
- LGPD: documentos da empresa têm dados de sócios/RT (CPF, endereço); armazenar com acesso restrito. Nenhum dado de paciente/tutor é necessário.
- Receituário controlado: fora do escopo desta tarefa (há obrigações próprias de vigilância/MAPA/ANVISA; não verificado).
- Alucinação: se usar LLM, proibir citar norma/prazo sem fonte colada pelo usuário; prazos vêm só do documento cadastrado.
- Risco clínico: praticamente nulo; risco real é lapso de licença (multa/interdição, não verificado).

## 4. Pontuação
- Impacto: 3 (evita lapsos e tempo de caça a documentos; frequência baixa)
- Viabilidade: 5
- Risco: 2 (legal indireto, por data errada ou falsa sensação de conformidade)

## 5. MVP sem dados reais e sem pago
Sim. Planilha/CSV com dados fictícios + script (Python) que lista vencimentos próximos e gera um .ics de lembretes e um checklist de fiscalização. Testável com datas sintéticas.
