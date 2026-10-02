# Marketing: redes sociais, avaliações e campanhas sazonais

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Aviso de verificação
Nesta execução a cota de WebSearch estava esgotada (200/200) e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br, cfmv.gov.br). **Nenhuma afirmação abaixo tem fonte com URL verificada.** Tudo que é factual (produtos, normas, estudos) está marcado como "não verificado" e precisa ser conferido antes de uso. O que segue de recomendação é raciocínio de engenharia, não fato pesquisado.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com lembrete de vacina e campanhas (ex.: módulos de CRM/lembrete em sistemas veterinários brasileiros e internacionais): não verificado.
- Ferramentas genéricas de agendamento de posts (Meta Business Suite, Buffer etc.) e de resposta a avaliações do Google Business Profile: não verificado.
- Estudos sobre eficácia de lembretes de vacina/retorno em clínicas: não verificado.
- Normas: Código de Ética do médico-veterinário e regras de publicidade do CFMV (número e texto da resolução vigente): não verificado. LGPD (Lei 13.709/2018), em especial bases legais, consentimento e opt-out: não verificado nesta rodada, conferir no Planalto/ANPD. Regras do WhatsApp Business para mensagens ativas: não verificado.

## 2. Forma recomendada: workflow determinístico + rascunho por LLM (não agente autônomo)
- Lembretes de vacina/retorno: é regra de negócio (data da última dose + intervalo -> mensagem com modelo fixo). Planilha/script ou módulo do PIMS resolve. Não precisa de LLM.
- Posts e respostas a avaliações: LLM ajuda só a gerar rascunho a partir de calendário e modelos; publicação sempre manual/aprovada.
- Agente autônomo que publica ou responde sozinho: não recomendado (risco de alucinação, promessa clínica indevida, exposição de dados do paciente).

Pipeline sugerido: calendário de campanhas (CSV) -> gerador de rascunhos com modelos + checklist de conformidade -> fila de aprovação -> agendamento manual na plataforma.

## 3. Human-in-the-loop e riscos
- Validação do veterinário (RT): todo post e toda resposta de avaliação antes de publicar; lista de envio de lembretes antes de disparar.
- Clínico: promessas de resultado, preço promocional de procedimento anestésico/cirúrgico (castração) sem avaliação pré-operatória, orientações de dose/medicamento em post. Proibir no prompt e checar na revisão.
- Legal (CFMV): sensacionalismo, garantia de resultado, antes/depois e concorrência desleal em publicidade; regra exata não verificada, o RT deve confrontar com a resolução vigente.
- LGPD: dados do tutor (nome, telefone) e do paciente ligados ao tutor são dados pessoais; lembrete exige base legal e opt-out; foto de animal com tutor identificável precisa de autorização; avaliações respondidas não devem confirmar que a pessoa é cliente nem revelar dados do atendimento (sigilo). Detalhe jurídico: não verificado.
- Receituário controlado: nunca mencionar medicamentos controlados em material público; incluir regra de bloqueio por palavra-chave.
- Alucinação: o LLM pode inventar horários, preços, serviços ou estudos; mitigar com modelos fechados e dados da clínica como única fonte.

## 4. Pontuação (honesta)
- Impacto: 3. Economiza horas semanais e melhora retorno de vacina, mas é tarefa periférica à clínica.
- Viabilidade: 5. Ferramentas simples bastam.
- Risco: 2 (com aprovação humana); 4 se publicar/responder automaticamente.

## 5. MVP sem dados reais e sem serviços pagos
Cabe. Escopo: script em Python que lê um CSV sintético de calendário e de pacientes fictícios, gera lembretes por modelo fixo (sem LLM) e rascunhos de posts por modelo, com verificador de conformidade (palavras proibidas: garantia, 100%, medicamentos controlados; ausência de dados pessoais) e saída em fila de aprovação (CSV/Markdown). Resposta a avaliações no MVP: modelos por faixa de nota, sem LLM. Integração com Google/Meta/WhatsApp fica fora do MVP.
