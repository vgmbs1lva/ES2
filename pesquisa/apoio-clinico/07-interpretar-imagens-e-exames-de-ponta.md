# 07 - Interpretar imagens e exames de ponta (radiografia, US, ECG, laudos de terceiros, PA)

Dominio: apoio-clinico. Data da analise: 2026-10-02. Estimativa de tempo (~10 min x 10-15 exames/semana, ou 1,7-2,5 h/semana) e do usuario, sem fonte.

## Veredito

**Nao automatizar a leitura de imagem/ECG por IA.** Automatizar apenas o entorno, com a forma mais simples: **script/planilha (checklist deterministico)** para (a) classificar pressao arterial pelo consenso ACVIM e (b) estruturar a revisao de laudos de terceiros (campos, discrepancias, correlacao com a clinica). Opcionalmente, um LLM so sobre o *texto* do laudo (resumo e lista de perguntas ao laudista), nunca sobre pixels/traçados, e sempre com revisao do veterinario.

## 1. Solucoes existentes (com fontes)

| Solucao / evidencia | Achado | Fonte |
|---|---|---|
| Posicionamento ACVR/ECVDI sobre IA (JAVMA, mar/2025) | Exige veterinario no circuito, preferencialmente radiologista; segundo a nota, nenhum produto comercial atende hoje criterios de transparencia, validacao e seguranca; recomenda informar o tutor do uso de IA | https://avmajournals.avma.org/view/journals/javma/263/6/javma.25.01.0027.xml ; https://pubmed.ncbi.nlm.nih.gov/40107235/ ; https://acvr.org/artificial-intelligence-in-veterinary-diagnostic-imaging-and-radiation-oncology/ |
| Estudo piloto de validacao externa (JAVMA, 2025): 6 plataformas comerciais (incl. RapidRead/Antech, SignalRAY/SignalPET, Vetology) em radiografias abdominais caninas de clinica geral | Titulo indica "deficiencias na interpretacao"; so vi o resumo via busca (nao abri o artigo completo, numeros especificos "nao verificado") | https://avmajournals.avma.org/view/journals/javma/aop/javma.25.10.0691/javma.25.10.0691.xml |
| SignalPET (SignalRAY) - estudo em Frontiers in Veterinary Science vs 11 radiologistas, 50 casos | Alta acuracia, forte em confirmar normal; critica metodologica: diagnostico de referencia incluiu o proprio algoritmo (via busca; texto original nao aberto, "parcialmente verificado") | https://www.signalpet.com/articles/breakthrough-study-validates-ai/ (fonte do fornecedor, conflito de interesse) |
| Li et al. 2020, CNN para aumento atrial esquerdo em RX toracico canino (VRU) | Acuracia 82,7%, sens. 68,4%, espec. 87,1% (792 imagens, 1 centro); piloto | https://pmc.ncbi.nlm.nih.gov/articles/PMC7689842/ ; https://onlinelibrary.wiley.com/doi/10.1111/vru.12901 |
| Muller et al. 2022, IA para efusao pleural em caes (VRU) | Acuracia 88,7%, sens. 90,2%, espec. 81,8% (conforme resumo da busca) | https://onlinelibrary.wiley.com/doi/10.1111/vru.13089 |
| IA em ECG | Evidencia robusta e quase toda em humanos; revisao de escopo achou 17 estudos (13 humanos, 3 equinos, 1 canino). Para caes, evidencia escassa | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12477403/ |
| Consenso ACVIM 2018 de hipertensao sistemica (JVIM) | Protocolo: aclimatar 5-10 min, local calmo, mesmo operador, descartar a 1a medida, 5-7 medidas consistentes; classificacao normotenso / pre-hipertenso / hipertenso / hipertenso grave por risco de lesao de orgao-alvo. Isso e regra deterministica, automatizavel | https://pmc.ncbi.nlm.nih.gov/articles/PMC6271319/ |
| Telemedicina veterinaria, Res. CFMV 1465/2022 | Atendimento presencial como padrao ouro; teleconsulta exige RPVAR presencial previa; vedada em urgencia/emergencia. A busca nao retornou texto especifico sobre laudo de imagem: "nao verificado" para laudo a distancia | https://jornal.unesp.br/wp-content/uploads/2022/08/Resolucao_TelemedicinaVeterinaria-1.pdf ; https://www.legisweb.com.br/legislacao/?id=433219 |

Lacunas: nao encontrei IA validada para ECG canino/felino de uso clinico; nao verifiquei produtos disponiveis/registrados no Brasil, nem plug-ins de PIMS brasileiros para isso ("nao verificado"). Tentativa de abrir a materia da VIN foi bloqueada pelo proxy.

## 2. Forma recomendada e justificativa

- **Leitura de imagem/ECG por IA: nao automatizar.** Evidencia publicada e piloto/monocentrica ou do proprio fornecedor; a posicao dos colegios de radiologia e que nenhum produto comercial atende o padrao. O ganho de tempo (~2 h/semana) nao compensa o risco.
- **PA: script/planilha.** Entrada: valores das 5-7 medidas, especie, metodo; saida: media, descarte da 1a, categoria ACVIM, alerta de variabilidade e lembrete de lesao de orgao-alvo. Deterministico, auditavel, sem IA.
- **Revisao de laudo de terceiro: workflow/checklist estruturado** (template: achados-chave, impressao diagnostica, limitacoes tecnicas, discrepancia com exame fisico/labs, perguntas ao laudista, conduta proposta pelo veterinario). Um LLM opcional so resume o texto e levanta perguntas; sem inventar achados.
- Agente autonomo: injustificado; nao ha ciclo de decisao que o veterinario deva delegar.

## 3. Human-in-the-loop, riscos

- **Validacao:** o veterinario le a imagem/traçado original e assina a conclusao e a conduta. A saida da ferramenta e rascunho/organizacao, nunca laudo. Imagem sempre ao lado do texto.
- **Clinico:** falso-negativo de IA em imagem (sens. 68% em LAE no piloto) gera falsa seguranca; vies de ancoragem ao ler apos a sugestao da maquina; classificar PA errada muda conduta (anti-hipertensivo). Para PA, validar o dispositivo/manguito (o consenso pede dispositivos validados na especie).
- **Alucinacao:** LLM pode inventar achado ausente do laudo. Mitigacao: exigir citacao literal do trecho do laudo para cada item; campo "nao consta" quando ausente.
- **Legal:** responsabilidade tecnica e do medico-veterinario (CFMV); laudo de especialista externo continua sendo de quem o assinou; registrar no prontuario a fonte. Informar tutor do uso de IA conforme recomendacao ACVR/ECVDI. Receituario controlado: nao se aplica diretamente; a ferramenta nao deve prescrever.
- **LGPD:** imagens/laudos tem dados pessoais do tutor (nome, contato) e DICOM carrega metadados; anonimizar antes de enviar a qualquer servico externo; evitar enviar a LLM em nuvem sem base legal/contrato (nao verifiquei texto da LGPD nesta analise, "nao verificado").

## 4. Pontuacao (1-5)

- **Impacto: 2.** Tempo liberado pequeno (~2 h/semana, estimativa propria); o valor esta mais em qualidade (padronizar PA e checklist) do que em tempo.
- **Viabilidade: 4** para script de PA e checklist; 1-2 para IA de imagem/ECG confiavel hoje.
- **Risco: 4** se IA lesse imagem/ECG; 2 para a versao recomendada (script + checklist com validacao humana).

## 5. Cabe num MVP sem dados reais e sem pago?

**Sim, para a parte recomendada.** Um script Python/planilha que recebe medidas de PA sinteticas e devolve classificacao ACVIM (limiares a conferir direto no consenso, https://pmc.ncbi.nlm.nih.gov/articles/PMC6271319/), mais um template Markdown de checklist de laudo testado com laudos ficticios. Nao cabe testar IA de imagem/ECG (exigiria dados reais rotulados e/ou servico pago).

Proximos passos: (1) codificar os limiares ACVIM e testar com casos limite; (2) template de checklist; (3) so entao avaliar LLM sobre texto de laudo ficticio.
