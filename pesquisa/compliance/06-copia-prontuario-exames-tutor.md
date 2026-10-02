# 06 - Atender pedidos de cópia de prontuário e de exames pelo tutor

Domínio: compliance. Data: 2026-10-02.

## Limitações desta pesquisa (leia primeiro)
- O limite de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy para crmvgo.org.br e planalto.gov.br.
- Portanto, **nenhuma afirmação abaixo foi verificada por mim em fonte**. Os prazos (5 dias úteis, prorrogação até 30 dias úteis com justificativa do RT) vêm só da descrição da tarefa, que cita https://crmvgo.org.br/resolucao-cfmv-no-1-653-2025-estabelece-novas-regras-sobre-o-prontuario-veterinario/ (não consegui abrir). Texto da Resolução CFMV 1.653/2025: não verificado.
- Soluções existentes (produtos, plug-ins de PIMS, estudos): **não verificado**. Não cito produto algum para não inventar. Sabe-se apenas, em termos gerais, que PIMS costumam exportar prontuário em PDF; isso precisa ser confirmado no sistema usado na clínica.
- LGPD (Lei 13.709/2018, direito de acesso do titular, arts. 18-19): aplicabilidade e prazos para dados de tutor: não verificado. Dados do tutor (nome, contato, histórico financeiro) são dados pessoais; o prontuário do animal em si, em parte, não. Tratar como ponto a validar com jurídico/CRMV.
- Receituário controlado (Portaria SVS/MS 344/98 e retenção de notificações/receitas): não verificado se há regra específica para cópia ao tutor.

## 1. Soluções existentes
Não verificado. Recomenda-se pesquisar depois: recurso de "exportar prontuário/histórico" e portal do tutor no PIMS em uso; modelos de requerimento publicados pelos CRMVs.

## 2. Forma recomendada: script/planilha (checklist + controle de prazo)
Justificativa: frequência baixa e irregular; o gargalo é o cumprimento do prazo e a conferência humana, não volume. Um agente de IA agrega risco (vazamento, alucinação ao "resumir" prontuário) sem ganho. Basta:
- Planilha de protocolo: nº, data de recebimento, solicitante, prova de que é o tutor (checagem de identidade), itens pedidos, data-limite calculada (5 dias úteis, com função de dias úteis; feriados municipais à mão), status, justificativa de prorrogação (campo obrigatório do RT, limite 30 dias úteis), data/forma de entrega, quem revisou.
- Alerta de prazo (formatação condicional ou lembrete de calendário em D-2).
- Modelos de texto: confirmação de recebimento, pedido de comprovação de identidade, justificativa de prorrogação, termo de entrega.
- Opcional: script que gera o PDF consolidado a partir da exportação do PIMS e registra hash/data.

Não é caso para agente. LLM no máximo como redator opcional de e-mail-modelo, sem acesso ao prontuário.

## 3. Human-in-the-loop e riscos
- O veterinário/RT: valida identidade e legitimidade do solicitante, revisa o que será entregue (dados de terceiros, anotações que não pertençam ao tutor, receitas), decide e assina prorrogação, aprova a entrega.
- Clínico: entrega de cópia incompleta ou de paciente errado (homônimos). Conferir nome do animal, tutor e ID.
- Legal: perda de prazo (CFMV; não verificado texto exato); entrega a pessoa sem legitimidade; LGPD ao enviar dados por canal inseguro (e-mail comum, WhatsApp) - preferir link com senha ou entrega presencial; registrar a entrega.
- Receituário controlado: não verificado; conferir com a norma aplicável antes de incluir cópias de receitas/notificações.
- Alucinação: nula se não houver IA; se houver, proibir geração de conteúdo clínico - só o documento original é entregue.

## 4. Pontuação
- Impacto: 2 (baixa frequência; valor está em evitar infração/prazo vencido).
- Viabilidade: 5 (planilha e modelos).
- Risco: 3 (legal moderado se o prazo ou a identidade falharem; clínico baixo). Seria 4-5 com IA manipulando prontuários.

## 5. MVP sem dados reais e sem serviços pagos
Sim. Planilha (CSV/Google Sheets gratuito ou LibreOffice) com dados fictícios, cálculo de dias úteis, status e modelos de texto; testável em poucas horas.
