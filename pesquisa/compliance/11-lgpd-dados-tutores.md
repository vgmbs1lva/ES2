# 11. Tratar dados pessoais de tutores sob a LGPD

Data: 2026-10-02. Domínio: compliance.

## Limitação desta análise (leia primeiro)

Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy para planalto.gov.br e gov.br. **Nenhuma fonte foi consultada.** Pela regra do projeto, tudo o que depende de fonte fica como "não verificado". Os links abaixo são apontamentos para o colega conferir, não evidência lida por mim.

## 1. Soluções existentes

Não verificado: nenhum produto, plug-in de PIMS, estudo ou artigo específico de LGPD em clínica veterinária foi confirmado. Não afirmo que existam ou não.

Fontes primárias a conferir antes de agir (não lidas):
- Lei 13.709/2018 (LGPD): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- ANPD, guias e resoluções (agentes de pequeno porte, encarregado, comunicação de incidente): https://www.gov.br/anpd
- CFMV, normas de prontuário (ver `04-prontuario-cfmv-1653-2025-arquivo.md`): https://www.cfmv.gov.br

Pontos a verificar na lei e nas normas da ANPD (do meu conhecimento geral, **não verificado**):
- bases legais aplicáveis ao cadastro de tutor (execução de contrato, obrigação legal/regulatória, legítimo interesse); consentimento pode nem ser a base principal;
- prazos e forma de resposta a pedidos de titular (art. 18 e 19);
- regime simplificado para agentes de pequeno porte e eventual dispensa de encarregado;
- obrigação e prazo de comunicar incidente de segurança;
- conflito entre pedido de eliminação e dever de guarda do prontuário (CFMV).

## 2. Forma recomendada: script/planilha (workflow determinístico leve)

Não é caso para agente de IA. O trabalho é pequeno, recorrente e de baixa variação: manter aviso, inventário de dados, registro de pedidos de titulares com prazo, revisão periódica de acessos e backup. Um modelo gerando resposta jurídica a titular tem risco de alucinação sem ganho que justifique.

Proposta mínima:
1. Planilha de inventário de dados (que dado, onde, base legal, quem acessa, prazo de guarda). Base legal e prazos preenchidos pelo humano após conferir a lei.
2. Registro de solicitações de titulares com data de recebimento, tipo, prazo calculado, status e responsável. Um script/fórmula só calcula prazo e alerta vencimento. O prazo em dias deve ser parâmetro configurável, a confirmar na lei.
3. Checklist periódico (trimestral): revisão de contas de usuários do PIMS, remoção de ex-funcionários, teste de restauração de backup, revisão do aviso de privacidade.
4. Modelos de resposta pré-aprovados (acesso, correção, negativa fundamentada por guarda obrigatória), revisados por advogado.
5. Opcional e secundário: LLM apenas para rascunhar texto simples do aviso de privacidade a partir do inventário, sempre revisado por humano. Não é necessário.

## 3. Humano no circuito e riscos

- Veterinário/responsável pela clínica (controlador) aprova: aviso de privacidade, bases legais, toda resposta a titular, decisão de negar eliminação por dever de guarda, comunicação de incidente.
- Advogado/consultor de LGPD valida modelos e política (recomendado, não verificado se obrigatório).
- Riscos legais: responder fora do prazo; eliminar dado que o CFMV obriga a guardar; vazamento via acesso compartilhado de login, WhatsApp pessoal ou backup sem controle; comunicação de incidente omitida.
- Risco clínico: baixo direto; indireto se eliminação/anonimização corromper prontuário ou histórico vacinal/controlados (receituário controlado tem retenção própria, ver tarefas 01 e 02).
- Alucinação: se usar LLM, ele pode inventar artigo, prazo ou base legal. Por isso fica fora de decisões e respostas ao titular.
- Dados pessoais de tutores nunca devem ir para ferramenta de IA externa sem base e contrato adequados (não verificado o enquadramento de transferência internacional).

## 4. Pontuação

- Impacto: 3. Obrigação legal que evita multa e dano reputacional, mas volume de trabalho baixo para clínica pequena.
- Viabilidade: 5. Planilha e script simples, sem integração.
- Risco: 3. Risco jurídico moderado se feito errado; o automatismo em si é de baixo risco, pois não decide nada.

## 5. MVP sem dados reais e sem serviço pago

Cabe. Entregáveis com dados sintéticos: (a) planilha/CSV de inventário com campos vazios para base legal; (b) script Python que lê um CSV fictício de solicitações, calcula vencimento (prazo parametrizável) e lista atrasados; (c) checklist trimestral em Markdown. Ficam de fora e dependem de conferência humana: conteúdo jurídico, bases legais, prazos oficiais.
