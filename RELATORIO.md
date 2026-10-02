# Relatório: onde automatizar o dia a dia do veterinário clínico, e o MVP escolhido

Data: 2026-10-02. Público: médico-veterinário clínico (Brasil). Pergunta de partida: "um agente ou um workflow?"

## Resumo em 30 segundos

- **Resposta curta: workflow.** Nas 90 tarefas analisadas, nenhuma recebeu "agente autônomo" como forma recomendada. O quadro final é 62 workflows (etapas fixas com revisão humana), 26 scripts/planilhas e 2 integrações. O LLM aparece quase sempre como camada opcional de rascunho, nunca como quem decide ou lança.
- **Candidato escolhido para protótipo:** "Fechamento do dia: pendências de prontuário, conferência de cobrança e lançamentos", um workflow determinístico, sem LLM no núcleo, com portões humanos.
- **O que o protótipo prova e o que não prova:** prova a lógica e o fluxo (106 testes passando, rodei de novo hoje). **Não prova valor**: ganho de tempo e de receita não foram medidos, e os números de perda de receita vêm de fornecedores dos EUA e da Europa, sem validação para o Brasil.
- **O que mais pesa nas ressalvas:** o texto oficial das Res. CFMV 1.321/2020 e 1.653/2025 não foi lido, e a principal hipótese não verificada é que os PIMS brasileiros exportem dados estruturados (consulta, procedimento, fatura com identificador comum).

---

## 1. Método e limites

### 1.1 O que foi feito

1. **90 tarefas do dia a dia** foram analisadas, uma por arquivo, em 8 domínios: administrativo (11), apoio clínico (11), atendimento ao tutor (12), compliance (11), educação e pesquisa (10), exames e imagem (12), gestão da clínica (11) e hospital e cirurgia (12). Os arquivos estão em `pesquisa/<domínio>/NN-*.md`.
2. Cada análise segue o mesmo roteiro: soluções existentes, forma recomendada (agente, workflow, script/planilha ou integração), onde o humano valida, riscos (clínico, legal/CFMV, LGPD, alucinação, receituário controlado), pontuação de 1 a 5 em impacto, viabilidade e risco, e se cabe um MVP sem dados reais e sem serviço pago.
3. `pesquisa/RANKING.md` ordena as 90 tarefas por **score = impacto x viabilidade x (6 - risco)**, gerado a partir das análises, sem nova pesquisa. Empates mantêm a ordem de entrada.
4. Das 90, o fluxo informa que **12 foram verificadas**. Uma delas, o fechamento do dia, virou especificação (`prototipo/SPEC.md`), protótipo e revisão.

### 1.2 O que NÃO foi coberto, e limites que você precisa ter em mente

- **As 12 verificações não estão no repositório.** Não há lista de quais são as 12 nem registro do que foi checado em cada uma. Não inferi quais são. O SPEC (seção 0) chama o fechamento do dia de "candidato único verificado"; como o repositório não traz o registro das outras 11, não consigo explicar o que foi checado nelas nem por que não seguiram para protótipo.
- **Verificação da tarefa escolhida é limitada.** A própria SPEC (seção 13) diz que, na rodada de especificação, o orçamento de WebSearch estava esgotado e o WebFetch foi bloqueado pelo proxy em vários domínios; as fontes vieram do arquivo de pesquisa e não foram reabertas. Este relatório também não fez pesquisa nova: só repete o que os arquivos afirmam, com as ressalvas que eles mesmos trazem.
- **Qualidade de evidência muito desigual entre domínios** (contagem por busca de texto nos arquivos):
  - 47 dos 90 arquivos registram que o orçamento de WebSearch da sessão estava esgotado (200/200): atendimento ao tutor 5 de 12, compliance 10 de 11, exames e imagem 11 de 12, gestão 11 de 11, hospital e cirurgia 10 de 12. Administrativo, apoio clínico e educação e pesquisa não registram isso.
  - Pelo menos 16 arquivos declaram expressamente que nenhuma afirmação externa ou fonte foi verificada (8 em exames e imagem, 4 em gestão, 3 em hospital e cirurgia, 1 em atendimento).
  - 60 arquivos mencionam bloqueio de acesso (WebFetch ou sites específicos). Na prática, muita citação de norma vem de resumo de resultado de busca, não do texto oficial.
  - A marca "não verificado" aparece nos 90 arquivos (676 ocorrências somadas). Leia-a como o estado normal desta pesquisa, não como exceção.
- **Os scores são estimativas dos analistas**, não medições. As economias de tempo citadas (por exemplo 1 a 3 h por semana em apoio clínico) são, nos próprios arquivos, estimativas do usuário ou do analista, não medidas.
- **Fontes de fornecedor e de outros países.** Muito do que existe como "solução" são páginas comerciais; estudos de eficácia são, em geral, de medicina humana ou dos EUA/Europa. Estudos veterinários revisados por pares sobre ganho de tempo ou acurácia de escribas de IA, de cobrança perdida em clínicas e de LLM em exames laboratoriais: os arquivos dizem "não encontrei / não verificado".
- **Nenhum dado real** de paciente ou tutor foi usado em nenhuma etapa.
- **Sem integração real:** o protótipo não foi testado com PIMS real, e o adaptador opcional da API da Anthropic só foi testado com cliente falso (sem rede e sem credencial no ambiente de construção).

---

## 2. Panorama por domínio

Leitura rápida (pontuação média por domínio é a média dos scores do ranking; "risco 4" é o número de tarefas com nota de risco 4):

| Domínio | Tarefas | Score médio | Formas recomendadas | Risco 4 | Qualidade da evidência |
|---|---|---|---|---|---|
| gestão da clínica | 11 | 51,4 | 7 script/planilha, 4 workflow | 0 | fraca: busca esgotada em 11 de 11 |
| educação e pesquisa | 10 | 44,2 | 6 workflow, 4 script/planilha | 0 | sem registro de busca esgotada; alguns acessos bloqueados |
| administrativo | 11 | 44,0 | 11 workflow | 1 | sem registro de busca esgotada; texto das normas não lido |
| compliance | 11 | 41,9 | 6 script/planilha, 5 workflow | 2 | fraca: busca esgotada em 10 de 11 |
| atendimento ao tutor | 12 | 39,2 | 11 workflow, 1 script/planilha | 3 | mista: busca esgotada em 5 de 12 |
| exames e imagem | 12 | 39,0 | 9 workflow, 3 script/planilha | 2 | fraca: busca esgotada em 11 de 12 |
| hospital e cirurgia | 12 | 38,9 | 9 workflow, 2 script/planilha, 1 integração | 2 | fraca: busca esgotada em 10 de 12 |
| apoio clínico | 11 | 35,9 | 7 workflow, 3 script/planilha, 1 integração | 1 | sem registro de busca esgotada |

O padrão geral que os analistas repetem: o que é **aritmética, data, regra fixa ou checklist** vai para script ou workflow determinístico; o que é **linguagem** (texto leigo ao tutor, redação de narrativa) pode ter um passo de LLM como rascunho; o que é **ato clínico ou documento regulado** (dose, receita, laudo, prontuário, consentimento) fica com o veterinário, que revisa e assina. Os 11 itens de risco 4 são todos de ato clínico ou documento regulado: dose e prescrição, controlados, triagem de urgência por mensagem, interpretação clínica de exame e de laudo, e notificação compulsória.

### Administrativo (11 tarefas, média 44,0)
- Quase tudo é "núcleo determinístico (modelo, regra, conta) mais LLM opcional só para redação", com revisão e assinatura do veterinário. O prontuário é ato do veterinário (Res. CFMV 1.321/2020, segundo resultados de busca).
- Topo do domínio: fechamento do dia (64) e orçamentos e planos de tratamento (60). Em orçamentos, o ponto legal citado é o art. 40 do CDC (orçamento prévio discriminado, validade de 10 dias salvo estipulação), e os analistas avisam que muitos PIMS já têm módulo de orçamento: "verificar antes de construir".
- Emissão de receitas é o único de risco 4 do domínio. O tipo de receituário é tabela de decisão por princípio ativo; a emissão de controlados depende de sistema oficial do MAPA (SNCR) e de assinatura. O quadro normativo "mudou várias vezes em 2025 e 2026" (Portaria MAPA 837/2025 aparece nos resultados; conteúdo exato não verificado). Para dose, a análise cita um estudo (Okur, Vet Record) em que LLMs erraram fármaco, dose e jejum em protocolos anestésicos; só o resumo da busca foi lido.
- Mensagens a tutores: a literatura citada é de medicina humana (Lancet Digital Health: 7,1% dos rascunhos de GPT-4 com risco de dano grave, e revisores deixaram passar em média 66,6% dos erros perigosos; números do resumo de busca, a conferir no artigo). Também consta que, desde 15/01/2026, chatbots de IA de propósito geral são proibidos na API do WhatsApp Business, enquanto automações de finalidade específica seguem permitidas (fontes secundárias; texto oficial da Meta não verificado).
- Laudos de imagem: a recomendação é não automatizar a interpretação por IA; um piloto no JAVMA aponta deficiências em radiografia abdominal canina por serviços comerciais de IA (só o título foi visto, números não verificados).

### Gestão da clínica (11 tarefas, média 51,4, o maior)
- 10 das 11 têm risco 2. São problemas de aritmética, calendário e restrições: agenda, confirmação e no-show, estoque e validade, compras, caixa, contas a pagar e repasses, indicadores, escala, marketing, reunião de equipe. Nenhuma tem risco clínico direto, e o LLM "não agrega" nas contas.
- O gargalo repetido é o **dado**: fechamento de caixa e indicadores dependem de exportação do PIMS; se só houver tela ou PDF, a viabilidade cai de 4 para 2.
- Impacto 3 em quase todas, com "ganho moderado" e magnitude "não verificada". É o domínio com evidência mais frágil (busca esgotada em todas as 11 análises).

### Educação e pesquisa (10 tarefas, média 44,2)
- Baixo risco (a única tarefa de risco 1 do ranking está aqui: triagem de alertas e newsletters). Triagem por PubMed e RSS, fichas de leitura, rounds com fechamento de ações, acervo e POPs.
- Cuidados repetidos: LLM não deve ser fonte de referências (risco de citação inventada), e a análise de leitura crítica diz que a evidência mostra LLMs pouco confiáveis para avaliar risco de viés sozinhos. Impacto 2 a 3: o valor está em disciplina e padronização, não em tempo.

### Compliance (11 tarefas, média 41,9)
- Obrigações são calendário, saldo e prazo: livro de controlados, RSS, CRMV e vigilância, LGPD, cópia de prontuário, termos de consentimento. Forma típica: script/planilha com alerta de vencimento.
- Risco 4: notificação de receita de controlados e notificação de doença de notificação obrigatória. Nas duas, o documento é oficial, numerado em sistema ou talonário, e a ferramenta no máximo valida e rascunha.
- **Limite importante:** os prazos citados (guarda de 5 anos, cópia em 5 dias úteis, prorrogação até 30 dias úteis) vêm do enunciado das tarefas e de fontes secundárias; os próprios arquivos dizem que o texto da Res. CFMV 1.653/2025 não foi lido.

### Atendimento ao tutor (12 tarefas, média 39,2)
- Lembretes de vacina, follow-up de 24 a 72 h, contato com faltosos: workflow com lista diária, mensagem-modelo e registro, com a ligação continuando humana.
- Risco 4: triagem de urgência por WhatsApp, dúvidas de tutores de pacientes em tratamento e renovação de receita de medicação contínua. Regra de ouro da triagem: o LLM só pode subir a urgência, nunca reduzi-la abaixo do que as regras de sinais de alerta determinaram.

### Exames e imagem (12 tarefas, média 39,0)
- Entorno de exames é rastreio e prazo: resultados pendentes de laboratório externo, recheck, achados incidentais, entrega de laudos. A interpretação clínica e a revisão do laudo ficam com o veterinário (as duas são risco 4).
- É o domínio com mais arquivos que declaram "nenhuma afirmação externa verificada" (8 de 12). Inclusive o #2 do ranking (achados incidentais): "Nenhuma afirmação factual externa foi verificada com URL".

### Hospital e cirurgia (12 tarefas, média 38,9)
- Dose e prescrição (plano anestésico, mapa de medicação do internado): calculadora determinística com tabela de fármacos curada pelo veterinário, sem LLM calculando. Ambas risco 4.
- Registro intraoperatório da ficha anestésica é uma das duas "integrações" (importar sinais vitais do monitor), com viabilidade 2 a 3 conforme o modelo do monitor. É o domínio com mais marcas de "não verificado" (130) e 10 de 12 análises com busca esgotada.

### Apoio clínico (11 tarefas, média 35,9, o menor)
- Dose por script, calculadoras, histórico e SOAP assistidos, protocolos com corpus fechado. A checagem de interações medicamentosas é a pior do ranking (score 12): é integração com base curada, risco 4 por falso negativo, e o gargalo é obter uma base veterinária licenciável e estruturada (não verificado).
- Leitura de imagem e ECG por IA: "não automatizar". Os ganhos de tempo estimados são pequenos (1 a 3 h por semana, estimativa dos analistas) e o valor está mais em padronização e segurança.

---

## 3. Top oportunidades, forma recomendada e objeções que restaram

**Atenção ao rótulo:** o ranking abaixo é o dos analistas. Pelo que consta no repositório, **apenas a #1 é tratada como verificada**; as demais são candidatas ranqueadas, sem registro de verificação. O score é impacto x viabilidade x (6 - risco).

| # | Tarefa | Score | Forma recomendada | Objeções que restaram (segundo as análises) |
|---|---|---|---|---|
| 1 | Fechamento do dia: pendências de prontuário, conferência de cobrança e lançamentos | 64 | **Workflow** determinístico, sem LLM no caminho crítico | Números de perda de receita são de fornecedores dos EUA e da Europa; exportação estruturada dos PIMS brasileiros não verificada; PIMS pode já cruzar prontuário e fatura; texto oficial das resoluções do CFMV não lido; valor não medido |
| 2 | Seguimento de achados incidentais e de imagem que exigem reavaliação | 64 | **Script/planilha** com regras de data | Nenhuma afirmação externa verificada com URL; gargalo é obter achados estruturados (disciplina de registro ou extração assistida); depende de adesão do tutor; extração por LLM subiria o risco para 3 |
| 3 | Orçamentos e planos de tratamento/cirurgia | 60 | **Workflow** (planilha/script), LLM só na redação ao tutor | Muitos PIMS já têm módulo de orçamento; CDC art. 40 e comunicação da faixa de variação; dados de recusa por custo (Gallup/PetSmart Charities) são dos EUA e só em resumo de busca |
| 4 | Revisar casos em reunião e acompanhar resultados pendentes | 60 | **Workflow** (planilha/script semanal), sem LLM no caminho crítico | Falso senso de segurança (o que não está no registro some); LGPD com planilhas compartilhadas; tempos (60 a 90 min por semana de "caça") são estimativa do usuário; evidência de exames pendentes é de medicina humana |
| 5 | Discussão de casos (rounds) da equipe | 60 | **Workflow** leve (modelo, checklist, registro de ações) | Valor depende de disciplina de fechar ações, não de tecnologia; risco sobe para 3 se usar LLM com dados de prontuário |
| 6 | Organização do acervo e dos POPs | 60 | **Script/planilha** | Risco sobe para 3 a 4 se um modelo editar POPs ou receber prontuários; ganho moderado |
| 7 | Orientação de estagiários e material educativo para tutores | 60 | **Workflow** com LLM assistente (rubrica e fontes fornecidas pelo veterinário) | Uso esporádico (frequência não verificada); depende de revisão humana do texto |
| 8 | Regras de lembretes de vacina e retorno | 60 | **Workflow** (tabela de regras e datas) | O PIMS pode já cobrir; risco sobe para 3 se o envio for automático sem conferência |
| 9 | Contato com faltosos e retornos em atraso | 60 | **Workflow** (lista de vencidos, escalonamento, roteiro) | Ligação continua humana; evidência veterinária de desfecho não verificada; risco 4 a 5 se um agente ajustasse conduta |
| 10 | Contagem de estoque e checagem de validade | 60 | **Script/planilha** | O gargalo é a contagem física; automatizar leitura de rótulo tem viabilidade 2 a 3 |

Também empatados em 60 e fora do top 10 por ordem de entrada: pedido de compras, contas a pagar e repasses, marketing, laudo próprio de US/RX, relatório cirúrgico, termos de consentimento, RSS e perfurocortantes, obrigações perante o CRMV.

**Sobre "agente":** nenhuma das 90 análises recomendou agente autônomo. A justificativa repetida é que o fluxo é linear e previsível, e que autonomia (alterar fatura, fechar prontuário, responder tutor, definir dose) acrescenta risco sem ganho. O que mais se aproxima de "LLM com ferramenta" são etapas opcionais e restritas, por exemplo recuperação em corpus fechado de diretrizes e POPs com citação obrigatória (apoio clínico, protocolos), sempre com revisão.

---

## 4. Por que "Fechamento do dia: pendências de prontuário, conferência de cobrança e lançamentos" foi escolhido

O candidato é um **workflow determinístico, sem LLM, com portões humanos**. Razões:

1. **Era o único candidato verificado, e atende aos critérios.** Os critérios da SPEC são valor, viabilidade, risco baixo e demonstração do padrão workflow com humano no circuito. Observação honesta: no ranking ele empata em 64 com o #2 (achados incidentais), e o empate no ranking é resolvido pela ordem de entrada. O repositório não registra outro critério de desempate. Uma diferença documentada entre os dois: a análise do #2 declara que nenhuma afirmação externa foi verificada com URL, enquanto a do #1 traz fontes citadas, ainda que só por resultados de busca.
2. **É viável como MVP local:** Python stdlib, 5 CSVs sintéticos, sem rede e sem API paga.
3. **O risco é baixo:** a ferramenta só lê e sugere, nunca escreve em prontuário ou fatura.
4. **Demonstra bem o padrão workflow com humano no circuito:** etapas fixas, portões H1 a H6, decisão registrada em log append-only com motivo obrigatório.
5. **Usa a regra "encaminhado não encerra":** só o dado corrigido no PIMS encerra a pendência.

### Ressalvas

- O MVP prova a lógica e o fluxo, **não o valor**: ganho de tempo e de receita não foram medidos.
- Os números de perda de receita (cerca de 17% de cobranças diagnósticas não faturadas e perdas de 8 a 15% da receita, em fontes de mercado como dvm360 e Shepherd) vêm de fornecedores dos EUA e da Europa, sem revisão por pares, e **não foram verificados para o Brasil**. Estudo revisado por pares sobre cobrança perdida em clínicas veterinárias: não encontrado.
- O texto oficial das Res. CFMV 1.321/2020 e 1.653/2025 **não foi lido**. Por isso o checklist de campos do prontuário é configuração versionada (`campos_obrigatorios.csv`) marcada como `EXEMPLO_FICTICIO`, e não a lista oficial.
- A principal hipótese não verificada é a **exportação estruturada dos PIMS brasileiros**. SimplesVet e Vetsmart aparecem só em páginas comerciais; Vetsmart, VetSoft e outros: módulo de conferência de cobrança "não verificado". Há risco de redundância com recurso nativo do PIMS (por exemplo, a descrição comercial do SimplesVet fala em lançamento da venda pelo prontuário e conciliação; não testei).

### Como é o fluxo (resumo)

`verificar` lê os CSVs, valida e aplica regras; gera relatório e CSV de pendências; o dia fica `PENDENTE`. Humanos decidem cada pendência nos portões:

| Portão | Quem | O que |
|---|---|---|
| H1 | veterinário | fechar ou completar prontuário no PIMS (a ferramenta não preenche, não assina, não deixa ignorar P01 e P02) |
| H2 | recepção ou financeiro (e veterinário se ato clínico) | lançar no PIMS item possivelmente não cobrado (C03) |
| H3 | financeiro (e veterinário se ato clínico) | corrigir cobrança indevida (C04, C05, C02) |
| H4 | veterinário | conferir controlado contra livro ou sistema de controle (K01), decisão `conferido_manual` com motivo |
| H5 | quem tem permissão do portão | `ignorar` falso positivo, com motivo registrado |
| H6 | quem roda a nova verificação | o dia só vira `CONFERIDO` quando tudo foi tratado |

---

## 5. Resultado do protótipo e da revisão

### 5.1 O que foi construído (`prototipo/`)

- **Núcleo determinístico** (`fechamento/`, Python 3.11, só biblioteca padrão):
  - lê e valida os 5 CSVs; entrada inválida sai com código 2, citando arquivo e linha, e não gera relatório parcial;
  - aplica uma função de regra por código (P01 a P03 prontuário, C01 a C05 cobrança, K01 controlados: 9 regras), com `finding_id` estável;
  - gera `relatorio_<data>.md` e `pendencias_<data>.csv`, idênticos byte a byte para a mesma entrada;
  - registra decisões em `decisoes.jsonl` (append-only) e calcula o estado do dia;
  - checklist e tabela de regras vêm só dos CSVs, nunca do código.
- **Etapa de LLM plugável** (`fechamento/redator.py`): a interface `Redator` tem uma implementação offline, `RedatorStub`, com marcadores `[PREENCHER ...]` para o que só o veterinário pode afirmar. O redator só recebe dados opacos (código da regra, `consulta_id` e a mensagem da regra), e a saída passa por guardas determinísticas (padrões de dose, CPF, e-mail, telefone) antes de ser gravada. O texto nasce `RASCUNHO`, só vira `APROVADO` com `--confirmo` do veterinário, e `exportar` só grava um arquivo local. O pacote não importa SDK de LLM nem rede; o adaptador opcional da API da Anthropic fica em `adaptadores/`.
- Essa etapa de redação é um desvio da SPEC original (que a dava como fora de escopo) e está documentada no README e na SPEC (nota 0.2). O núcleo que seria medido segue sem LLM e sem rede.

### 5.2 Testes e verificação

- **106 testes `unittest`, 0 falhas, sem rede.** A contagem era 75 antes das correções da revisão. Rodei de novo hoje, na pasta `prototipo/`: `python3 -W error -m unittest discover` terminou com 106 testes OK em cerca de 1 s.
- Segundo o registro da construção, para garantir que os testes pegam erro foram desligadas de propósito a regra "P01/P02 não são ignoráveis" e depois a exigência de `--confirmo`; cada mutação derrubou testes (5 e 1 falhas) e o código foi restaurado. Depois da revisão, 9 mutações adicionais foram pegas pelos testes novos em `tests/test_correcoes.py`.
- O passo a passo do README foi percorrido na CLI (verificar, decidir, encaminhado, novo export, rascunho, aprovar, exportar) com os códigos de saída esperados (1, 0, 3, 2). Após as correções, os `finding_id` e as contagens continuaram iguais (12 pendências, 11 abertas, saída 1).
- **Não foi exercitado:** o adaptador da API da Anthropic contra a API real (sem rede e sem credencial); só com cliente falso. Também não houve teste com PIMS real nem com dado real.

### 5.3 Correções aplicadas após a revisão

- Falha inesperada passou a sair com 2 (não mais com 1), para que 1 signifique apenas "dia pendente"; os testes rodam o processo real.
- Proteção contra injeção de Markdown (quebra de linha e caracteres de controle em `--responsavel` e `--motivo`; escape no relatório) e de fórmula em CSV (valor que comece com `=`, `+`, `-`, `@` ganha apóstrofo).
- `decidir` rejeita CPF, e-mail e telefone em motivo e responsável (nomes e endereços não são detectáveis, e isso está no README).
- Rascunho `REJEITADO` agora pode ser refeito.
- P02 só vale para atendimento `realizado` (como P01), porque P02 não é ignorável e, sem o filtro, uma consulta cancelada com campo `N` bloquearia o dia para sempre. Documentado no README e na SPEC 6.1.

### 5.4 O que ficou sem correção de propósito (README, "Limitações")

Trilha sem encadeamento de hash (log editável por quem tem acesso ao disco), `--agora` aceito em `decidir`, sem trava de concorrência no log, sem decisão em lote, erros de entrada reportados um por vez, item controlado ausente de `regras.csv` não gera alerta, colunas `campo_*` fora do checklist ignoradas sem aviso. Também: sem autenticação (papel e nome são declarados e apenas registrados) e `--redator modulo:Classe` executa código local arbitrário (aceitável só para uso local com dados fictícios).

### 5.5 Estado do repositório

As alterações pós-revisão estão na árvore de trabalho e **não foram commitadas** (`git status` mostra arquivos modificados em `prototipo/`). Nenhuma operação de git foi feita nesta etapa.

---

## 6. Próximos passos e perguntas em aberto

### Próximos passos, em ordem sugerida

1. **Validar a hipótese central com 2 ou 3 clínicas, sem coletar dado de paciente** (SPEC, seção 12): qual PIMS usam; se exporta CSV ou API com identificador comum de consulta; se o PIMS já cruza prontuário e fatura; quanto tempo leva o fechamento hoje (cronometrar). Se o PIMS já resolve ou não exporta dado estruturado, o valor incremental cai. É isso que confirma ou refuta o Impacto 4.
2. **Ler o texto oficial** das Res. CFMV 1.321/2020 e 1.653/2025 (vigência, campos obrigatórios, relação entre as duas) e só então trocar o checklist fictício, preenchendo `fonte_norma` e `versao` em `campos_obrigatorios.csv`.
3. **Medir valor**: tempo de fechamento antes e depois, e pendências de cobrança realmente encontradas, em cenário real e com os cuidados de LGPD. Sem isso, os números de perda de receita seguem sendo hipótese de outro mercado.
4. **Requisitos de produção que o MVP não cobre:** autenticação e autorização reais, exportação do PIMS, retificação de prontuário sem apagar histórico, LGPD (base legal e minimização se algum dado sair da máquina), retenção do log, e log com encadeamento de hash.
5. **Etapa de LLM, se um dia for usada:** avaliação LGPD antes de enviar qualquer texto a API externa; testar o adaptador contra a API real com dados sintéticos; manter a regra "só sugestão ancorada em trecho do prontuário, nunca lançamento".
6. **Refazer verificações onde a busca ficou esgotada** (gestão, compliance, exames e imagem, hospital e cirurgia), principalmente as que dependem de norma (CFMV, MAPA, ANVISA, CDC, LGPD) não lida.
7. **Candidatos seguintes** (sugestão minha, a partir do ranking): achados incidentais (#2) e revisão de pendências em reunião (#4) usam o mesmo padrão do protótipo (registro com regras de data, humano decide, "encaminhado não encerra"). Antes, verificar as fontes do #2.
8. **Decisão sua:** commitar ou não as alterações pós-revisão do protótipo.

### Perguntas em aberto

- Quais são as 12 tarefas verificadas e o que foi checado em cada uma? (O repositório não registra.)
- Qual PIMS a sua clínica usa, e ele exporta consulta, procedimento e fatura com identificador comum?
- O PIMS já faz o cruzamento prontuário x fatura ou alerta de prontuário aberto?
- Quanto tempo leva hoje o fechamento do dia e quantos atendimentos por dia? (A persona de teste da SPEC é clínica pequena, 1 a 3 veterinários, 20 a 60 atendimentos por dia.)
- Quais pares procedimento e item esperado a sua clínica quer na tabela `regras.csv`, e quem é responsável por mantê-la (para evitar fadiga de alerta)?
- Quem decide em cada portão na sua rotina (veterinário, recepção, financeiro, responsável técnico)?
- Qual é a regra real do CFMV para campos obrigatórios e retificação de prontuário fechado?
- Normas de controlados (MAPA e ANVISA), CDC e fiscal: nunca foram lidas para este trabalho; a lista de itens controlados do exemplo é inventada.

---

## 7. Fontes

**Como ler esta lista:** são URLs citadas nos arquivos de pesquisa, agrupadas por uso. Pelos limites da seção 1, muitas foram vistas só como resultado de busca; **o texto integral das normas, em geral, não foi lido**. A lista completa por tarefa (mais de 400 URLs distintas) está dentro de cada análise em `pesquisa/`. Para estudos e produtos, lembre que várias são páginas de fornecedor.

### 7.1 Fechamento do dia (a tarefa escolhida)

- SimplesVet, prontuário (descrição comercial, não testada): https://simples.vet/funcionalidades/prontuario-medico/ e https://simples.vet/funcionalidades/
- Vetsmart (prontuário digital; módulo de conferência de cobrança não verificado): https://vetsmart.com.br/
- Captura de cobranças e cobrança perdida (fornecedores e mídia de mercado, EUA e Europa): https://www.ezyvet.com/charge-capture ; https://software.covetrus.com/emea/veterinary-insights/article/practice-solutions/the-opportunity-more-revenue-the-gap-missed-charges/ ; https://www.dvm360.com/view/missing-charges-your-software-should-help ; https://www.shepherd.vet/blog/how-to-get-15-missed-revenue-back-in-your-veterinary-practice/ ; https://www.vetxbill.ai/

### 7.2 Normas e fontes oficiais ou institucionais brasileiras (texto integral em geral não lido)

- Prontuário, Res. CFMV 1.321/2020: https://www.legisweb.com.br/legislacao/?id=480427 ; https://www.normasbrasil.com.br/norma/resolucao-1321-2020_480427.html ; https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf
- Prontuário, Res. CFMV 1.653/2025 (fonte secundária): https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ ; https://crmvgo.org.br/wp-content/uploads/2025/08/1653.pdf ; https://crmvgo.org.br/resolucao-cfmv-no-1-653-2025-estabelece-novas-regras-sobre-o-prontuario-veterinario/ ; https://www.legisweb.com.br/legislacao/?id=480419
- Estabelecimentos de pequenos animais e termos, Res. CFMV 1.275/2019: https://manual.cfmv.gov.br/arquivos/resolucao/1275.pdf
- Prescrição, Res. CFMV 1.318/2020: https://manual.cfmv.gov.br/arquivos/resolucao/1318.pdf
- Honorários e consentimento, Res. CFMV 1.138/2016: https://manual.cfmv.gov.br/arquivos/resolucao/1138.pdf
- Telemedicina, Res. CFMV 1.465/2022: https://www.legisweb.com.br/legislacao/?id=433219
- Controlados, Portaria SVS/MS 344/98: https://antigo.anvisa.gov.br/documents/10181/2718376/PRT_SVS_344_1998_COMP.pdf
- Portaria MAPA 837/2025 (conteúdo exato não verificado): https://www.legisweb.com.br/legislacao/?id=488965 ; https://www.agricultura.rs.gov.br/upload/arquivos/202602/19162152-portaria-mapa-837-2025-subst-controladas.pdf
- Guia de prescrição CRMV-MG (controlados e antimicrobianos): https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf
- Manual de orientações técnicas CRMV-RJ 2026: https://www.crmvrj.org.br/wp-content/uploads/2026/07/manual_orientacoes_tecnicas_crmv_rj_2026_07_29.pdf.pdf
- Notificação de epizootias: https://crmvsp.gov.br/saiba-mais-sobre-a-notificacao-obrigatoria-de-epizootias-ao-ministerio-da-saude/ ; https://bvsms.saude.gov.br/bvs/saudelegis/gm/2023/prt0217_04_05_2023.html
- LGPD (Lei 13.709/2018): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- CDC (Lei 8.078/1990; art. 40 sobre orçamento): https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm ; https://www.legjur.com/legislacao/art/lei_00080781990-40
- Assinaturas eletrônicas (Lei 14.063/2020): https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14063.htm

### 7.3 Estudos e evidência citados nas análises (resumos de busca; conferir antes de usar)

- Custo como principal motivo de recusa (EUA): https://news.gallup.com/poll/700115/veterinarians-say-cost-main-driver-declined-care.aspx ; discussão de custo nas consultas (JAVMA 2022): https://avmajournals.avma.org/view/journals/javma/260/14/javma.22.06.0268.xml
- Rascunhos de IA em mensagens a pacientes (medicina humana, Lancet Digital Health): https://www.thelancet.com/journals/landig/article/PIIS2589-7500(24)00060-8/fulltext
- Alucinação e omissão em notas clínicas por LLM (medicina humana): https://www.nature.com/articles/s41746-025-01670-7 ; https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2822301
- LLMs em protocolos anestésicos veterinários (Vet Record, só o resumo): https://bvajournals.onlinelibrary.wiley.com/doi/10.1002/vetr.70741
- IA comercial em radiografia abdominal canina (JAVMA, só o título): https://avmajournals.avma.org/view/journals/javma/aop/javma.25.10.0691/javma.25.10.0691.xml
- Passagem de plantão I-PASS e exames pendentes na alta (medicina humana, analogia): https://pmc.ncbi.nlm.nih.gov/articles/PMC7651935 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC9491200/
- Intervalos de referência por espécie e analisador (diretriz ASVCP): https://onlinelibrary.wiley.com/doi/10.1111/vcp.12006
- Política do WhatsApp Business para chatbots de IA (fontes secundárias; texto oficial da Meta não verificado): https://z-api.io/blog/meta-atualiza-politica-do-whatsapp-business/ ; https://wsa.adv.br/noticias/whatsapp-termos-de-uso-proibe-chatbots-de-ia/

### 7.4 Arquivos do projeto

- Análises por tarefa: `/home/user/ES2/pesquisa/<domínio>/NN-*.md` (90 arquivos)
- Ranking: `/home/user/ES2/pesquisa/RANKING.md`
- Análise da tarefa escolhida: `/home/user/ES2/pesquisa/administrativo/11-fechamento-do-dia-prontuario-e-cobranca.md`
- Especificação e protótipo: `/home/user/ES2/prototipo/SPEC.md`, `/home/user/ES2/prototipo/README.md`, `/home/user/ES2/prototipo/fechamento/`, `/home/user/ES2/prototipo/tests/`
- Dados sintéticos: `/home/user/ES2/prototipo/exemplos/dados_ficticios/`
