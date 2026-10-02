# Reunião curta de equipe e revisão de pendências operacionais

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Aviso sobre fontes
Nesta execução o limite de WebSearch (200/200) estava esgotado e o WebFetch foi bloqueado pelo proxy (planalto.gov.br, aclanthology.org). Portanto **nenhuma afirmação factual externa foi verificada**. Onde aparece "não verificado", é para ser checado antes de uso. Não há URLs citadas de propósito, para não inventar.

## 1. Soluções existentes
- Transcritores/atas com IA genéricos (Otter, Fireflies, Microsoft Teams Copilot, Google Meet "Take notes"): existem, mas produto, preço, política de dados e suporte a pt-BR **não verificados**.
- Plug-ins de PIMS veterinário (Simples Vet, SimplesVet, Vetus, etc.) com módulo de ata/tarefas: **não verificado**; provavelmente os PIMS cobrem agenda, estoque e financeiro, não ata de reunião.
- Estudos sobre huddles em equipe veterinária ou sumarização de reuniões por LLM (taxa de erro em itens de ação, alucinação): **não verificado**. Há literatura geral de sumarização de reuniões, mas não a citarei sem fonte.
- Alternativas sem IA: quadro kanban (Trello, Notion, planilha) com colunas Pendência / Responsável / Prazo / Status.

## 2. Forma recomendada: script/planilha (workflow determinístico mínimo)
Justificativa: a reunião é curta, o valor está na disciplina (responsável + prazo + revisão da pendência anterior), não em inteligência. Uma planilha com modelo fixo de pauta e carregamento automático das pendências abertas da semana anterior resolve ~90%. Um agente só se justifica como opcional: transformar anotações livres em linhas da planilha, sempre com revisão humana.

Fluxo proposto:
1. Planilha de pendências (id, descrição, categoria: internados, processo, reclamação, compras, agenda; responsável; prazo; status).
2. Script gera a pauta: itens vencidos e abertos, agrupados por categoria.
3. Durante a reunião alguém anota; opcionalmente um LLM estrutura as notas em linhas (responsável, prazo).
4. Responsável da reunião confere, e a ata (texto curto) é gerada por modelo de texto fixo a partir da planilha.
5. Itens sem responsável ou prazo são sinalizados, não preenchidos pela IA.

## 3. Human-in-the-loop, riscos
- Validação: o médico-veterinário RT/coordenador aprova a ata antes de distribuir. Responsáveis e prazos nunca são atribuídos pela IA.
- Clínico: a parte "casos internados" não deve conter conduta, dose ou prognóstico gerado por IA; apenas lista de pacientes por identificador interno e pendência (ex.: "exame X aguardando"). A decisão clínica permanece no prontuário.
- Alucinação: LLM pode inventar prazo/responsável ou omitir item. Mitigação: extração apenas literal, campos vazios mantidos vazios, conferência humana.
- LGPD (Lei 13.709/2018): nome e dados de tutores, e funcionários citados em reclamações, são dados pessoais; aplicam-se finalidade, necessidade e segurança. Enviar a serviço de IA em nuvem implica transferência/operador: exigir contrato e avaliar transferência internacional. Detalhes de artigos **não verificados** nesta execução. Minimizar: usar iniciais/ID do paciente, sem telefone, CPF ou endereço.
- CFMV: prontuário e responsabilidade técnica seguem normas do CFMV (número da resolução **não verificado**); a ata operacional não substitui o prontuário.
- Receituário controlado: não incluir qualquer dado de substância controlada, receitas ou estoque de controlados na ata/IA; o controle segue a regulação do MAPA/ANVISA (norma exata **não verificada**).
- Gravação de áudio: informar a equipe e obter ciência; guardar o mínimo.

## 4. Pontuação (honesta)
- Impacto: 2/5. Ganho real mas modesto (10 a 20 min/semana de ata e follow-up); o maior benefício é organizacional e já obtido com planilha.
- Viabilidade: 5/5 para planilha/script; 3/5 para a camada LLM em pt-BR com privacidade.
- Risco: 2/5 (baixo, se a ata ficar fora de conduta clínica e dados pessoais forem minimizados); sobe para 3 se usar transcrição de áudio em nuvem.

## 5. MVP sem dados reais e sem serviços pagos
Cabe: sim. Modelo de planilha (CSV) com dados fictícios + script (Python ou Apps Script) que gera pauta das pendências abertas/vencidas e a ata em Markdown, e sinaliza itens sem responsável/prazo. A camada LLM é opcional e pode ser testada com texto fictício.
