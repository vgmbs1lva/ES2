# Contato com tutores faltosos ou em atraso de retorno (doença crônica, pós-op)

Domínio: atendimento-tutor. Data da análise: 2026-10-02.

Limitação desta pesquisa: o orçamento de WebSearch da sessão acabou e o WebFetch foi bloqueado para PMC e dvm360. Só uso o que apareceu nos resumos de busca; o resto está marcado "não verificado".

## Recomendação: workflow determinístico (lista de vencidos + escalonamento + roteiro de ligação), sem agente autônomo

O gargalo é descobrir quem está vencido, priorizar e registrar o desfecho. Isso se resolve com regra, não com raciocínio clínico. Fluxo proposto:
1. Consulta diária ao prontuário/PIMS (ou planilha): paciente crônico com retorno ou exame de controle vencido (data prevista + tolerância por condição).
2. Priorização por regras definidas pelo veterinário (ex.: medicação de uso contínuo que acaba, exame pendente de resultado, pós-op com retirada de pontos vencida sobem de prioridade).
3. Escalonamento: lembrete padronizado (mensagem) no D+X, ligação humana no D+Y, última tentativa e registro de recusa.
4. Roteiro de ligação com o porquê do retorno, preenchido por condição (modelo aprovado pelo veterinário).
5. Registro estruturado do desfecho: agendado, recusou (motivo), sem contato, relato de piora (escala ao veterinário).

IA (LLM) só agrega em: rascunhar mensagem em tom humano e resumir o que o tutor disse para a nota do prontuário. Ambos como rascunho. Qualquer ajuste de conduta por telefone é ato do veterinário, nunca automático.

## 1. Soluções existentes

- Lembretes automáticos de retorno/consulta em PIMS: Digitail (https://digitail.com/), Provet Cloud (https://www.provet.com/), IDEXX Neo (https://software.idexx.com/top-veterinary-software-solutions-a-2025-comparison-guide). Texto de busca cita agendamento e lembretes como funções centrais; são fontes de fornecedor. Disponibilidade no Brasil, WhatsApp e idioma: não verificado. Lembrete específico por doença crônica (renal, cardíaco etc.): não verificado.
- Estudo veterinário sobre adesão a lembretes de PIMS: "Analysis of a practice management computer software program for owner compliance with recall reminders" (https://pmc.ncbi.nlm.nih.gov/articles/PMC1371051/). Pelo resumo de busca: avaliou lembretes de vacina, exame anual, recheck/progresso, castração, odontologia e laboratório em 12 meses (2001-2002) e fatores associados à resposta. Não consegui abrir o texto; taxas de adesão e conclusões: não verificado.
- Percepção do tutor de que recheck é "grátis e opcional" e orientação de frequência de monitoramento em DRC: dvm360 (https://www.dvm360.com/view/facilitating-client-management-chronic-kidney-disease-proceedings), anais de congresso, nível de evidência baixo. Não li o texto completo.
- Material de prática sobre adesão: Today's Veterinary Nurse (https://todaysveterinarynurse.com/practice-management/can-we-talk-ensuring-owner-compliance/), Veterinary Practice News (https://www.veterinarypracticenews.com/words-that-turn-confusion-into-compliance/). Opinião/prática; apontam que faltar a retorno sugere problema de adesão ao tratamento e que lembretes por texto reduzem faltas (resumo de busca).
- Ensaio clínico de lembretes automatizados em DRC humana (NCT00688285): https://clinicaltrials.gov/study/NCT00688285. Medicina humana, só analogia; resultado: não verificado.
- Ensaio veterinário controlado mostrando melhor desfecho clínico com contato ativo de tutores faltosos: não verificado (não encontrei).
- Produto nacional com este fluxo: não verificado.

## 2. Forma recomendada e justificativa

Workflow determinístico/planilha. Entrada estruturada (data do último controle, intervalo definido pelo clínico, exame pendente), regras fixas, perguntas fechadas. Agente não se justifica: o valor de uma "conversa livre" com tutor é pequeno e o risco de o agente dar orientação clínica (ajustar insulina, diurético, dieta) é alto. Integração com PIMS é desejável depois, mas o MVP é planilha/script. Não é caso de "não automatizar": a parte administrativa (listar, lembrar, registrar) é segura de automatizar; a ligação em si deve continuar humana.

## 3. Human-in-the-loop e riscos

Onde o veterinário valida:
1. Define uma vez, por condição, o intervalo de retorno, a tolerância e o motivo do retorno (texto aprovado).
2. Revisa a fila priorizada antes do contato; decide quem recebe ligação vs. lembrete.
3. Qualquer relato de piora, falta de medicação ou dúvida sobre dose vai ao veterinário; ajuste de conduta por telefone é dele e fica registrado.
4. Prontuário: nota rascunho assinada pelo veterinário.

Riscos:
- Clínico: lista incompleta ou data errada deixa paciente de fora (falso senso de segurança); tutor minimiza sinais; paciente crônico sem medicação por semanas (ex.: diabético com insulina interrompida) exige triagem rápida. Mitigar: regra conservadora, sinais de alerta e canal de urgência em toda mensagem, relato de piora nunca fica na fila comum.
- Alucinação: LLM pode inventar justificativa clínica, dose ou prazo. Mitigar: textos clínicos só de modelos aprovados; LLM não fala com o tutor sozinho.
- Legal/CFMV: contato com paciente já atendido presencialmente se aproxima do que a regulamentação de telemedicina veterinária chama de teleorientação/telemonitoramento (sem diagnóstico, exame ou prescrição à distância), segundo resumos CRMV-SP/CFMV (https://crmvsp.gov.br/resolucao-que-regulamenta-a-telemedicina-veterinaria-e-publicada-entenda-como-funciona/). Número da resolução, exigências de consentimento e registro: não verificado no texto primário (CFMV inacessível nesta sessão). Prontuário: Resolução CFMV 1321/2020 (https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf), não relida. Conferir antes de implantar.
- Receituário controlado: o fluxo não emite nem renova receita; pedido de renovação (ex.: fenobarbital, opioides) vai ao veterinário e segue a norma do MAPA/ANVISA aplicável (não verificado).
- LGPD: telefone e nome do tutor + dados do animal são dados pessoais; contato de recall costuma se apoiar em execução do serviço contratado, com aviso na ficha; consentimento para WhatsApp recomendado por fontes de mercado (https://www.socialhub.pro/blog/lgpd-clinica-whatsapp-consentimento-obrigatorio/, fonte comercial). Guia da ANPD sobre legítimo interesse: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_legitimo_interesse.pdf/@@display-file/file. Minimizar dados se usar LLM em nuvem; validar com assessoria jurídica.
- Relacional: insistência excessiva pode soar como cobrança; limitar tentativas e respeitar recusa registrada.

## 4. Pontuação (1-5)

- Impacto: 3. Retorno de crônicos tem valor clínico e de receita plausível, mas o ganho de tempo é moderado e a evidência veterinária de desfecho não foi verificada.
- Viabilidade: 5 para planilha/script; 3 com integração a PIMS e envio por WhatsApp.
- Risco clínico/legal: 2 para o workflow com revisão (não decide conduta); 4-5 se um agente ajustasse conduta por telefone.

## 5. MVP sem dados reais e sem serviços pagos: sim

Script em Python/planilha com CSV sintético (pacientes fictícios, condição, último controle, exame pendente) que: (a) calcula vencidos por regra de intervalo por condição; (b) prioriza por regras; (c) gera mensagem e roteiro de ligação por modelo aprovado; (d) registra desfecho (agendado/recusa/sem contato/escalar) e produz nota rascunho para assinatura. Sem envio real, sem LLM obrigatório, sem integração paga. Envio por WhatsApp/SMS e integração com PIMS ficam fora do MVP.
