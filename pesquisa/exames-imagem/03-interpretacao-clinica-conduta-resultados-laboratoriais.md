# Interpretação clínica e conduta sobre resultados laboratoriais

Domínio: exames-imagem | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch (200/200) estava esgotado e o WebFetch foi bloqueado pelo proxy (iris-kidney.com, planalto.gov.br). **Nenhuma afirmação factual externa foi verificada com URL.** Tudo sobre produtos, estudos, normas e doses está "não verificado" e precisa ser pesquisado antes de uso. O restante é raciocínio de engenharia.

## 1. Soluções existentes (todas não verificadas)
- Relatórios interpretativos de laboratórios de referência e de fabricantes de analisadores (comentário de patologista, painéis com flags): não verificado. Pesquisar IDEXX, Antech, Zoetis e laboratórios brasileiros.
- Módulos de apoio à decisão em PIMS e prontuários eletrônicos veterinários: não verificado.
- Estudos de LLMs interpretando hemograma/bioquímica veterinária: não verificado; buscar em PubMed/Google Scholar (ex.: "large language model veterinary clinical pathology").
- Diretrizes de referência para regras: estadiamento IRIS (DRC), consensos ACVIM, WSAVA: não verificado (URLs não acessadas).
- Normas: CFMV (prontuário, responsabilidade técnica, telemedicina), LGPD (dado pessoal do tutor; art. 20 sobre decisões automatizadas), receituário controlado (Portaria SVS/MS 344/98 e normas MAPA): não verificado.

## 2. Forma recomendada: workflow determinístico de apoio, com LLM opcional apenas para redigir rascunho de registro
Justificativa: a parte "correlacionar e decidir conduta" é julgamento clínico, que não deve ser automatizado. O que dá para automatizar com segurança é:
1. Reunir contexto (resultado atual, histórico de resultados anteriores, anamnese) em uma única tela.
2. Aplicar regras explícitas e citadas, escolhidas pelo clínico (ex.: faixas de estadiamento, delta vs. exame anterior, padrões como "ureia e creatinina altas + densidade urinária baixa").
3. Montar rascunho de registro no prontuário (estrutura SOAP) com campos de conduta em branco ou como "sugestões a confirmar".
Agente autônomo não se justifica: o custo de erro é alto e a rastreabilidade das regras é mais importante que flexibilidade. Se for usado LLM, só para redigir texto a partir de dados estruturados já conferidos, sem criar números, sem sugerir doses e com o rascunho sempre marcado "não validado".
Escolha final: **workflow**.

## 3. Human-in-the-loop e riscos
- O veterinário decide e assina a conduta. O sistema não solicita exame, não ajusta terapia nem grava no prontuário sem clique de confirmação.
- Pontos de validação: (a) antes de aceitar o contexto reunido; (b) antes de aceitar qualquer sugestão de regra; (c) antes de gravar o registro.
- Risco clínico: viés de ancoragem (sugestão do sistema influencia o clínico), regra desatualizada, resultado pré-analítico errado (hemólise, lipemia, espécie/idade fora da referência). Mitigação: exibir a regra e sua fonte, mostrar valores originais, sinalizar limitações, versionar regras.
- Alucinação: um LLM pode inventar diagnóstico diferencial, valor de referência ou dose. Mitigação: sem LLM no núcleo; se houver, saída restrita a texto sobre campos fornecidos e checagem automática de que todo número do rascunho existe na entrada.
- Legal: responsabilidade técnica permanece com o médico-veterinário (CFMV, resolução específica: não verificado). Registro no prontuário deve identificar autoria humana e que houve apoio automatizado.
- LGPD: dados de tutor e paciente ligados a ele são pessoais; processar localmente, minimizar, evitar API externa sem base legal e contrato (artigos: não verificado).
- Receituário controlado: o sistema não gera nem sugere prescrição de controlados; qualquer ajuste terapêutico fica fora do escopo automatizado.

## 4. Pontuação
- Impacto: 3 (economiza tempo de organização e redação do registro; o ganho clínico real é modesto, pois a decisão continua humana)
- Viabilidade: 4 para o workflow de regras e rascunho; 2 para interpretação autônoma confiável
- Risco: 4 se evoluir para sugerir conduta ou tratamento sem controle; 2 se limitado a reunir dados, aplicar regras citadas e rascunhar

## 5. MVP sem dados reais e sem serviços pagos
Sim, em escopo reduzido. Python local com casos **sintéticos** (pacientes, tutores e valores fictícios): (a) carregar resultado atual e anteriores; (b) regras em YAML escritas pelo clínico (ex.: delta percentual de creatinina, faixas de hematócrito) com campo "fonte" obrigatório, preenchido como "a verificar" no protótipo; (c) gerar painel de tendência e rascunho SOAP em texto com conduta vazia; (d) testes: histórico ausente, unidade divergente, resultado sem referência para a espécie, rascunho sem número inventado. Sem LLM no MVP; o piloto com LLM, se desejado, vem depois e usa apenas modelo local ou contrato adequado de privacidade.
