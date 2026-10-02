# Comunicação de resultados ao tutor (ligação, WhatsApp, e-mail) e orientação

Domínio: exames-imagem. Data: 2026-10-02.

## Aviso sobre fontes
A cota de WebSearch da sessão (200/200) estava esgotada e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br, cfmv.gov.br). Portanto **nenhuma afirmação factual abaixo foi verificada com URL nesta rodada**. Tudo que depende de fonte está marcado "não verificado" e deve ser conferido antes de uso.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com mensagens automáticas ao tutor (lembretes, resultados, WhatsApp): não verificado (sem URL). Exemplos a pesquisar depois: módulos de comunicação dos PIMS veterinários mais usados no Brasil e globalmente.
- Estudos sobre IA redigindo comunicação clínica ao cliente/paciente: não verificado.
- Normas: Código de Ética/resoluções CFMV sobre prontuário e telemedicina veterinária, e LGPD (Lei 13.709/2018): não verificado nesta rodada.

## 2. Forma recomendada: workflow determinístico com rascunho por LLM opcional (não agente autônomo)
Motivo: a comunicação em si é um ato clínico (explicar, justificar conduta, obter autorização) e deve ser feita pelo veterinário. O que se automatiza é o trabalho em volta:
1. Gatilho: laudo/interpretação marcado como "liberado" pelo veterinário.
2. Modelo de mensagem (template com campos: nome do paciente, exame, achado em linguagem leiga já aprovada pelo veterinário, conduta, prazo, opções de retorno).
3. Rascunho gerado a partir do texto que o próprio veterinário aprovou (LLM só reescreve em linguagem leiga, sem acrescentar achados, doses ou prognóstico).
4. Veterinário revisa e envia (ou aprova envio).
5. Registro automático no prontuário: canal, data/hora, texto enviado, resposta/autorização do tutor, retorno agendado.
6. Lembrete/fila de pendências: tutor que não respondeu em X horas volta para a lista da recepção/veterinário.

Não recomendo agente autônomo: risco de alucinação em conteúdo clínico e de envio sem revisão. Um script/planilha com templates já resolve boa parte do valor.

## 3. Human-in-the-loop, riscos
- Validação obrigatória: texto leigo do resultado e a conduta antes de qualquer envio; envio de casos graves/achados inesperados (suspeita de neoplasia, prognóstico reservado) sempre por ligação do veterinário, não por mensagem escrita.
- Autorização de tratamento/novos exames: só vale o consentimento do tutor, registrado por ele (resposta explícita), nunca inferido pela IA.
- Clínico: simplificação excessiva, omissão de incerteza do exame de imagem, atraso por mensagem não lida.
- Alucinação: LLM inventando achado, dose ou prazo. Mitigação: restringir a campos pré-aprovados, sem texto livre novo; diff entre laudo e rascunho.
- Legal: LGPD (dados do tutor e, por vínculo, do paciente; base legal, minimização, operador/fornecedor de LLM e transferência internacional, retenção) e normas CFMV sobre prontuário, sigilo e telemedicina: não verificado, conferir texto atual. Receituário controlado: o fluxo não deve enviar ou gerar receitas controladas por mensagem; isso fica fora do escopo.
- WhatsApp: uso da API oficial/consentimento do tutor para contato por esse canal: não verificado.

## 4. Pontuação
- Impacto: 3/5 (economiza tempo de recepção e registro; a explicação clínica continua humana).
- Viabilidade: 4/5 (templates + registro são simples; integração com PIMS varia).
- Risco: 3/5 (clínico moderado, legal moderado por LGPD/sigilo; cai para 2 se só houver templates fixos).

## 5. MVP sem dados reais e sem serviços pagos
Sim. Um script (Python) ou planilha que: recebe um JSON fictício de "resultado aprovado", preenche templates de mensagem (WhatsApp/e-mail/roteiro de ligação), gera o registro de contato para prontuário e uma fila de pendências, com revisão manual antes do "envio" (simulado, sem enviar). Rascunho por LLM é opcional e pode ficar fora do MVP.
