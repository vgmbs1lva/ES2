# Discussão de casos (rounds) da equipe

Domínio: educação/pesquisa. Data da análise: 2026-10-02.

## Recomendação: workflow determinístico leve (template + checklist + registro de ações), com LLM só opcional para rascunho

O gargalo dos rounds não é "inteligência", e sim seleção de casos, estrutura da discussão e fechamento do ciclo (ações com responsável e prazo). A literatura aponta exatamente isso. Um agente autônomo não se justifica.

## Evidências e soluções existentes

- M&M em medicina veterinária (mini revisão e aplicação ilustrada): https://pmc.ncbi.nlm.nih.gov/articles/PMC5845710/
- Revisão integrativa de M&M com foco em melhoria de qualidade. Três temas: seleção criteriosa de casos, formato da discussão e planos de ação: https://pmc.ncbi.nlm.nih.gov/articles/PMC7813522/
- Modelo Ottawa M&M (OM3), análise estruturada de erros cognitivos e de sistema: https://www.researchgate.net/publication/260801325_Enhancing_the_Quality_of_Morbidity_and_Mortality_Rounds_The_Ottawa_MM_Model
- Caso de hospital veterinário (Illinois) que adotou M&M rounds em 2021: https://vetmed.illinois.edu/2022/10/10/mm-rounds-promote-culture-of-quality-improvement/
- Ferramenta estruturada de revisão retrospectiva M&M em cuidados intensivos (resumo): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11023106/
- Scribes de IA para PIMS (focam consulta/SOAP, não rounds): ScribbleVet https://www.scribblevet.com/ ; VetRec https://www.dvmcentral.com/vetrec ; Digitail https://digitail.com/blog/the-ultimate-guide-to-the-best-ai-scribes-for-veterinary-clinics/ . Preços citados em comparativos (cerca de US$ 99-150/vet/mês) vêm de blogs de terceiros, não verificados em fonte primária.
- Não encontrei produto veterinário específico para preparo/registro de rounds. Lacuna: "não verificado" se existe.

## Normas (Brasil)

- Resolução CFMV 1.275/2019 (prontuário obrigatório, guarda mínima de 5 anos, sigilo sobre prontuários): https://manual.cfmv.gov.br/arquivos/resolucao/1275.pdf ; comentada: https://www.cfmv.gov.br/wp-content/uploads/2022/05/Resolucao1275_ComentadaFinal.pdf
- Código de Ética (sigilo profissional): https://www.crmv-pr.org.br/uploads/documentos/codeticacfmv.pdf
- LGPD (dados do tutor): texto da lei não consultado nesta pesquisa, "não verificado" aqui. Verificar antes de qualquer envio de dados a serviço externo.
- Receituário controlado: o round só discute condutas, sem emitir receita. Não aplicável ao MVP.

## Desenho do workflow

1. Entrada: planilha de casos pendentes (ID interno anonimizado, espécie, idade, motivo da discussão: complicação / óbito / dúvida diagnóstica / encaminhamento).
2. Triagem determinística: critérios fixos (óbito, retorno não planejado em 7 dias, complicação anestésica/cirúrgica) sugerem pauta; o responsável confirma.
3. Template de preparo (one-pager): linha do tempo, achados, decisão em cada ponto, pergunta ao grupo, classificação tipo OM3 (cognitivo / sistema / sem falha).
4. Registro pós-round: consenso, ações (responsável, prazo, status), ajuste de protocolo proposto.
5. Lembrete semanal das ações vencidas.
6. Opcional: LLM rascunha o one-pager a partir de resumo já desidentificado digitado pelo médico.

## Human-in-the-loop

- O veterinário seleciona os casos, revisa o resumo, e o grupo decide a conduta. A IA nunca registra conclusão clínica sozinha.
- Ajuste de protocolo só vigora após aprovação do responsável técnico.

## Riscos

- Clínico: alucinação em resumo de prontuário (datas, doses, achados trocados); viés de confirmação ao sugerir "causa". Mitigação: resumo sempre conferido com o prontuário; sem sugerir diagnóstico/dose.
- Legal: sigilo do prontuário e LGPD; enviar prontuário a LLM de nuvem sem base legal e contrato é risco. Mitigação: desidentificar, usar só dados mínimos, preferir modelo local.
- Cultural/jurídico: registros de óbitos e erros podem ser usados como prova. Definir política (foco em aprendizado, sem culpabilização; consultar assessoria jurídica; não verificado se há proteção legal equivalente à "peer review privilege" no Brasil).

## Pontuação (honesta)

- Impacto: 3 (ganho moderado de tempo; maior valor é a disciplina do fechamento de ações)
- Viabilidade: 5 (planilha/formulário e template bastam)
- Risco: 2 sem LLM; 3 se usar LLM com dados de prontuário

## MVP

Cabe sim, sem dados reais e sem serviço pago: planilha ou Markdown com template, casos fictícios, script simples que lista ações vencidas e gera a pauta semanal. LLM não é necessário ao MVP.
