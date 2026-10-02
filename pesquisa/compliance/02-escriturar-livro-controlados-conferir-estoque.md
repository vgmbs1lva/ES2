# Escriturar o livro/sistema de registro de controlados e conferir estoque

Domínio: compliance. Data da análise: 2026-10-02.

## Aviso sobre verificação

Nesta execução WebSearch estava sem orçamento (200/200) e WebFetch foi bloqueado pelo proxy para legisweb.com.br, flyvet.com.br e gov.br. Portanto **nenhuma afirmação normativa ou de produto abaixo foi verificada**. Tudo o que depender de norma está marcado "não verificado" e deve ser confirmado antes de uso.

Fontes indicadas na tarefa (não lidas por mim):
- https://www.legisweb.com.br/legislacao/?id=317701 (base normativa; não verificado o conteúdo)
- https://www.flyvet.com.br/geo/controle-medicamento-controlado-clinica-veterinaria-livro-registro-mapa/ (blog comercial; não verificado)

## 1. Soluções existentes

Não verificado: não consegui pesquisar. Categorias a investigar (sem afirmar que existem com essa funcionalidade): módulo de controlados em PIMS/ERP veterinário; planilha de livro de registro; sistemas de farmácia com escrituração de portaria 344 (uso humano, a verificar adaptação). Pendente: pesquisar quando houver orçamento de busca, e checar a norma aplicável (a base legal citada, e se o MAPA ou a ANVISA/SVS é o órgão relevante, e se há obrigação de envio periódico para veterinária) em fontes oficiais.

## 2. Forma recomendada: script/planilha (workflow determinístico)

Justificativa: a tarefa é contábil e regrada (entrada, saída, saldo, perdas). Exige exatidão aritmética e rastreabilidade, não interpretação. Um LLM agregaria risco de alucinação sem ganho. Recomendo planilha/script com:
- lançamentos append-only (entrada com nº da NF, lote, validade; saída com nº da notificação/receita; perda/quebra com justificativa);
- saldo calculado por fórmula, nunca digitado;
- conferência: campo de contagem física, diferença calculada, alerta se diferente de zero;
- validações: saída maior que saldo, lote vencido, campos obrigatórios vazios;
- relatório periódico exportável (formato exato conforme norma: não verificado).

IA opcional e limitada: extrair campos de PDF/foto de NF para pré-preencher, sempre confirmado por humano. Não é necessária no MVP.

Não automatizar: a contagem física, o armário trancado, a assinatura/responsabilidade técnica.

## 3. Human-in-the-loop e riscos

- Médico-veterinário/responsável técnico confere cada lançamento de entrada e saída, faz e assina a contagem física, e aprova baixas por perda/quebra.
- Legal: livro e notificações têm responsabilidade do RT; prazos de guarda e formato dependem da norma (não verificado). O sistema não substitui o livro oficial se a norma exigir formato/rubrica específicos (não verificado).
- Dados: usar apenas dados de estoque e documentos; evitar dados de tutores/pacientes (LGPD). Se a notificação contiver dados pessoais, guardar o mínimo, com acesso restrito.
- Alucinação: nula no núcleo determinístico; só existe se houver extração por IA de NF, mitigada por confirmação humana.
- Risco de fraude/desvio: manter trilha de auditoria; não permitir edição/exclusão silenciosa de lançamentos.
- Se a clínica só prescreve, a tarefa não se aplica.

## 4. Pontuação

- Impacto: 3. Tarefa recorrente e com risco de autuação, mas só para clínicas que mantêm controlados.
- Viabilidade: 5. Planilha/script simples.
- Risco: 3. Consequência legal de erro de escrituração; o risco técnico é baixo.

## 5. MVP sem dados reais e sem serviços pagos

Sim. Um script Python + CSV (ou planilha) com dados sintéticos, testes de saldo, de saída maior que saldo, e de divergência na conferência. Os campos exatos do livro oficial precisam ser confirmados na norma antes de qualquer uso real.
