# Aprovar solicitações de receita/renovação de medicação contínua

Domínio: atendimento-tutor. Data da análise: 2026-10-02.

## Aviso sobre fontes (leia primeiro)

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br, fda.gov). **Nenhuma afirmação factual abaixo foi verificada com fonte.** Não cito URLs porque não consegui abrir nenhuma. Tudo que é norma, produto ou estudo está marcado "não verificado" e deve ser conferido antes de uso. Os pontos de raciocínio (arquitetura, riscos) são julgamento meu, não fato pesquisado.

## 1. Soluções existentes

- Produtos/plug-ins de PIMS com fila de pedidos de refill e agentes de IA para atendimento: não verificado (não consegui pesquisar). Sei, de memória e sem fonte, que PIMS e apps de tutor costumam ter "solicitar receita/refill" como formulário que cai numa fila para o veterinário. Tratar como hipótese a confirmar.
- Estudos sobre IA em renovação de receita veterinária: não verificado.
- Ação sugerida: conferir se o PIMS usado pela clínica já tem fila de solicitação de receita e regras de bloqueio por data. Se tiver, a automação é configuração, não desenvolvimento.

## 2. Forma recomendada: workflow determinístico (regras) com triagem; sem agente decisório

Justificativa:
- A decisão central é uma regra checável: medicamento, data da última consulta, data do último exame de monitoramento, categoria (comum ou controlado), limite de prazo definido pela clínica. Isso é tabela de regras + datas, não precisa de LLM.
- Um LLM só se justifica opcionalmente para ler a mensagem livre do tutor e extrair paciente, fármaco e dose em campos estruturados. Mesmo aí, um formulário estruturado resolve com menos risco.
- O sistema nunca emite receita sozinho. Ele classifica o pedido em: (a) elegível, pronto para revisão rápida do veterinário; (b) exige reavaliação/exame antes; (c) controlado ou caso especial, vai direto ao veterinário.

Regras de exemplo (parâmetros da clínica, não normas):
- Cardiotônico (ex.: pimobendana, furosemida, IECA): exigir exame/consulta recente conforme protocolo do clínico (valores de prazo: definir pela clínica; evidência: não verificado).
- Anticonvulsivante (ex.: fenobarbital): monitoramento sérico e hepático conforme protocolo; controlado, sempre humano.
- Antialérgico/imunomodulador: checar última reavaliação.
- Qualquer sinal de piora citado no pedido (palavras-chave como convulsão, tosse, cansaço, vômito) bloqueia a fila rápida e escala para o veterinário.

## 3. Human-in-the-loop, riscos e conformidade

Validação humana obrigatória:
- O veterinário assina e emite toda receita. O sistema apenas pré-organiza: resumo do prontuário (datas, última dose, exames) e recomendação "liberar para revisão" ou "exigir consulta".
- Controlados: nunca automatizar a emissão; fluxo 100% humano com receituário/notificação adequados. A norma aplicável (Portaria SVS/MS 344/98 e regras do CFMV/MAPA para veterinária): não verificado, confirmar texto vigente.
- Se o pedido sai da regra, ou o tutor pressiona por urgência, vai para o humano.

Riscos clínicos:
- Renovar sem reavaliação mascara progressão da doença (cardiopatia, epilepsia, doença renal/hepática) e toxicidade cumulativa. Mitigação: regra de prazo máximo + bloqueio por sintomas.
- Mudança de dose ou de peso do animal desde a última consulta: exigir confirmação do veterinário.
- Interações com medicação nova: o sistema não avalia; humano revisa.

Riscos legais (todos não verificados, conferir):
- CFMV: responsabilidade técnica e exigência de relação clínica prévia/exame do animal para prescrever; regras sobre telemedicina veterinária e prescrição à distância. Verificar resolução vigente.
- Receituário controlado: ver acima.
- LGPD (Lei 13.709/2018): dados do tutor são pessoais; dados de pacientes animais em si não são dados pessoais, mas prontuário vinculado ao tutor é. Se usar LLM em nuvem, definir base legal, minimização (enviar só campos necessários, sem nome/CPF) e contrato com o operador. Detalhes de artigos: não verificado.

Risco de alucinação:
- Núcleo sem LLM elimina o problema de inventar dose ou prazo. Se usar LLM para extrair campos, validar contra o cadastro (animal existe? fármaco consta no prontuário?) e nunca deixar o modelo sugerir fármaco, dose ou prazo.
- Registrar auditoria: quem pediu, regra aplicada, quem aprovou, quando.

## 4. Pontuação (1-5, julgamento próprio, sem base empírica verificada)

- Impacto: 3. Renovações são frequentes e interrompem a rotina, mas a economia real de tempo por pedido é pequena, pois o veterinário ainda revisa e assina. Valor maior está em padronizar e não esquecer reavaliações.
- Viabilidade: 4. Regras + datas + formulário são simples; o difícil é a integração com o PIMS real.
- Risco: 4. Erro leva a renovar medicação cardíaca/anticonvulsivante sem monitoramento, e controlados têm exigência legal. Cai para 3 se for só fila de triagem com assinatura humana.

## 5. MVP em repositório

Cabe, sim, sem dados reais nem serviço pago: script Python (ou planilha) que lê CSV fictício de pedidos + prontuário sintético, aplica tabela de regras (fármaco, categoria, prazo máximo desde última consulta e exame) e gera três filas (revisão rápida, exigir consulta, humano/controlado) com justificativa legível. Testes com casos de borda: exame vencido, palavra de alerta, controlado, paciente inexistente. Sem LLM no MVP. Os prazos das regras no MVP seriam valores de exemplo, não recomendação clínica.
