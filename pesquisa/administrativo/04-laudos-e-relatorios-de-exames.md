# Laudos e relatórios de exames (hemograma/bioquímica, US, RX) e resumo ao tutor

Domínio: administrativo. Data: 2026-10-02.

## Recomendação: workflow determinístico + rascunho de texto por LLM (não agente autônomo)

Dividir a tarefa em três partes com risco bem diferente:

1. **Hemograma/bioquímica (valores numéricos)**: workflow determinístico. Comparar cada analito com o intervalo de referência (espécie, idade, laboratório), marcar alto/baixo, calcular o grau do desvio e listar achados. Isso é regra, não IA. Planilha ou script resolve.
2. **Resumo ao tutor**: único ponto em que um LLM agrega valor real (linguagem leiga). Entrada = achados já estruturados e a conclusão já escrita pelo veterinário. O LLM só reescreve, não interpreta. Saída = rascunho que o veterinário revisa.
3. **Imagem (US/RX)**: não automatizar a interpretação com LLM genérico. Se houver IA de imagem, usar produto validado como segunda opinião. O laudo continua sendo do veterinário (ou do radiologista terceirizado). O workflow só confere e anexa o laudo recebido ao prontuário.

Um agente autônomo não se justifica: o fluxo é linear e curto, e a autonomia só aumenta o risco.

## Soluções existentes (pesquisadas)

- **VetAI Diagnostics**: interpretação estruturada de hemograma, bioquímica e urinálise (153 analitos, 424 intervalos de referência, 305 raças) com nível de confiança. Fonte: https://vetaidiagnostics.pro/en (página do fornecedor; não verifiquei validação independente nem disponibilidade no Brasil).
- **IDEXX / Zoetis**: analisadores com IA/comentários interpretativos (ProCyte One, Vetscan OptiCell). Citados em https://www.dvm360.com/view/how-ai-is-shaping-veterinary-hematology e https://www.idexx.com/en/veterinary/analyzers/artificial-intelligence-veterinary-medicine-leads-to-efficiency/ (material do fabricante).
- **SignalPET (RX)**: estudo em Frontiers in Veterinary Science (Edimburgo, 50 estudos, 11 radiologistas certificados): IA com maior especificidade e menor sensibilidade que humanos. Fontes: https://www.signalpet.com/articles/new-research-validates-signalpets-ai-in-radiographic-interpretation/ e comentário/artigo em https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11886591/ (há também comentário crítico: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12238720/). Os dados vêm do site da empresa e do artigo indexado; não li o texto integral.
- **Validação externa independente**: pilot study no JAVMA indica "deficiências na interpretação de radiografias abdominais caninas de clínica geral" por serviços comerciais de IA: https://avmajournals.avma.org/view/journals/javma/aop/javma.25.10.0691/javma.25.10.0691.xml. Só vi o título; o site estava bloqueado, então números e conclusões **não verificado**.
- **Revisões**: IA em medicina veterinária (revisão sistemática) https://pmc.ncbi.nlm.nih.gov/articles/PMC10668547/ ; IA em patologia clínica veterinária https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12852980/ (li apenas os resumos de busca).
- **PIMS**: não verifiquei plug-ins específicos de PIMS brasileiros para esta tarefa: **não verificado**.

## Evidência sobre alucinação de LLM

- LLMs visuais em radiologia humana: acurácia 8,1% a 29,2% e alucinações em 74,4% (180 imagens): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12842777/. É medicina humana, mas desaconselha LLM genérico para ler imagem.
- LLMs repetiram ou elaboraram dados falsos plantados (valores de exame inventados) em até 83% dos casos: https://pmc.ncbi.nlm.nih.gov/articles/PMC12318031/ (medicina humana).
- Não encontrei estudo veterinário específico de LLM em exames laboratoriais: **não verificado**.

## Onde o veterinário valida (human-in-the-loop)

1. Conferir os valores extraídos (OCR/importação) contra o laudo original antes de qualquer cálculo. Erro de extração é a falha mais perigosa.
2. Revisar os flags de referência e escolher/confirmar o intervalo apropriado (espécie, idade, método do laboratório).
3. Escrever ou aprovar a interpretação clínica e a conclusão/diferenciais.
4. Ler e editar o resumo ao tutor antes do envio. Nada vai ao tutor sem clique de aprovação.
5. Assinar o laudo (assinatura e CRMV são do profissional; a ferramenta nunca assina).

## Riscos

- **Clínico**: falso normal (IA de RX com baixa sensibilidade), interpretação sem contexto clínico, tutor receber texto tranquilizador indevido. Mitigar: resumo sem diagnóstico novo e sem prognóstico, com a conclusão do veterinário como única fonte.
- **Alucinação**: valores inventados ou achados não presentes. Mitigar: o LLM recebe só dados estruturados, é proibido de citar valor que não esteja na entrada, e uma checagem determinística confere se todo número do texto existe na entrada.
- **Legal/CFMV**: a Res. CFMV 1.465/2022 (telemedicina) mantém a responsabilidade integral no veterinário, inclusive no telediagnóstico, e exige informar limitações ao responsável: https://www.legisweb.com.br/legislacao/?id=433219 e https://crmvsp.gov.br/resolucao-que-regulamenta-a-telemedicina-veterinaria-e-publicada-entenda-como-funciona/. Código de Ética: Res. CFMV 1.138/2016 (citada nas fontes acima). Não verifiquei norma do CFMV sobre uso de IA especificamente: **não verificado**.
- **LGPD**: dados do tutor (nome, contato) são pessoais. Enviar a API externa só dados anonimizados (espécie, idade, valores), sem nome/CPF/telefone. Verificar contrato e local de processamento. Não consultei o texto da LGPD nesta análise: **não verificado** quanto a pontos específicos.
- **Receituário controlado**: fora do escopo; o resumo não deve sugerir medicamento nem dose.

## Pontuação (1-5)

| Critério | Nota | Observação |
|---|---|---|
| Impacto | 3 | Economiza tempo de redação e comunicação, mas a validação continua sendo do veterinário e o ganho depende do volume de exames. |
| Viabilidade | 4 | Parte laboratorial e resumo são simples. Imagem não é viável sem produto validado. |
| Risco | 3 | Moderado com revisão obrigatória; sobe para 4-5 se alguém automatizar o laudo de imagem ou enviar ao tutor sem revisão. |

## Cabe num MVP sem dados reais e sem serviço pago?

**Sim, parcialmente.** O MVP é um script/planilha em que se cola ou importa valores sintéticos, compara com referências configuráveis (tabela editável, sem dados reais), gera achados estruturados e um modelo de texto para o tutor preenchido por template. O rascunho por LLM é opcional (exige API, normalmente paga) e pode ser substituído por templates determinísticos no MVP. A interpretação de imagem fica fora do MVP.
