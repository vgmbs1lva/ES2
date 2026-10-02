# 09 - Consultar e adaptar protocolos clínicos (anestesia, dor, vacinação, parasitas, doenças crônicas)

Data: 2026-10-02. Tempo atual: ~1,5 h/sem consultando + ~1 h/sem mantendo POPs.

## Recomendação: workflow determinístico (checklist/planilha + RAG restrito opcional), não agente autônomo

Dividir a tarefa em duas:

1. **Manutenção de POPs (1 h/sem)**: workflow simples. Biblioteca de POPs em Markdown/planilha, cada POP com campos fixos (diretriz de origem, URL, versão/ano, data da última revisão, responsável). Um script/rotina mensal lista POPs com revisão vencida e diretrizes-fonte com versão nova. Isso é script/planilha; não precisa de IA.
2. **Consulta/adaptação ao paciente (1,5 h/sem)**: LLM com recuperação (RAG) limitada a um corpus fechado (PDFs das diretrizes e POPs da clínica), sempre citando trecho e página. Saída é rascunho de "protocolo individualizado" com os campos de risco do paciente preenchidos pelo veterinário. Sem busca aberta na web e sem calcular dose de forma autônoma.

Justificativa: o dano clínico vem de dose/indicação errada ou diretriz desatualizada. Um corpus fechado e versionado, com citação obrigatória, reduz alucinação; um agente autônomo adicionaria risco sem ganho proporcional. A economia realista é de 30-50% das 2,5 h/sem (estimativa minha, não verificada).

## Soluções existentes (pesquisadas)

- Plumb's (bula/doses, interações) e Standards (algoritmos e guias de tratamento): https://plumbs.com/ , https://plumbs.com/explore-standards/ , https://plumbs.com/features/. Pago; é referência curada, não gera POP próprio. Preços: https://plumbs.com/pricing/ (não detalhado aqui).
- Diretrizes-fonte, todas gratuitas:
  - WSAVA vacinação 2024 (FeLV passa a core; leptospirose core onde endêmica; há versão em português e guia regional para América Latina): https://wsava.org/global-guidelines/vaccination-guidelines/ ; PDF https://wsava.org/wp-content/uploads/2024/05/2024-Guidelines-for-the-Vaccination-of-Dogs-and-Cats.pdf ; resumo AVMA https://www.avma.org/news/wsava-updates-global-guidelines-vaccination
  - AAHA anestesia e monitoramento 2020: https://www.aaha.org/resources/2020-aaha-anesthesia-and-monitoring-guidelines-for-dogs-and-cats/ ; PubMed https://pubmed.ncbi.nlm.nih.gov/32078360/
  - WSAVA dor 2022 (J Small Anim Pract): https://onlinelibrary.wiley.com/doi/10.1111/jsap.13566
  - Parasitas (ESCCAP/CAPC) e doenças crônicas (ISCAID, IRIS etc.): URLs não verificadas aqui.
- Literatura sobre LLM em medicina veterinária:
  - Guia sobre ChatGPT em veterinária (Frontiers Vet Sci 2024): https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2024.1395934/pdf . Os resultados de busca citam referências inventadas (erro de ~18% no GPT-4 vs ~55% no GPT-3.5); essa cifra veio de resumo de busca, não a confirmei no texto.
  - Revisão sobre IA em veterinária e letramento: https://pmc.ncbi.nlm.nih.gov/articles/PMC12870133/
  - Estudo de RAG sobre diretrizes hepatológicas (humana), mostra que RAG melhora aderência à diretriz: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11039454/
  - AVA, sistema de apoio à decisão veterinário (preprint/ResearchGate, não revisado): https://www.researchgate.net/publication/404762596_AVA_AI_Veterinary_Assistance_-An_NLP_and_Semantic_Vector-Based_Clinical_Decision_Support_System_for_Animal_Healthcare
- Plug-ins de PIMS com IA para este uso específico (protocolos): não verificado. Encontrei apenas a categoria geral de ferramentas; não afirmo que existam.

## Human-in-the-loop

- O veterinário valida todo protocolo individualizado antes de uso: confere a citação (página/trecho) contra o PDF original, as doses contra Plumb's/bula e o estado do paciente.
- Revisão de POP: a IA só propõe diff com a fonte; o responsável técnico aprova e assina a nova versão.
- Doses e cálculos: feitos por tabela/calculadora determinística revisada, não pelo LLM.

## Riscos

- Clínico: dose errada, diretriz desatualizada (WSAVA/AAHA mudam; hoje é 2026-10, checar versões mais novas que 2024/2020), generalização de diretriz norte-americana ou global para o contexto brasileiro (doenças endêmicas, produtos registrados no MAPA, disponibilidade de fármacos). Vacinas e antiparasitários devem ser conferidos com registro MAPA.
- Alucinação: referências e doses inventadas. Mitigação: corpus fechado, citação obrigatória, recusa quando não houver trecho.
- Legal CFMV: a responsabilidade técnica e a prescrição são do veterinário; a IA é apoio. Documentação eletrônica deve garantir segurança, autenticidade e integridade (Resolução CFMV 1321/2020: https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf). Prontuário só é compartilhado com tutor/autorizado.
- Receituário controlado: não deixar a IA redigir ou preencher receitas de controle especial (Portaria SVS/MS 344/98; fonte não pesquisada aqui, "não verificado").
- LGPD (Lei 13.709/2018): dados do tutor são pessoais; não enviar a APIs externas sem base legal e contrato. Para o MVP, usar apenas casos fictícios. Detalhes de aplicação da LGPD a clínicas veterinárias: não verificado.
- Direitos autorais: PDFs de diretrizes têm licença própria; usar em corpus local para uso interno e verificar termos. Não verificado.

## Pontuação (honesta)

- Impacto: 3. Só 2,5 h/sem em jogo e o ganho real é parcial; valor maior está em padronização e redução de POPs desatualizados.
- Viabilidade: 4. Planilha/script de revisão é trivial; RAG sobre PDFs abertos é viável com ferramentas atuais.
- Risco: 3 (clínico/legal moderado, controlado por corpus fechado e validação obrigatória; sobe para 4-5 se virar agente que decide dose).

## MVP sem dados reais e sem serviços pagos?

Sim, na parte determinística. Proposta: (a) 3 POPs fictícios em Markdown com metadados; (b) script Python que lista POPs vencidos e gera checklist de revisão; (c) template de "protocolo individualizado" com campos de espécie, peso, idade, comorbidades, risco; (d) opcional: RAG local sobre PDFs públicos (WSAVA vacinação, AAHA anestesia) com modelo local/gratuito, avaliado em ~20 perguntas com gabarito conferido manualmente. A parte de LLM exige modelo (local ou API); com API paga fica fora do critério, e com modelo local a qualidade precisa ser medida. Não é possível validar utilidade clínica real sem uso em clínica.
