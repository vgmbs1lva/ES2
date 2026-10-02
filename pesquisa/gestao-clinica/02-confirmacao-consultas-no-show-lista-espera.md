# Confirmação de consultas e gestão de faltas (no-show) com lista de espera

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Aviso sobre fontes

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br e business.whatsapp.com). **Nenhuma afirmação factual abaixo foi verificada com fonte.** Tudo o que depende de produto, estudo, norma ou número está marcado "não verificado". Antes de usar, repetir a pesquisa com busca liberada. A recomendação de forma (item 2) se apoia em raciocínio de engenharia, não em evidência externa.

## 1. Soluções existentes

- Produtos/PIMS veterinários brasileiros com lembrete e confirmação por WhatsApp: não verificado (sem URL). Há vários sistemas de gestão veterinária no mercado, mas não posso citar nome, preço ou funcionalidade sem fonte.
- Plataformas internacionais de PIMS com lembrete automático e lista de espera: não verificado.
- Estudos sobre efeito de lembretes na taxa de falta (humana e veterinária): não verificado. Existe literatura em saúde humana sobre lembretes por SMS reduzirem faltas, mas não tenho URL; não usar número algum até confirmar.
- Antes de construir, verificar se o PIMS que a clínica já usa tem confirmação e lista de espera nativas. Se tiver, a resposta é "ligar a função existente", não desenvolver.

## 2. Forma recomendada: workflow determinístico (script/planilha na fase MVP)

Escolha: **workflow determinístico** com regras fixas, sem agente autônomo.

Justificativa:
- O processo é quase todo regra: listar consultas de amanhã, gerar mensagem de template, ler resposta (sim / não / remarcar), atualizar status, oferecer o horário liberado ao próximo da lista por ordem de prioridade definida.
- Texto livre dos tutores é pequeno e pode ser tratado por palavras-chave. Um LLM só seria opcional para interpretar respostas ambíguas ("acho que vou, mas depende do trabalho"), e mesmo aí o resultado deve cair em "revisar manualmente".
- Agente autônomo adicionaria risco (alucinação, mensagem errada para tutor errado) sem ganho proporcional.

Fluxo:
1. D-1 manhã: extrai agenda do dia seguinte.
2. Gera mensagens a partir de template aprovado (nome do tutor, nome do animal, horário, instruções de preparo fixas, ex.: jejum só se o veterinário definiu no cadastro do procedimento).
3. Recepção/veterinário revisa a fila e aprova o envio (ou envio automático só de template fixo, após período de confiança).
4. Respostas classificadas: confirmado / cancelou / sem resposta / ambíguo.
5. Sem resposta até horário-limite: ligação humana.
6. Cancelamento: sugere até N nomes da lista de espera conforme critérios fixos (ordem de chegada, urgência registrada pelo veterinário, porte/tempo de consulta compatível). Humano confirma antes de ofertar.
7. Fim do dia: registra comparecimento/falta; calcula taxa de falta (faltas / agendadas) por dia, semana e profissional.

## 3. Human-in-the-loop, riscos

Validação humana:
- Aprovar templates e regras de priorização (uma vez, e a cada mudança).
- Aprovar ou ao menos amostrar envios nas primeiras semanas.
- Todo caso ambíguo, e toda oferta de horário vago, passa por recepção.
- Triagem clínica: **o sistema nunca decide urgência**. Se o tutor responde com sintoma ("está vomitando", "piorou"), a mensagem sobe para o veterinário/recepção com prioridade, sem resposta automática de orientação clínica.

Riscos:
- Clínico: tutor relatar piora por mensagem e a resposta ficar na fila sem leitura. Mitigação: palavras-chave de alerta e aviso na própria mensagem de que urgências devem ligar para o telefone da clínica.
- Alucinação: eliminada pelo uso de templates fixos; se usar LLM, restringir a classificação em categorias fechadas e nunca gerar texto livre para o tutor.
- LGPD (Lei 13.709/2018): dados do tutor (nome, telefone) são dados pessoais. Base legal provável é execução de contrato/procedimentos preliminares, mas a escolha final, minimização de dados, informação ao titular e possibilidade de não receber mensagens devem ser validadas. Citação exata dos artigos: não verificado nesta execução. Se um LLM em nuvem processar nomes/telefones, há transferência a operador/internacional: avaliar. Em testes, só dados fictícios.
- WhatsApp: regras de opt-in e de mensagens iniciadas pela empresa e uso de API oficial vs. não oficial (risco de banimento de número): não verificado.
- CFMV: não identifiquei norma específica sobre lembretes de agenda (não verificado). Cuidado com sigilo e publicidade: a mensagem não deve incluir diagnóstico nem dados clínicos. Receituário controlado: não se aplica a esta tarefa e o sistema não deve tocar nele.
- Lista de espera com critério opaco pode gerar reclamação; documentar a regra e dar a ela um responsável.
- Overbooking/dupla oferta: uma oferta por vez por horário, com prazo curto de resposta.

## 4. Pontuação

- Impacto: 3/5. Libera tempo de recepção e recupera horários, mas o ganho depende da taxa de falta da clínica, que não conheço (não verificado).
- Viabilidade: 4/5. É lógica simples; a parte difícil é o canal WhatsApp e a integração com o PIMS real.
- Risco clínico/legal: 2/5. Baixo se houver template fixo, humano no ciclo e ausência de dados clínicos; sobe para 3 se houver LLM em nuvem ou resposta clínica automática.

## 5. MVP sem dados reais e sem serviços pagos

Cabe. Proposta: script Python (ou planilha) com:
- CSV fictício de agenda, tutores e lista de espera;
- geração das mensagens de template (saída em arquivo/console, sem envio real);
- simulador de respostas (arquivo) e classificador por palavras-chave;
- remanejamento da lista de espera por regras fixas, com saída "proposta, aguarda aprovação humana";
- cálculo da taxa de falta;
- testes unitários com casos ambíguos e mensagem com sintoma (deve escalar).
Fica fora do MVP: envio real por WhatsApp e integração com PIMS (dependem de serviços e dados reais).
