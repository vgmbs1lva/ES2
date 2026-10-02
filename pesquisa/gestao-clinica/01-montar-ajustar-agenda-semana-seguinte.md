# Montar e ajustar a agenda da semana seguinte

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Aviso de verificação (leia primeiro)

A pesquisa web não pôde ser feita nesta execução: o limite de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br, pmc.ncbi.nlm.nih.gov e outros). Por isso **nenhuma afirmação factual abaixo tem fonte com URL**. Tudo o que depende de fonte está marcado como "não verificado". Antes de decidir qualquer coisa com base neste documento, as seções 1 e 3 precisam ser refeitas com acesso à web.

## 1. Soluções existentes

- Produtos de PIMS com agendamento online, lembretes e lista de espera: não verificado. Não posso afirmar nomes, funcionalidades nem preços. No Brasil, o ponto a checar é se o PIMS que a clínica já usa expõe API ou exportação (CSV/iCal) da agenda.
- Ferramentas genéricas (Google Calendar, planilhas, Calendly e similares): não verificado quanto a recursos e preços para o caso veterinário.
- Literatura sobre previsão de faltas (no-show) e overbooking em ambulatórios humanos: não verificado. Sei que o tema existe, mas não tenho estudo citável nesta sessão.
- Estudos específicos de agenda em clínica veterinária: não verificado.

## 2. Forma recomendada: workflow determinístico (script/regras), com um passo opcional de LLM

Recomendo o mais simples que resolve: um **workflow determinístico** que lê a exportação da agenda, retornos pendentes, cirurgias previstas e escala, e gera uma **proposta** de agenda da semana seguinte. As regras são:

1. Bloquear primeiro as cirurgias previstas (sala, veterinário e anestesista, mais janela de recuperação).
2. Reservar uma cota fixa de slots de emergência/encaixe por veterinário e por turno, definida pela clínica.
3. Alocar retornos pendentes perto da data-alvo, no mesmo veterinário quando possível.
4. Preencher o restante com consultas conforme a escala.
5. Reorganizar após faltas: listar os buracos e sugerir candidatos de lista de espera ou remarcação.

Isso é um problema de alocação com restrições. Regras explícitas são auditáveis e reproduzíveis, e não alucinam. Um agente de IA autônomo não se justifica, porque não há ambiguidade clínica a resolver na montagem da grade.

Onde um LLM pode entrar (opcional, de baixo risco): redigir mensagens de confirmação ou remarcação aos tutores e interpretar pedidos de remarcação em texto livre, sempre como rascunho.

Não recomendo "agente com escrita direta na agenda". A integração direta com o PIMS fica para depois do MVP e depende de a API existir (não verificado).

## 3. Human-in-the-loop, riscos e conformidade

**Onde o veterinário (ou o responsável pela recepção/gestão) valida**
- Aprova a agenda proposta antes de qualquer gravação no sistema (a saída é um diff: o que mudaria).
- Decide a triagem de urgência. O sistema nunca classifica gravidade clínica: quem encaixa uma emergência é a pessoa.
- Valida cirurgias (jejum, pré-operatório, disponibilidade de anestesista) e qualquer remanejamento de procedimento já confirmado.
- Aprova mensagens antes do envio ao tutor.

**Riscos clínicos**
- Retorno de paciente crítico ser empurrado por regra de "preencher buraco". Mitigação: marcar retornos com flag de prioridade clínica, informada por humano, e nunca remanejá-los automaticamente.
- Encaixe de emergência sem slot disponível: manter cota reservada e alerta quando ela acabar.
- Cirurgia sobreposta a consulta do mesmo veterinário: validação por regra de conflito.

**Riscos de alucinação**: baixos na parte determinística. Existem apenas se um LLM for usado para interpretar texto livre ou redigir mensagens. Nesse caso, ele não deve inventar horários: só preenche modelos com slots calculados pelo código.

**Riscos legais (todos não verificados, confirmar na fonte)**
- LGPD (Lei 13.709/2018): a agenda contém dados pessoais do tutor (nome, telefone). Pontos a verificar: finalidade e necessidade, minimização, e contrato/transferência se usar LLM em nuvem. Mitigação prática: enviar ao LLM apenas identificadores pseudonimizados e nenhum dado de contato.
- CFMV: normas sobre prontuário, atendimento e publicidade. A agenda em si provavelmente não é ato médico-veterinário, mas não verifiquei nenhuma resolução específica.
- Receituário controlado: **não se aplica** a esta tarefa. O workflow não deve tocar em prescrição.

## 4. Pontuação (1-5)

| Critério | Nota | Justificativa |
|---|---|---|
| Impacto | 3 | Libera tempo de recepção/gestão toda semana e reduz buracos, mas o ganho é moderado e depende do volume da clínica. Sem dados reais, é estimativa minha. |
| Viabilidade | 4 | Regras simples. O gargalo é obter a exportação da agenda do PIMS (não verificado). |
| Risco | 2 | Sem decisão clínica autônoma; risco principal é priorização errada de retorno, mitigada por validação humana, mais LGPD. |

## 5. Cabe em MVP testável sem dados reais e sem serviços pagos?

**Sim.** Um script em Python (somente biblioteca padrão) que:
- lê CSVs sintéticos (escala de veterinários, cirurgias previstas, retornos pendentes, agenda atual com faltas);
- aplica as regras da seção 2 e gera a agenda proposta mais um relatório de conflitos e buracos;
- tem testes com cenários sintéticos (falta, cirurgia longa, estouro de cota de emergência).

Não precisa de dados de pacientes/tutores nem de serviço pago. O que o MVP não prova: integração com o PIMS real e a qualidade das regras para a rotina da clínica; isso exige piloto com dados reais anonimizados e aprovação do responsável.

## Referências

Nenhuma fonte verificada nesta execução (ver aviso no topo).
