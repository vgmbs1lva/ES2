# Orientação de estagiários/residentes e preparo de aula/palestra para tutores

Domínio: educacao-pesquisa. Data da análise: 2026-10-02.

## Recomendação
**Workflow determinístico com LLM assistente (não agente autônomo)**, em dois fluxos separados:
1. **Feedback de relatórios de estagiário**: rubrica fixa + LLM sugere comentários; o orientador edita e assina.
2. **Material educativo para tutores**: o veterinário fornece as fontes (diretrizes, artigos); a ferramenta gera rascunho de slides/roteiro ancorado nelas, com linguagem leiga e checklist de revisão.

Não precisa de agente: as etapas são previsíveis (entrada -> rubrica/fontes -> rascunho -> revisão humana). Para palestra, o caminho mais simples é uma ferramenta pronta ancorada em fontes, sem desenvolver nada.

## Soluções existentes (pesquisadas)
- NotebookLM (Google): responde só a partir das fontes enviadas, com citações, e gera guias de estudo, quiz, slides e flashcards. Serve ao preparo de palestra. https://edu.google.com/ai-notebooklm/ e https://academictech.uchicago.edu/2026/04/06/google-notebooklm-an-ai-tool-for-research-and-studying/ . Preço e política de dados para uso no Brasil: não verificado.
- Estudo de LLMs em provas de graduação em veterinária: modelos de ponta chegaram a cerca de 90% de acerto em 250 questões de múltipla escolha, o que não equivale a competência clínica nem a qualidade de feedback. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12418517/
- Pesquisa com estudantes de veterinária na Austrália: acharam o ChatGPT prático, mas notaram o tom autoritário mesmo com informação incorreta; quem fez análise crítica via melhor sua utilidade. https://pmc.ncbi.nlm.nih.gov/articles/PMC11162838/
- Guia sobre ChatGPT em clínica, ensino e pesquisa veterinária (alerta explícito sobre alucinação). https://arxiv.org/pdf/2403.14654
- Plug-in de PIMS veterinário específico para orientação de estagiários: não encontrado / não verificado.

## Normas
- Estágio supervisionado: a supervisão cabe ao professor orientador e/ou ao veterinário supervisor local, com CRMV ativo (regulamentos institucionais, p. ex. https://vet.ufmg.br/wp-content/uploads/2023/03/Caderno-de-Normas-ESO-Med-Vet-EV_UFMG_21_julho_2022.pdf). A responsabilidade técnica pelo ato é do veterinário, não da ferramenta. Resolução CFMV específica sobre IA em ensino: não verificada. Lei do Estágio (11.788/2008): citada de memória, não verificada nesta pesquisa.
- LGPD: casos usados em aula ou relatório devem ser anonimizados (tutor, animal identificável, clínica). Dados de estagiário (notas, avaliações) também são dados pessoais. Enviar a serviço de IA em nuvem exige cuidado; política do fornecedor: não verificado.

## Human-in-the-loop
- Feedback ao estagiário: o orientador revisa e envia; a IA nunca pontua nem reprova sozinha.
- Material para tutores: o veterinário confere cada afirmação clínica (dose, prazo, conduta) contra a fonte e aprova antes de usar. Evitar doses e condutas individuais em material geral.
- Receituário controlado: o material não deve citar posologia de controlados nem incentivar automedicação.

## Riscos
- Alucinação e referências inventadas: mitigar com fontes fornecidas pelo próprio veterinário, citação obrigatória por trecho e checagem manual.
- Tom autoritário do LLM, que pode induzir o estagiário ao erro (estudo acima).
- Vazamento de dados de pacientes/tutores/estagiários.
- Dependência: o estagiário não desenvolve raciocínio clínico se receber respostas prontas; usar a IA para perguntas socráticas, não respostas.
- Clínico: baixo, pois o produto é educativo, desde que revisado.

## Pontuação (honesta)
- Impacto: 3 (economiza horas em slides e correção, mas ocorre de forma esporádica; frequência não verificada)
- Viabilidade: 5 (ferramentas prontas)
- Risco: 2 (clínico/legal baixo com revisão e anonimização)

## MVP sem dados reais e sem serviço pago
Sim. Um prompt/rubrica em Markdown mais 2-3 relatórios de estágio fictícios e um conjunto de fontes públicas (ex.: diretrizes WSAVA sobre nutrição/obesidade, não verificadas aqui) permitem testar: (a) feedback com rubrica e (b) roteiro de palestra com citações. Medir: fatos sem suporte na fonte, utilidade segundo o orientador, tempo economizado. Camada gratuita do NotebookLM pode servir para o teste; limites atuais: não verificado.
