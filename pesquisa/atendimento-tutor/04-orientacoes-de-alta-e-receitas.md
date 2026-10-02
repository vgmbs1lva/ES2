# Redigir orientações de alta e receitas para o tutor

Domínio: atendimento-tutor. Análise de 2026-10-02.

## Recomendação

**Workflow determinístico com um passo opcional de LLM, sempre com aprovação do veterinário.** Não é um agente autônomo.

- Blocos de texto validados pela clínica (modelos por procedimento, curativo, dieta, sinais de alarme) são montados por regras a partir de campos estruturados: diagnóstico, medicamentos, dose, duração, retorno.
- O LLM entra só para adaptar o tom e o nível de leitura. Ele não escolhe medicamento nem dose, e não inventa sinais de alarme.
- Receita comum: o sistema monta o rascunho a partir do plano terapêutico, e o veterinário confere e assina.
- Receita de controlado: **não automatizar a emissão**. O sistema no máximo sinaliza que o item exige documento específico.

Por que não um agente: o texto tem de ser reprodutível e auditável, e o erro de dose ou de sinal de alarme tem custo clínico. Modelos e campos resolvem a maior parte do trabalho.

## Soluções existentes (pesquisadas)

| Solução | O que faz | Fonte |
|---|---|---|
| Provet Cloud | Resumos clínicos e instruções de alta auto-preenchidas | https://www.dvm360.com/view/ai-provides-relief-for-the-relief-veterinarian e https://www.shepherd.vet/blog/8-best-ai-powered-veterinary-practice-management-software-platforms-2026-comparison-guide/ |
| VetGeni | SOAP, instruções de alta e plano a partir de voz ou texto | https://www.vetgeni.com/blog/tutorial-discharge-instructions |
| VetRec | SOAP, resumo de alta e comunicação com o cliente | https://www.g2.com/products/vetrec/discuss |
| Modelo de alta (sem IA) | Template gratuito de instruções de alta | https://www.co.vet/post/veterinary-discharge-instructions-template |
| Receita digital e modelo (Brasil) | Guias de blogs comerciais, **não normativos** | https://vetagora.online/receita-veterinaria-digital-cfmv-2026/ |

Observações:
- Esses são produtos comerciais, quase todos voltados ao mercado dos EUA, e de resumos de fornecedor. Não verifiquei preço, aderência às normas brasileiras nem disponibilidade em português. **Não verificado.**
- Não encontrei, nesta busca, produto que gere receita conforme CFMV/MAPA em português dentro de um PIMS. **Não verificado.**

## Evidência sobre LLM em instruções de alta

Os estudos abaixo são em **medicina humana**, não veterinária. Li apenas os resumos dos resultados de busca. As páginas da JAMA e da revista do CFMV foram bloqueadas pelo proxy e não pude abri-las.

- LLM torna o sumário de alta mais legível, com diferença significativa (p < 0,0001): https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2815868 (texto completo em https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10928500/).
- Nesse mesmo estudo, segundo o resumo da busca: 56 de 100 revisões consideraram o texto completamente completo, e 18 apontaram preocupações de segurança por omissões e imprecisões. A conclusão é que a implantação inicial exige revisão do médico.
- Avaliação de LLM para simplificar sumários e dar recomendações de estilo de vida: https://www.nature.com/articles/s43856-025-00927-2
- Instruções de alta supervisionadas por clínico no pronto-socorro: https://pubmed.ncbi.nlm.nih.gov/42455479/
- InstructDS (modelo ajustado): https://link.springer.com/article/10.1007/s44443-026-01068-9. O resumo da busca cita 4% de alucinação, medida com GPT-4 como juiz, ou seja, avaliação automática e não clínica.

Conclusão honesta: há ganho de legibilidade, mas omissão e alucinação em fração relevante dos casos. Isso reforça restringir o LLM a reescrita e manter revisão obrigatória.

## Norma aplicável

Nada abaixo foi lido na íntegra por mim. Vem de resultados de busca e de guias de conselhos regionais. Conferir o texto oficial antes de usar.

- Prescrição é ato exclusivo do médico-veterinário, regulada pela Resolução CFMV nº 1.318/2020: https://manual.cfmv.gov.br/arquivos/resolucao/1318.pdf e https://revista.cfmv.gov.br/prescricao-de-medicamentos-veterinarios-e-um-ato/ (a segunda não consegui abrir).
- Conteúdo típico da receita: cabeçalho com nome e CRMV, identificação do animal e do tutor, medicamento com concentração e forma, posologia. Guia do CRMV-MG/PR: https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf
- Controlados de uso veterinário: regime da Portaria SDA/MAPA nº 837/2025, notificação de receita veterinária emitida pelo SIPEAGRO (segundo os resultados de busca; confirmar no texto da portaria e no guia acima).
- Controlados de uso humano prescritos a animais seguem a Portaria SVS/MS nº 344/1998 (ANVISA), com receituário próprio: http://www.infoconsult.com.br/legislacao/portaria_svs/p_svs_344_1998.htm
- Antimicrobianos e a Resolução CFMV 1.465/2022 apareceram na busca (https://www.legisweb.com.br/legislacao/?id=433219), mas **não verifiquei** o conteúdo e a relação com receita. Não verificado.
- Prontuário: Resolução CFMV 1.321/2020 (estrutura e retenção), segundo https://www.flyvet.com.br/geo/guia-completo-prontuario-veterinario-brasil-clinicas-cfmv/ (blog comercial; confirmar na norma).
- Telemedicina veterinária exige termo de consentimento específico: https://crmvsp.gov.br/resolucao-que-regulamenta-a-telemedicina-veterinaria-e-publicada-entenda-como-funciona/ . Para termo de consentimento cirúrgico ou anestésico, não encontrei norma específica nesta busca. **Não verificado.**
- Receita digital: assinatura eletrônica qualificada citada para controlados. Regras exatas de assinatura para receita comum: **não verificado.**
- LGPD (Lei 13.709/2018): dados do tutor são dados pessoais. Ver https://www.cfmv.gov.br/perguntas-frequentes-lgpd/ e https://www.flyvet.com.br/geo/melhores-praticas-conformidade-lgpd-clinica-veterinaria-brasil-2026/ . Enviar a alta por WhatsApp e passar texto a API de LLM no exterior são tratamentos que a clínica deve cobrir (base legal, aviso, transferência internacional). Parecer jurídico: **não verificado.**

## Onde o veterinário valida (human-in-the-loop)

1. **Revisão do rascunho completo antes de qualquer envio.** Medicamento, dose, frequência, duração, sinais de alarme, data de retorno. Sem botão de "enviar" antes da aprovação registrada.
2. **Receita**: o veterinário assina (CRMV). O sistema não assina por ele.
3. **Controlados**: fluxo fora da automação, no SIPEAGRO ou no receituário ANVISA.
4. **Termo de consentimento**: o veterinário decide se cabe, e o tutor assina.
5. **Cópia no prontuário** gerada junto, com a versão exata entregue, data/hora e quem aprovou.

## Riscos

- **Clínicos**: erro de dose ou espécie (ex.: fármaco tóxico para gatos), omissão de sinal de alarme, contradição com o que foi dito na consulta, interação medicamentosa. Mitigação: dose vem do plano do veterinário, não do LLM; checagem de regras (espécie, peso, campos obrigatórios); diff entre o plano e o texto gerado.
- **Alucinação**: LLM inventa orientação, número de telefone ou prazo. Mitigação: texto livre limitado a reescrita; fatos preenchidos por campos; proibir conteúdo fora do modelo.
- **Legais**: receita sem assinatura ou campos obrigatórios; uso indevido de controlados; guarda do prontuário; LGPD no envio por WhatsApp e no envio a LLM externo.
- **Operacionais**: tutor com baixa alfabetização ou sem WhatsApp, impressão como padrão alternativo.

## Pontuação

| Critério | Nota | Justificativa |
|---|---|---|
| Impacto | 3 | Tarefa repetitiva em toda alta e fonte comum de retrabalho, mas o ganho de tempo por caso é de minutos e a revisão permanece. Não medi o tempo real. |
| Viabilidade | 4 | Templates e preenchimento por campos são simples. A parte de LLM é opcional. A integração com PIMS brasileiro é o ponto incerto (**não verificado**). |
| Risco (5 = pior) | 3 | Moderado se a dose vier do veterinário e houver aprovação obrigatória. Sobe para 5 se incluir controlados ou envio sem revisão. |

## Cabe num MVP testável sem dados reais e sem serviço pago?

**Sim, para a parte determinística.** Um script em Python ou planilha, com:
- casos fictícios (JSON) com espécie, peso, diagnóstico e prescrição;
- modelos de texto por procedimento, em linguagem leiga;
- geração de PDF/Markdown da alta e da receita (rascunho) com validação de campos obrigatórios e lista de pendências para o veterinário;
- bloqueio de itens marcados como controlados, com aviso.

Fica de fora do MVP gratuito e sem dados reais: o passo de LLM (exige API paga ou modelo local), integração com PIMS e WhatsApp, assinatura digital e SIPEAGRO.
