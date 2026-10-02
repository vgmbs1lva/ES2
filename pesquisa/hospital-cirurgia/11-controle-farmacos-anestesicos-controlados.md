# Controle de fármacos anestésicos e controlados (estoque, registro de uso, descarte)

Domínio: hospital-cirurgia | Data: 2026-10-02

## Aviso de verificação (leia primeiro)

Nesta execução a ferramenta de busca atingiu o limite de 200 consultas e o acesso a www.gov.br foi bloqueado pelo proxy de saída. Portanto **nenhuma afirmação factual abaixo tem fonte verificada**. Tudo que depende de norma, produto ou estudo está marcado como "não verificado". Antes de implementar, confirmar na ANVISA, no CFMV e no CRMV local:

- Portaria SVS/MS 344/98 e atualizações (listas, escrituração, balanços, guarda de receitas, descarte): não verificado.
- Como a escrituração de controlados se aplica a clínica/hospital veterinário (livro físico, sistema informatizado, SNGPC ou outro): não verificado.
- Regras de descarte/inutilização de controlados e resíduos de serviços de saúde (RDC ANVISA de RSS, CONAMA): não verificado.
- Resoluções do CFMV sobre receituário e prontuário: não verificado.
- Soluções existentes (módulos de PIMS, armários dispensadores, estudos sobre desvio de opioides em clínicas veterinárias): não verificado; sem URLs porque não pude pesquisar.

## 1. Soluções existentes

Não verificado. Hipótese a checar: vários PIMS veterinários têm módulo de estoque e algumas rotinas de controlados, e existem armários dispensadores eletrônicos na medicina humana. Não afirmo que existam, nem seus preços, para o mercado brasileiro. Primeiro passo: perguntar ao fornecedor do PIMS em uso se há baixa de controlados vinculada à ficha anestésica.

## 2. Forma recomendada: script/planilha (workflow determinístico simples), sem agente de IA

Justificativa:
- O problema é aritmético e de rastreabilidade: saldo = entradas (NF) - saídas (fichas anestésicas) - perdas/descartes. Isso é conferível de forma exata; LLM adiciona risco de alucinação sem ganho.
- Livro de controlados é documento legal; erro inventado por IA é pior que erro humano rastreável.
- Uso pontual de LLM é opcional e restrito: extrair campos de foto de NF/ficha manuscrita (OCR), sempre com conferência humana. Não é necessário no MVP.

Desenho do MVP:
1. Planilha/CSV de lotes: substância, concentração, lote, validade, qtd entrada, NF.
2. Planilha de movimentações: data, paciente (código fictício/ID, nunca nome de tutor no MVP), substância, lote, volume administrado, volume descartado/sobra, responsável anestesista, testemunha do descarte.
3. Script (Python) que calcula saldo por lote, aponta divergência entre saldo teórico e contagem física, lista lotes a vencer (ex.: 60/30 dias, limiar configurável), sugere ponto de reposição e gera rascunho de pedido e de balanço.
4. Alertas determinísticos: saída sem lote, sobra não registrada, saldo negativo, ampola aberta sem destino, lote vencido em uso.

## 3. Human-in-the-loop e riscos

Validação humana obrigatória:
- Médico-veterinário responsável (e RT, quando aplicável) assina o registro, o balanço e o pedido; o sistema só gera rascunho.
- Contagem física periódica por duas pessoas; divergências são investigadas por humano, nunca "ajustadas" automaticamente.
- Descarte/sobra: executado e testemunhado por pessoas; sistema apenas registra.
- Pedido de controlados exige documentação formal; exigências exatas: não verificado.

Riscos:
- Legal: o registro automático não substitui o livro/sistema exigido pela norma; confirmar se planilha é aceita (provavelmente não como livro oficial, não verificado). Usar o MVP como conferência paralela, não como escrituração oficial.
- Clínico: dose e escolha de fármaco ficam fora do escopo; a ferramenta não recomenda doses.
- Desvio/segurança: log com trilha de auditoria, acesso por perfil, sem edição retroativa sem justificativa.
- LGPD: dados de paciente/tutor mínimos (ID interno); sem dados reais no MVP. Se houver dados de funcionários (responsáveis), tratar como dados pessoais; base legal e retenção: não verificado.
- Alucinação: nula no caminho determinístico; se OCR/LLM for adicionado, só preenche campos para revisão.

## 4. Pontuação (1-5)

- Impacto: 3. Reduz tempo de conferência e risco de autuação/desvio, mas é tarefa periódica, não diária de alto volume.
- Viabilidade: 4. Lógica simples; a dificuldade é integrar à ficha anestésica real do PIMS.
- Risco clínico/legal: 3. Baixo risco clínico, risco legal moderado por ser documento regulado se usado como registro oficial.

## 5. Cabe em MVP sem dados reais e sem serviços pagos?

Sim. Script Python local + CSVs sintéticos (fichas e NFs fictícias) cobrem saldo, validade, divergência, reposição e balanço-rascunho. Fora do MVP: integração com PIMS, envio oficial a órgãos, OCR.

## Pendências de verificação

Portaria 344/98 (aplicação à veterinária, prazos de guarda, balanços), norma de descarte, resoluções CFMV, e levantamento de produtos existentes.
