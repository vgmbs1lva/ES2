# Triagem e conferência de resultados laboratoriais antes de liberar ao clínico

Domínio: exames-imagem | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch (200/200) estava esgotado e o WebFetch foi bloqueado pelo proxy (idexx.com, planalto.gov.br). **Nenhuma afirmação factual externa foi verificada com URL.** Tudo abaixo sobre produtos, estudos e normas está marcado "não verificado" e deve ser pesquisado antes de uso. O restante é raciocínio de engenharia, não afirmação factual.

## 1. Soluções existentes
- Integração de analisadores/laboratórios de referência com PIMS (importação automática de resultados, flags de anormal/crítico): não verificado. Candidatos a pesquisar: portal/integração dos grandes laboratórios veterinários e seus conectores para PIMS; os fabricantes dos analisadores internos (HL7/ASTM/CSV) e o seu PIMS.
- Conceitos de laboratório clínico humano aplicáveis (autoverificação, delta check, valores críticos, identificação do paciente): não verificado; buscar CLSI AUTO10/EP33 e literatura de erros pré-analíticos.
- Normas brasileiras (CFMV sobre prontuário, LGPD arts. 6 e 46, uso de IA): não verificado.

## 2. Forma recomendada: workflow determinístico (script + planilha de regras), com LLM opcional apenas para extrair texto de PDF
Justificativa: a tarefa é de conferência por regra (ID bate? espécie bate? exame recebido = exame pedido? valor fora do limiar crítico?). Isso é comparação de campos e limiares, onde determinismo é auditável e não alucina. LLM só entra para parsear PDFs heterogêneos, e sua saída é conferida por regras (todo número extraído deve ser localizado literalmente no texto do PDF). Agente autônomo não se justifica. Se o PIMS e o laboratório já oferecem integração, a melhor solução é a integração nativa e este workflow vira apenas camada de checagem.

Pipeline:
1. Entrada: arquivo (CSV/JSON do analisador ou PDF) + pedido na ficha (campos estruturados).
2. Extração para esquema fixo (analito, valor, unidade, referência, espécie, ID, data).
3. Regras: (a) ID da ficha e nome/espécie coincidem, senão BLOQUEIA; (b) analitos pedidos vs. recebidos (faltante/extra); (c) unidade reconhecida; (d) valor vs. limiares críticos configurados pelo clínico por espécie; (e) delta check opcional vs. resultado anterior do mesmo paciente.
4. Saída: relatório "conferido / pendente / divergente" e lista de críticos no topo.

## 3. Human-in-the-loop e riscos
- O veterinário libera/assina todo resultado; a automação nunca vincula sozinha em caso de divergência de ID e nunca interpreta clinicamente nem sugere conduta/dose.
- Valores críticos: alerta imediato ao clínico, com confirmação de leitura registrada. Limiares são definidos e aprovados pelo responsável técnico, não pelo modelo.
- Risco clínico: vincular resultado ao paciente errado (mitigação: chave dupla, ID + espécie + nome, bloqueio na dúvida); falso negativo de crítico por unidade/extração errada (mitigação: valor extraído deve existir literalmente no original; sempre exibir o original ao lado).
- Alucinação: eliminada por regras e verificação literal; LLM nunca preenche campo ausente (fica "não encontrado").
- LGPD: dados de tutor (nome, contato) são pessoais; minimizar, processar localmente, sem enviar a API externa sem base legal e contrato. Detalhes de artigos: não verificado.
- CFMV: resultados fazem parte do prontuário; guarda e responsabilidade do médico-veterinário. Resolução aplicável: não verificado.
- Receituário controlado: não se aplica a esta tarefa; o sistema não deve gerar prescrição.

## 4. Pontuação
- Impacto: 3 (poupa tempo de conferência e reduz risco de troca/atraso de crítico; ganho limitado em clínica pequena)
- Viabilidade: 4 (regras simples; parsing de PDF é o ponto frágil; integração real depende do PIMS)
- Risco: 3 (erro de vínculo ou crítico perdido tem consequência clínica, mitigado por bloqueios e revisão humana)

## 5. MVP sem dados reais e sem serviços pagos
Sim. Em Python local: gerador de resultados **sintéticos** (CSV/JSON e PDFs fictícios com IDs inventados), tabela YAML/planilha de limiares críticos de exemplo (valores fictícios, a serem substituídos pelos do clínico), regras de conferência e relatório em texto/HTML. Testes unitários cobrindo: ID divergente, espécie divergente, exame faltante, unidade desconhecida, valor crítico, PDF ilegível. Sem LLM no MVP; extração de PDF textual com biblioteca livre.
