# Cobrança de inadimplentes e negociação de orçamentos/internações

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Aviso sobre fontes (leia primeiro)
Nesta execução o limite de WebSearch da sessão (200/200) estava esgotado e o proxy bloqueou WebFetch para planalto.gov.br e cfmv.gov.br. **Nenhuma afirmação abaixo foi verificada por fonte.** Tudo que é factual (produtos, normas, artigos) está marcado "não verificado" e deve ser conferido antes de uso. Os URLs listados são os endereços oficiais que eu tentei abrir, não confirmações de conteúdo.

## Soluções existentes
- Produtos/plug-ins de PIMS veterinários brasileiros ou internacionais com cobrança, orçamento e lembretes (ex.: Simples Vet, Vetsmart, Digitail, Shepherd, Vetspire): **não verificado** se e como cada um oferece orçamento com aceite digital, régua de cobrança ou pagamento parcelado. Conferir nos sites e demos dos fornecedores.
- Gateways/ERP genéricos (boleto/Pix, régua de cobrança, link de pagamento, parcelamento): existem de forma geral, mas **não verificado** por fonte nesta execução.
- Estudos sobre eficácia de cobrança automatizada ou conversa sobre custos em veterinária: **não verificado**; nenhum estudo localizado.

## Normas a conferir (não verificado)
- CDC (Lei 8.078/1990), art. 42: cobrança sem exposição a ridículo ou constrangimento. Fonte oficial a conferir: https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm
- LGPD (Lei 13.709/2018): base legal (execução de contrato, exercício regular de direitos), minimização, segurança, art. 20 sobre decisões automatizadas. Conferir: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- CFMV: resoluções sobre Código de Ética, prontuário e consentimento/termo de ciência (número e teor exatos não verificados). Conferir: https://www.cfmv.gov.br
- Receituário controlado: não se aplica a esta tarefa, salvo se o orçamento listar medicamentos controlados; nesse caso o agente nunca deve gerar nem sugerir receita.

## Forma recomendada: workflow determinístico (com redação assistida opcional por LLM)
Não precisa de agente autônomo. O trabalho é: filtrar contas vencidas, aplicar uma régua fixa de mensagens, registrar contato, gerar orçamento a partir de tabela de preços e coletar aceite. Isso é regra de negócio e cabe em planilha + script/automação simples.

Sugestão de desenho:
1. Script lê o contas a receber (CSV) e classifica por dias de atraso e valor.
2. Régua de modelos de mensagem fixos (lembrete, segunda via, proposta de parcelamento dentro da política da clínica).
3. Um LLM, se usado, apenas reescreve o tom de um modelo aprovado; não inventa valores, descontos nem prazos. Valores vêm só da planilha.
4. Gerador de orçamento: itens e preços vêm da tabela da clínica; o veterinário preenche/valida a parte clínica (procedimentos, estimativa de internação, riscos).
5. Termo de ciência: modelo fixo revisado pela clínica/assessoria jurídica; o sistema só preenche campos.
6. Log de cada contato (data, canal, modelo usado, quem aprovou).

Por que não agente: autonomia para negociar valor ou prometer desconto traz risco financeiro e jurídico sem ganho; o agente alucinar condição de pagamento é o pior caso.

## Human-in-the-loop
- Financeiro/recepção aprova o lote de mensagens antes do envio (no MVP, nada é enviado automaticamente).
- Qualquer desvio da política (desconto, parcelas extras) exige aprovação humana.
- O veterinário valida o conteúdo clínico do orçamento (procedimentos, prognóstico, estimativa de internação e a faixa de variação) e conduz a conversa sobre risco; o termo de ciência não substitui explicação ao tutor.
- Casos de emergência/internação em curso: nunca condicionar atendimento emergencial a cobrança por automação; decisão humana.
- Revisão periódica de amostra dos textos enviados.

## Riscos
- Legais: tom de cobrança constrangedor ou exposição da dívida a terceiros (CDC art. 42, não verificado); contato fora de horário razoável; uso de dados sem base legal ou sem segurança (LGPD); mensagem a número errado expõe dado do tutor/animal. Dados do paciente nas mensagens devem ser mínimos.
- Clínicos: orçamento desatualizado ou subestimado levando a decisão de tutor mal informada; pressão financeira interferindo em conduta; eutanásia/abandono por custo é situação sensível que exige humano.
- Alucinação: valores, parcelas, juros ou prazos inventados; promessa de resultado clínico. Mitigação: valores só de dados estruturados, texto de modelo fixo, validação por regra (números da mensagem batem com a planilha).
- Jurídico contratual: aceite digital e termo precisam de validade e guarda de prova; **não verificado** o que o CFMV exige. Consultar assessoria.

## Pontuação (1-5, avaliação própria, sem fonte)
- Impacto: 3. Libera tempo da recepção e melhora recuperação de crédito, mas o ganho depende do volume de inadimplência da clínica (não medido).
- Viabilidade: 5 para workflow/planilha; 3 se exigir integração com PIMS e WhatsApp oficial.
- Risco: 3 (legal/relacional moderado; clínico baixo se o veterinário valida orçamentos).

## MVP sem dados reais e sem serviços pagos
Cabe. Escopo: script em Python que lê CSV sintético de contas a receber, calcula atraso, escolhe modelo da régua, valida os números da mensagem contra o CSV, gera rascunhos em arquivo para aprovação humana e grava o log em CSV; mais um gerador de orçamento em Markdown/HTML a partir de uma tabela de preços fictícia. Sem envio real, sem LLM obrigatório.
