# Seguimento de achados incidentais e achados de imagem que exigem reavaliação

Domínio: exames-imagem | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch estava esgotado (200/200) e WebFetch foi bloqueado pelo proxy de saída (PubMed, Planalto). **Nenhuma afirmação factual externa foi verificada com URL.** Tudo que cita produto, estudo ou norma está como "não verificado". O restante é raciocínio de engenharia e deve ser lido assim.

## 1. Soluções existentes (todas: não verificado)
- Medicina humana: existem programas de "closed-loop" para achados incidentais (rastreamento de recomendações de seguimento em laudos radiológicos, às vezes com NLP para extrair a recomendação). Não verificado; buscar em PubMed por "incidental findings follow-up tracking radiology". Úteis como modelo de fluxo, não como produto veterinário.
- PIMS veterinários (inclusive brasileiros): módulos de lembrete/retorno e agenda podem permitir "pendência" com data. Não verificado se há campo específico para achado de imagem. Primeiro passo: checar o PIMS em uso.
- Estudos veterinários sobre taxa de seguimento de achados incidentais e adesão a reavaliação: não verificado.
- Normas: CFMV (prontuário, responsabilidade do médico-veterinário), LGPD (Lei 13.709/2018, dados do tutor), recomendações de seguimento (ex.: critérios por tipo de lesão) em literatura de diagnóstico por imagem veterinário: não verificado.

## 2. Forma recomendada: script/planilha com workflow determinístico (sem agente)
O núcleo é um registro estruturado de achados com regras de data (reavaliar em N dias/semanas, por modalidade ou citologia) e cruzamento com a agenda. Tudo determinístico e auditável. O intervalo de reavaliação é decisão clínica do veterinário, não sai de LLM.

Papel opcional de LLM (não necessário no MVP): extrair candidatos a achado de texto livre do laudo (nódulo, massa, linfonodo, cálculo, medidas) para **pré-preencher** o registro, sempre com confirmação humana campo a campo. Agente autônomo não se justifica: agendar, contatar tutor e definir conduta são atos da clínica.

Fluxo:
1. Veterinário (ou radiologista) marca no laudo/prontuário: achado, órgão, lado, medida, data do exame, intervalo sugerido, modalidade de controle (US, RX, TC, citologia), prioridade, prazo de tolerância.
2. Script gera lista diária: a vencer (ex.: 14 dias), vencidos, agendados, concluídos.
3. Concluído = novo exame registrado com vínculo ao achado; o sistema exibe medidas anteriores e atuais lado a lado e o delta aritmético, sem classificar progressão.
4. Vencido sem agendamento: rascunho de mensagem ao tutor por modelo fixo; recepção envia após aprovação.
5. Escalonamento após N tentativas: aviso ao veterinário, que registra recusa/ciência do tutor.

## 3. Human-in-the-loop e riscos
- Veterinário valida: cada achado registrado, intervalo e modalidade, texto ao tutor, e qualquer fechamento do item (resolvido/descartado).
- Mensagem ao tutor: mínima ("recomendamos retorno para reavaliação do exame de DATA"), sem descrever achado/suspeita por canal inseguro.
- Risco clínico: item perdido por falha de transcrição do laudo (mitigar: confirmação dupla e painel de pendências com "última execução"); casar exame de outro paciente ou outro nódulo/lado (chave paciente + órgão + lado + identificador do achado); achados múltiplos no mesmo órgão confundidos; medidas em unidades/planos diferentes entre exames e examinadores (exibir, não concluir).
- Alucinação: nula nas regras; se LLM extrair do laudo, risco de inventar medida/lado ou omitir achado. Mitigar: exigir citação literal do trecho, validar contra o texto, nunca gravar sem aprovação.
- LGPD: nome/telefone do tutor são dados pessoais; definir base legal e canal de contato, minimizar, armazenar local, não enviar laudos a API externa sem contrato. Artigos específicos: não verificado.
- CFMV: registrar no prontuário a recomendação de seguimento e as tentativas de contato; responsabilidade permanece do médico-veterinário. Resolução aplicável: não verificado.
- Receituário controlado: fora do escopo; nada de prescrição ou renovação.
- Risco legal adicional: lista que "garante" prazo cria expectativa de vigilância; deixar claro que é apoio, com dono nomeado por item.

## 4. Pontuação
- Impacto: 4 (achado incidental perdido é falha silenciosa e potencialmente grave, ex.: massa não reavaliada; ganho em segurança e retenção, mas depende de adesão do tutor)
- Viabilidade: 4 (lógica simples; gargalo é obter achados estruturados, o que exige disciplina de registro ou extração assistida)
- Risco: 2 (baixo com regras e revisão humana; sobe para 3 se houver extração por LLM ou envio automático ao tutor)

## 5. MVP sem dados reais e sem serviços pagos
Sim. Python local ou planilha com pacientes e achados **sintéticos**: tabela de achados, cálculo de vencimento por intervalo, lista diária (a vencer/vencido/agendado/concluído), comparação de medidas em série, rascunhos de mensagem por modelo (arquivo, sem envio), relatório HTML/CSV. Testes: achado vencido, novo exame conclui apenas o achado correto (órgão/lado), dois nódulos no mesmo órgão, tentativas esgotadas escalam ao veterinário, achado sem intervalo bloqueia o registro. Extração por LLM e integração com PIMS/WhatsApp ficam fora do MVP.
