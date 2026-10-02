# Seguimento de alterações e exames de controle (recheck)

Domínio: exames-imagem | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch estava esgotado (200/200) e nenhuma fonte pôde ser aberta. **Nenhuma afirmação factual externa foi verificada com URL.** Produtos, estudos e normas abaixo estão como "não verificado" e precisam ser pesquisados antes de decisão. O restante é raciocínio de engenharia.

## 1. Soluções existentes (todas: não verificado)
- Módulos de lembrete/retorno e agenda em PIMS (inclusive brasileiros como Simples Vet, SoftVet, Vetsoft): não verificado se permitem "pendência de recheck" vinculada a um analito. Primeiro passo: checar o PIMS já em uso, pois a solução mais simples é a nativa.
- Lembretes por SMS/WhatsApp/e-mail de PIMS ou ferramentas de CRM: não verificado.
- Estudos sobre adesão de tutores a retornos e o efeito de lembretes: não verificado; buscar em PubMed/JAVMA/JVIM.
- Normas: CFMV (prontuário e responsabilidade), LGPD (bases legais, comunicação ao titular, consentimento para contato): não verificado, conferir texto oficial.

## 2. Forma recomendada: script/planilha com workflow determinístico (sem agente)
O núcleo é uma lista de pendências com regras de data (alteração X, repetir em N dias), cruzamento com a agenda e comparação numérica com resultado anterior. É tudo determinístico e auditável; LLM não é necessário. O LLM, se usado, apenas redige mensagem ao tutor a partir de modelo, e o texto é revisado/aprovado pela clínica. Agente autônomo não se justifica: contato com tutor e conduta são atos da clínica.

Fluxo:
1. Clínico marca no prontuário: analito, valor, motivo, intervalo sugerido por ele, prazo de tolerância.
2. Script gera a lista diária: a vencer, vencidos, agendados, resolvidos (resultado novo recebido).
3. Para cada resolvido, calcula delta e tendência (série de valores, variação absoluta e percentual) e mostra gráfico/tabela; não classifica melhora/piora clínica.
4. Para vencidos sem retorno, gera rascunho de mensagem; a recepção envia após aprovação.
5. Escalonamento: após N tentativas, aviso ao veterinário, que decide (ex.: registrar recusa/ciência do tutor).

## 3. Human-in-the-loop e riscos
- Veterinário define o que é recheck e o intervalo; a automação nunca decide prazo clínico nem interpreta tendência como diagnóstico ou ajuste de dose.
- Mensagens ao tutor: aprovadas por humano; conteúdo mínimo (convite para retorno), sem valores de exame nem detalhes clínicos por canais inseguros.
- Risco clínico: falso "resolvido" por casar resultado de outro paciente/analito (mitigar com chave dupla e unidade); alerta perdido por falha do script (mitigar com painel de pendências visível e checagem de última execução); unidades diferentes entre laboratórios afetam o delta (normalizar ou bloquear).
- Alucinação: inexistente nas regras; se houver LLM na redação, restringir a modelo com campos e proibir inclusão de dado clínico.
- LGPD: telefone/nome de tutor são dados pessoais; base legal e canal de contato a validar; minimizar, armazenar local, sem enviar a API externa sem contrato. Artigos específicos: não verificado.
- CFMV: registro da recomendação de retorno e da tentativa de contato no prontuário; responsabilidade permanece do médico-veterinário. Resolução aplicável: não verificado.
- Receituário controlado: fora do escopo; o sistema não prescreve nem renova receita. Não vincular "recheck" a renovação automática de medicamento.

## 4. Pontuação
- Impacto: 3 (reduz perda de seguimento e tempo de recepção; ganho clínico real, mas depende de adesão do tutor)
- Viabilidade: 4 (lógica simples; o gargalo é obter dados estruturados do PIMS)
- Risco: 2 (baixo se limitado a lembrete e tabela; sobe se enviar mensagens sem revisão ou interpretar tendências)

## 5. MVP sem dados reais e sem serviços pagos
Sim. Python local ou planilha com: pacientes e resultados **sintéticos** (IDs inventados), tabela de pendências, cálculo de vencimento, delta/tendência, rascunhos de mensagem por modelo (arquivo, sem envio real) e relatório diário em HTML/CSV. Testes: recheck vencido, resultado novo resolve, unidade divergente bloqueia, paciente duplicado, tentativas esgotadas escalam ao veterinário. Sem integração real com WhatsApp/PIMS no MVP.
