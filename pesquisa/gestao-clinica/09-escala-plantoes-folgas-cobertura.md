# Escala de plantões, folgas e cobertura

Domínio: gestão clínica. Data da análise: 2026-10-02.

## Limitação desta pesquisa (leia primeiro)

Nesta execução o orçamento de WebSearch estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br, developers.google.com). **Nenhuma fonte foi consultada.** Por regra, tudo que é afirmação factual externa abaixo está marcado como "não verificado" e sem URL inventada. Antes de usar, confirmar nas fontes primárias indicadas (somente nomes de onde procurar, não citações).

## 1. Soluções existentes

- Softwares genéricos de escala (Deputy, When I Work, Humanity, Tangerino/Ponto, Pontomais etc.) e módulos de agenda de RH: existência plausível, funcionalidades e preços **não verificados**.
- Módulos de escala de equipe em PIMS veterinários: **não verificado**; não afirmo que algum PIMS tenha.
- Literatura de "nurse/employee scheduling problem" e solvers (OR-Tools CP-SAT, em developers.google.com/optimization): conhecidos, mas não consegui abrir a página; **não verificado** nesta sessão.
- Legislação a conferir na fonte primária (Planalto/TST): CLT arts. 58-59 (jornada e horas extras), 59-A (12x36), 66 e 71 (interjornada e intervalo), 67 (DSR), 244 (sobreaviso), 129 e ss. (férias); convenção coletiva da categoria e contrato individual. Conteúdo exato **não verificado**.
- LGPD: dados de disponibilidade/saúde/ponto de funcionários são dados pessoais; base legal e minimização a confirmar com jurídico. Não verificado.

## 2. Forma recomendada: script/planilha (workflow determinístico simples)

**Recomendação: script/planilha com validador de regras, sem agente de IA para decidir a escala.**

Justificativa:
- É um problema de restrições (cobertura mínima por turno, descanso entre jornadas, DSR, limite de horas, férias, qualificações como "habilitado a internação/anestesia"). Regras são explícitas e verificáveis; um solver/heurística ou até planilha com checagens resolve e é auditável.
- LLM não deve gerar a escala diretamente: pode violar restrições trabalhistas silenciosamente e é não determinístico. Uso aceitável de LLM: apenas para ler pedidos de troca em texto livre e transformá-los em registros estruturados, sempre confirmados por um humano.
- Passo 1 (barato): planilha com regras e validação automática (conflitos, horas, descanso mínimo). Passo 2: gerador por restrições (CP-SAT ou guloso) quando a equipe passar de poucas pessoas. Passo 3 opcional: notificação e registro de trocas.

## 3. Human-in-the-loop, riscos

- Validação: o responsável técnico/gestor aprova a escala antes de publicar; trocas exigem aceite das duas partes e aprovação do gestor; o sistema só **sinaliza** violações, o humano decide.
- Cobertura clínica: garantir sempre ao menos um médico-veterinário habilitado presente/sobreaviso para internação; checagem da exigência de responsável técnico e normas do CFMV a confirmar (não verificado).
- Legal trabalhista: erro de regra gera passivo (horas extras, intervalo). Regras devem ser parametrizadas por contrato/convenção e revisadas por contador/advogado trabalhista. Pagamento de plantões de profissional PJ/autônomo vs CLT: atenção a risco de vínculo (não verificado).
- LGPD: restringir acesso, não coletar motivos de saúde de ausência além do necessário.
- Receituário controlado: não é afetado diretamente, mas a escala deve garantir quem detém autorização/responsabilidade em cada turno (a confirmar com a regulação aplicável; não verificado).
- Alucinação: se houver LLM, limitá-lo a extrair campos (quem, data, troca) e nunca inventar regras legais; regras vêm de configuração versionada.

## 4. Pontuação (honesta)

- Impacto: 3 (poupa horas do gestor por mês e reduz conflitos; baixo em clínicas pequenas).
- Viabilidade: 4 (problema bem definido, ferramentas abertas).
- Risco: 2 (sem dado clínico de pacientes; risco principal trabalhista e de cobertura, mitigado por revisão humana).

## 5. MVP sem dados reais e sem serviços pagos

Cabe. Protótipo: CSV sintético de equipe, disponibilidades e regras parametrizáveis; script Python que gera escala (guloso ou CP-SAT local, gratuito), valida restrições, e exporta CSV/planilha; registro de trocas em arquivo. Testes com equipe fictícia. Não incluído: integração com PIMS, ponto eletrônico, notificações.
