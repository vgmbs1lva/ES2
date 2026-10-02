# Busca focada de literatura para a dúvida clínica do dia

Domínio: educação e pesquisa. Data da análise: 2026-10-02.

Nota de método: WebSearch funcionou; WebFetch foi bloqueado pelo proxy de saída (legisweb, PubMed, NCBI, veterinaryevidence.org). Portanto, tudo abaixo vem de resumos de busca, não de leitura integral. Onde não houve fonte, está "não verificado".

## Recomendação: workflow determinístico com assistente de síntese (não um agente autônomo)

Fluxo: pergunta PICO -> consulta booleana -> busca em bases abertas -> lista de resumos recuperados -> síntese curta feita só sobre o que foi recuperado -> o veterinário lê, valida e assina a nota. Cada etapa é fixa; o LLM só entra na formulação da query e no resumo, com citações ancoradas em PMID/DOI recuperados. Não há necessidade de agente com autonomia: o caminho é sempre o mesmo e o risco está justamente na liberdade de "citar de memória".

Formas descartadas: agente livre (risco de referência inventada, sem ganho); só planilha (resolve o arquivamento, não a busca); integração com PIMS (prematuro, depende de fornecedor, dados do paciente); não automatizar (viável, mas a etapa de montar query, triar e formatar nota é repetitiva).

## Soluções existentes (URLs)

- PICO/SPICO como método padrão em MBE veterinária; ferramenta PICO.vet (construtor de pergunta sobre PubMed), com alerta de que perguntas muito específicas dão zero resultado: https://veterinaryevidence.org/index.php/ve/article/view/77 e guias de biblioteca como https://guides.library.illinois.edu/c.php?g=347349&p=2339712 e https://guides.library.oregonstate.edu/c.php?g=1081101&p=7879033
- VetSRev: base pública de revisões sistemáticas de interesse veterinário (CEVM, Univ. de Nottingham), citada em https://guides.library.upenn.edu/vetmedalumniresources/vetmedalumni-eresources e https://veterinaryevidence.org/index.php/ve/links
- Vetlexicon (assinatura, ponto de atendimento) e CAB Abstracts (assinatura): mesmas páginas acima. Preços: não verificado.
- Guia de busca de evidência veterinária para equinos (Equine Vet Educ, 2023): https://beva.onlinelibrary.wiley.com/doi/10.1111/eve.13634
- OpenEvidence (IA com citações, foco humano, limitações descritas): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11787857/ ; pré-print de acurácia e repetibilidade em cenários complexos: https://www.medrxiv.org/content/10.64898/2025.11.29.25341091.full.pdf. Cobertura veterinária: não verificado.
- OpenVet (IA para casos veterinários, com histórico e evidência): https://www.openvet.ai/ . Alegações são do próprio site; sem validação independente encontrada.
- Revisão sobre busca biomédica na era da IA: https://arxiv.org/pdf/2307.09683 ; reescrita de query por PICO em RAG: https://arxiv.org/pdf/2510.23998 (pré-print, não revisado por pares).
- Diretrizes de sociedades (WSAVA, ISCAID, IRIS): uso proposto na tarefa; não pesquisei as URLs individuais, então "não verificado" quanto a licenças de reuso.

## Alucinação de referências

Estudo em neurocrítica: 165 de 300 referências geradas por LLMs (55,0%) tinham alguma imprecisão e 85 (28,3%) eram totalmente fabricadas: https://pmc.ncbi.nlm.nih.gov/articles/PMC13506236/ (resumo via busca). Outros: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12658395/ , https://arxiv.org/pdf/2603.22344. Não achei estudo específico em medicina veterinária: não verificado. Conclusão de projeto: o LLM nunca pode gerar referência; só formata as recuperadas via PMID/DOI.

## Onde o veterinário valida (human-in-the-loop)

1. Aprova a pergunta PICO e a query antes de buscar.
2. Seleciona os artigos (título/resumo) a incluir; o sistema mostra espécie, desenho e n do estudo.
3. Lê os trechos-chave dos artigos escolhidos; a síntese traz marcadores de nível de evidência e de "extrapolação de outra espécie".
4. Edita e assina a nota de prontuário; o rascunho nunca entra no PIMS sozinho.
Decisão de conduta, dose e prescrição permanece exclusivamente do clínico.

## Riscos

- Clínico: evidência escassa e de outra espécie (zero resultados são comuns, ver artigo acima); viés de confirmação; resumo que omite ressalvas; diretriz desatualizada (checar data/versão).
- Alucinação: mitigada por ancoragem em PMID/DOI e verificação do link.
- LGPD/sigilo: enviar a um serviço externo dados do tutor ou identificáveis do caso é risco. Fontes (via busca) tratam dados do tutor como pessoais pela LGPD (Lei 13.709/2018) e apontam sigilo profissional e acesso ao prontuário restrito ao responsável, nas Resoluções CFMV 1.321/2020 e 1.653/2025: https://www.migalhas.com.br/depeso/435877/resolucao-1-653-25-do-cfmv-na-visao-do-prontuario-medico-veterinario e https://www.flyvet.com.br/geo/guia-completo-prontuario-veterinario-brasil-clinicas-cfmv/ (blog comercial, fonte fraca). Texto oficial das resoluções não lido: não verificado; confirmar em https://www.cfmv.gov.br. Regra do projeto: a query envia só espécie, faixa etária, problema, intervenção; nada de nome, CPF, telefone, número de ficha.
- Receituário controlado: o fluxo não gera receita nem dose a prescrever; qualquer menção a controlado exige conferência manual contra a norma vigente (não pesquisada aqui: não verificado).
- Direitos autorais: arquivar PDFs de artigos pagos pode violar licença; guardar referência, link e resumo próprio, e PDF só de acesso aberto ou licenciado.

## Pontuação (honesta)

- Impacto: 3/5. Busca bem feita poupa tempo e melhora a conduta, mas o gargalo é ler e julgar o artigo, que continua humano. Tempo economizado: estimativa própria, não medida. A âncora sobre educação continuada e burnout (Frontiers Vet Sci, 10.3389/fvets.2026.1936424) é indireta e não li o texto integral.
- Viabilidade: 4/5. PubMed, e outras bases abertas, permitem busca por API; limites e termos exatos não verifiquei (NCBI bloqueado). Triagem e síntese por LLM são factíveis; qualidade em literatura veterinária escassa é incerta.
- Risco: 2/5 com validação obrigatória e sem dados identificáveis; sobe para 4 se virar agente que escreve no prontuário ou cita sem checagem.

## MVP sem dados reais e sem serviço pago

Cabe: sim. Escopo: script (Python) com 1) formulário PICO em CSV/YAML; 2) montagem de query e chamada à API pública do PubMed (E-utilities, gratuita, a confirmar); 3) saída em Markdown com PMID, título, ano, espécie, desenho e link; 4) modelo de nota de prontuário com campos vazios para o clínico; 5) validador que rejeita CPF/telefone/nomes por regex na entrada. Teste com perguntas fictícias e casos sintéticos. A etapa de síntese por LLM é opcional e exige chave de API (custo): sem ela, o MVP entrega busca e nota-modelo, o que já é testável. Critério de sucesso: tempo até lista triada e 100% das referências resolvendo para PMID/DOI real.
