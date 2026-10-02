# 11 - Revisão de CRM: base de tutores, segmentação e campanhas

Domínio: atendimento-tutor. Data da análise: 2026-10-02.

## Aviso sobre fontes (leia primeiro)

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída para planalto.gov.br, wsava.org e business.whatsapp.com. **Nenhuma afirmação abaixo foi verificada nesta sessão.** Onde cito norma ou produto, é conhecimento prévio e está marcado "não verificado"; as URLs são os pontos de partida para o veterinário conferir, não evidência já lida. Não há dose, estudo ou número de mercado afirmado.

## Resumo da tarefa

Conferir cadastro (telefone, espécie, nascimento, consentimento), montar listas (vacinação, check-up sênior, dentística, vermifugação), aprovar o texto clínico e disparar. Entradas: relatório do PIMS, calendário sazonal, estoque.

## 1. Soluções existentes (não verificado)

- Os PIMS com lembretes e campanhas (Simples Vet, Vetsoft, SimplesVet, Vet Smart e similares no Brasil; ezyVet, Digitail, Provet no exterior) costumam ter lembretes de vacina e filtros por espécie/idade/último atendimento. Não verifiquei recursos nem preços atuais de nenhum. Ponto de partida: sites oficiais de cada fornecedor.
- Ferramentas genéricas de CRM e automação de WhatsApp (API oficial da Meta via provedores) servem ao disparo, mas cobram por conversa/mensagem. Referência de política a conferir: https://business.whatsapp.com/policy (não verificado; bloqueado nesta sessão).
- Diretriz de vacinação para fundamentar o texto clínico: WSAVA, https://wsava.org/global-guidelines/vaccination-guidelines/ (não verificado nesta sessão; conteúdo clínico das mensagens deve citar esta ou a bula do produto, nunca o modelo de IA).
- Base legal: LGPD, Lei 13.709/2018, https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (não verificado nesta sessão). Pelo meu conhecimento prévio, os arts. 7º, 8º e 18 tratam de bases legais, consentimento e direitos do titular, incluindo revogação. Conferir também orientações da ANPD (gov.br/anpd), não consultadas.
- CFMV: o Código de Ética e normas sobre publicidade/propaganda de médico-veterinário e estabelecimentos existem, mas não verifiquei número nem texto vigente das resoluções. Pesquisar em https://www.cfmv.gov.br/ (não verificado).
- Não encontrei, nem pude buscar, estudos sobre eficácia de lembretes automatizados em clínicas veterinárias. Qualquer ganho de adesão vacinal: **não verificado**.

## 2. Forma recomendada: script/planilha (com workflow determinístico leve)

Justificativa: o trabalho é, na maior parte, regra fixa e conferência de dados. Telefone válido, espécie preenchida, nascimento plausível, consentimento registrado, data da última vacina, faixa etária sênior por espécie/porte: tudo isso é filtro determinístico, reproduzível e auditável. Um LLM não acrescenta confiabilidade ali e adiciona risco.

Proposta:
1. Script (Python ou planilha) que lê a exportação CSV do PIMS e gera: (a) relatório de higiene do cadastro (campos faltantes, telefone malformado, duplicatas, nascimento futuro/impossível, espécie inconsistente com serviço); (b) listas por campanha com regras explícitas e versionadas; (c) exclusão automática de quem não tem consentimento registrado, pediu opt-out, ou tem óbito/inativo.
2. Biblioteca de modelos de mensagem pré-aprovados pelo veterinário (texto fixo com variáveis nome do tutor/pet/data). Sem geração livre de texto clínico.
3. Opcional: LLM só para rascunhar variações de tom de modelos, que voltam à aprovação humana. É dispensável no MVP.

Por que não agente: não há decisão aberta que exija raciocínio; um agente com poder de disparo é o pior desenho para risco. Por que não "não automatizar": higiene de base e segmentação são tediosas e propensas a erro humano.

## 3. Human-in-the-loop e riscos

Validação humana obrigatória (veterinário/RT):
- Aprovar cada modelo de mensagem clínica uma vez (e ao mudar), e a lista final de cada campanha por amostragem antes do disparo.
- Decidir regras clínicas de segmentação (intervalo de revacinação, idade sênior, quando sugerir dentística) com base em protocolo da clínica e na diretriz adotada, individualizadas por risco; a regra "todo mundo a cada 12 meses" pode contradizer protocolos atuais.
- Disparo: botão manual após revisão; nada sai sozinho.

Riscos:
- Clínico: mensagem enviando animal a vacina/vermífugo contraindicado (doente, gestante, filhote jovem, histórico de reação). Mitigar com exclusão por flags de prontuário e linguagem que convida a consulta, sem prescrever.
- Alucinação: eliminada se não há texto gerado em produção; se houver rascunho por LLM, revisão humana obrigatória e nenhuma dose/posologia em mensagem.
- Legal, LGPD: dados de tutor são pessoais; marketing exige base legal e canal de opt-out (conforme meu conhecimento prévio, não verificado). Registrar origem e data do consentimento; minimizar campos; não colocar dados reais em ferramentas externas/LLM; cuidado com a lista exportada (acesso, descarte).
- Legal, CFMV/publicidade: mensagens promocionais de procedimentos devem respeitar as normas de publicidade profissional (não verifiquei o texto vigente; o RT deve conferir). Evitar promessas de resultado e apelo comercial indevido em saúde.
- Receituário controlado: fora de escopo; campanhas não devem citar fármacos de controle especial nem oferecer prescrição por mensagem.
- Plataforma: disparo em massa por WhatsApp fora da API oficial pode levar a bloqueio do número (política da Meta não verificada).

## 4. Pontuação (1-5)

- Impacto: **3**. Economiza horas mensais e melhora a higiene de dados, mas o ganho de receita/adesão é incerto e não comprovado aqui.
- Viabilidade: **5** para o script/planilha; 2 para integração direta com o PIMS (depende de exportação/API de cada fornecedor, não verificado).
- Risco: **3** (principalmente LGPD e erro de segmentação clínica); cairia a 2 com texto fixo aprovado e consentimento rigoroso.

## 5. Cabe num MVP testável sem dados reais e sem serviços pagos?

**Sim.** Um script em Python com CSV sintético (tutores/pets fictícios, incluindo casos de erro propositais: telefone inválido, nascimento futuro, sem consentimento, opt-out, duplicata) que produz o relatório de higiene e as listas por campanha, mais modelos de mensagem em arquivo. O disparo fica fora do MVP (apenas gera a lista e as mensagens renderizadas para revisão). Dá para testar regras e exclusões com testes unitários sem custo e sem dado real.

## Próximos passos para verificar (pendentes)

1. Ler a LGPD (arts. 7, 8, 9, 18) e guias da ANPD sobre marketing/consentimento.
2. Consultar CFMV sobre resolução vigente de publicidade/propaganda.
3. Conferir diretriz WSAVA e bulas para os intervalos usados nas regras.
4. Verificar recursos de lembrete/campanha do PIMS em uso antes de construir algo.
