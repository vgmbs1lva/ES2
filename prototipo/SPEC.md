# SPEC do MVP: Fechamento do dia (prontuário x cobrança)

Versão: 0.1 (rascunho para implementação) | Data: 2026-10-02
Origem da escolha: `/home/user/ES2/pesquisa/administrativo/11-fechamento-do-dia-prontuario-e-cobranca.md`

## 0. Decisão em uma linha

Prototipar um **workflow determinístico, local, sem LLM e sem rede**, que cruza três listas (consultas do dia, itens da fatura, regras da clínica), gera uma lista de pendências e **só avança o dia para "conferido" quando um humano decide cada pendência, com motivo registrado**. O programa nunca escreve em prontuário nem em fatura.

Por que este caso (candidato único verificado, escolhido porque cumpre os critérios):
- Valor: fechamento diário e vazamento de cobrança são dor recorrente da clínica. A magnitude (~17% de cobranças diagnósticas não faturadas; 8-15% da receita) vem de fornecedores dos EUA/Europa, sem revisão por pares, e **não vale para o Brasil: não verificado**. Fontes: https://www.dvm360.com/view/missing-charges-your-software-should-help ; https://www.shepherd.vet/blog/how-to-get-15-missed-revenue-back-in-your-veterinary-practice/
- Viabilidade: regras fixas, CSV sintético, Python 3.11 (stdlib), zero custo de API.
- Risco baixo: só lê e sugere; ato clínico e lançamento continuam humanos.
- Padrão workflow + human-in-the-loop: etapas fixas, portões de aprovação, log auditável. Agente autônomo não se justifica (alterar fatura ou fechar prontuário sozinho aumenta risco sem ganho).

Ressalva honesta: o MVP prova a **lógica e o fluxo**, não o **valor** (ganho de tempo e receita recuperada). Isso só se mede com clínica real; ver seção 11 (validação posterior).

---

## 1. Problema

Ao fim do expediente, a clínica precisa saber: (a) quais prontuários continuam abertos ou incompletos, (b) se tudo o que foi atendido foi cobrado, (c) se nada foi cobrado sem ter sido feito, (d) se há item controlado que exige conferência manual. Hoje isso é feito olhando telas do sistema de gestão (PIMS) uma a uma, o que gera esquecimento nos dois sentidos (cobrança perdida e cobrança indevida) e prontuários fechados às pressas ou depois do dia.

Contexto normativo (não parametrizar sem ler o texto oficial):
- Resolução CFMV 1.321/2020: prontuário escrito e datado, assinado exclusivamente pelo médico-veterinário, com data, hora, local e identificação do responsável; guarda mínima de 5 anos. Fontes: https://www.legisweb.com.br/legislacao/?id=480427 ; https://www.normasbrasil.com.br/norma/resolucao-1321-2020_480427.html (conhecidas por resultados de busca; leitura integral não feita).
- Resolução CFMV 1.653/2025 aparece em fonte secundária como atualização que amplia informações obrigatórias: https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ . **Vigência, campos obrigatórios e relação com a 1.321/2020: não verificado.** Por isso a lista de campos obrigatórios é **dado de configuração versionado**, nunca constante no código (RF-07).

## 2. Usuários e papéis

| Papel | Quem | O que faz no fluxo |
|---|---|---|
| `veterinario` | Médico-veterinário responsável pelo atendimento | Revisa e fecha prontuários no PIMS (fora da ferramenta); decide sobre pendências com ato clínico |
| `recepcao` / `financeiro` | Recepção ou financeiro | Decide sobre pendências de cobrança sem ato clínico; lança no PIMS (fora da ferramenta) |
| `responsavel_tecnico` | RT / gestor (opcional) | Lê o relatório e o log de auditoria |

Usuário primário do MVP: o médico-veterinário clínico que quer fechar o dia em minutos, e quem faz a conferência financeira. Persona de teste: clínica pequena, 1 a 3 veterinários, ~20-60 atendimentos/dia.

Limitação assumida: o MVP não tem autenticação. O papel e o nome são **declarados** pelo usuário e registrados (rastro, não segurança). Autenticação real é requisito de produção (seção 8).

## 3. Escopo do MVP

Dentro:
1. Ler 5 CSVs sintéticos (seção 5).
2. Aplicar regras determinísticas e produzir pendências com código, severidade e evidência (linha de origem).
3. Relatório Markdown + CSV, agrupado por veterinário e por tipo.
4. Comando para registrar decisão humana por pendência, em log append-only.
5. Estado do dia: `PENDENTE` ou `CONFERIDO`, recalculado a cada execução.
6. Testes automatizados com dados sintéticos e casos de borda.

Fora de escopo (ver seção 9 para a lista completa): integração com PIMS, LLM, qualquer escrita em prontuário/fatura, baixa de controlados, fiscal, WhatsApp/Drive/e-mail, interface web, autenticação, dados reais.

## 4. Fluxo ponta a ponta

```
[PIMS da clínica]                       (no MVP: CSVs sintéticos em dados_ficticios/)
      | exportação manual (fora do MVP)
      v
 1. verificar  -- lê CSVs, valida formato (falha alto se inválido)
      |
      v
 2. aplica regras determinísticas  --> lista de pendências (cada uma com id estável)
      |
      v
 3. relatório (MD + CSV) + estado do dia = PENDENTE
      |
      v
 4. HUMANO revisa  (portão de aprovação)
      |-- prontuário aberto/incompleto  -> veterinário corrige/fecha NO PIMS
      |-- "possível item não cobrado"   -> recepção/financeiro (e vet se ato clínico) lança NO PIMS
      |-- "possível cobrança indevida"  -> corrige NO PIMS
      |-- controlado                    -> conferência manual contra livro/sistema de controle
      |-- falso positivo                -> "ignorar" COM MOTIVO
      v
 5. decidir  -- registra decisão no log append-only (decisoes.jsonl)
      |
      v
 6. nova execução de `verificar` (após novo export do PIMS)
      -> pendência some se o dado foi corrigido, ou fica "decidida" se ignorada com motivo
      -> estado = CONFERIDO somente quando não resta pendência sem decisão válida
```

Princípio central: **a ferramenta nunca "resolve"; só o dado corrigido no PIMS ou a decisão humana registrada resolve.** Decisão `encaminhado` não encerra a pendência: ela só encerra quando o dado mudar no export seguinte (evita "marquei como feito" sem ter feito).

## 5. Entradas

Todas em UTF-8, CSV com cabeçalho, separador vírgula, datas ISO (`YYYY-MM-DD`), data-hora ISO (`YYYY-MM-DDTHH:MM`). Todos os dados são **fictícios**; identificadores são códigos opacos (`C001`, `V01`), sem nome de tutor, CPF, telefone ou nome real de paciente.

### 5.1 `consultas.csv`
| Coluna | Descrição |
|---|---|
| `consulta_id` | Único no arquivo |
| `data` | Data do atendimento |
| `veterinario_id` | Código do veterinário responsável |
| `status_atendimento` | `realizado` ou `cancelado` |
| `status_prontuario` | `aberto` ou `fechado` |
| `fechado_em` | Data-hora do fechamento (vazio se aberto) |
| `campo_<nome>` | Uma coluna por campo do checklist, valor `S` (preenchido) ou `N` |

### 5.2 `procedimentos_realizados.csv`
`consulta_id`, `procedimento_codigo` (procedimentos registrados no prontuário/atendimento).

### 5.3 `itens_fatura.csv`
`consulta_id`, `item_codigo`, `quantidade` (inteiro > 0).

### 5.4 `regras.csv` (tabela clínica, versionada)
| Coluna | Descrição |
|---|---|
| `procedimento_codigo` | Procedimento que dispara a regra |
| `item_codigo` | Item esperado na fatura |
| `grupo_alternativa` | Linhas do mesmo procedimento com mesmo grupo: basta uma presente |
| `ato_clinico` | `S` se a decisão sobre esta pendência exige `veterinario` |
| `controlado` | `S` se o item é controlado/psicotrópico (alerta manual, seção 6.3) |

### 5.5 `campos_obrigatorios.csv` (checklist, versionado)
`campo`, `fonte_norma`, `versao`. No fixture, `fonte_norma` = `EXEMPLO_FICTICIO`. **A lista do fixture não é a lista oficial do CFMV**; a lista real só entra após leitura do texto oficial (seção 10, R1).

Cabeçalho `# versao=...` não é usado; a versão vai na coluna `versao` e o relatório imprime a versão e o SHA-256 de `regras.csv` e `campos_obrigatorios.csv` usados na execução.

## 6. Regras (requisitos funcionais)

Cada pendência tem: `finding_id` (estável: hash curto de `codigo + consulta_id + chave`), `codigo`, `severidade` (`acao` ou `atencao` ou `info`), `consulta_id`, `veterinario_id`, `evidencia` (arquivo e número da linha), `mensagem`.

### 6.1 Prontuário
| Código | Condição | Severidade |
|---|---|---|
| `P01_PRONTUARIO_ABERTO` | `status_atendimento=realizado` e `status_prontuario=aberto` | acao |
| `P02_PRONTUARIO_INCOMPLETO` | Algum campo do checklist com `N` (lista os campos faltantes), em atendimento `realizado` (revisão 0.2: cancelado não gera P02, senão o dia ficaria bloqueado, pois P02 não é ignorável) | acao |
| `P03_FECHADO_RETROATIVO` | `fechado_em` em data posterior à `data` do atendimento | info (mostra data-hora real; não bloqueia) |

### 6.2 Cobrança (conferência bidirecional)
| Código | Condição | Severidade |
|---|---|---|
| `C01_CONSULTA_SEM_FATURA` | Atendimento `realizado` sem nenhum item de fatura | acao |
| `C02_FATURA_SEM_CONSULTA` | Item de fatura com `consulta_id` inexistente em `consultas.csv` | acao |
| `C03_PROCEDIMENTO_SEM_ITEM` | Procedimento realizado cujo item esperado (ou grupo de alternativas) não está na fatura da consulta. Texto: "possível item não cobrado" | atencao |
| `C04_ITEM_SEM_PROCEDIMENTO` | Item que a tabela de regras associa a um procedimento, cobrado numa consulta sem esse procedimento. Texto: "possível cobrança indevida" | atencao |
| `C05_CANCELADA_COM_ITENS` | Atendimento `cancelado` com itens de fatura | acao |

### 6.3 Controlados
| Código | Condição | Severidade |
|---|---|---|
| `K01_CONTROLADO_CONFERIR` | Qualquer item com `controlado=S` na fatura | acao. Só pode ser encerrado com decisão `conferido_manual`, papel `veterinario`, com motivo. A ferramenta não registra baixa de estoque nem escrituração. |

### 6.4 Requisitos gerais
- **RF-01** Idempotência: mesmos CSVs resultam em relatório byte a byte idêntico (ordem determinística; timestamps de execução ficam fora do corpo comparável ou fixados por parâmetro `--agora`).
- **RF-02** Somente leitura: nenhum arquivo de entrada é modificado.
- **RF-03** Falha alto: arquivo ausente, coluna faltando, `consulta_id` duplicado em `consultas.csv`, valor fora do domínio (`S/N`, `realizado/cancelado`, `aberto/fechado`), `quantidade` não inteira ou ≤ 0, `fechado_em` preenchido com prontuário `aberto` ou vazio com `fechado` => erro com arquivo e linha, código de saída 2, **nenhum relatório parcial**.
- **RF-04** Decisões em `decisoes.jsonl`, append-only. Campos: `finding_id`, `decisao`, `motivo`, `papel`, `responsavel`, `registrado_em`, `hash_regras`.
- **RF-05** Decisões válidas: `ignorar`, `encaminhado` (humano vai corrigir/lançar no PIMS), `conferido_manual` (só K01). Motivo obrigatório (mínimo 10 caracteres não brancos) para `ignorar` e `conferido_manual`.
- **RF-06** Permissões declaradas: pendências `P*` e `K*` e `C*` com `ato_clinico=S` só aceitam decisão de papel `veterinario`; demais `C*` aceitam `recepcao`, `financeiro` ou `veterinario`. `P01`/`P02` **não podem ser ignorados** (só se resolvem fechando/completando no PIMS).
- **RF-07** Checklist e regras vêm só de arquivos; trocar o conteúdo muda o resultado sem alterar código.
- **RF-08** Estado do dia: `CONFERIDO` somente se toda pendência `acao`/`atencao` tem decisão válida terminal (`ignorar` com motivo ou `conferido_manual`) ou deixou de existir. `encaminhado` não é terminal. `info` não bloqueia.
- **RF-09** Decisão presa à evidência: se o conteúdo da pendência mudar entre execuções (ex.: outros campos faltantes), o `finding_id` muda e a decisão antiga **não** se aplica.
- **RF-10** Sem rede: o código não importa `socket`, `urllib`, `http`, `requests`, nem qualquer SDK de LLM.
- **RF-11** Relatório: cabeçalho com data, totais por código, estado do dia, versões/hashes das regras; seções por veterinário; cada pendência com evidência; tabela final "Decisões registradas" com motivo.
- **RF-12** Privacidade: o relatório imprime apenas códigos opacos. O README do protótipo avisa que dados reais não devem ser usados com este MVP.

### 6.5 Interface (CLI)
```
python -m fechamento verificar --data 2026-10-02 --entrada dados_ficticios/ --saida saida/ [--agora ISO]
python -m fechamento decidir --finding F-xxxxxxxx --decisao ignorar|encaminhado|conferido_manual \
       --motivo "texto" --papel veterinario|recepcao|financeiro --responsavel "Nome Ficticio" --saida saida/
```
Saídas: `saida/relatorio_<data>.md`, `saida/pendencias_<data>.csv`, `saida/decisoes.jsonl`.
Códigos de saída de `verificar`: 0 = CONFERIDO; 1 = PENDENTE; 2 = erro de entrada. `decidir`: 0 ok; 3 decisão rejeitada (regra RF-05/06); 2 erro de entrada.

## 7. Onde o humano valida (portões)

| # | Portão | Quem | O que é obrigatório |
|---|---|---|---|
| H1 | Fechar/completar prontuário | `veterinario` | Ação no PIMS; a ferramenta apenas lista. Não preenche, não assina, não permite "ignorar" P01/P02 |
| H2 | Lançar item sugerido como não cobrado (C03) | `recepcao`/`financeiro` (e `veterinario` se `ato_clinico=S`) | Lançamento manual no PIMS; a ferramenta nunca lança |
| H3 | Corrigir cobrança indevida (C04, C05, C02) | `financeiro` (+ `veterinario` se ato clínico) | Correção manual no PIMS |
| H4 | Controlados (K01) | `veterinario` | Conferência contra livro/sistema de controle fora da ferramenta; decisão `conferido_manual` com motivo |
| H5 | Falso positivo | Quem tem permissão do portão correspondente | `ignorar` com motivo registrado e auditável |
| H6 | Encerramento do dia | Humano que roda a nova `verificar` | Estado `CONFERIDO` só com tudo tratado; relatório arquivado |

## 8. Requisitos não funcionais

- Python >= 3.11, **somente biblioteca padrão** (testes com `unittest`).
- Execução local e offline; sem custo de API.
- Determinismo e legibilidade: regras em módulos pequenos, uma função por código.
- Estrutura sugerida: `prototipo/fechamento/` (pacote), `prototipo/dados_ficticios/`, `prototipo/tests/`, `prototipo/README.md`.
- Requisitos de **produção** (fora do MVP, registrados para não se perderem): autenticação e autorização reais, integração/exportação do PIMS, retificação de prontuário sem apagar histórico, LGPD (base legal e minimização se algum dado sair da máquina), retenção do log.

## 9. Fora de escopo (explícito)

1. Integração com qualquer PIMS (SimplesVet, Vetsmart, VetSoft ou outro). Cobertura de exportação estruturada desses sistemas: **não verificado**.
2. Etapa com LLM (sugerir item a partir de texto livre). Se existir no futuro: só sugestão ancorada em trecho citado do prontuário, sem trecho sem sugestão, nunca lançamento automático, e avaliação LGPD antes de enviar dados a API externa.
3. Escrever, alterar, preencher ou assinar prontuário; lançar ou editar fatura.
4. Baixa de estoque, escrituração e receituário de controlados (K01 apenas alerta).
5. Conformidade fiscal, Código de Defesa do Consumidor, LGPD em produção (textos não consultados: não verificado).
6. WhatsApp, Drive, e-mail, interface web, painel, multiusuário, autenticação.
7. Medição de ganho de tempo ou receita recuperada.
8. Qualquer dado real de paciente ou tutor.

Nota de revisão 0.2 (desvio conhecido): o protótipo inclui, além desta SPEC, os comandos `rascunho`, `aprovar`,
`rejeitar` e `exportar` e o adaptador opcional `adaptadores/anthropic_redator.py` (redação de rascunhos atrás de
portão de aprovação do veterinário). Não são cobertos por AC-01 a AC-21 (têm testes próprios) e não fazem parte
do MVP a ser medido: o núcleo (verificar/decidir) segue sem LLM e sem rede (RF-10, AC-19). Ver README, "Desvios".

## 10. Riscos e mitigação

| # | Risco | Mitigação no MVP |
|---|---|---|
| R1 | Checklist de campos desatualizado em relação às Res. CFMV 1.321/2020 e 1.653/2025 (não lidas integralmente) | Checklist em arquivo versionado com `fonte_norma`; fixture marcado `EXEMPLO_FICTICIO`; relatório imprime versão/hash; leitura do texto oficial é pré-requisito de uso real |
| R2 | Cobrança indevida por automação/alucinação | Sem LLM; sem escrita na fatura; texto "possível"; decisão humana obrigatória |
| R3 | Prontuário preenchido às pressas ou retroativo para "zerar" a lista | Ferramenta não preenche nada; P03 mostra data-hora real do fechamento; P01/P02 não são ignoráveis |
| R4 | Fadiga de alerta por tabela de regras desatualizada | Regras em CSV simples de manter; `ignorar` exige motivo; relatório mostra taxa de ignorados por regra (insumo para ajustar a tabela) |
| R5 | "Marquei como feito" sem ter feito | `encaminhado` não encerra; só o dado corrigido no export seguinte encerra |
| R6 | Controlado tratado como rotina | K01 sempre acao, só `veterinario`, só `conferido_manual` com motivo; a ferramenta não toca em baixa |
| R7 | Vazamento de dado pessoal (LGPD) | Núcleo local e offline (RF-10); apenas códigos opacos; dados reais proibidos no MVP |
| R8 | Papel declarado sem autenticação (qualquer um diz ser veterinário) | Documentado como limitação; registrado no log; autenticação é requisito de produção |
| R9 | Premissa de que o PIMS exporta consultas, procedimentos e itens com `consulta_id` comum | Não verificado; é a principal hipótese a validar antes de investir (seção 11) |
| R10 | Possível redundância com recursos nativos do PIMS (ex.: lançamento da venda pelo prontuário, conciliação: https://simples.vet/funcionalidades/prontuario-medico/, descrição comercial, não testado) | Validar com clínicas se o PIMS já cruza prontuário x fatura |
| R11 | Números de impacto não aplicáveis ao Brasil | Spec não promete ganho; tratado como hipótese |

## 11. Critérios de aceite testáveis

Fixture `dados_ficticios/` (1 dia, `2026-10-02`, ~14 consultas sintéticas) construído para exercitar cada código. Cada critério é verificável por teste automatizado `unittest` comparando saída com valores esperados.

Casos do fixture (consulta -> pendências esperadas):

| consulta | Situação construída | Esperado |
|---|---|---|
| C001 | Tudo correto: fechada, campos completos, fatura coerente | nenhuma pendência |
| C002 | Realizada, prontuário `aberto` | P01 |
| C003 | Fechada, falta 1 campo (`campo_*` = N) | P02 (lista o campo) |
| C004 | Fechada, 2 campos faltando | P02 (lista os 2) |
| C005 | Fechada em `2026-10-03T08:00` (dia seguinte) | P03 (info) |
| C006 | Realizada, nenhum item de fatura | C01 |
| C007 | Procedimento com item esperado ausente | C03 |
| C008 | Procedimento com grupo de alternativas e uma alternativa presente | nenhuma pendência |
| C009 | Item mapeado a procedimento que não consta nos realizados | C04 |
| C010 | Cancelada com item de fatura | C05 |
| C011 | Cancelada sem itens | nenhuma pendência |
| C012 | Fatura com item de controlado | K01 |
| C013 | Prontuário aberto + sem fatura | P01 e C01 (ambas) |
| (linha extra) | Item de fatura com `consulta_id=C999` inexistente | C02 |

Critérios:

- **AC-01** `verificar` no fixture produz exatamente o conjunto de pendências da tabela acima (códigos e `consulta_id`), nem mais nem menos.
- **AC-02** C001, C008 e C011 não geram nenhuma pendência (anti falso positivo).
- **AC-03** C013 gera P01 e C01 separadamente (regras independentes).
- **AC-04** P02 lista nominalmente todos os campos faltantes (C004: 2 campos).
- **AC-05** Cada pendência traz arquivo e número de linha de origem; teste confere que a linha citada contém o `consulta_id`.
- **AC-06** Duas execuções com os mesmos CSVs e `--agora` fixo geram `relatorio_*.md` e `pendencias_*.csv` com SHA-256 idêntico (RF-01).
- **AC-07** SHA-256 de todos os CSVs de entrada é igual antes e depois de `verificar` e de `decidir` (RF-02).
- **AC-08** Entradas inválidas (um teste por caso: arquivo ausente, coluna faltando, `consulta_id` duplicado, `S/N` inválido, `quantidade=0`, `aberto` com `fechado_em`) => saída 2, mensagem com arquivo e linha, **sem** `relatorio_*.md` criado (RF-03).
- **AC-09** Estado do dia: com pendências sem decisão => código de saída 1 e `PENDENTE`; com todas tratadas => 0 e `CONFERIDO`.
- **AC-10** `decidir --decisao ignorar` sem motivo ou com motivo < 10 caracteres úteis => saída 3 e nada gravado no log.
- **AC-11** `decidir` sobre P01 ou P02 com `ignorar` => saída 3 (não ignoráveis).
- **AC-12** `decidir` sobre K01 com papel `recepcao` => saída 3; com `veterinario` + `conferido_manual` + motivo => saída 0 e K01 passa a "decidida" na nova execução.
- **AC-13** `decidir` sobre C03 cuja regra tem `ato_clinico=S` com papel `financeiro` => saída 3; com `veterinario` => saída 0.
- **AC-14** `encaminhado` não encerra: após `encaminhado` sem alterar o CSV, C03 continua pendente e o estado segue `PENDENTE`; após adicionar o item em `itens_fatura.csv` e rodar de novo, C03 desaparece.
- **AC-15** `ignorar` válido em C04: na nova execução a pendência aparece como "decidida" com motivo, responsável e papel, e não conta como aberta.
- **AC-16** Decisão presa à evidência: após `ignorar` em P02 (se permitido por teste de unidade da função, não pela CLI, ver AC-11) ou em C03/C04, alterar o dado de modo que o conteúdo da pendência mude (ex.: outro item faltando) gera novo `finding_id` e a decisão antiga não se aplica.
- **AC-17** `decisoes.jsonl` é append-only: `decidir` nunca reescreve linhas anteriores (teste compara prefixo do arquivo antes e depois).
- **AC-18** Trocar uma linha de `campos_obrigatorios.csv` (adicionar um campo) muda o resultado de P02 sem alteração de código (RF-07); relatório mostra o novo hash.
- **AC-19** Teste estático: nenhum módulo do pacote importa `socket`, `urllib`, `http`, `requests`, `anthropic`, `openai` (RF-10).
- **AC-20** O relatório não contém padrões de dado pessoal: o fixture só contém códigos opacos e um teste verifica que as colunas de entrada aceitas não incluem campos de nome/CPF/telefone.
- **AC-21** Controle de qualidade do código: `python -m unittest discover` passa com 0 falhas em ambiente sem rede.

Critério de "MVP pronto": AC-01 a AC-21 passando e um passo-a-passo no README que reproduz o fluxo completo (verificar, decidir, verificar de novo) no fixture em menos de 5 minutos.

## 12. Validação posterior (fora do MVP, antes de investir em produto)

Com 2 ou 3 clínicas, sem coletar dado de paciente: (1) qual PIMS usam e se exporta CSV/API com identificador comum de consulta; (2) se o PIMS já faz o cruzamento prontuário x fatura; (3) quanto tempo leva o fechamento hoje (cronometrar). Se o PIMS já resolve ou não exporta dado estruturado, o valor incremental do workflow cai. Esse resultado é o que realmente confirma ou refuta o Impacto 4 da pesquisa.

## 13. Verificação desta spec (transparência)

Nesta rodada o orçamento de WebSearch estava esgotado e o WebFetch foi bloqueado pelo proxy para vários domínios; as fontes acima vêm do arquivo de pesquisa do repositório e **não foram reabertas**. Itens como o texto oficial das Res. CFMV 1.321/2020 e 1.653/2025, LGPD, CDC, normas de controlados (MAPA/ANVISA), cobertura dos PIMS brasileiros e números de perda de receita no Brasil estão **não verificados** e não sustentam nenhuma regra do MVP além do que está marcado como configuração.
