# Prescrever antimicrobianos conforme exigência de receita e orientar o tutor

Data: 2026-10-02. Domínio: compliance.

## Limitação desta pesquisa (leia primeiro)
- O orçamento de WebSearch da sessão estava esgotado (200/200) e o proxy bloqueou WebFetch para portal.crmvmg.gov.br.
- Resultado: nenhuma afirmação normativa, de produto ou de estudo abaixo foi verificada em fonte. Tudo está marcado "não verificado".
- Fonte indicada na tarefa (fonte secundária, não lida por mim): https://portal.crmvmg.gov.br/2026/03/12/prescricao-de-medicamentos-3/
- Pendência: ler o texto normativo aplicável a pequenos animais (campos obrigatórios, retenção de via/receita de antimicrobianos, regime MAPA vs ANVISA, quem deve reter). Não verificado.

## 1. Soluções existentes
Não verificado (sem busca). Hipóteses a pesquisar depois, sem afirmar existência ou conformidade:
- Módulos de receituário em PIMS veterinários brasileiros.
- Ferramentas de stewardship antimicrobiano veterinário e guias de uso prudente (ex.: diretrizes de sociedades como ISCAID, WSAVA). Não verificado.
- Modelos de receita fornecidos pelos CRMVs. Não verificado.

## 2. Forma recomendada: workflow determinístico (formulário + validador), sem LLM na geração
Justificativa:
- Campos obrigatórios e retenção são regras fixas: é checagem por regras, não geração de texto.
- Dose, duração e escolha do antimicrobiano são decisão clínica. Um LLM sugerindo dose ou fármaco tem risco de alucinação e de induzir uso inadequado (resistência).
- O LLM, se usado, entra só em duas tarefas de baixo risco: (a) rascunhar o texto de orientação ao tutor em linguagem simples a partir dos campos já validados; (b) pré-preencher campos extraídos do prontuário para conferência. Nunca decide molécula, dose ou duração.
- Por que não agente: não há ganho em autonomia; o fluxo é linear e a responsabilidade é indelegável.

Esboço do workflow:
1. Entrada estruturada: espécie, peso, diagnóstico, resultado de cultura/antibiograma (opcional), histórico de alergias/uso prévio.
2. Veterinário escolhe fármaco, dose, via, frequência e dias.
3. Validador determinístico: campos obrigatórios presentes (lista a ser carregada de tabela versionada com fonte, não verificado), quantidade = dose x frequência x dias calculada, dose dentro de faixa de referência cadastrada pelo veterinário (alerta informativo), registro do racional (campo obrigatório: justificativa, se cultura foi feita, se empírico).
4. Saída: PDF da receita para assinatura, texto de orientação ao tutor (aderência, completar o tratamento conforme prescrito, armazenamento, sinais de alerta) revisado pelo veterinário, e registro estruturado no prontuário.
5. Lembrete de retenção/arquivo conforme norma (prazo e responsável: não verificado).

## 3. Human-in-the-loop e riscos
Validação do veterinário (CRMV), obrigatória:
- Indicação, fármaco, dose, duração, via e quantidade.
- Racional documentado e texto ao tutor.
- Assinatura (manual ou digital válida; aceitação não verificada).

Riscos:
- Clínico: dose errada por peso/espécie, escolha sem cultura quando indicada, duração excessiva, contribuição para resistência antimicrobiana. Mitigação: cálculo determinístico, alertas informativos, sem sugestão autônoma.
- Legal (CFMV/MAPA/ANVISA): campos faltantes, regime e retenção de receita erradas (não verificado), responsabilidade técnica. Mitigação: tabela de regras versionada com data e fonte, revisada pelo veterinário. Se o fármaco também for controlado, aplicar o fluxo do arquivo 01 (receituário controlado).
- LGPD: dados de tutor e paciente; no MVP só dados fictícios; sem envio de dados reais a APIs externas de LLM; base legal e retenção: não verificado.
- Alucinação: orientação ao tutor gerada por LLM pode inventar contraindicações ou doses. Mitigação: template fixo com lacunas preenchidas só por campos validados; revisão humana antes de entregar.

## 4. Pontuação (honesta)
- Impacto: 3. Ganho moderado de tempo por receita e padronização do registro; o tempo gasto é pequeno por consulta, mas frequente.
- Viabilidade: 4. Formulário mais regras mais template é simples; a incerteza está em carregar as regras normativas corretas.
- Risco: 3. Clínico e legal moderados, bem reduzidos se o sistema não sugerir fármaco/dose.

## 5. MVP sem dados reais e sem serviço pago?
Sim. Script/app local (Python ou planilha) com formulário, validação de campos, cálculo de quantidade, geração de PDF/texto de orientação por template, dados fictícios. Sem LLM no MVP; LLM opcional depois, para reescrever a orientação ao tutor sobre texto já aprovado. Pré-requisito: o veterinário fornecer/validar a lista de campos obrigatórios e a regra de retenção a partir do texto normativo.
