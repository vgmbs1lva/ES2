# Interpretar hemograma, bioquímico e urinálise

Domínio: apoio-clínico | Data da análise: 2026-10-02

Volume: ~8 min x 25-35 exames/semana = ~3,3 a 4,7 h/semana na clínica toda (estimativa própria, não verificada em levantamento). Só a parte mecânica (sinalizar fora do intervalo, montar tendência, redigir rascunho) seria automatizável; ela é uma fração desses 8 min, então o ganho real tende a ser menor que o total.

## Recomendação: workflow determinístico (script/planilha) para a parte mecânica + LLM opcional só para redigir rascunho. Não começar com agente autônomo.

Justificativa:
- A parte de maior valor e menor risco é determinística: comparar valor com intervalo de referência da espécie/idade/analisador, calcular delta contra exame anterior, destacar o que mudou. Isso não precisa de LLM e é auditável.
- A parte interpretativa (relacionar com quadro clínico, decidir SDMA/cortisol/T4) é julgamento clínico; um LLM pode sugerir, mas tem risco de alucinação. Deve ser rascunho para o vet, nunca registro automático.
- Intervalos de referência dependem de espécie, idade e analisador/método; a diretriz ASVCP reforça RIs específicos por espécie e analisador (https://onlinelibrary.wiley.com/doi/10.1111/vcp.12006). Portanto a tabela de RIs deve vir do laudo/laboratório do próprio usuário, não de um LLM "de memória".

Forma: workflow (script) em 3 etapas: (1) entrada estruturada do laudo (CSV/JSON/planilha, sem identificação do tutor); (2) regras: flag alto/baixo, delta %, tendência; regras explícitas de "considerar" (ex.: creatinina/ureia altas -> sugerir lembrar SDMA, urinálise com densidade) escritas pelo vet e versionadas; (3) rascunho de nota para o prontuário. LLM só na etapa 3 e opcional.

## Soluções existentes (pesquisadas)

| Solução | O que faz | Fonte |
|---|---|---|
| IDEXX VetConnect PLUS | Unifica resultados in-house e de referência, gráficos de analitos e tendências; gratuito a clientes IDEXX | https://www.idexx.com/en/veterinary/software-services/vetconnect-plus/ |
| IDEXX DecisionIQ | ML sobre dados do paciente (espécie, idade, sinais, exames) com interpretação e "próximos passos"; versão para DRC alinhada às diretrizes IRIS | https://www.idexx.com/en/veterinary/software-services/vetconnect-plus/decision-iq/ |
| IDEXX SDMA (guia de interpretação) | Orienta interpretação de SDMA; recomenda tendência de SDMA, ureia, creatinina e fósforo | https://www.idexx.com/en/veterinary/reference-laboratories/sdma/interpreting-your-sdma-results/ |
| Zoetis Vetscan/Imagyst, OptiCell | Analisadores com IA (hemograma, sedimento urinário, massas) | https://www.marketsandmarkets.com/ResearchInsight/us-veterinary-diagnostics-companies.asp (fonte secundária de mercado) |
| Integração PIMS (ex.: Vetspire) com IDEXX/Antech/Zoetis/SignalPET | Resultados dentro do prontuário | https://www.signalpet.com/articles/5-best-veterinary-diagnostic-software/ (fonte de fornecedor concorrente; tratar como indicativa) |

Observações:
- Disponibilidade no Brasil de DecisionIQ e das integrações acima: não verificado. A pesquisa retornou páginas dos EUA.
- Se a clínica já usa laboratório/analisador com portal próprio que traz tendência e flags, a melhor opção pode ser usar o que já existe e não construir nada.

## Evidência sobre LLMs

- Estudos veterinários localizados avaliam LLMs em diagnóstico com dados multimodais (ex.: doenças esplênicas em cães e gatos, ChatGPT-5 76,3% vs. especialistas 89,5-92,1% de acerto específico, segundo o resumo recuperado na busca): https://pubmed.ncbi.nlm.nih.gov/42431356/ . Não li o artigo completo; os números vêm do resumo da busca. Isso mostra desempenho inferior ao de especialistas, mesmo bom.
- Não encontrei estudo veterinário específico validando LLM para interpretação de hemograma/bioquímico/urinálise de rotina: não verificado. Estudo em medicina humana sobre impacto de exames laboratoriais em diagnósticos diferenciais de LLM: https://www.nature.com/articles/s41746-025-01556-8 (não lido em profundidade).

## Human-in-the-loop

- O veterinário valida 100% das saídas antes de entrarem no prontuário; o sistema grava como "rascunho" e só o vet confirma/edita.
- Pontos de validação: (a) conferência dos valores transcritos contra o laudo original; (b) revisão da lista de alterações; (c) decisão de repetir exame ou pedir SDMA/cortisol/T4 é sempre do vet; (d) assinatura da nota.
- O sistema não prescreve, não calcula dose e não toca em receituário controlado.

## Riscos

Clínicos:
- Alucinação/invenção de valores ou intervalos (mitigar: RIs vêm de tabela fornecida pelo laboratório; LLM não recebe a tarefa de "lembrar" RIs; saída deve citar o valor e o intervalo usados).
- Viés de automação: o vet aceitar o rascunho sem ler. Mitigar mostrando primeiro os valores brutos e as flags, depois o texto.
- Intervalo errado por espécie/idade/analisador (ver ASVCP acima) e erros de unidade (mg/dL vs. µmol/L).
- Falso conforto ao não sinalizar alterações dentro do RI mas relevantes na tendência (por isso a tendência é calculada por regra).

Legais/regulatórios:
- CFMV: o prontuário é documento privativo do médico-veterinário, que o assina e é responsável pelo conteúdo (Res. CFMV 1321/2020, https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf ; alterada pela Res. 1.653/2025 segundo https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/). Texto gerado por máquina deve ser revisado e assumido pelo vet. Posição específica do CFMV sobre IA em prontuário: não verificado.
- LGPD (Lei 13.709/2018): dados do tutor são pessoais (art. 5º, I). Enviar laudo com nome/telefone a API de LLM no exterior pode configurar transferência internacional (art. 33). Mitigar: enviar apenas dados anonimizados (espécie, idade, valores), sem nome de tutor/paciente; fonte: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm . Dados do animal isoladamente podem não ser pessoais, mas a ligação ao tutor sim.
- Receituário controlado: fora do escopo; não incluir.

## Pontuação (1-5, sem inflar)

- Impacto: 3. Economia real provavelmente 1-3 h/semana na clínica; ganho maior em consistência (não esquecer tendência/exame complementar) do que em tempo.
- Viabilidade: 4 para a versão determinística (script/planilha); 3 para a parte com LLM (depende de RIs corretos e anonimização).
- Risco: 3 (clínico moderado se o vet confiar sem conferir; mitigável com a regra "valores brutos primeiro" e anonimização).

## Cabe num MVP testável sem dados reais e sem serviços pagos? Sim

MVP sugerido (apenas Python/planilha, sem rede):
1. Tabela de RIs fictícia (cão adulto, gato adulto) em CSV, claramente marcada como exemplo; o usuário substitui pelos RIs do seu laboratório.
2. Entrada: JSON/CSV sintético com 2 exames do "mesmo" paciente fictício.
3. Saída: tabela de flags, deltas, e lista de "considerar" a partir de regras editáveis (ex.: creatinina alta + densidade urinária baixa -> considerar SDMA/repetir em hidratação adequada; regras escritas e validadas pelo vet, não inventadas).
4. Teste: casos sintéticos com resultados esperados (valor no limite do RI, unidade errada, analito ausente).
5. Etapa LLM opcional: fora do MVP; depois testar com modelo local ou com anonimização.

Critério de sucesso: o vet confere em casos sintéticos que as flags e deltas estão 100% corretos antes de qualquer uso real.

## Lacunas / não verificado

- Tempo real gasto (estimativa própria).
- Disponibilidade e preço no Brasil de DecisionIQ e integrações.
- Validação de LLM para clínica patológica veterinária de rotina.
- Posição do CFMV sobre IA no prontuário.
