# Cursos online, webinars e palestras de educação continuada

Domínio: educação-pesquisa. Data: 2026-10-02.

## 1. Tarefa
Assistir webinars, aulas curtas e podcasts; fazer login, anotações e emitir certificados. Muito ocorre fora do horário (trabalho não remunerado). Entradas: plataformas, convites de fabricantes/sociedades, agenda. Saídas: certificados de horas e anotações aplicáveis à rotina.

## 2. Soluções existentes (pesquisadas)
- Zoom AI Companion / My Notes: resumo, transcrição e itens de ação. Instituições alertam que transcrição e resumo "provavelmente têm imprecisões" e exigem revisão. https://www.zoom.com/en/products/ai-assistant/features/ai-note-taking/ e https://uis.georgetown.edu/zoom/zoom-ai/meeting-record-features/ (o resumo geralmente fica disponível ao anfitrião; em webinar de terceiros, o veterinário não é anfitrião, então não se aplica automaticamente).
- NotebookLM (Google): usa a transcrição do YouTube como fonte e gera resumo, guia de estudo e FAQ com citações ligadas à transcrição; só funciona se o vídeo tiver legenda. https://blog.google/technology/ai/notebooklm-audio-video-sources/ e https://www.kdnuggets.com/how-to-create-youtube-video-study-guides-with-notebooklm
- Exterior (referência de mercado, não BR): Vet Candy, CE gratuito aprovado pelo RACE/AAVSB, https://www.myvetcandy.com/ce-on-demand ; VETgirl, com painel de equipe para acompanhar CE, https://vetgirlontherun.com/ ; AAVSB tem página de rastreio de CE (https://www.aavsb.org/veterinary-continuing-education-tracking/, o acesso foi bloqueado aqui, então detalhes de custo e funções: não verificado).
- Plug-in de PIMS para controle de educação continuada: não encontrei. Não verificado.

## 3. Requisito regulatório
Não encontrei, nas buscas, exigência de horas anuais obrigatórias de educação continuada para médico-veterinário no sistema CFMV/CRMV: não verificado. Os achados são sobre cursos de especialização (Res. CFMV 935/2009, 500 h, segundo resumo de busca) e de auxiliar de veterinário (Res. 1.259/2019, https://abmes.org.br/arquivos/legislacoes/Resolucao-CFMV-1259-2019-02-28.pdf). Título de especialista: https://crmvgo.org.br/titulo-de-especialista-requisitos-exigidos-pelo-cfmv/. Confirmar no CRMV local o que certificados comprovam (concurso, título, currículo). Sem exigência formal, o valor do controle é pessoal e curricular.

## 4. Forma recomendada: script/planilha (mais um workflow leve opcional)
Justificativa: o gargalo real é triagem de convites, agenda e guarda de certificados, que são determinísticos. Assistir é o ato educativo e não se automatiza. Um agente autônomo não agrega: não pode "assistir" por você nem emitir certificado.

Componentes:
1. Planilha/CSV de eventos: data, tema, organizador, patrocinador (sim/não), carga horária, link, status (interesse, inscrito, assistido, certificado recebido), arquivo do certificado, nota de aplicação clínica.
2. Script que lê arquivos .ics/e-mails exportados e faz regras simples (palavras-chave, espécie/área de interesse, horário fora do expediente) para ranquear convites.
3. Opcional, com LLM: resumir transcrição/legenda de um webinar já escolhido em "3 pontos aplicáveis e dúvidas a checar", sempre com citações de trecho (timestamp).
4. Lembrete de certificados pendentes e soma de horas por ano.

## 5. Human-in-the-loop e riscos
- Veterinário decide o que assistir, valida cada anotação antes de levá-la à rotina e confere doses/condutas na bula, diretriz ou artigo original. Nada de conduta clínica nova a partir de resumo de IA.
- Alucinação: resumos podem errar números e doses (aviso de imprecisão em https://uis.georgetown.edu/zoom/zoom-ai/meeting-record-features/). Exigir timestamp/trecho e marcar "não verificado".
- Conflito de interesse: webinars de fabricantes são marketing. A planilha marca patrocinador e o resumo deve separar evidência de promoção. Publicidade de medicamento: verificar normas do MAPA (não verificado aqui).
- Legal: certificados são do profissional; não automatizar emissão nem falsificar presença (login por terceiros violaria termos e ética). Gravar/transcrever sessões de terceiros pode exigir permissão do organizador; verificar termos.
- LGPD: casos clínicos apresentados podem conter dados de tutor/paciente; não colar imagens ou dados de casos em ferramentas externas. Certificado tem CPF/nome: guardar localmente.
- Receituário controlado: não se aplica diretamente; só não registrar doses de controlados como conduta a partir de resumo.

## 6. Pontuação (honesta)
- Impacto: 2/5. Economia de tempo real mas modesta (organização e certificados), o tempo de assistir permanece.
- Viabilidade: 5/5 com planilha e script; 4/5 se incluir resumo via LLM (depende de legenda/transcrição disponível).
- Risco: 2/5 (sem dado clínico se bem feito; risco de aplicar conduta errada vindo de resumo é mitigado pela validação).

## 7. MVP sem dados reais e sem serviço pago
Cabe. Protótipo: CSV sintético com 15 eventos fictícios + script Python que ranqueia por interesse/horário, soma horas e lista certificados pendentes; modelo de nota estruturada (ponto, fonte, verificado S/N). A etapa de resumo por LLM pode ser testada com uma transcrição pública de legenda, sem custo no plano gratuito de ferramentas, mas é opcional.
