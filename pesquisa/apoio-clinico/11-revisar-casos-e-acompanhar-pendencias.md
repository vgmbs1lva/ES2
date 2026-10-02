# Revisar casos em reunião de equipe e acompanhar resultados pendentes

Domínio: apoio-clinico. Data da análise: 2026-10-02.
Estimativa de tempo (do usuário, não verificada): ~30 min/semana de reunião + 60-90 min/semana de caça a pendências.

## Recomendação: workflow determinístico (script/planilha com rotina semanal), sem LLM no caminho crítico

Não é um problema de raciocínio, é de **não perder itens abertos**. Basta um registro estruturado de pendências (paciente, item, responsável, prazo, status), uma consulta semanal que lista o que está vencido ou sem dono, e uma pauta gerada a partir disso. LLM só como opcional, para rascunhar mensagens de contato com tutor ou resumir texto livre, sempre revisado.

## Soluções existentes
- Quadros de internação e fichas de tratamento em PIMS: Digitail (https://digitail.com/), Vet Radar (https://www.vetradar.com/), Covetrus Pulse (https://covetrus.com/covetrus-platform/workflow-and-productivity-tools/covetrus-pulse/), Provet (https://www.provet.com/), IntraVet (https://www.pattersonvet.com/software/practice-management/intravet). Foram vistos só nas páginas comerciais; não verifiquei se rastreiam resultados externos pendentes nem se há equivalente nacional.
- Plataformas de fluxo com IA: VetCheck (https://vetcheck.it/). Não verificado em detalhe.
- Ferramentas de passagem de plantão: I-PASS (gravidade, resumo, lista de ações, consciência situacional, síntese). Na medicina humana reduziu eventos adversos em 23% (conforme o resumo da busca; estudo original: https://pmc.ncbi.nlm.nih.gov/articles/PMC7651935 — confirmar). Em veterinária: https://www.dvm360.com/view/patient-handoffs-improve-team-dynamics-and-hospital-culture-through-collaboration
- Evidência sobre exames pendentes (medicina humana, transferível por analogia): revisão sistemática https://pmc.ncbi.nlm.nih.gov/articles/PMC9491200/ e https://pubmed.ncbi.nlm.nih.gov/29352419/. Até 23% dos internados têm exames pendentes na alta e 30-40% deles trazem resultado acionável. Intervenções promissoras: documentar o pendente de forma confiável, notificação por e-mail e tempo dedicado da equipe. Não encontrei dado equivalente em veterinária: não verificado.

## Desenho do MVP
1. Planilha ou CSV (ou SQLite) com colunas: id_caso (código, sem nome real), tipo (exame externo / retorno / ligar tutor / decisão), descrição, responsável, data_pedido, prazo, status, nota.
2. Script (Python) que roda antes da reunião: pendências vencidas, sem responsável, ou abertas há mais de N dias; agrupa por responsável; gera pauta em Markdown.
3. Pós-reunião: decisões e responsáveis entram no registro; a ata é gerada do próprio registro.
4. Lembrete simples (e-mail para a equipe, sem dados clínicos no corpo) apontando para o sistema interno.

## Human-in-the-loop
- O veterinário decide conduta e prioridade; a ferramenta só lista e lembra.
- Fechar uma pendência exige confirmação humana (resultado visto e interpretado).
- Qualquer texto para o tutor é revisado antes de enviar.
- Ao final da reunião, o responsável confirma a atribuição.

## Riscos
- **Clínico:** falso senso de segurança (o que não está no registro some). Mitigação: entrada obrigatória na solicitação do exame; o registro não substitui o prontuário. Tentação de usar IA para priorizar clinicamente: não fazer.
- **Alucinação:** só se houver LLM; por isso fora do caminho crítico, nunca resumir resultados de exames nem sugerir conduta sem revisão.
- **LGPD (Lei 13.709/2018):** nome, telefone e endereço do tutor são dado pessoal. Planilhas compartilhadas e WhatsApp são apontados como inadequados (fonte secundária: https://www.flyvet.com.br/geo/guia-completo-prontuario-veterinario-brasil-clinicas-cfmv/). Usar identificadores internos, controle de acesso, e não enviar dados a LLM externo sem base legal e contrato. Verificar texto da lei diretamente: não verificado aqui.
- **CFMV:** Resolução CFMV 1.321/2020 trata de prontuário e documentos (https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf) e sigilo profissional. O registro de pendências não deve virar prontuário paralelo; decisões clínicas devem ir ao prontuário oficial. Confirmar com o texto da norma.
- **Receituário controlado:** fora do escopo; não incluir prescrição de controlados na ferramenta. Normas do MAPA/ANVISA não pesquisadas: não verificado.

## Pontuação (1-5)
- Impacto: 3. O ganho está nos 60-90 min de caça e no risco de pendência perdida; a reunião em si continua humana. Valores são estimativa própria.
- Viabilidade: 5 (planilha/script simples).
- Risco: 2 (baixo, desde que seja apoio e sem dados identificáveis).

## Cabe num MVP testável sem dados reais e sem serviço pago?
Sim. CSV sintético com 20-30 pendências fictícias, script Python local e geração de pauta em Markdown. Não requer integração com PIMS nem LLM. Integração real com o PIMS da clínica fica para depois.
