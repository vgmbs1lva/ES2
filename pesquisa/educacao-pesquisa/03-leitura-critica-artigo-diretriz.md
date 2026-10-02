# Leitura crítica de artigo / diretriz atualizada

Domínio: educação/pesquisa. Data da análise: 2026-10-02.

## Tarefa
Ler integralmente 1-2 artigos ou diretrizes por semana e registrar o que muda na rotina (analgesia, DRC, antimicrobianos). Entrada: PDFs da triagem (ver 01). Saída: anotação de 3-5 linhas e decisão de alterar ou não o protocolo. Tempo gasto: não verificado (estimativa própria).

## Soluções existentes (fontes pesquisadas)
- Diretrizes de sociedades já prontas e gratuitas, ex.: WSAVA 2022 de dor (Monteiro et al., JSAP 64(4):177-254), com PDF livre. https://onlinelibrary.wiley.com/doi/10.1111/jsap.13566 e https://wsava.org/wp-content/uploads/2023/01/Updated-WSAVA-Global-Pain-Guidelines-Launched.pdf
- Assistentes de pesquisa com IA (Elicit, Consensus, scite): extraem dados de artigos e mostram contexto de citação (scite). Cobertura de literatura veterinária: não verificado. Fontes de apoio são blogs comparativos, de baixa confiabilidade: https://paperguide.ai/blog/elicit-vs-scite/ . Observação: um estudo de avaliação dessas ferramentas aparece como retratado (https://ojs.lib.uwo.ca/index.php/cjils/article/view/23075), mais um motivo para cautela.
- Estudos sobre LLM em avaliação crítica/risco de viés: desempenho variável e não confiável para uso autônomo. ROBIS/AMSTAR 2 com 4 LLMs: https://pmc.ncbi.nlm.nih.gov/articles/PMC12361857/ ; QUADAS-2: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12191753/ ; RoB em ECR (conclusão: nenhum LLM suficientemente confiável para avaliação autônoma): https://pubmed.ncbi.nlm.nih.gov/41905260/ . Todos em medicina humana; em veterinária: não verificado.
- Viés de generalização em resumos por LLM (resumos exageram o alcance dos achados): https://royalsocietypublishing.org/rsos/article/12/4/241776/235656/Generalization-bias-in-large-language-model
- Alucinação de referências: em avaliação de 300 referências geradas por LLMs em neurocuidados críticos, 55,0% tinham inexatidões e 28,3% eram totalmente fabricadas. https://pmc.ncbi.nlm.nih.gov/articles/PMC13506236/
- Plug-ins de PIMS para leitura crítica: nenhum encontrado (não verificado).

## Forma recomendada: workflow determinístico simples (modelo de ficha + checklist), com LLM opcional e restrito
Não recomendo agente autônomo. O gargalo é o julgamento clínico, que é do veterinário, e a evidência mostra que LLMs não são confiáveis para avaliar risco de viés sozinhos. O que automatiza bem é o entorno:
1. Ficha padrão por artigo (planilha ou nota): referência/DOI, desenho do estudo, espécie, n, desfecho principal, limitações, nível de evidência, "muda a rotina? (sim/não/talvez)", protocolo afetado, decisão, data de revisão.
2. Checklist de leitura crítica (ex.: tipo de estudo, população vs. meus pacientes, tamanho de efeito, conflito de interesse, financiamento).
3. Opcional: LLM recebendo o PDF/texto fornecido pelo usuário (sem busca aberta, sem pedir referências) para pré-preencher campos de extração, cada campo com trecho citado literalmente e número de página. O veterinário confere o trecho e preenche a avaliação crítica e a decisão.
4. Registro de decisões de protocolo com data, para rastreabilidade (revisão periódica).

## Human-in-the-loop
- Leitura integral e julgamento crítico: veterinário. O LLM nunca decide mudança de protocolo nem avalia qualidade/viés sozinho.
- Cada campo extraído pelo LLM é conferido contra o trecho citado; campo sem trecho = descartado.
- Doses, intervalos e contraindicações: sempre conferidos no texto original e em bula/formulário antes de qualquer mudança.

## Riscos
- Clínico: o principal é mudar conduta (dose, analgesia, antimicrobiano) com base em resumo errado ou exagerado. Mitigação: não gerar recomendação, exigir trecho citado, decisão humana.
- Alucinação: referências inventadas e resumos que generalizam demais (fontes acima). Mitigação: não usar o LLM para achar ou citar referências; trabalhar só com o documento fornecido; verificar DOI no PubMed.
- Legal/CFMV: a responsabilidade técnica pela conduta é do médico-veterinário; a ferramenta é apoio. Normas específicas do CFMV sobre uso de IA: não verificado.
- LGPD/receituário controlado: baixo, pois não há dados de pacientes ou tutores. Não colar casos reais na ferramenta. Evitar enviar PDFs com restrição de licença a serviços de terceiros (termos de uso, direitos autorais; verificar caso a caso).
- Viés de confirmação: registrar também artigos que não mudam a rotina.

## Pontuação (1-5)
- Impacto: 2. A leitura é a parte de valor e não deve ser automatizada; o ganho está em padronização e rastreabilidade, e em economizar alguns minutos por artigo (não medido).
- Viabilidade: 4. Ficha e checklist são triviais; a extração com LLM é viável mas exige validação manual.
- Risco: 3 se usar LLM (resumo errado influenciando protocolo); 1 se só ficha/checklist.

## MVP sem dados reais e sem serviços pagos
Sim, para a parte determinística: ficha em planilha/Markdown + checklist, testável com 1-2 diretrizes públicas (ex.: WSAVA 2022 de dor, acesso livre) preenchendo a ficha à mão e medindo o tempo. A extração por LLM é um teste opcional que dependeria de acesso a um modelo (pode ter custo; não incluído) e deve ser avaliada comparando campos extraídos com a ficha manual. Nada foi construído nesta análise.
