# Triagem diária de alertas e newsletters científicas

Domínio: educação/pesquisa. Data da análise: 2026-10-02.

## Tarefa
Varrer e-mails de periódicos (JAVMA, JSAP, JVIM), alertas do PubMed e boletins de associações; descartar o irrelevante e salvar 1-3 artigos por semana. Tempo gasto: estimativa própria, não verificado.

## Soluções existentes (fontes verificadas via busca)
- PubMed: busca salva com alerta por e-mail (My NCBI, frequência e formato configuráveis) e feed RSS por busca, até 100 itens. https://www.nlm.nih.gov/pubs/techbull/ja20/ja20_pubmed_updated.html e https://guides.lib.unc.edu/search-pubmed/save-search
- Zotero: assinatura de feeds RSS por URL (inclui RSS do PubMed); leitura e triagem dentro do app. https://www.zotero.org/support/feeds . Observação de fórum: "saved searches" do My NCBI não funcionam como feed; usar o RSS gerado na busca (https://forums.zotero.org/discussion/81840/saved-search-does-not-support-rss-feeds).
- AVMA/JAVMA: alertas eTOC e "Online Early" para assinantes; boletim "Veterinary Advances" (mensal, só membros). https://www.avma.org/news/avma-newsletters-and-alerts . Disponibilidade de RSS do JAVMA: não verificado.
- JSAP, JVIM, ANCLIVEPA, WSAVA: opções de alerta/RSS não verificadas nesta análise (não verificado).
- Estudos sobre LLM para triagem de literatura veterinária: não verificado.

## Forma recomendada: script/planilha (workflow determinístico simples)
Não precisa de agente. Fluxo: (1) 3-5 buscas salvas no PubMed por tema de interesse (ex.: filtro por revista e termos MeSH) com RSS; (2) feeds RSS dos periódicos que oferecerem; (3) leitor de feeds (Zotero ou similar) ou script que junta os feeds, remove duplicados por DOI/PMID e filtra por palavras-chave; (4) uma planilha/pasta com colunas título, revista, DOI, tema, status (ler/descartar). Resumo por LLM é opcional e secundário: só como auxílio de leitura do abstract, nunca como fonte.

Os boletins por e-mail ficam como complemento (filtro/rótulo no cliente de e-mail), pois são o item mais difícil de automatizar de forma confiável.

## Human-in-the-loop
- O veterinário decide o que ler e o que mudar na conduta clínica; a lista curta é só sugestão.
- Qualquer resumo de LLM deve ser conferido contra o abstract/texto original; citar sempre DOI.

## Riscos
- Clínico: alto só se alguém mudar conduta com base em resumo automático sem ler o artigo. Mitigação: o sistema não gera recomendação clínica.
- Alucinação: só se usar LLM; evitável usando apenas metadados e abstracts originais.
- Legal/LGPD/CFMV/receituário: baixo; não envolve dados de pacientes ou tutores. Atenção a direitos autorais e termos de uso ao baixar e organizar PDFs (uso pessoal; não redistribuir).
- Viés: filtros por palavra-chave podem esconder artigos relevantes; revisar os filtros periodicamente.

## Pontuação (1-5)
- Impacto: 2 (economia de tempo modesta; ganho em consistência de atualização; tempo real não verificado)
- Viabilidade: 5 (ferramentas gratuitas já existentes)
- Risco: 1 (sem dados sensíveis; sobe a 2 se usar LLM)

## MVP sem dados reais e sem serviços pagos
Sim. Um script Python com feedparser lendo 1-2 RSS do PubMed, deduplicando por PMID/DOI, filtrando por palavras-chave e gerando CSV de candidatos. Sem dados de pacientes e sem serviço pago. Não construído nesta análise.
