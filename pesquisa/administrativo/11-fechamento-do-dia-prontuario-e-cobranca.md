# Fechamento do dia: pendências de prontuário, conferência de cobrança e lançamentos

Domínio: administrativo. Data da análise: 2026-10-02.

## Recomendação
**Workflow determinístico (script/planilha de reconciliação), sem LLM no caminho crítico.** A tarefa é essencialmente um *join* entre três listas: consultas do dia, status do prontuário e itens da fatura. Regras fixas (consulta fechada sem fatura; procedimento sem insumo esperado; prontuário sem campos obrigatórios) resolvem a maior parte e são auditáveis. LLM só como etapa opcional e posterior (sugerir "possível item não cobrado" a partir do texto livre do prontuário), sempre como sugestão e nunca como lançamento automático. Agente autônomo não se justifica: alterar fatura ou fechar prontuário sozinho traz risco sem ganho.

## Soluções existentes
- SimplesVet: lançamento da venda pelo prontuário com reconhecimento no caixa, painéis de fechamento de caixa e conciliação de cartões. https://simples.vet/funcionalidades/prontuario-medico/ ; https://simples.vet/funcionalidades/ (descrição comercial; não testei).
- Vetsmart: prontuário digital gratuito e bulário. https://vetsmart.com.br/ . Módulo de conferência de cobrança: não verificado. Outros PIMS brasileiros (VetSoft etc.): não verificado.
- Captura de cobranças (charge capture) em PIMS internacionais: ezyVet https://www.ezyvet.com/charge-capture ; Covetrus https://software.covetrus.com/emea/veterinary-insights/article/practice-solutions/the-opportunity-more-revenue-the-gap-missed-charges/ ; dvm360 https://www.dvm360.com/view/missing-charges-your-software-should-help ; Shepherd https://www.shepherd.vet/blog/how-to-get-15-missed-revenue-back-in-your-veterinary-practice/ ; VetXbill.AI (conferência prontuário x fatura com IA) https://www.vetxbill.ai/ .
- Magnitude do problema: fontes de mercado citam ~17% de cobranças diagnósticas não faturadas (dvm360 / Today's Veterinary Business) e perdas de 8-15% da receita; auditoria típica compara prontuário e fatura em amostra de ~10 faturas por veterinário/trimestre (resultados de buscas, textos de fornecedores). **São números de marketing e de mercado dos EUA/Europa, sem revisão por pares; não extrapolar para o Brasil. Estudo revisado por pares sobre cobrança perdida em clínicas vet: não encontrei, não verificado.**

## Norma (CFMV) - ponto de atenção
- Resolução CFMV 1.321/2020 (resultados de busca): prontuário é documento escrito e datado, sem rasuras, assinado exclusivamente pelo médico-veterinário; deve trazer data, hora, local e identificação do veterinário responsável; guarda mínima de 5 anos após última consulta; cópia em até 5 dias úteis. https://www.legisweb.com.br/legislacao/?id=480427 ; https://www.normasbrasil.com.br/norma/resolucao-1321-2020_480427.html . A Resolução 1.653/2025 aparece em fontes secundárias como atualização (https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ ; https://crmvgo.org.br/wp-content/uploads/2025/08/1653.pdf). Não li o texto oficial integral: **vigência, campos obrigatórios e relação entre as duas: verificar antes de parametrizar o checklist.**
- Implicação: o prontuário é ato do veterinário. O sistema pode apontar "faltam campos", mas não pode preencher, alterar ou assinar. Edição de prontuário já fechado deve seguir a regra de retificação do PIMS (sem apagar histórico).

## Human-in-the-loop
1. Veterinário responsável revisa e assina/fecha cada prontuário pendente; a ferramenta só lista e destaca lacunas.
2. Todo item sugerido como "não cobrado" passa por recepção/financeiro (e veterinário se envolver ato clínico) antes de entrar na fatura; nada é lançado automaticamente.
3. Itens de baixa/estoque de medicamentos controlados e psicotrópicos: conferência humana contra livro/sistema de controle; a ferramenta não toca nisso.
4. Divergências geradas pela regra (falso positivo) têm botão "ignorar com motivo", registrado em log.
5. Cobrar sem ter feito o procedimento é tão grave quanto deixar de cobrar: a conferência é bidirecional.

## Riscos
- Clínico: baixo direto, mas pressão para "fechar" prontuário rápido pode induzir preenchimento apressado ou retroativo. Mitigação: não auto-preencher; mostrar data/hora real do registro.
- Alucinação (se houver LLM): inventar procedimento/insumo que justifique cobrança, gerando cobrança indevida (risco de relação de consumo e ético). Mitigação: sugestão sempre ancorada em trecho citado do prontuário; sem trecho, sem sugestão.
- Legal CFMV: integridade e autoria do prontuário (ver acima); fatura x prontuário inconsistentes dificultam defesa em processo ético ou de consumo. Código de Defesa do Consumidor e normas fiscais: não pesquisados, não verificado.
- LGPD: prontuário e fatura contêm dados pessoais do tutor. Enviar a API externa de LLM exige base legal, minimização e contrato; o núcleo determinístico roda local e não precisa enviar nada. Texto da LGPD não consultado: não verificado.
- Receituário controlado: fora do escopo da automação; só alertar humano quando item controlado aparecer na fatura sem registro correspondente (regra, sem LLM).
- Operacional: tabela de "insumos esperados por procedimento" desatualizada gera ruído e fadiga de alerta.

## Pontuação
- Impacto: 4 (tempo diário de fechamento e vazamento de receita são reais, mas os números citados são de fornecedores e de outros países)
- Viabilidade: 4 (regras determinísticas simples; depende de exportação de dados do PIMS, que varia por produto)
- Risco: 2 (baixo clínico se ficar em lista/sugestão; sobe para 3 se tocar fatura ou usar LLM com dados reais)

## MVP sem dados reais e sem serviços pagos
**Sim.** Script Python (ou planilha) com três CSVs fictícios: consultas do dia (id, status do prontuário, campos obrigatórios preenchidos S/N, veterinário), itens da fatura (id da consulta, item) e tabela de regras (procedimento -> insumos/itens esperados). Saída: relatório Markdown/CSV com (a) prontuários abertos ou incompletos por veterinário, (b) consultas sem fatura, (c) faturas sem consulta, (d) procedimentos sem item esperado e itens sem procedimento, (e) log de decisões humanas (ignorar/lançar/corrigir). Testes com dados sintéticos e casos de borda. Integração real com PIMS e etapa de LLM ficam fora do MVP (exigem dados reais e/ou serviço pago para avaliar de verdade).
