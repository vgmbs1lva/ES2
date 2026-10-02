# Alta: receita, instruções pós-operatórias e resumo de alta

Data: 2026-10-02. Domínio: hospital-cirurgia.

## Limitação da pesquisa (leia primeiro)
Nesta execução o WebSearch estava sem orçamento (200/200) e o WebFetch foi bloqueado pelo proxy (gov.br e pubmed). Portanto **nenhuma afirmação factual externa foi verificada**. Tudo abaixo sobre produtos, estudos e normas é "não verificado" e precisa ser conferido antes de decidir qualquer coisa.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com geração de alta por IA: não verificado (sem URL). Pistas a pesquisar depois: módulos de "discharge instructions"/scribe em PIMS veterinários (ex.: ezyVet, Cornerstone, Provet Cloud, Simples Vet, Vetsmart). Não confirmei que tenham o recurso.
- Estudos sobre LLM em resumo de alta/hallucination (medicina humana, em geral): não verificado (sem URL).
- Normas: receita de controlados em veterinária (Portaria SVS/MS 344/98 e RDCs ANVISA; resoluções CFMV sobre receituário): não verificado, conferir texto vigente em gov.br/anvisa e cfmv.gov.br. A própria descrição da tarefa já marca isso como "não verificado".

## 2. Forma recomendada: workflow determinístico com redação assistida (não agente autônomo)
Justificativa: a alta é um documento com estrutura fixa, e a maior parte do conteúdo já existe na prescrição de alta e no prontuário. O trabalho é montar e formatar, não decidir.
- Núcleo determinístico: template (resumo, receita, orientação ao tutor) preenchido por campos estruturados do prontuário (identificação, procedimento, medicamentos, dose, via, frequência, duração, data de retorno). Doses e medicamentos vêm só da prescrição validada pelo veterinário, nunca gerados pelo modelo.
- Camada opcional de LLM: apenas (a) reescrever a orientação ao tutor em linguagem leiga a partir de blocos já aprovados (curativo, colar elisabetano, dieta, sinais de alerta por tipo de cirurgia) e (b) resumir a evolução em texto corrido. Biblioteca de blocos revisados por cirurgião reduz alucinação.
- Checagens por regra (script): todo item da receita bate com a prescrição; medicamento controlado sinaliza e bloqueia a emissão comum, exigindo o documento próprio; campos obrigatórios preenchidos; retorno agendado; alergias/interações listadas.
- Por que não agente: não há decisão aberta, ferramentas ou planejamento que justifiquem; aumenta risco sem ganho.

## 3. Human-in-the-loop e riscos
Validação obrigatória:
1. Veterinário responsável revisa e assina resumo e receita (o ato prescritivo e a assinatura são dele). Nada sai ao tutor sem aprovação explícita.
2. Diff visível: receita gerada vs. prescrição de alta, destacando dose, frequência e duração.
3. Controlados: emissão do documento oficial (notificação) fica fora da automação ou em etapa manual; a ferramenta só avisa. Regras de numeração, talonário/sistema e retenção: não verificado.
4. Tutor recebe versão final; primeira vez, entrega explicada pela equipe (enfermagem/veterinário).

Riscos:
- Clínico: erro de dose/duração, omissão de interação, instrução de curativo inadequada ao procedimento, esquecer sinais de alerta específicos. Alucinação do LLM em dose é o pior caso, mitigado por não deixar o modelo escrever doses.
- Legal: responsabilidade do RT/prescritor (CFMV, não verificado quanto aos artigos), receituário controlado (ANVISA/MAPA, não verificado), prontuário e guarda de documentos.
- LGPD: dados do tutor (nome, contato, endereço) são pessoais; usar LLM externo exige base legal, minimização e contrato de operador. Recomendação: pseudonimizar, ou modelo local, no MVP usar só dados sintéticos. Vínculo exato com LGPD no contexto veterinário: não verificado.
- Automação complacente: revisor passa a aprovar sem ler. Mitigar com diff e campos que exigem confirmação.

## 4. Pontuação (1-5, estimativa própria, sem benchmark)
- Impacto: 4. Alta é repetitiva, ocorre diariamente e consome tempo de cirurgião/enfermagem; ganho real, mas limitado ao tempo de redação (não mede-se aqui; sem dado).
- Viabilidade: 4. Template mais regras é simples; a integração com o PIMS real é o gargalo (depende do sistema; não verificado).
- Risco: 3 com validação humana e doses fora do LLM; seria 4-5 se o modelo gerasse prescrição.

## 5. MVP sem dados reais e sem serviço pago
Sim, cabe. Escopo sugerido:
- Script (Python/planilha) que lê um JSON/CSV sintético de caso (ex.: OSH canina, orquiectomia felina) e gera resumo, receita e orientação em Markdown/PDF a partir de templates e uma biblioteca de blocos de orientação.
- Validador: confere campos obrigatórios, compara receita com prescrição, sinaliza controlados.
- Sem LLM no MVP; a redação em linguagem leiga pode vir de blocos pré-escritos. LLM opcional depois, com dados sintéticos.
- Teste: casos sintéticos com erros plantados (dose divergente, campo faltando, controlado) para medir se o validador pega.
Não cabe no MVP: integração com PIMS real, emissão oficial de notificação de controlados, validação jurídica.

## Pendências de verificação
Normas ANVISA/CFMV vigentes de receituário veterinário; produtos de PIMS existentes; evidência publicada de LLM em resumos de alta; enquadramento LGPD.
