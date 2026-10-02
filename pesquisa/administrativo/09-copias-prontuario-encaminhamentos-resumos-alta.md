# Cópias de prontuário, encaminhamentos e resumos de alta

Domínio: administrativo. Data da análise: 2026-10-02.

## Recomendação
**Workflow determinístico (script/template) com redação opcional por LLM, sempre como rascunho.** Não é caso para agente autônomo. Duas metades distintas:
1. **Pedido de cópia (tutor/colega):** 100% determinístico. Checklist de quem pode pedir, prazo, registro do pedido e da entrega. Sem LLM.
2. **Resumo de alta / carta de encaminhamento:** montagem por template a partir de campos estruturados do prontuário (identificação, histórico, exames com valores e datas, tratamento realizado, pendências). LLM opcional só para redigir a narrativa a partir desses campos, com o veterinário revendo e assinando.

## Soluções existentes
- Provet Cloud: IA para resumo de instruções de alta dentro do PIMS. https://www.provet.com/product/clinical-ai ; https://support.provet.cloud/hc/en-gb/articles/21552765141788-Generate-an-AI-Summary-for-Discharge-Instructions (só vi título/trecho da busca; páginas bloqueadas ao fetch).
- Escribas de IA que geram resumo de alta e carta de encaminhamento a partir da consulta: CoVet (https://co.vet/post/after-a-veterinary-ai-scribe-generates-the-note/), Coggo (https://www.coggo.ai/), VetNotes (https://www.vetnotes.com/solutions/large-animal), PawfectNotes (https://pawfectnotes.com/medical-records/discharge-note/). Descrição vem de material comercial; eficácia e acurácia: não verificado.
- VetRec: transforma e-mail de encaminhamento em contexto estruturado e gera recapitulação do histórico e resumo de alta. https://vetrec.io/events/referral-to-discharge-2026 (divulgação comercial).
- Produtos no Brasil com integração a prontuário em português (SimplesVet, Vetsmart, VetSoft): módulo específico de cópia/encaminhamento com IA: não verificado.
- Evidência em medicina humana (não veterinária): LLMs para resumo de alta, com revisão sistemática https://link.springer.com/article/10.1007/s13721-026-00876-3 ; avaliação com GPT-4o e especialistas https://www.medrxiv.org/content/10.1101/2025.04.03.25325204.full.pdf (preprint) ; https://www.nature.com/articles/s41598-025-01618-7. Li apenas os títulos/trechos da busca; não extrapolar números. Estudo veterinário sobre resumo de alta por LLM: não encontrei, não verificado.

## Norma (CFMV) - ponto de atenção
- A tarefa descreve "atendimento imediato". Na busca, fontes secundárias indicam que a Resolução CFMV 1.653/2025 fixa **até 5 dias úteis** a partir do pedido para entrega da cópia (papel ou digital), com possibilidade de prorrogação justificada até 30 dias, e pedido apenas pelo tutor cadastrado ou pessoa por ele autorizada. Isso conflita com "imediato" e **não consegui ler o texto oficial** (domínios bloqueados). Fontes: https://www.legisweb.com.br/legislacao/?id=480419 ; https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ ; https://www.migalhas.com.br/depeso/435877/resolucao-1-653-25-do-cfmv-na-visao-do-prontuario-medico-veterinario ; anterior: https://www.cfmv.gov.br/wp-content/uploads/2022/05/Resolucao1275_ComentadaFinal.pdf. **Prazo, vigência e se revoga a 1.275/2019: verificar no texto oficial antes de parametrizar o sistema.** Deixar o prazo como parâmetro configurável.

## Human-in-the-loop
1. Veterinário responsável confere o resumo/carta contra o prontuário (diagnóstico, valores de exames, fármacos, doses, retornos) e assina. Nada sai sem esse aceite.
2. Cada dado numérico e cada fármaco no rascunho deve ser copiado do prontuário, não gerado; o rascunho marca o campo de origem.
3. Verificação de legitimidade do solicitante (tutor cadastrado ou autorizado por escrito) feita por pessoa da recepção/RT, não por IA.
4. Revisão do que vai anexado (exames do paciente certo, sem dados de outros pacientes).

## Riscos
- Clínico/alucinação: LLM pode inventar, omitir ou trocar diagnóstico, dose, lateralidade, resultado de exame; um colega que receba a carta pode agir sobre isso. Mitigação: campos estruturados, narrativa mínima, destaque de valores, revisão obrigatória.
- Legal CFMV: prontuário é documento do médico-veterinário e sigiloso; entrega só a quem a norma permite; registro da solicitação e da entrega. Texto exato: não verificado (ver acima).
- LGPD: dados de tutor e do paciente (vinculados ao tutor) são pessoais; enviar a API externa de LLM exige base legal, minimização, contrato e, preferencialmente, anonimização. Envio a colega/especialista deve ter finalidade e consentimento do tutor. Texto da LGPD não consultado nesta rodada: não verificado.
- Receituário controlado: carta/resumo que cite medicamentos controlados não substitui receita; não gerar nem reproduzir receituário; regras específicas não pesquisadas: não verificado.
- Segurança do envio: e-mail/WhatsApp com prontuário ao destinatário errado. Mitigação: confirmação do destinatário e envio sempre manual.

## Pontuação
- Impacto: 3 (poupa tempo real por caso, mas é tarefa de volume moderado; o PIMS já pode oferecer parte)
- Viabilidade: 4 (template e checklist são simples; LLM opcional)
- Risco: 3 (erro numa carta de encaminhamento pode afetar conduta de terceiro; sigilo/LGPD)

## MVP sem dados reais e sem serviços pagos
**Sim**, para o núcleo determinístico. Script Python (ou planilha): prontuário fictício em JSON/CSV, template de resumo de alta e carta de encaminhamento em Markdown, lista de exames anexados com data, log CSV de pedidos de cópia (data do pedido, solicitante, vínculo, prazo parametrizável, data de entrega, quem aprovou), alerta de prazo vencendo e checklist de validação. Redação por LLM fica fora do MVP (exigiria serviço pago/externo e dados reais para avaliar de verdade).
