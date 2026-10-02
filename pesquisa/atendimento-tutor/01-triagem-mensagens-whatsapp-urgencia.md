# Triagem de mensagens de WhatsApp/telefone (urgência vs. rotina)

Domínio: atendimento-tutor | Data da pesquisa: 2026-10-02

## Recomendação (resumo)

**Workflow determinístico com apoio de LLM apenas para rascunho/extração, com humano em 100% das classificações em fase inicial.** Não um agente autônomo conversando com o tutor.

Camadas, da mais simples à mais complexa:
1. Regras/palavras-chave de "red flags" (convulsão, atropelamento, intoxicação, sangramento, colapso, dispneia, abdome distendido, gato obstruído/sem urinar, parto difícil, etc.) que sempre forçam "URGENTE - ligar/trazer agora" e acionam a recepção/vet. Sem LLM, auditável.
2. Classificação em 3 baldes (urgente / agendar / orientar por texto) com checklist de perguntas padrão (espécie, idade, sintoma, duração, ingestão de tóxicos, ainda come/bebe, respira bem).
3. LLM opcional só para: extrair campos do texto/áudio transcrito, sugerir categoria e redigir resposta-modelo para aprovação. Regra de ouro: o LLM só pode **subir** a urgência, nunca reduzi-la abaixo do que as regras determinaram.
4. Registro estruturado no prontuário (tutor/paciente, mensagem, classificação sugerida, classificação final, quem validou, horário).

Por que não agente autônomo: a CFMV veda diagnóstico, exames e prescrição em teleorientação/teletriagem; erro de subtriagem é o risco dominante; evidência de desempenho de IA em triagem veterinária é escassa (ver abaixo).

## 1. Soluções existentes (o que achei)

Atenção: a maior parte é material de fornecedor/blog (marketing), não estudo revisado por pares. Trate como descrição de mercado, não como evidência de eficácia.

- Chatbots/atendentes de IA para clínicas vet (descrevem categorias emergência / mesmo dia / 24-48 h / rotina e guardrails de "não diagnosticar"): https://blog.fastbots.ai/ai-chatbot-for-veterinary-clinics/ , https://www.puppilot.co/learn/veterinary-answering-service-ai-triage-guide , https://kordless.ai/blog/veterinary-clinic-automate-after-hours-calls
- Pearl (triagem veterinária por IA, EUA): https://www.pearl.com/post/ai-veterinary-triage-bot-how-pearl-ai-accelerates-pet-care-while-protecting-trust
- Panorama de ferramentas de IA vet (blog comercial): https://co.vet/post/ai-vet-tools/ e https://www.whippetnotes.com/blog/ai-for-veterinarians
- Evidência científica veterinária: estudo misto (PLOS ONE) sobre triagem telefônica de cólica equina no Reino Unido. Achou inconsistência maior entre a equipe de recepção, e que um pacote de informação + fluxograma + formulário de registro aumentou a confiança em reconhecer casos críticos. Ou seja, o ganho veio de protocolo padronizado, não de IA. O texto também afirma que a evidência sobre triagem telefônica em veterinária é escassa. https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0238874 (PMC: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7510986/)
- Medicina humana (analogia, não transferível diretamente): triagem telefônica digitalmente apoiada na Inglaterra, estudo observacional: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11792721/ ; segurança/acurácia de IA em triagem de pronto-socorro: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12636208/ (li apenas os títulos/resumos nos resultados de busca; resultados quantitativos: **não verificado**).
- Produtos brasileiros de PIMS com triagem por IA no WhatsApp: **não verificado** (não pesquisei de forma exaustiva; vale checar fornecedores de PIMS que você já usa). Não afirmo existência nem ausência.
- Plug-ins de PIMS específicos: **não verificado**.

## 2. Por que essa forma

- O problema central é padronização (o estudo equino mostra isso), e um fluxograma/regra resolve boa parte.
- Workflow determinístico é auditável, barato e testável com mensagens sintéticas.
- LLM agrega onde regra é fraca: texto livre, áudio transcrito, gírias, mensagem longa. Ainda assim como sugestão.
- Planilha/script puro serve para MVP; integração com WhatsApp Business API (custo e aprovação da Meta) fica para fase 2.

## 3. Human-in-the-loop

| Etapa | Quem valida |
|---|---|
| Red flag detectado | Recepção liga ao tutor imediatamente e avisa o vet; sistema nunca "tranquiliza" |
| Sugestão "agendar" ou "orientar" | Recepção confere contra checklist; dúvida escala ao vet |
| Resposta de texto ao tutor | Rascunho; envio só após aprovação humana (fase 1). Autoenvio no máximo para mensagens administrativas (horário, endereço) |
| Orientação clínica | Somente vet |
| Pedido de receita | Nunca automatizar a decisão; apenas registrar e encaminhar ao vet |
| Auditoria | Revisão semanal por amostragem de casos classificados como não urgentes, com foco em falsos negativos |

Resposta ao tutor sempre com aviso de que se trata de triagem/orientação e não de consulta, e com instrução de procurar atendimento se piorar.

## 4. Riscos

**Clínicos**
- Subtriagem (falso negativo) é o risco principal: gato com obstrução urinária, intoxicação, torção gástrica, filhote com vômito/diarreia podem parecer "rotina" no texto. Mitigação: red flags por regra, viés conservador, upgrade-only.
- Tutor omite informação; fotos/áudio ambíguos; espécies exóticas.
- Falso positivo gera sobrecarga, mas é aceitável frente ao outro erro.

**Alucinação**
- LLM pode inventar dose, diagnóstico ou conduta. Mitigação: proibir esses conteúdos no prompt e por filtro de saída; respostas só de modelos pré-aprovados pelo vet; sem acesso a prescrever.

**Legais (CFMV / LGPD / receituário)**
- CFMV Resolução 1.465/2022 (telemedicina veterinária): prevê teleorientação e teletriagem; nelas é obrigatório informar previamente ao responsável que não é consulta, e são vedados diagnóstico, solicitação de exames e qualquer prescrição; presencial é o padrão-ouro. Fonte: https://www.cfmv.gov.br/resolucao-do-cfmv-regulamenta-a-telemedicina-veterinaria/comunicacao/noticias/2022/06/29/ e texto: https://jornal.unesp.br/wp-content/uploads/2022/08/Resolucao_TelemedicinaVeterinaria-1.pdf . Se o resumo estiver incompleto (ex.: exigências de registro/prontuário e responsabilidade do RT), conferir o texto integral: **não verificado em detalhe**.
- Receituário controlado: Portaria SVS/MS 344/1998 exige receita/notificação própria com campos específicos, inclusive identificação do animal (https://www.legisweb.com.br/legislacao/?id=317701). Para medicamentos veterinários sob controle especial, a IN MAPA 35/2017 substituiu a IN 25/2012 segundo os resultados de busca (https://www.crmvpb.org.br/mapa-estabelece-novos-procedimentos-para-comercializacao-de-produtos-de-uso-veterinario/ — conferir norma vigente em 2026: **não verificado**). Conclusão prática: o sistema nunca emite nem promete receita, e pedido de receita de controlado vira apenas tarefa para o vet.
- LGPD (Lei 13.709/2018, https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm): dados do tutor (nome, telefone, endereço, áudio, foto) são pessoais; precisa de base legal e transparência (art. 7); art. 20 dá direito de revisão por pessoa natural de decisões tomadas unicamente por tratamento automatizado — outro motivo para manter humano no circuito. Envio de dados a LLM em nuvem/exterior exige avaliar transferência internacional e contrato com o operador: **não verificado**. Dados do animal em si não são dados pessoais, mas o vínculo com o tutor é.
- WhatsApp: uso comercial automatizado depende dos termos da Meta/API oficial: **não verificado**.

## 5. Pontuação (honesta)

- Impacto: **4/5.** Tempo de recepção/vet liberado e padronização são reais, mas o ganho depende do volume da clínica e de a recepção já não ter um protocolo.
- Viabilidade técnica: **4/5** para regras + rascunho por LLM; **2/5** para autonomia segura com fotos/áudio.
- Risco clínico/legal: **4/5** (alto) se houver autonomia; cai para **2-3/5** com humano validando tudo e sem diagnóstico/prescrição.

## 6. MVP sem dados reais e sem serviços pagos?

**Sim, em parte.** Cabe no repositório:
- Protocolo de triagem em YAML/JSON (red flags, perguntas, categorias) escrito/validado pelo vet.
- Script Python (sem API paga) que classifica por regras e gera registro estruturado + resposta-modelo.
- Conjunto de 50-100 mensagens **sintéticas** em português coloquial (com erros de digitação, áudio transcrito simulado) com gabarito do vet, e métricas: sensibilidade para urgentes (meta: ~100% nos red flags), taxa de superalerta.
- Camada de LLM fica fora do MVP gratuito (ou opcional com modelo local), e integração WhatsApp e PIMS ficam para fase 2.
Limitação: sem dados reais não se mede desempenho verdadeiro; só se valida o protocolo e o fluxo.
