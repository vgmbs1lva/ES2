# Fechamento do dia (prontuário x cobrança) — MVP

Protótipo em Python 3 puro (stdlib), local e offline. Cruza três listas (consultas do dia, itens da fatura,
regras da clínica), gera pendências com evidência (arquivo e linha) e só marca o dia como `CONFERIDO` quando um
humano decide cada pendência com motivo registrado. Especificação: [`SPEC.md`](SPEC.md).

> **AVISO — somente dados fictícios.** Os dados de `exemplos/dados_ficticios/` são inventados. Não use este MVP
> com dados reais de pacientes ou tutores (sem autenticação, sem avaliação LGPD). O checklist de campos do
> exemplo é `EXEMPLO_FICTICIO` e **não é a lista oficial do CFMV** (ver "Limitações").

## O que ele faz e o que nunca faz

- Lê 5 CSVs, valida (falha alto, saída 2, sem relatório parcial) e aplica 9 regras determinísticas
  (P01–P03 prontuário, C01–C05 cobrança, K01 controlados).
- Gera `relatorio_<data>.md` e `pendencias_<data>.csv` (byte a byte idênticos para a mesma entrada e `--agora`).
- Registra decisões humanas em `decisoes.jsonl` (append-only).
- **Nunca** escreve em prontuário nem em fatura, nunca envia nada a tutor, nunca dá baixa em controlado,
  nunca altera os CSVs de entrada. **Nenhuma** dose ou conduta clínica está embutida no código.

## Requisitos

Python >= 3.11, só biblioteca padrão. Testes com `unittest` (pytest não é necessário). Nenhuma rede.

## Uso rápido (passo a passo, menos de 5 minutos)

Rode a partir da pasta `prototipo/`. Os identificadores `F-...` abaixo são determinísticos para o exemplo
(também estão na coluna `finding_id` de `saida/pendencias_2026-10-02.csv`).

```bash
cp -r exemplos/dados_ficticios meus_dados          # cópia para poder "corrigir o PIMS" sem mexer no exemplo

# 1) Verificar. Sai com código 1 (PENDENTE) enquanto houver pendência sem decisão.
python -m fechamento verificar --data 2026-10-02 --entrada meus_dados --saida saida/ --agora 2026-10-02T19:00
#    -> Estado do dia 2026-10-02: PENDENTE (11 pendencia(s) aberta(s), 12 total)
#    leia saida/relatorio_2026-10-02.md

# 2) Decisões humanas (papel e nome são DECLARADOS; ver Limitações)
python -m fechamento decidir --finding F-f8c1327d --decisao ignorar --papel financeiro \
   --responsavel "Fulano Ficticio" --motivo "item faturado em pacote, conferido com o financeiro" --saida saida/
python -m fechamento decidir --finding F-b43d2caf --decisao ignorar --papel veterinario \
   --responsavel "Vet Ficticio" --motivo "tentando ignorar prontuario aberto" --saida saida/
#    -> DECISAO REJEITADA (saida 3): P01/P02 so se resolvem no PIMS, nao podem ser ignoradas
python -m fechamento decidir --finding F-9f5f07e3 --decisao conferido_manual --papel veterinario \
   --responsavel "Vet Ficticio" --motivo "conferido contra o livro de controle fisico" --saida saida/

# 3) 'encaminhado' NAO encerra: a pendência só some quando o dado mudar no export seguinte
python -m fechamento decidir --finding F-e04fece2 --decisao encaminhado --papel veterinario \
   --responsavel "Vet Ficticio" --motivo "vou lancar o exame no PIMS" --saida saida/
python -m fechamento verificar --data 2026-10-02 --entrada meus_dados --saida saida/ --agora 2026-10-02T19:00
#    -> continua com a pendência C03 (status "encaminhada")
echo "C007,ITEM_EXAME_LAB,1" >> meus_dados/itens_fatura.csv      # simula o novo export do PIMS
python -m fechamento verificar --data 2026-10-02 --entrada meus_dados --saida saida/ --agora 2026-10-02T19:00
#    -> C03 de C007 desapareceu; as decisões 'ignorar'/'conferido_manual' aparecem como "decididas"
```

O dia só chega a `CONFERIDO` (saída 0) depois que prontuários abertos/incompletos (P01/P02) forem corrigidos no
dado de origem e todas as demais pendências `acao`/`atencao` tiverem decisão terminal. Os testes
(`tests/test_fluxo.py::test_ac09_conferido_quando_tudo_tratado`) percorrem esse caminho completo.

### Rascunhos de texto (tutor/prontuário) com aprovação do veterinário

```bash
python -m fechamento rascunho --finding F-08ca3ca6 --destino tutor --saida saida/     # gera RASCUNHO (stub, offline)
python -m fechamento exportar --rascunho R-11bceb7f --saida saida/                    # saida 3: ainda nao aprovado
# o veterinario le, EDITA e salva o texto final (sem marcadores [PREENCHER ...]) em texto_final.txt
python -m fechamento aprovar --rascunho R-11bceb7f --papel veterinario --responsavel "Vet Ficticio" \
   --texto-final texto_final.txt --confirmo --saida saida/
python -m fechamento exportar --rascunho R-11bceb7f --saida saida/                    # grava saida/liberados/R-11bceb7f.txt
```

`exportar` só grava um arquivo local. O envio ao tutor e o lançamento no prontuário continuam **manuais**.
Subcomandos extras: `rejeitar` (motivo obrigatório). `python -m fechamento --help` lista tudo.

### Códigos de saída

Qualquer falha inesperada (disco, arquivo/log corrompido, não UTF-8) sai com **2**, nunca com 1: para quem
automatiza, 1 significa só "dia pendente". Se a entrada falhar, `relatorio_<data>.md` e `pendencias_<data>.csv`
de uma execução anterior são renomeados para `*.OBSOLETO` (um `CONFERIDO` antigo não pode continuar parecendo atual).

| Comando | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `verificar` | `CONFERIDO` | `PENDENTE` | entrada inválida ou falha inesperada (arquivo/linha na mensagem) | – |
| `decidir`, `rascunho`, `aprovar`, `rejeitar`, `exportar` | ok | – | entrada/uso inválido (inclui finding desconhecido) | recusado por regra |

## Arquitetura

```
fechamento/
  entrada.py     leitura + validação dos CSVs (falha alto, só códigos opacos)        [determinístico]
  regras.py      uma função por código (P01..K01) + finding_id estável              [determinístico]
  decisoes.py    log append-only, permissões (RF-05/06), estado do dia              [determinístico]
  relatorio.py   Markdown + CSV, ordem fixa                                         [determinístico]
  redator.py     interface Redator + RedatorStub + guardas (dose, CPF, e-mail, fone) [única etapa "LLM"]
  rascunhos.py   RASCUNHO -> APROVADO/REJEITADO (portão do veterinário) + exportar  [determinístico]
  cli.py         argparse e códigos de saída
adaptadores/anthropic_redator.py   adaptador OPCIONAL (fora do pacote) para a API da Anthropic
exemplos/dados_ficticios/          fixture do dia 2026-10-02 (13 consultas + 1 linha órfã de fatura)
tests/                             106 testes unittest (AC-01..AC-21 da SPEC + rascunhos + adaptador + correções pós-revisão)
```

Separação pedida: **toda a lógica de regras, validação e templates é determinística** e roda sem LLM. A única
etapa que poderia usar um LLM é a *redação de rascunhos* (`redator.py`), exposta como interface:

```python
class Redator(Protocol):
    nome: str
    def redigir(self, contexto: ContextoRascunho) -> str: ...   # contexto = só dados opacos
```

- **Stub offline (padrão)**: `RedatorStub`, texto fixo com marcadores `[PREENCHER ...]` para tudo que só o
  veterinário pode afirmar. Sem doses, sem conduta clínica.
- **Plugar outro redator**: `--redator pacote.modulo:Classe` (classe com `nome` e `redigir`, construtor sem
  argumentos). O pacote `fechamento` **não importa** SDK de LLM nem rede (teste estático AC-19); por isso o
  adaptador fica em `adaptadores/`.
- **Conectar à API da Anthropic**: `adaptadores/anthropic_redator.py`.
  ```bash
  pip install anthropic
  export ANTHROPIC_API_KEY=...          # não grave a chave no código
  python -m fechamento rascunho --finding F-08ca3ca6 --destino tutor --saida saida/ \
     --redator adaptadores.anthropic_redator:AnthropicRedator
  ```
  Usa `anthropic.Anthropic()` + `client.messages.create(...)`, modelo padrão `claude-opus-5-5` (parâmetro
  `modelo` da classe), `output_config={"effort": "low"}`, trata `stop_reason` `refusal` e `max_tokens` como falha.
  Conferido na documentação da skill `claude-api` (Python). **Não foi exercitado contra a API real** (sem rede nem
  credencial aqui); os testes usam cliente falso. Não habilitei o parâmetro opcional de fallback server-side
  (beta): para uso real, avalie-o na documentação da Anthropic. Enviar texto a API externa exige avaliação LGPD
  antes de qualquer dado real (**não verificado** nesta spec).

### Garantias do portão de aprovação (valem para qualquer redator, inclusive LLM)

1. O redator só recebe código da regra, `consulta_id` e a mensagem da regra (nada de texto livre de prontuário).
2. A saída do redator passa por guardas determinísticas antes de ser gravada: padrões de dose/quantidade clínica
   (mg, ml, %, UI...), CPF, e-mail e telefone barram o rascunho (saída 3, nada gravado). Destino é restrito por
   código (cobrança -> tutor; prontuário/controlado -> nota ao prontuário).
3. Todo texto nasce `RASCUNHO`. Só vira `APROVADO` com `aprovar --confirmo`, papel `veterinario`, texto final
   sem marcadores pendentes e sem os padrões acima. A aprovação grava o texto exato e o SHA-256.
4. `exportar` recusa tudo que não esteja `APROVADO`, ou cujo texto não confira com o hash aprovado.
5. `verificar` e `decidir` nunca geram texto para tutor ou prontuário.

As guardas barram padrões óbvios; **não** provam segurança clínica. O veterinário continua responsável por ler.

## Testes

```bash
python -m unittest discover        # a partir de prototipo/; 106 testes, sem rede
```

Cobrem AC-01 a AC-21 da SPEC (conjunto exato de pendências, anti falso positivo, evidência com linha,
determinismo por SHA-256, entradas intactas, 6+ entradas inválidas, estado do dia, motivo mínimo, não ignoráveis,
K01 e ato clínico, `encaminhado`, decisão presa à evidência, log append-only, checklist configurável, sem
imports de rede/SDK, sem dado pessoal) e o ciclo de rascunho/aprovação, incluindo adulteração do log.

## Desvios e escolhas em relação à SPEC (para o revisor)

- Fixture em `exemplos/dados_ficticios/` (pedido da tarefa) em vez de `dados_ficticios/` na raiz.
- A SPEC lista "etapa com LLM" como fora de escopo; aqui ela existe **só** como redação de rascunhos, opcional,
  atrás de interface, com stub offline e portão de aprovação. O núcleo continua sem LLM e sem rede.
- `decidir` não recebe `--entrada`: localiza a pendência em `saida/pendencias_*.csv` gerado por `verificar`
  (finding desconhecido => saída 2). Esse CSV é tratado como confiável (limitação).
- Pendências `info` (P03) não aceitam decisão. Vale a última decisão por `finding_id`. Uma decisão registrada
  que não passa de novo pelas regras (ex.: log editado à mão para ignorar P02) não conta.
- `finding_id` inclui a data do export além de `codigo + consulta_id + chave`.
- Um `--data` diferente da data de uma consulta é erro de entrada (um export por dia). Procedimento de
  `consulta_id` inexistente também é erro (só item de fatura órfão vira C02).
- As regras são independentes (RF/AC-03): numa base real, consulta realizada sem nenhum item **e** com
  procedimento mapeado gera C01 **e** C03. No fixture, C006/C013 não têm procedimento registrado para manter o
  conjunto esperado da SPEC exato.
- **P02 só vale para atendimento `realizado`** (como P01). A SPEC §6.1 não filtrava por status, mas P02 não é
  ignorável: sem o filtro, uma consulta `cancelado` com campo `N` bloquearia o dia para sempre.
- `fechado_em` anterior à data do atendimento e `regras.csv` sem nenhuma regra são erro de entrada (saída 2).
- `decidir`: `--responsavel` e `--motivo` não aceitam quebra de linha/caractere de controle nem CPF, e-mail ou
  telefone (nomes e endereços **não** são detectáveis: use só códigos opacos). Texto livre vai escapado ao
  relatório (`_md`) e, no CSV, `responsavel` que comece com `=`, `+`, `-`, `@` ganha apóstrofo.
- Rascunho `REJEITADO` pode ser refeito: `rascunho` grava novo evento `criado` com o mesmo id.
- `finding_id` de K01 órfão (fatura sem consulta) inclui a data do export. `finding_id` repetido (colisão de
  hash de 32 bits) aborta com erro em vez de sobrescrever em silêncio.
- A tabela "Decisões registradas" tem a coluna "Efeito": decisão substituída ou reprovada nas regras atuais
  aparece como "sem efeito". Decisão **não** é presa ao hash de `regras.csv` (RF-09 prende à evidência).
- `--redator modulo:Classe` faz `importlib.import_module` de qualquer módulo no `sys.path`: executa código
  arbitrário local. Aceitável para uso local com dados fictícios; não exponha esse parâmetro a terceiros.
- Guardas de dose ampliadas (comp, gts, ampola, mililitro, número por extenso, "dobro da dose"), mas continuam
  **não** provando segurança clínica. `consulta_id` não dispara a guarda de CPF/telefone.
- `aprovar` reimprime o texto aprovado e o SHA-256. Não há prova de que o veterinário o leu.
- K01 para item controlado em fatura órfã e em atendimento cancelado.

## Limitações

- Não corrigido de propósito (ver relatório de triagem): trilha sem encadeamento de hash (log editável),
  `--agora` aceito em `decidir`, sem trava de concorrência no log, sem decisão em lote, erros de entrada reportados
  um por vez, item controlado ausente de `regras.csv` não gera alerta (conforme SPEC), colunas `campo_*` fora do
  checklist ignoradas sem aviso (conforme SPEC).

- Sem autenticação: papel e nome são declarados e apenas registrados (rastro, não segurança).
- O checklist de campos do exemplo é fictício. Res. CFMV 1.321/2020 e 1.653/2025: vigência, campos obrigatórios
  e relação entre elas **não verificado** (texto oficial não lido). A lista real só deve entrar após leitura do
  texto oficial, em `campos_obrigatorios.csv` (campo `fonte_norma`/`versao`).
- Tabela de regras de exemplo é inventada; não representa preço, procedimento ou lista de controlados reais
  (normas MAPA/ANVISA: **não verificado**).
- Não há integração com PIMS; que PIMS brasileiros exportam consultas, procedimentos e itens com identificador
  comum é **não verificado** (principal hipótese a validar). O MVP prova a lógica e o fluxo, **não** o valor
  (ganho de tempo, receita recuperada). Números de perda de receita citados na SPEC vêm de fontes dos EUA/Europa
  sem revisão por pares e não valem para o Brasil.
- Logs (`decisoes.jsonl`, `rascunhos.jsonl`) são append-only por convenção do programa, não imutáveis: quem tem
  acesso ao disco pode editá-los. Mitigações no código: reavaliação das decisões na leitura e hash do texto aprovado.
- Requisitos de produção fora do MVP: autenticação/autorização, exportação do PIMS, retificação de prontuário sem
  apagar histórico, LGPD, retenção de log.
