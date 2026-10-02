# Checar dose, via e frequência e calcular volume/comprimidos

Domínio: apoio-clínico | Data da pesquisa: 2026-10-02

Nota de método: WebSearch funcionou; WebFetch foi bloqueado pelo proxy (PubMed, CFMV). Os dados abaixo vêm de snippets de busca e estão marcados "não verificado no texto integral" quando cabe. Nenhuma dose é afirmada neste documento.

## Recomendação

**Workflow determinístico (script/calculadora) com dose de referência digitada/curada pelo veterinário. Não usar LLM para calcular nem para fornecer a dose.**

Divisão do problema:
1. Aritmética (mg/kg x peso -> mg -> mL ou fração de comprimido, arredondamento para frações viáveis, volume por tomada, total do tratamento): determinística, testável, sem IA.
2. Conteúdo clínico (faixa de dose, ajuste por espécie, renal/hepático, gestação): vem de formulário licenciado (Plumb's, bula) e continua sendo julgamento do veterinário. Um LLM aqui seria risco de alucinação sem ganho.
3. Opcional, depois do MVP: camada de LLM só para redigir o texto da posologia e para checar a prescrição final contra o cálculo (segunda leitura), sempre sem poder alterar números.

Justificativa: o gargalo (~3 min x 40-60/semana = 2 a 3 h/semana) é majoritariamente conta e digitação; a conta é o ponto onde a literatura mostra erro humano; e o erro de LLM em número é inaceitável quando existe método exato.

## Soluções existentes (URLs)

- Plumb's (monografias, verificador de interações, calculadoras CRI, RCP, BSA, conversão): https://plumbs.com/features/calculator/ , https://plumbs.com/blog/medical-calculators-plumbs-veterinary-medicine/ , https://plumbs.com/features/drug-monographs/ . Licença paga (https://plumbs.com/pricing/). Cobre dose de referência e calculadora genérica; não verificado se integra a PIMS brasileiros.
- Vetsmart (bulário com mais de 4000 itens, doses e prontuário digital com prescrição): https://vetsmart.com.br/ , https://plano.vetsmart.com.br/ . Não verificado: se o cálculo de volume é automático nem a fonte das doses.
- SimplesVet (gestão, prontuário, controle de prescrições): https://simples.vet/ . Não verificado: cálculo de dose automático.
- DVMCalc e calculadoras web: https://dvmcalc.com/ , https://www.vet-ebooks.com/vetdrugslist/drug-dose-calculator/ . Qualidade/curadoria das doses não verificada.
- LLMs: não encontrei estudo específico de dosagem veterinária por LLM. Em medicina humana, resultados variam muito (ex.: dosagem pediátrica com 100% em um estudo https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12602315/ ; acurácia baixa/variável em perguntas reais de informação de medicamentos https://accpjournals.onlinelibrary.wiley.com/doi/10.1002/jac5.70038 ). Em medicina veterinária, ChatGPT ficou abaixo de estudantes em prova (55% vs 86%, não específico de dose): https://arxiv.org/pdf/2403.14654 . Conclusão: evidência heterogênea e não transferível; não basear a decisão em LLM.

## Evidência do problema

- Erros de cálculo de dose por estudantes em laboratório de anestesia: 12 erros em 686 doses (1,8% por cálculo; 10,8% por protocolo); 83% seriam overdoses (snippet): https://pubmed.ncbi.nlm.nih.gov/40587234/ (texto não verificado).
- Hospital-escola: erros de medicação eram 66% dos relatos de incidente; 51% por dose incorreta (snippet): https://pubmed.ncbi.nlm.nih.gov/40015553
- Revisão em anestesia veterinária (cálculo, distração, carga de trabalho como fatores): https://www.vaajournal.org/article/S1467-2987(24)00003-5/fulltext
- Estudo de prescrições em farmácias nos EUA com erros em 66% (verbais) e 88% (escritas) (snippet; fonte primária não verificada): https://www.vettimes.com/clinical/small-animal/drug-dosage-calculation-errors

Implicação: a conta com checagem automática reduz um erro real e mensurável.

## Normas (Brasil)

Verificação parcial (textos integrais inacessíveis); confirmar nas fontes oficiais:
- Resolução CFMV nº 1.318/2020 (prescrição como ato exclusivo do médico-veterinário): citada em https://revista.cfmv.gov.br/prescricao-de-medicamentos-veterinarios-e-um-ato/ . Itens obrigatórios: não verificado.
- Antimicrobianos de uso humano: RDC Anvisa 471/2021, via guia https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf
- Controlados (Portaria SVS/MS 344/98): mesmo guia. Há tratativas da Anvisa sobre normas de prescrição de controlados em 2026: https://www.cfmv.gov.br/cfmv-acompanha-tratativas-da-anvisa-sobre-normas-de-prescricao-de-medicamentos-controlados/comunicacao/noticias/2026/02/14/ (conteúdo e status não verificados; checar se há mudança vigente antes de codificar regras).
- Res. CFMV 1.275/2019 trata de estabelecimentos; não é a norma de prescrição.
- Uso off-label/extrabula e manipulados: não verificado.

## Onde o veterinário valida (human-in-the-loop)

1. Seleciona o fármaco e confirma a dose de referência (faixa mg/kg, via, intervalo) olhando a fonte; a ferramenta mostra a fonte e a data da entrada.
2. Confere o peso e o ajuste clínico (espécie, renal/hepático, gestação, interações): a ferramenta só alerta por regras que ele mesmo cadastrou; ausência de alerta não significa segurança.
3. Revisa e assina a prescrição final; para controlados/antimicrobianos, emissão no receituário/sistema exigido continua manual.
4. Cálculo exibido com a conta passo a passo (mg/kg x kg = mg; mg / concentração = mL) para conferência em 10 segundos.

## Riscos

- Clínicos: erro de peso/unidade (mg vs mcg, mg/mL vs %), concentração do produto errada (várias apresentações), fração de comprimido impraticável, espécies sensíveis (gatos, não verificado por fármaco), automation bias. Mitigação: validação de faixa, bloqueio de dose acima do máximo cadastrado, arredondamento explícito, testes unitários com casos-limite.
- Alucinação: eliminada no núcleo ao não usar LLM; se houver LLM, só texto, com números injetados pelo código e verificação automática de igualdade.
- Legais: responsabilidade é do veterinário (Res. 1.318/2020); a ferramenta é apoio. Regras de controlados/antimicrobianos mudam; versionar regras e conferir fonte vigente.
- Licença: copiar dados de Plumb's/bulários para base própria pode violar direitos autorais; a base deve ser preenchida pelo próprio veterinário ou de fontes de uso livre. Não verificado: termos de uso de cada fonte.
- LGPD: nome de tutor e dados identificáveis não são necessários para o cálculo; usar só peso/espécie/ID local. Se virar produto com prontuário, aplicar LGPD (não verificado em detalhe).

## Pontuação (1-5)

- Impacto: 3 (2-3 h/semana, mais redução de erro; ganho modesto de tempo, relevante em segurança).
- Viabilidade: 5 (aritmética simples; o difícil é curar a base de doses, que não é automatizável com segurança).
- Risco: 3 (erro de dose pode causar dano; mitigado por cálculo determinístico e validação humana; sobe a 4-5 se usar LLM para dose).

## MVP sem dados reais e sem serviços pagos

Cabe: sim, parcialmente.
- Planilha ou script (Python/JS local) com: entrada de peso, espécie, fármaco; tabela de fármacos preenchida pelo usuário (dose mín/máx mg/kg, intervalo, via, concentrações/comprimidos disponíveis, flag "controlado"/"antimicrobiano", notas de ajuste); saída: mg, mL por tomada, comprimidos em frações de 1/4, total para a duração, alertas (fora de faixa, fração impraticável, espécie com observação).
- Testar com fármacos fictícios e pacientes sintéticos, sem tutor. Não incluir doses reais no repositório sem fonte citada.
- Fora do MVP: base real de doses (licença), integração com PIMS, emissão de receituário controlado.
