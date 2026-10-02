# Mensagens a tutores por WhatsApp/e-mail (resultados, dúvidas pós-consulta, acompanhamento)

Data da pesquisa: 2026-10-02. Domínio: administrativo. Afirmações sem fonte estão marcadas "não verificado". Nota: alguns sites (cfmv.gov.br, respond.io) foram bloqueados na busca; o que vem deles está citado a partir de resumos de busca, não de leitura da página.

## 1. Soluções existentes

Produtos (fonte majoritariamente de fornecedores; evidência de eficácia independente: não verificado):
- Plataformas de comunicação com tutor (texto bidirecional, lembretes, follow-up pós-operatório, resultados): https://otto.vet/veterinary-client-communication-platforms/ e https://emitrr.com/blog/texting-software-for-veterinary-practices/
- IDEXX Vello (engajamento do cliente): https://software.idexx.com/vello
- Guia de automação de WhatsApp para clínicas (blog de fornecedor): afirma que check-ins pós-operatórios podem ser disparados e as respostas registradas no PIMS, com integração a vários PIMS (eVetPractice, Cornerstone, AVImark, Digitail, Provet Cloud etc.). https://bossbot.uk/blog/whatsapp-automation-veterinary
- Recepcionistas de IA para clínicas: https://www.puppilot.co/blog/ai-vet-receptionist-for-vets-the-complete-guide-to-always-on-client-communication e https://solvea.cx/blog/best-ai-receptionist-for-veterinary-clinics
- Brasil: não encontrei produto brasileiro específico verificado nesta busca. Não verificado.

Evidência sobre rascunhos de IA para mensagens de pacientes (medicina humana, não veterinária):
- Lancet Digital Health: GPT-4 redigiu 156 respostas em portal de paciente; 7,1% dos rascunhos tinham risco de dano grave e os 20 médicos revisores deixaram passar em média 66,6% dos erros perigosos; 58,3% foram julgados enviáveis sem edição. https://www.thelancet.com/journals/landig/article/PIIS2589-7500(24)00060-8/fulltext (números vindos do resumo de busca; conferir no artigo).
- Rascunhos de IA podem aumentar a carga cognitiva de edição: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12198195/ e https://www.nature.com/articles/s41746-025-01586-2
- Estudo veterinário equivalente validando respostas automáticas a tutores: não encontrei. Não verificado.

Normas e plataforma:
- Res. CFMV 1.465/2022 (telemedicina): informação, orientação ou monitoramento feitos por WhatsApp, telefone ou outro meio remoto devem ser registrados no prontuário (segundo resumo de busca; ler o texto): https://jornal.unesp.br/wp-content/uploads/2022/08/Resolucao_TelemedicinaVeterinaria-1.pdf e https://www.legisweb.com.br/legislacao/?id=433219
- Res. CFMV 1.321/2020 (prontuário): https://www.normasbrasil.com.br/norma/resolucao-1321-2020_480427.html
- Meta/WhatsApp Business API: desde 15/01/2026, chatbots de IA de propósito geral são proibidos; automações com finalidade específica (atendimento, notificações transacionais, suporte) seguem permitidas. Fontes secundárias: https://z-api.io/blog/meta-atualiza-politica-do-whatsapp-business/ e https://wsa.adv.br/noticias/whatsapp-termos-de-uso-proibe-chatbots-de-ia/ . Texto oficial da Meta: não verificado.
- LGPD art. 33 (transferência internacional só nas hipóteses legais; cláusulas-padrão da ANPD): http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm e https://www.gov.br/participamaisbrasil/regulamento-de-transferencias-internacionais-de-dados-pessoais-e-do-modelo-de-clausulas-padrao-contratuais

## 2. Forma recomendada

**Workflow determinístico (gatilhos + modelos aprovados), com rascunho de IA opcional apenas para dúvidas, sempre revisado. Não agente autônomo.**

Justificativa:
- A maior parte do volume é previsível: lembrete de retorno/vacina, "resultado disponível", check-in D+1/D+3/D+7 pós-cirurgia. Isso é agenda + modelo de mensagem + perguntas fechadas (come? urina? ferida? dor?). Planilha/script e modelos resolvem, sem alucinação.
- Respostas dos tutores são classificadas por regras simples (palavras de alerta como vômito, sangramento, dor, não come, dispneia) e escalam para o veterinário. A classificação não decide conduta.
- Dúvida aberta sobre o caso clínico: a IA só rascunha, com base no prontuário, e o veterinário aprova. Risco documentado na literatura humana acima.
- Resultado de exame: não enviar interpretação automática. Enviar aviso de disponibilidade ou o laudo já liberado pelo veterinário.
- Agente que conversa livremente com o tutor: não recomendado (conduta clínica sem veterinário, risco com a política do WhatsApp, e CFMV 1.465 trata orientação remota como ato do veterinário, a confirmar no texto).

## 3. Human-in-the-loop e riscos

Validação:
1. Modelos de mensagem (lembrete, check-in, aviso de resultado) aprovados uma vez pelo veterinário responsável; conteúdo clínico fixo.
2. Toda resposta a dúvida clínica, e qualquer envio de resultado com interpretação, é revisada e enviada pelo veterinário (rascunho "não enviado" por padrão).
3. Respostas com sinais de alerta geram notificação imediata à equipe e orientação padrão de procurar atendimento, definida pela clínica.
4. O que for clínico (queixa, orientação dada, evolução relatada) é registrado no prontuário com data, hora e autor, em registro rascunho até o veterinário confirmar.

Riscos:
- Clínicos: tutor relata piora e a mensagem fica sem leitura fora do horário; orientação genérica errada; revisor que aprova por hábito (a literatura mostra erros perigosos não detectados). Mitigação: aviso de horário de atendimento e canal de urgência nos modelos, fila priorizada, auditoria por amostragem.
- Alucinação: IA inventar conduta, dose ou prognóstico. Mitigação: só recebe campos estruturados, proibida de citar medicamento/dose, saída conferida.
- Legais (CFMV): registro no prontuário de toda orientação remota (1.465/2022); prescrição a distância exige elementos e assinatura eletrônica avançada, segundo resumo de busca (verificar no texto). Receituário controlado (Portaria SVS/MS 344/98): nunca enviar ou gerar receita de controle especial por mensageria automática. Requisitos de receita eletrônica veterinária: não verificado.
- LGPD: telefone, e-mail e dados do animal ligado ao tutor são dados pessoais; base legal e aviso ao tutor sobre uso de canal e IA; minimizar dados enviados a LLM externo (sem nome/telefone/CPF); LLM em servidor no exterior implica transferência internacional (art. 33). Consentimento específico para contato por WhatsApp: recomendado, base exata não verificada.
- Plataforma: usar API oficial do WhatsApp Business com opt-in; número pessoal automatizado pode levar a banimento (não verificado). Automação específica de atendimento permanece permitida segundo fontes secundárias.

## 4. Pontuação

- Impacto: 4. Tarefa diária e fragmentada, com ganho real em lembretes e check-ins.
- Viabilidade: 4 para o workflow de modelos e lembretes; 2 a 3 para resposta de dúvida por IA com segurança.
- Risco: 3 com validação e sem texto clínico livre; 5 se for autônomo.

## 5. MVP sem dados reais e sem serviços pagos

Cabe: sim.
- Script Python/planilha com tutores e pacientes fictícios: tabela de procedimentos e datas gera fila de mensagens (retorno, check-in D+1/D+3/D+7) a partir de modelos, em arquivo, sem envio real.
- Classificador por regras de respostas fictícias com palavras de alerta; saída: "escalar" ou "rotina".
- Gerador de entrada de prontuário em rascunho a partir da conversa.
- Teste: conjunto sintético com casos de alerta plantados, medindo sensibilidade; e conferência de que nenhuma mensagem sai sem aprovação.
- Fora do MVP: API real do WhatsApp, integração com PIMS, LLM para rascunho (pode ser local gratuito depois), receituário.
