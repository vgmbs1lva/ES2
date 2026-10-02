# Emitir notificação de receita veterinária de controlado (A/B/B2) e preencher o receituário

Data: 2026-10-02. Domínio: compliance.

## Limitação desta pesquisa (leia primeiro)
- O orçamento de WebSearch da sessão estava esgotado (200/200) e o proxy bloqueou WebFetch para legisweb.com.br e crmv-pr.org.br.
- Resultado: nenhuma afirmação normativa abaixo foi verificada em fonte. Tudo que é norma, produto ou estudo está marcado "não verificado".
- Fontes indicadas na tarefa, a serem lidas pelo veterinário antes de qualquer implementação:
  - https://www.legisweb.com.br/legislacao/?id=488965 (Portaria SDA/MAPA 837/2025 - texto não lido por mim)
  - https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf (guia CRMV-MG - não lido por mim)
- Pendência: confirmar no texto da 837/2025 quais classes migraram para o regime MAPA e quais ficam na Portaria SVS/MS 344/98. Não verificado.

## 1. Soluções existentes
Não verificado (sem busca). Hipóteses a pesquisar depois, sem afirmar existência ou conformidade:
- Módulos de receituário de PIMS veterinários brasileiros.
- Receita eletrônica/assinatura digital ICP-Brasil: a aceitação para controlados veterinários depende da norma vigente. Não verificado.
- Modelos em planilha/PDF preenchível fornecidos pelos CRMVs e vigilâncias locais.

## 2. Forma recomendada: workflow determinístico (formulário + validador de regras), sem LLM na geração
Justificativa:
- O documento é rígido: um produto por notificação, sem rasura, algarismos arábicos, limite de 30 dias de tratamento, validade de 30 dias (conforme a descrição da tarefa, não verificado na norma). Isso é checagem por regras, não geração de texto.
- Um LLM só aumenta o risco de alucinar dose, quantidade ou numeração. Se usado, que seja apenas para extrair dados do prontuário para pré-preencher campos, sempre com conferência.
- Notificação física exige talonário numerado da vigilância sanitária e assinatura. O sistema não pode numerar nem emitir sozinho.
- Nota: o "preenchimento por extenso" (quantidade em extenso e algarismos) deve ser conferido contra a norma. Não verificado.

Proposta de MVP (workflow):
1. Formulário estruturado: paciente (espécie, peso), tutor (dados fictícios no teste), substância, concentração, forma, posologia, duração em dias, quantidade.
2. Validador: um produto por notificação; duração <= 30 dias; quantidade = dose x frequência x dias (calculada, não digitada); dose em algarismos arábicos; lista da substância (A/B/B2/controle especial) vinda de tabela mantida pelo veterinário a partir da norma; campo de número do talonário informado manualmente e checado por formato/duplicidade.
3. Saída: PDF/pré-visualização para transcrição ou impressão no modelo oficial, mais registro estruturado para o prontuário.

## 3. Human-in-the-loop, riscos
Validação obrigatória do veterinário (CRMV):
- Indicação, substância, dose, via, duração e quantidade (decisão clínica e responsabilidade legal exclusiva do profissional).
- Conferência final e assinatura (manual ou digital válida).
- Numeração do talonário e correspondência com o livro/registro de controle.

Riscos:
- Clínico: erro de dose (opioides, fenobarbital) por peso/espécie; interação medicamentosa. Mitigação: cálculo determinístico, alertas apenas informativos, sem sugestão autônoma de dose.
- Legal (CFMV/MAPA/ANVISA): classe/regime errado (344/98 vs 837/2025 - não verificado), prazos, retenção de via, rasura, numeração. Mitigação: tabela de regras versionada com data e fonte, revisada pelo veterinário.
- LGPD: dados de tutor e paciente; usar apenas dados fictícios/pseudonimizados no MVP; minimização; sem envio a APIs externas de LLM com dados reais. Base legal e retenção: não verificado.
- Alucinação: evitar LLM na geração de campos; se usado em extração, saída restrita a schema e conferência campo a campo.
- Desvio/fraude: ferramenta não deve emitir sem talonário válido nem sem ação humana de assinatura.

## 4. Pontuação (1-5)
- Impacto: 3. Tarefa frequente e repetitiva em clínicas que usam controlados, mas o ganho por receita é de poucos minutos e a assinatura/talonário permanecem manuais.
- Viabilidade: 4 para validador/formulário; 2 para integração oficial/receita eletrônica (dependente de norma e integrações não verificadas).
- Risco: 4. Documento de controle sanitário e responsabilidade penal/administrativa; erros têm consequência legal e clínica.

## 5. Cabe em MVP testável sem dados reais e sem serviços pagos?
Sim, para o escopo reduzido: formulário local (HTML/planilha/script) com validador de regras e dados fictícios. Não cobre emissão oficial, numeração real nem assinatura digital. As regras do validador só devem ser consideradas corretas após o veterinário confirmar o texto da 837/2025 e da 344/98, que não pude verificar.
