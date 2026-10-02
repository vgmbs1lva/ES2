# Comunicação com tutores durante a internação (boletim, autorização de custos adicionais)

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Aviso sobre fontes (leia primeiro)

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o proxy bloqueou WebFetch (fve.org, cfmv.gov.br). **Nenhuma afirmação externa foi verificada.** Não cito URLs que não abri. Tudo que depende de fonte externa está marcado "não verificado". Tempo gasto nessa tarefa: não verificado (sem levantamento específico).

## 1. Soluções existentes

Não verificado. Hipóteses a checar, sem afirmar que existam nas formas descritas:
- PIMS veterinários com módulo de internação, mensagens ao tutor (WhatsApp/SMS) e orçamento/estimativa com aprovação. Produtos e recursos específicos, inclusive os disponíveis no Brasil: não verificado.
- API oficial do WhatsApp Business (templates aprovados) como canal: não verificado quanto a regras e custos atuais.
- Estudos sobre comunicação com tutor de internados, satisfação e rascunhos de texto por LLM: não verificado.
- Âncora de tempo da tarefa anterior (FVE 2025, n=75, Europa): não reaberta, não aplicável ao Brasil.

Pendência: refazer a pesquisa quando houver orçamento de busca.

## 2. Forma recomendada: workflow determinístico com rascunho por template; LLM opcional só para redação

Justificativa:
- O boletim tem estrutura fixa (estado geral, alimentação, hidratação, dor, exames, plano do dia, próximos passos). Dá para montar por template a partir de campos já preenchidos na evolução, sem IA.
- O orçamento é aritmético: itens previstos + extras acumulados, variação percentual contra o valor autorizado, gatilho "pedir autorização" quando ultrapassar um limite combinado com o tutor. Isso é regra, não IA.
- Registro no prontuário: o script grava data/hora, canal, texto enviado, quem enviou e resposta do tutor.
- LLM, se usado, apenas converte a evolução técnica em linguagem leve, como rascunho que o veterinário lê e edita. Não precisa de agente: não há decisão autônoma nem encadeamento de ferramentas.
- Autorização de custo é ato com consequência legal/financeira: **não automatizar o envio nem o aceite**. Automatiza-se o preparo e o registro.

Fluxo:
1. Entradas: evolução do dia (campos estruturados), lista de itens/procedimentos com valores, orçamento autorizado, preferência de contato do tutor.
2. Script gera rascunho do boletim (template) e a posição financeira (autorizado x acumulado x previsto).
3. Veterinário revisa, edita e aprova; o envio é feito pela equipe (ou disparado após clique do veterinário).
4. Se o acumulado passar do limite, gera pedido de autorização com itens e valores; fica pendente até haver resposta registrada do tutor (texto/áudio/e-mail, com data e hora).
5. Tudo é anexado ao prontuário com trilha de auditoria.

## 3. Human-in-the-loop, riscos e conformidade

Validação:
- O veterinário aprova todo boletim antes do envio, em especial prognóstico, complicações e óbito/piora (esses devem ser comunicados por ligação/conversa, não por mensagem automática).
- A equipe administrativa confere valores; o aceite do tutor deve ser humano e registrado.
- Urgência (piora súbita, decisão de reintervenção): fluxo fora da automação.

Riscos clínicos:
- Boletim otimista ou impreciso (omissão de complicação), ou texto "suavizado" por LLM que mude o sentido clínico. Mitigação: template com campos fixos, LLM só reformula e é diffável, revisão obrigatória.
- Comunicação de piora por canal frio. Mitigação: regra que bloqueia envio automático quando status = crítico/piora e exige contato telefônico.

Alucinação:
- LLM pode inventar exame, valor ou prognóstico. Mitigação: só pode usar campos fornecidos; checagem de que números/valores do texto coincidem com a fonte; sem LLM para valores financeiros.

Legais (todos não verificados; confirmar o texto vigente):
- CFMV: exigências de prontuário, informação ao tutor e consentimento. Resolução/artigo específico: não verificado.
- Defesa do consumidor: informação prévia sobre preço e serviços adicionais (CDC). Enquadramento exato: não verificado.
- LGPD: telefone/nome do tutor e dados do paciente são dados pessoais; base legal, consentimento do canal (WhatsApp), minimização, e não enviar dados identificáveis a APIs externas de LLM sem avaliação. Não verificado quanto ao detalhe.
- Receituário controlado: não se aplica diretamente, mas o boletim não deve conter prescrição de controlados nem substituir receita.
- Prova: registrar a autorização é a principal proteção; mensagem de WhatsApp como prova depende de preservar o conteúdo (não verificado).

## 4. Pontuação (1-5)

- Impacto: 3. Tarefa diária e recorrente, com ganho real em redigir e registrar; mas o valor central da conversa com o tutor é humano e não deve ser removido. Tempo economizado: não verificado.
- Viabilidade: 4. Template + planilha de orçamento + registro são simples; a dificuldade é a integração com o PIMS e com o canal de mensagem.
- Risco: 3. Risco clínico baixo-moderado com revisão humana; sobe para 4 se enviar sem revisão ou se o LLM redigir prognóstico; o risco legal está no consentimento de custos e na LGPD.

## 5. MVP sem dados reais e sem serviços pagos: sim

Script Python/planilha com:
- Pacientes e tutores sintéticos (nomes fictícios, sem telefone real).
- Evolução em campos estruturados (JSON/CSV) e template de boletim em Markdown/texto.
- Planilha de orçamento: autorizado, extras, acumulado, percentual de desvio e gatilho de pedido de autorização.
- Regras de bloqueio (status crítico exige ligação; valor acima do limite exige autorização registrada).
- Registro em arquivo (CSV/SQLite) com data/hora, autor e conteúdo; testes automatizados para os gatilhos e cálculos.
- Sem envio real: saída em arquivo/console. Integração com WhatsApp/PIMS fica fora do MVP (custos e dados reais).
Limite: o MVP valida lógica e fluxo, não a linguagem clínica nem a conformidade jurídica.

## Decisão resumida

Workflow determinístico com aprovação do veterinário; LLM opcional apenas para reformular texto do boletim (rascunho); autorização de custos e comunicação de piora permanecem humanas. Pesquisa externa pendente.
