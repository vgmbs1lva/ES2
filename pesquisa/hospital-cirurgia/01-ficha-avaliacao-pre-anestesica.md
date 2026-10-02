# Ficha de avaliação pré-anestésica (anamnese, exame físico, ASA, exames pré-op)

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Limitação desta pesquisa (leia primeiro)
Nesta execução o orçamento de WebSearch estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy (aaha.org e pubmed.ncbi.nlm.nih.gov). Portanto **não consegui verificar nenhuma fonte**. Tudo abaixo que for factual está marcado "não verificado", exceto a única referência fornecida no enunciado, que também não pude abrir:
- AAHA 2020 Anesthesia and Monitoring Guidelines for Dogs and Cats: https://www.aaha.org/resources/2020-aaha-anesthesia-and-monitoring-guidelines-for-dogs-and-cats/ (citada pelo enunciado como recomendando registrar o estado pré-anestésico; conteúdo exato não verificado por mim).

## 1. Soluções existentes
Nada verificado nesta rodada. Hipóteses a confirmar numa próxima pesquisa (não verificado):
- Módulos de ficha anestésica/pré-anestésica em PIMS (ex.: Simples Vet, Vetus, SoftVet no Brasil; Cornerstone/ezyVet/Digitail no exterior): provavelmente oferecem formulário estruturado, mas não interpretação assistida.
- Estudos sobre concordância interobservador da classificação ASA em veterinária e sobre LLMs classificando ASA: não verificado; buscar no PubMed "ASA physical status veterinary interobserver" e "large language model ASA".
- Escore ASA em si é reconhecidamente subjetivo (conhecimento geral, não verificado aqui), o que pesa contra delegar a classificação a IA.

## 2. Forma recomendada: workflow determinístico (formulário estruturado + regras), sem agente autônomo
Justificativa:
- O núcleo da tarefa é coleta estruturada + checagem de completude + sinalização de valores fora da referência. Isso se resolve com formulário e regras simples (planilha/script), sem LLM.
- A decisão de ASA e de risco é julgamento clínico do anestesista; a IA, no máximo, sugere um rascunho que o veterinário aceita ou troca.
- Camada opcional de LLM apenas para: resumir histórico em texto livre em campos estruturados e redigir o rascunho de "riscos/pendências", sempre rotulado como rascunho.

Componentes do MVP:
1. Formulário (CSV/JSON/planilha) com campos: espécie, idade, peso, escore corporal, histórico, medicações/suplementos, jejum (horas sólido/líquido), alergias/reações anestésicas prévias, FC/FR/TPC/mucosas/temperatura, auscultação, procedimento e urgência, exames.
2. Regras determinísticas: campos obrigatórios ausentes, jejum fora do protocolo da clínica (parâmetro configurável, não inventado), valores laboratoriais fora de faixas de referência do laboratório da própria clínica, exames pendentes conforme idade/condição (regra da clínica).
3. Sugestão de ASA: tabela de critérios editável; saída sempre "sugestão, requer confirmação".
4. Saída: ficha em PDF/Markdown com lacunas destacadas e campo de assinatura do veterinário.

## 3. Human-in-the-loop
- Veterinário responsável confirma/edita: ASA, risco, escolha de exames adicionais, liberação para anestesia e assina. Nada é finalizado sem assinatura.
- Exame físico é feito pelo veterinário; a ferramenta não preenche achados que ele não digitou.

## Riscos
- Clínico: ASA subestimado leva a protocolo inadequado; viés de ancoragem ao aceitar a sugestão. Mitigação: exibir os critérios usados, exigir confirmação ativa, não pré-selecionar ASA.
- Alucinação (se usar LLM): inventar achado, medicação ou valor ausente. Mitigação: extração só de texto fornecido, campo "não informado" explícito, sem completar lacunas, validação de intervalos por código.
- Legal: prontuário é responsabilidade do médico-veterinário (CFMV; normativa específica sobre prontuário: não verificado). Assinatura e rastreabilidade (versão, autor, horário) necessárias.
- LGPD: dados de tutor (nome, CPF, contato) são dados pessoais; não enviar a APIs externas sem base legal/contrato; anonimizar. Detalhes de enquadramento: não verificado.
- Receituário controlado: a ficha pode registrar medicação pré-anestésica, mas a ferramenta não deve prescrever nem gerar receita de controlados (Portaria SVS/MS 344/98; não verificado nesta rodada).

## 4. Pontuação (1-5, sem inflar)
- Impacto: 3. Economia de tempo plausível mas pequena por caso e a estimativa de minutos é própria e não verificada; o ganho real é padronização e menos esquecimentos.
- Viabilidade: 4 para formulário + regras; 2 para interpretação automática confiável de ECG/hemograma por LLM.
- Risco: 3 se limitado a rascunho com validação; subiria para 4-5 se sugerisse ASA/risco sem revisão.
- Incerteza geral: alta.

## 5. Cabe num MVP testável sem dados reais e sem serviços pagos?
Sim, a versão determinística: formulário + regras + gerador de ficha em Python/planilha, testado com casos fictícios (cães/gatos sintéticos) e faixas de referência parametrizáveis. Parte com LLM é opcional e fica fora do MVP para evitar custo e alucinação.

## Próximos passos de verificação
Ler o texto das diretrizes AAHA 2020; buscar estudo de concordância ASA em veterinária; verificar a resolução do CFMV sobre prontuário e orientações da ANPD/LGPD; levantar módulos de PIMS brasileiros.
