# ES2

Pesquisa e protótipo sobre onde automatizar o dia a dia de um médico-veterinário clínico no Brasil, respondendo à pergunta "um agente ou um workflow?". Resposta resumida: workflow com humano no circuito (nenhuma das 90 tarefas analisadas recebeu "agente autônomo" como forma recomendada).

**Comece por [`RELATORIO.md`](RELATORIO.md).** Ele traz método e limites, panorama por domínio, top oportunidades, o porquê do candidato escolhido, resultado do protótipo, próximos passos e fontes.

> Aviso: todos os dados do protótipo são fictícios. Não use dados reais de pacientes ou tutores. As fontes dos arquivos de pesquisa são, em grande parte, resultados de busca; textos normativos integrais frequentemente não foram lidos (ver "não verificado" nas análises).

## Estrutura

```
README.md                 este índice
RELATORIO.md              relatório final (método, panorama, top oportunidades, escolha, protótipo, próximos passos, fontes)

pesquisa/                 90 análises de tarefas, em 8 domínios (um arquivo por tarefa, NN-*.md)
  RANKING.md              ranking das 90 tarefas (score = impacto x viabilidade x (6 - risco))
  administrativo/         11 tarefas (inclui 11-fechamento-do-dia-prontuario-e-cobranca.md, a tarefa escolhida)
  apoio-clinico/          11 tarefas
  atendimento-tutor/      12 tarefas
  compliance/             11 tarefas
  educacao-pesquisa/      10 tarefas
  exames-imagem/          12 tarefas
  gestao-clinica/         11 tarefas
  hospital-cirurgia/      12 tarefas

prototipo/                MVP "Fechamento do dia" (Python 3.11, só biblioteca padrão, offline)
  README.md               uso, passo a passo, arquitetura, desvios da SPEC e limitações
  SPEC.md                 especificação: regras, portões H1 a H6, critérios de aceite AC-01 a AC-21
  fechamento/             núcleo: entrada.py, regras.py, decisoes.py, relatorio.py, redator.py, rascunhos.py, cli.py
  adaptadores/            adaptador opcional da API da Anthropic (fora do pacote; só testado com cliente falso)
  exemplos/dados_ficticios/   5 CSVs sintéticos (13 consultas e 1 linha órfã de fatura, dia 2026-10-02)
  tests/                  106 testes unittest
```

## Como rodar o protótipo

```bash
cd prototipo
python3 -m unittest discover        # 106 testes, sem rede
python3 -m fechamento --help        # subcomandos: verificar, decidir, rascunho, aprovar, rejeitar, exportar
```

O passo a passo completo (verificar, decidir, "encaminhado não encerra", novo export, rascunho e aprovação) está em `prototipo/README.md`.
