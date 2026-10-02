# 08 - Calculadoras clínicas (fluidoterapia, CRI, anestesia, IRIS, BCS, dieta)

Data da análise: 2026-10-02. Domínio: apoio clínico. Tarefa: ~4 min x 25-30 usos/semana (~2 h/semana, estimativa do usuário).

## Recomendação: script/planilha determinística (não agente)

Todas as contas são fórmulas fechadas. Um LLM não acrescenta nada e introduz risco de alucinação numérica. Forma recomendada: calculadora determinística (planilha ou página/script local) com tabela de protocolos versionada e revisada pelo veterinário. Um LLM, se usado, só serviria para entender texto livre ("gato 4,2 kg, 7% desidratado") e preencher campos, e nunca para calcular.

## Soluções existentes (verificadas por busca; páginas não abertas integralmente)

- Vetcalculators (app iOS/Android e web: emergência, CRI, fluidos, calorias, conversões; 600+ fármacos segundo a loja): https://www.vetcalculators.com/ e https://www.vetcalculators.com/app.html
- Plumb's Veterinary Drugs (dose + calculadora de conversão, assinatura): https://plumbs.com/features/calculator/
- VetDrugs Calculators (app): https://apps.apple.com/us/app/vetdrugs-calculators/id6458646967
- Calculadora de estadiamento IRIS de terceiros: https://askavet.com/pages/kidney-disease-staging-calculator
- Lista de calculadoras (VAA Support Group, CRI/TIVA/epidural), via guia da Univ. de Pretoria: https://library.up.ac.za/c.php?g=1085098&p=7983885
- Integração com PIMS brasileiro: não verificado (não pesquisei plug-ins específicos de PIMS nacionais).

Ou seja, o problema de cálculo já está resolvido por produtos prontos. O ganho real de automatizar é registrar o resultado na ficha, o que depende do PIMS usado (não verificado).

## Base normativa/clínica das fórmulas

- IRIS: estadiamento por creatinina e/ou SDMA, em paciente hidratado e estável, em pelo menos duas ocasiões, depois subestágio por proteinúria e pressão arterial. https://www.iris-kidney.com/iris-staging-system ; versão 2026 (PDF, não aberto por mim): https://static1.squarespace.com/static/666b9ecb4064a156963b4162/t/6a53129b031ea43169a7a89f/1783829156676/IRIS_staging_guidelines+2026.pdf . Os pontos de corte citados no resumo da busca (ex.: estágio 2 cão creat. 1,4-2,8 mg/dL) NÃO foram conferidos no documento oficial: não verificado. Tabela de cortes deve ser copiada do PDF oficial vigente.
- Fluidos (AAHA/AAFP 2013): manutenção gato 80 x PV^0,75 mL/dia, cão 132 x PV^0,75; déficit (L) = PV (kg) x % desidratação; fluido anestésico < 10 mL/kg/h (início 3 mL/kg/h gato, 5 mL/kg/h cão). Fonte: https://www.antechdiagnostics.com/wp-content/uploads/2025/01/Fluid_Therapy_GuidelinesAAFP-AAHA.pdf . Existe versão 2024 (https://www.aaha.org/resources/2024-aaha-fluid-therapy-guidelines-for-dogs-and-cats/section-3-fluids-for-replacement-and-maintenance/); os valores 2024 não foram conferidos: usar a versão vigente.
- Nutrição: BCS 9 pontos e avaliação nutricional (WSAVA): https://wsava.org/wp-content/uploads/2020/01/WSAVA-Nutrition-Assessment-Guidelines-2011-JSAP.pdf ; RER = 70 x PV^0,75 (resumo: https://todaysveterinarynurse.com/nutrition/veterinary-nutrition-math/ , fonte secundária). Fatores de multiplicação para MER: não verificado.
- CRI e doses de emergência/anestesia: dose por kg e concentração vêm de formulário (Plumb's etc.), não de fórmula; a tabela de doses precisa de fonte e revisão do veterinário. Não verificado nesta pesquisa.

## Evidência de que erro de cálculo importa

- Estudo prospectivo com estudantes: 10,8% dos protocolos anestésicos com erro de cálculo; 83% dos erros eram superdose. https://pubmed.ncbi.nlm.nih.gov/40587234/
- Hospital-escola: erros de medicação eram 66% dos relatos de incidente, 51% deles por dose incorreta. https://pubmed.ncbi.nlm.nih.gov/40015553
- FDA: superdoses de 10x por vírgula/zero mal lidos. https://www.fda.gov/animal-veterinary/product-safety-information/veterinary-medication-errors
Isso sustenta calculadora determinística com checagens (unidade, faixa plausível), mais do que um agente.

## Human-in-the-loop

1. Veterinário informa/confirma peso, espécie, % desidratação, concentração do frasco e protocolo.
2. A ferramenta mostra a conta passo a passo (fórmula, unidades) e emite alerta se fora da faixa plausível (ex.: dose/kg acima do máximo da tabela, volume > X mL/kg/h).
3. Veterinário confere e só então registra na ficha. Nenhum valor é escrito automaticamente sem confirmação.
4. Tabelas de doses e cortes IRIS são mantidas e datadas pelo veterinário (responsável técnico).

## Riscos

- Clínico: erro de entrada (peso em lb, mg vs mcg, concentração errada) e tabela desatualizada. Mitigação: unidades explícitas, limites, testes com casos conhecidos, versão/data da tabela exibida. Ajustes para cardiopata, renal, neonato e obeso exigem julgamento clínico, a ferramenta não decide.
- Alucinação: inaceitável em dose. Por isso, sem LLM no cálculo.
- Legal/CFMV: a prescrição é ato do médico-veterinário (https://revista.cfmv.gov.br/prescricao-de-medicamentos-veterinarios-e-um-ato/); a ferramenta é apoio. Prontuário/ficha com guarda mínima de 5 anos segundo resumo da Res. CFMV 1.275/2019 (https://manual.cfmv.gov.br/arquivos/resolucao/1275.pdf; prazo conferido só por resumo de busca). Controlados: regime da Portaria MAPA 837/2025 (https://www.legisweb.com.br/legislacao/?id=488965); a calculadora não deve emitir receita nem substituir a notificação/livro de controle.
- LGPD: dados de tutor são pessoais. MVP não deve receber nome/CPF do tutor; usar apenas peso/espécie/ID interno. Se integrar a PIMS ou nuvem, avaliar operador e base legal (análise jurídica não feita aqui).
- Software como dispositivo: não avaliei se há enquadramento regulatório para software veterinário de apoio à decisão: não verificado.

## Pontuação (honesta)

- Impacto: 2/5. ~2 h/semana, e já existem apps que fazem a conta em segundos; o ganho incremental é a integração à ficha.
- Viabilidade: 5/5 (fórmulas simples).
- Risco: 3/5 (dose errada pode causar dano, mas controlável com HITL e sem LLM).

## MVP testável sem dados reais e sem serviços pagos: sim

Planilha ou página HTML/Python local com: manutenção e déficit (fórmulas AAHA), RER, conversão mg/kg/h para mL/h e diluição de CRI, estadiamento IRIS por tabela configurável, testes unitários com casos sintéticos. Sem integração com PIMS e sem LLM. Antes de uso clínico, validar todas as saídas contra Vetcalculators/Plumb's e contra as diretrizes vigentes, por veterinário.

## Limites desta pesquisa

Pontos de corte IRIS, valores AAHA 2024, fatores de energia (MER) e doses de emergência não foram conferidos nas fontes primárias; marcados como não verificado.
