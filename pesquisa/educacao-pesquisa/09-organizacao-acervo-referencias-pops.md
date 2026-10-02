# Organização do acervo pessoal e da clínica (referências, protocolos, POPs)

Domínio: educação-pesquisa. Data da análise: 2026-10-02.

## Recomendação

**Script/planilha + workflow determinístico leve, sem agente autônomo.** Zotero (gerenciador) + pasta versionada de POPs com cabeçalho padronizado + planilha de casos anonimizada. A IA entra só como assistente pontual (resumir artigo, sugerir "quais POPs podem ser afetados"), nunca como autora de conteúdo clínico nem como fonte de referências.

## Soluções existentes (pesquisadas)

- Zotero: gerenciador gratuito e open source, com pastas, tags, notas, extração de metadados de PDFs/sites. Há plug-ins e opções de MCP para IA em 2026 (fonte secundária, de blog comercial; qualidade variável): https://paperguide.ai/blog/ai-reference-manager-tools/ e https://citationstyler.com/en/knowledge/ai-plugins-for-zotero/
- Zotero Web API v3 (leitura/escrita da biblioteca por script): https://www.zotero.org/support/dev/web_api/v3/basics
- Crossref REST API (valida DOI e metadados, sem chave para uso básico): https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Plug-in de terceiros para corrigir DOIs no Zotero via Crossref (não avaliei a qualidade): https://github.com/pandaAIGC/zotero-doi-fix
- Exemplo acadêmico de RAG sobre Zotero (KNIME + OpenAI), prova de conceito, não é produto clínico: https://arxiv.org/pdf/2311.04310
- Modelos de POP veterinário e importância de versionamento/revisão periódica (blogs de mercado, não normativos): https://co.vet/post/veterinary-sop-template/ e https://www.dvm360.com/view/how-to-write-a-standard-operating-procedure-sop-
- Base metodológica para atualizar protocolos com evidência (consensos/diretrizes ACVIM): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10658484/
- Plug-ins de PIMS específicos para gestão de POPs/biblioteca: não verificado (não encontrei produto que atenda isso de forma documentada).

## Por que não um agente

- O gargalo real é disciplina de processo (arquivar na hora, ter dono e data de revisão por POP), não falta de inteligência. Isso se resolve com convenção + checklist.
- LLMs fabricam referências. Estudo em revisões sistemáticas: alucinação de 39,6% (GPT-3.5), 28,6% (GPT-4) e 91,4% (Bard): https://pmc.ncbi.nlm.nih.gov/articles/PMC11153973/. Também: https://arxiv.org/html/2604.03173v1 (referências alucinadas em LLMs comerciais e agentes de pesquisa; não li o texto completo). Por isso toda referência deve entrar por DOI/PMID resolvido em base real, nunca gerada pelo modelo.
- Atualizar POP é decisão clínica; automatizar a edição aumenta risco sem ganho proporcional.

## Desenho do workflow

1. Entrada de artigo: salvar via conector do Zotero (ou DOI/PMID). Script opcional consulta Crossref e sinaliza itens sem DOI válido ou metadados divergentes.
2. Tags padronizadas: espécie, sistema/área, tipo de evidência (consenso, RCT, coorte, relato), "afeta POP-XXX".
3. Cada POP em Markdown/planilha com cabeçalho: código, versão, dono, data da última revisão, próxima revisão, referências (chaves do Zotero). Script lista POPs vencidos ou com artigo novo marcado "afeta POP-XXX".
4. (Opcional, IA) Para um artigo marcado, o modelo produz um rascunho de "o que mudaria no POP", citando trecho literal do PDF; o veterinário decide.
5. Planilha de casos para auditoria: colunas controladas, sem identificadores (ver riscos).

## Human-in-the-loop

- Veterinário responsável (RT) aprova toda alteração de POP e assina a nova versão; o rascunho de IA nunca é publicado direto.
- Conferência manual de cada referência (abrir o DOI) antes de citar em POP.
- Auditoria da planilha: revisão por colega ou RT em amostra periódica.

## Riscos

- Clínico: POP desatualizado ou alterado por interpretação errada de estudo (extrapolação de espécie, dose, população). Mitigação: citar trecho literal, nível de evidência, revisão pelo RT. Doses: só de bula/fonte primária, nunca de saída de IA.
- Alucinação: ver acima; mitigada por entrada via DOI/PMID e exigência de trecho citado.
- Legal/CFMV: o prontuário deve ser guardado por no mínimo 5 anos (Res. CFMV 1.321/2020, alterada pela 1.653/2025; resumo em fontes secundárias, confira o texto oficial): https://www.legisweb.com.br/legislacao/?id=480419 e https://www.legisweb.com.br/legislacao/?id=280723. A planilha de auditoria não substitui o prontuário. Resolução 1.690/2026 trata de atendimento domiciliar: https://www.legisweb.com.br/legislacao/?id=489828. Não verifiquei o texto integral de nenhuma.
- LGPD: dados de tutores são pessoais. Princípios de finalidade, adequação e necessidade (art. 6º): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Mitigação: planilha de auditoria com ID de caso sem nome/CPF/telefone/endereço; não enviar prontuários a LLMs externos; se usar IA em nuvem, só texto de artigos e POPs genéricos.
- Receituário controlado: não incluir dados de receitas/notificações (Portaria 344/98) nesse acervo; fora do escopo e sem fonte verificada por mim aqui.
- Direitos autorais: PDFs de artigos podem ter restrição de compartilhamento na equipe; compartilhe referência/DOI, não o arquivo, quando a licença não permitir (não verificado caso a caso).

## Pontuação

- Impacto: 3/5. Economiza tempo recorrente e melhora a rastreabilidade, mas o ganho é moderado.
- Viabilidade: 5/5. Zotero, planilha e script pequeno bastam.
- Risco: 2/5. Baixo se não houver dados de pacientes/tutores e a IA ficar só como rascunho; sobe para 3-4 se o modelo editar POPs ou receber prontuários.

## MVP sem dados reais e sem pagos

Cabe: sim. Conteúdo do MVP: (a) script Python que lê um CSV/JSON exportado do Zotero e valida DOIs no Crossref (gratuito); (b) script que lê o cabeçalho dos POPs fictícios e lista os vencidos/afetados por tag; (c) modelo de planilha de casos com dados sintéticos e checagem de colunas proibidas (nome, CPF, telefone). Camada de IA opcional e fora do MVP.
