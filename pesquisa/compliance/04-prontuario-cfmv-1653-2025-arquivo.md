# Compliance: manter prontuário conforme CFMV 1.653/2025 e arquivar

Data: 2026-10-02. Domínio: compliance.

## Limitação desta análise (ler primeiro)

Nesta execução, WebFetch foi bloqueado pelo proxy de saída para os três domínios fornecidos (crmvgo.org.br, legisweb.com.br, charthound.ai), e o orçamento de WebSearch da sessão estava esgotado (200/200). Portanto **não li o texto da resolução** nem pesquisei produtos. Tudo abaixo que depende de conteúdo externo está marcado "não verificado". Os URLs são os fornecidos na tarefa, citados como fontes a conferir, não como fontes lidas.

Fontes indicadas (não lidas por mim):
- https://crmvgo.org.br/resolucao-cfmv-no-1-653-2025-estabelece-novas-regras-sobre-o-prontuario-veterinario/
- https://www.legisweb.com.br/legislacao/?id=480419
- https://charthound.ai/blog/true-cost-veterinary-documentation (blog comercial, baixa confiabilidade, conforme a própria tarefa)

## O que a tarefa declara (não verificado contra o texto)

- Campos obrigatórios: anamnese, exame, diagnóstico, conduta, termos de consentimento.
- Assinatura e guarda por no mínimo 5 anos após o último atendimento.
- Requisitos de meio digital (assinatura ICP-Brasil, backup, trilha de auditoria): não verificado. Conferir no texto da resolução antes de projetar qualquer coisa.
- Vigência e regras transitórias: não verificado.

## 1. Soluções existentes

Não verificado: não consegui pesquisar. Categorias a investigar manualmente (sem afirmar que existam com essas funções):
- PIMS veterinários nacionais com prontuário eletrônico e campos obrigatórios configuráveis.
- Assinatura digital ICP-Brasil (certificado A1/A3) em PDF.
- Backup versionado (nuvem ou disco local criptografado).
- Scribes de IA para consulta (o blog charthound.ai é o tipo de produto; atende ao prontuário clínico, não à conformidade de arquivo).

## 2. Forma recomendada: script/planilha (workflow determinístico simples)

Justificativa: a parte de conformidade é verificável por regra. Os campos existem e estão preenchidos? Há assinatura? Há consentimento anexado? Qual a data do último atendimento e quando vence a guarda? O backup rodou? Nada disso exige LLM. Um checklist/validador determinístico mais rotina de backup resolve, é auditável e não alucina. Agente de IA só se justificaria para rascunhar texto clínico, que é outra tarefa e com risco maior.

Componentes:
1. Validador de completude: lê cada prontuário (JSON/CSV exportado do PIMS) e lista campos obrigatórios vazios. Não preenche nada.
2. Controle de retenção: planilha com data do último atendimento e "guardar até" (último atendimento + 5 anos, conforme descrito na tarefa; confirmar no texto). Bloqueia descarte automático; só sinaliza para revisão.
3. Backup e verificação de integridade: cópia versionada com hash (SHA-256) e teste periódico de restauração.
4. Lembrete de pendências (prontuários abertos sem assinatura).

## 3. Human-in-the-loop e riscos

O veterinário:
- Preenche e valida o conteúdo clínico (anamnese, exame, diagnóstico, conduta).
- Assina (a assinatura é ato pessoal; não delegar a automação).
- Aprova qualquer descarte após o prazo.

Riscos:
- Clínico: se uma IA preenchesse campos, risco de alucinação em diagnóstico/conduta. Por isso o validador só aponta lacunas.
- Legal (CFMV): prontuário é documento do profissional; perda, adulteração ou guarda abaixo do prazo gera exposição ética. Requisitos exatos: não verificado.
- LGPD: dados de tutores são pessoais; exigem controle de acesso, criptografia do backup, e cuidado com nuvem fora do Brasil (base legal e transferência internacional: não verificado, conferir Lei 13.709/2018).
- Receituário controlado: receitas de controle especial têm regras próprias de guarda (MAPA/ANVISA); não verificado se se integram a este prontuário. Não tratar neste escopo.
- Descarte automático: risco de apagar o que deveria ser retido; por isso, só sinalizar.

## 4. Pontuação (1-5)

- Impacto: **2**. A fração atribuível só à conformidade (campos extras, arquivo, backup) é pequena. A âncora de 25-35% do dia é de blog comercial e refere-se à documentação clínica inteira, não a esta fração; não a uso. Valor real é sobretudo redução de risco, não tempo.
- Viabilidade: **5**. Validador e rotina de backup são triviais com ferramentas atuais.
- Risco: **2** com a forma recomendada (determinística, sem IA decidindo); seria 4 se um agente preenchesse conteúdo clínico.

## 5. MVP sem dados reais e sem serviços pagos

Cabe. Gerar prontuários sintéticos fictícios em JSON, escrever um validador em Python (campos obrigatórios, data de guarda, hash de backup) e testes. Sem integração com PIMS e sem assinatura ICP-Brasil real (apenas verificar presença de um campo/arquivo de assinatura). Pendente: confirmar a lista exata de campos no texto da Resolução 1.653/2025 antes de fixar o esquema.
