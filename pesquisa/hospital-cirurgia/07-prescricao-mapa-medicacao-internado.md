# Prescrição e mapa de medicação do internado

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Aviso sobre fontes (leia primeiro)

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o proxy bloqueou WebFetch para fve.org, planalto.gov.br e pubmed. Portanto **nenhuma afirmação externa foi verificada nesta análise**. Tudo abaixo marcado "não verificado" precisa ser conferido antes de ser usado como base de decisão. Não foram citadas URLs que eu não tenha aberto.

- Âncora de tempo (dada na tarefa, não reaberta por mim): pesquisa FVE 2025, n=75, Europa, https://fve.org/cms/wp-content/uploads/Admin-burden-report-R13-1.pdf. Serve só como ordem de grandeza; não verificado por mim e não vale para o Brasil.

## 1. Soluções existentes

Não verificado (sem pesquisa possível). Hipóteses a checar, sem afirmar que existem nas formas descritas:
- PIMS com folha de tratamento/internação e cálculo de dose por peso (categoria comum em sistemas veterinários; produtos e recursos específicos: não verificado).
- Formulários de referência de dose (ex.: Plumb's) como base de consulta: não verificado quanto a API/licença para uso automatizado.
- Estudos sobre LLMs em dose veterinária e sobre erros de medicação em internação veterinária: não verificado; buscar em PubMed/Google Scholar.

Pendência: refazer a pesquisa (produtos de PIMS no Brasil, CPOE veterinário, estudos de erro de dose por LLM) quando houver orçamento de busca.

## 2. Forma recomendada: workflow determinístico (script/planilha com regras), com LLM opcional só para rascunho de texto

Justificativa:
- O núcleo da tarefa é aritmético e repetitivo: dose (mg/kg) x peso, volume a administrar, taxa de fluido (manutenção + déficit + perdas), horários a partir de frequência (SID/BID/TID/QID), alimentação por necessidade energética. Isso se resolve com tabela de fármacos curada pelo próprio hospital + fórmulas. Um LLM aqui adiciona risco de alucinação de dose sem ganho.
- O mapa de horários é derivado 100% da prescrição aprovada: gerar por código, não por IA.
- Onde IA poderia ajudar: resumir a evolução e sugerir pontos de revisão (suspender antibiótico, trocar via, reavaliar analgesia) como rascunho lido pelo veterinário. Isso é opcional e deve vir depois do núcleo determinístico.
- Não é "agente": não há decisão autônoma nem uso de ferramentas encadeadas que justifique.

Fluxo proposto:
1. Entrada: peso do dia, espécie, condições (renal/hepática), prescrição do dia anterior, formulário interno de fármacos (dose mín/máx, vias, diluição, concentração).
2. Script copia a prescrição anterior, recalcula doses/volumes pelo peso atual e sinaliza: dose fora da faixa do formulário, duplicidade de classe (ex.: dois AINEs), fármaco sem peso, alerta de espécie (ex.: restrições em gatos), medicamento sem estoque.
3. Veterinário revisa e assina; só então gera o mapa de horários (impressão/PDF).
4. Pedidos de exame: lista sugerida por regras do protocolo da internação, apenas como lembrete.

## 3. Human-in-the-loop, riscos e conformidade

Validação:
- O veterinário responsável revisa e aprova toda prescrição antes de virar mapa; nada vai à equipe sem aprovação registrada (quem, quando).
- Revisão obrigatória sempre que houver mudança de peso > limiar definido, medicamento novo, controlado, ou alerta do sistema.
- Dupla checagem por enfermagem na administração (fora do escopo da automação, mas o mapa deve facilitar).

Riscos clínicos:
- Erro de dose por peso errado/desatualizado, erro de unidade (mg vs mL, mg/kg vs mg/animal), erro de concentração, taxa de fluido inadequada em cardiopata/renal. Mitigação: faixas no formulário, exibição de cálculo transparente, bloqueio duro em valores absurdos.
- Alucinação: se LLM for usado, nunca para dose; apenas texto, sempre rotulado como rascunho.
- Automation bias: o veterinário aprovar sem ler. Mitigação: mostrar apenas diferenças em relação ao dia anterior e alertas.

Legais (todos não verificados; confirmar o texto vigente):
- CFMV: exigências de prontuário e responsabilidade técnica pela prescrição. Não verificado qual resolução/artigo.
- Receituário/medicamentos controlados (Portaria SVS/MS 344/98 e correlatas, notificação de receita): o sistema não deve emitir nem substituir receita controlada; apenas sinalizar que exige receituário próprio. Não verificado.
- LGPD: dados de tutores são pessoais; no MVP usar apenas dados sintéticos; em produção, evitar enviar dados identificáveis a APIs externas de LLM. Não verificado enquadramento exato.
- Registro: manter trilha de auditoria (versão da prescrição, quem alterou).

## 4. Pontuação (1-5)

- Impacto: 4. Prescrição/mapa é tarefa diária e repetitiva; a âncora FVE sugere horas por semana, mas é Europa, n=75, não verificada por mim. Ganho real depende do volume de internados.
- Viabilidade: 4. Cálculo e mapa são simples e determinísticos; a dificuldade é curar o formulário de fármacos e integrar ao PIMS existente.
- Risco: 4. Erro de dose em paciente internado pode causar dano grave; é mitigável por regras e validação humana, mas o risco residual é alto, e sobe para 5 se LLM decidir doses.

## 5. MVP sem dados reais e sem serviços pagos: sim

Cabe como planilha ou script (Python/CSV) com:
- Tabela fictícia de fármacos (dose mín/máx, concentração, via, frequência) marcada como exemplo não clínico, a ser substituída pelo formulário do hospital validado pelo clínico.
- Pacientes sintéticos (espécie, peso, condição).
- Funções: cálculo mg/kg -> mg -> mL, taxa de fluido, geração de grade de horários, alertas de faixa/duplicidade, diff com o dia anterior, exportação para tabela/PDF.
- Testes automatizados com casos de borda (peso zero, unidade errada, dose acima do máximo).
Limite: o MVP valida a lógica, não o conteúdo clínico; doses reais exigem fonte verificada.

## Decisão resumida

Workflow determinístico com aprovação do veterinário; LLM, se usado, só para rascunho de resumo da evolução, nunca para dose. Pesquisa externa pendente.
