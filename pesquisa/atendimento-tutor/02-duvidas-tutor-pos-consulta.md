# Responder dúvidas de tutores de pacientes em tratamento (pós-consulta)

Data da análise: 2026-10-02. Domínio: atendimento-tutor.

Nota de método: a busca web funcionou, mas o WebFetch foi bloqueado pelo proxy (crmvpb.org.br, doi.org). Só li trechos de resultados de busca, não os textos integrais. O que depende de ler o texto integral está marcado "não verificado".

## 1. Soluções existentes

- Chatbots de pós-consulta integrados a PIMS: respondem dúvidas de protocolo (horário da medicação, efeitos leves comuns) e escalam respostas preocupantes para a equipe. Exemplo: Tails AI da Digitail, integrada ao PIMS deles. Fontes: https://digitail.com/blog/ai-in-veterinary-clinics-20-use-cases-transforming-practice-workflows/ e https://www.vetsoftwarehub.com/article/veterinary-ai-messaging-save-staff-time
- Chatbots genéricos de FAQ e recepção por SMS/telefone: https://sitespeak.ai/for-veterinary e https://www.puppilot.co/blog/ai-chatbot-for-animal-hospitals-from-basic-faq-to-true-clinical-support-partner. São páginas de fornecedores (marketing); não achei validação independente. Nenhum produto verificado em português nem com integração a PIMS brasileiros.
- Estudos de LLM em comunicação com tutor:
  - Odontologia veterinária (2026): seis FAQs em vários LLMs; houve imprecisões clinicamente relevantes em vários modelos, por exemplo sobre anestesia geral com via aérea protegida. https://doi.org/10.1177/08987564261424454 (só o resumo da busca).
  - Folhetos para tutores gerados por ChatGPT em medicina interna, J Vet Intern Med: considerados úteis, precisos e fáceis de entender. https://academic.oup.com/jvim/article/40/1/aalaf058/8429719
  - Revisão sistemática de IA em saúde digital veterinária: https://pmc.ncbi.nlm.nih.gov/articles/PMC13467759/
  - Intenção de uso de chatbots em consulta veterinária (satisfação ligada à precisão e completude percebidas): https://www.sciencedirect.com/science/article/pii/S2444569X20300366
- Lacuna: não encontrei estudo que meça segurança de respostas a mensagens pós-consulta com prontuário e prescrição reais. As evidências são sobre FAQ genérica ou folhetos.

## 2. Norma (CFMV)

- Resolução CFMV 1465/2022 (27/06/2022) regulamenta a telemedicina veterinária. Prevê teleconsulta, teleorientação e teletriagem; o atendimento presencial é o padrão-ouro; o médico-veterinário tem autonomia e responde integralmente pelo ato. Fontes: https://www.legisweb.com.br/legislacao/?id=433219 e https://www.crmvpb.org.br/resolucao-do-cfmv-regulamenta-a-telemedicina-veterinaria/
- Não verificado (texto integral não lido): exigências de prontuário, consentimento, sigilo e prescrição remota. Conferir no PDF do DOU antes de implantar: https://static.poder360.com.br/2024/10/Resolucao-CFMV-1465-2022.pdf
- Leitura prática: a mensagem pós-consulta de paciente em tratamento é ato do veterinário responsável. A IA só pode ser ferramenta de rascunho; quem responde é o profissional.
- LGPD e receituário controlado: não pesquisei fontes. Não verificado. Princípio de cautela: dados do tutor são pessoais (LGPD); a IA nunca deve alterar dose nem orientar medicamento controlado.

## 3. Forma recomendada: workflow com rascunho assistido (human-in-the-loop obrigatório)

Não é agente autônomo. Pipeline determinístico com um passo de LLM:

1. Entrada: mensagem do tutor + resumo estruturado do caso (diagnóstico, prescrição vigente, orientações de alta, sinais de alerta combinados).
2. Triagem determinística por regras e palavras-chave (não pelo LLM): sinais de alerta (dispneia, convulsão, sangue, vômitos repetidos, apatia grave, anorexia prolongada em gato, toxicose, dor intensa, medicamento controlado, mudança de dose). Se disparar, vai para prioridade/humano, com sugestão de antecipar retorno ou urgência, sem rascunho automático de tranquilização.
3. Se não disparar, o LLM gera rascunho ancorado SÓ no resumo do caso e na prescrição fornecida, com instrução de dizer "preciso confirmar com o veterinário" quando faltar informação, sem inventar dose.
4. O veterinário revisa, edita e envia (texto ou áudio). Nada sai sem aprovação.
5. Registro: nota de prontuário rascunhada (mensagem, resposta, decisão: manter conduta ou antecipar retorno), confirmada pelo veterinário.

Por que não mais simples (planilha/script): a variedade de mensagens exige linguagem natural. Por que não agente: não há ação que justifique autonomia; o risco clínico exige humano no envio.

Alternativa mínima: modelos de resposta (macros) por protocolo/medicação + checklist de sinais de alerta, sem LLM. Resolve boa parte das perguntas repetitivas e é um bom ponto de partida.

## 4. Riscos

- Clínico: tranquilizar indevidamente ("é normal") quando é sinal precoce de piora; alucinação de dose, interação ou administração com alimento; falta de contexto (a mensagem do tutor é curta e subjetiva).
- Legal: responsabilidade integral do veterinário (CFMV 1465/2022); rastreabilidade do ato no prontuário; LGPD (dados do tutor/WhatsApp enviados a API de terceiro: base legal, minimização, contrato/operador, possível transferência internacional; não verificado em fonte); medicamentos controlados fora do escopo.
- Alucinação: estudos mostram imprecisões relevantes mesmo em FAQ simples (odontologia, link acima). Mitigação: ancorar no prontuário, recusar fora do escopo, avaliar com casos de teste.
- Operacional: tutor interpretar rascunho como atendimento 24h; definir horário e canal de urgência.

## 5. Pontuação (honesta)

- Impacto: 3/5. Economiza tempo repetitivo e melhora adesão, mas o veterinário continua revisando cada mensagem; o ganho é de redação, não de decisão.
- Viabilidade: 4/5 para rascunho assistido; 2/5 para integração real com PIMS/WhatsApp.
- Risco: 4/5 (clínico/legal), controlável com o desenho acima.

## 6. MVP sem dados reais e sem serviço pago

Cabe, em parte. Dá para fazer: base de casos sintéticos (5 a 10 prescrições fictícias), regras de triagem de sinais de alerta em script Python, macros de resposta por medicação/protocolo, gerador de nota de prontuário em template, e conjunto de 30 a 50 mensagens sintéticas para avaliar a triagem (recall de alertas). A etapa de LLM exige API (normalmente paga) ou modelo local; sem isso, o MVP fica em regras e macros, que já é testável. Não cabe sem dados reais: avaliar qualidade real das respostas e integração com PIMS/WhatsApp.
