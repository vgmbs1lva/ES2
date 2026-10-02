# 08 - Registrar vacinação antirrábica e emitir atestado/carteira

Data: 2026-10-02. Domínio: compliance.

## Limitação desta pesquisa (leia primeiro)
Nesta execução o limite de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy
(gov.br e planalto.gov.br). Portanto **nenhuma afirmação factual abaixo foi verificada com URL**.
Tudo que é fato externo está marcado "não verificado" e deve ser conferido antes de uso.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com carteira de vacinação e atestado: não verificado (sem busca). Hipótese a confirmar: PIMS veterinários brasileiros
  geralmente têm módulo de vacinas e impressão de carteira/atestado. Nome de produto: não verificado.
- Exigência federal de livro próprio: não verificado (já constava na descrição da tarefa). Depende da vigilância municipal/estadual.
- Normas a consultar (existência e teor não verificados): CFMV (regras de atestado e prontuário), MAPA (trânsito/viagem de animais, CVI),
  Ministério da Saúde/PNCRaiva (vacinação antirrábica), LGPD (Lei 13.709/2018, dados do tutor), regra do município e do destino/companhia aérea.

## 2. Forma recomendada: workflow determinístico (formulário + template + validações), sem agente de IA
Justificativa: a tarefa é transcrever campos estruturados (animal, lote, validade, data, vacina, fabricante) e gerar documento a partir
de modelo. Não há interpretação ambígua; LLM só adiciona risco de alucinação em lote/validade/data, que são dados legais.
Algo simples resolve: planilha ou formulário com validação + gerador de PDF a partir de template, assinatura do veterinário.
IA opcional e secundária: OCR/leitura da etiqueta do frasco por foto para pré-preencher lote/validade, sempre confirmado por humano;
ou checar se o destino exige itens adicionais (esse ponto exigiria fonte oficial e conferência humana).

Workflow:
1. Veterinário escolhe vacina em lista de produtos cadastrados (fabricante, registro MAPA: não verificado a fonte de consulta).
2. Informa/foto do lote e validade; sistema valida formato, validade >= data de aplicação, data de aplicação não futura.
3. Calcula próxima dose conforme regra configurável (a validar pelo vet; não codificar de memória).
4. Gera carteira/atestado em PDF por template com campos fixos; vet revisa e assina (ICP-Brasil ou manuscrito, conforme exigência local: não verificado).
5. Grava registro com trilha de auditoria.

## 3. Human-in-the-loop, riscos
- Validação obrigatória: o médico-veterinário confere identificação do animal, lote, validade, data, e assina. Atestado é ato profissional; não pode ser emitido/assinado automaticamente.
- Clínico: vacinar animal doente/inapto ou aplicar vacina vencida/mal armazenada; checagem de validade ajuda, mas não substitui o exame.
- Legal/CFMV: responsabilidade pelo conteúdo do atestado é do signatário; exigências de forma (identificação, CRMV, assinatura) não verificadas.
  Atestado falso ou lote errado tem implicação ética e legal.
- LGPD: dados do tutor (nome, CPF, contato) são pessoais; minimizar, base legal, retenção, controle de acesso. Não enviar a LLMs externos.
- Receituário controlado: não se aplica à vacina antirrábica (não verificado formalmente).
- Alucinação: se houver LLM, jamais deve gerar lote, validade ou data; campos vêm só de entrada humana ou OCR confirmado.

## 4. Pontuação (1-5)
- Impacto: 3 (tarefa frequente e repetitiva, mas já coberta por PIMS comuns; ganho é minutos por atendimento).
- Viabilidade: 5 (determinístico, ferramentas simples).
- Risco: 3 (documento de valor legal; erro de dado ou assinatura indevida; baixo se houver validação humana).

## 5. MVP sem dados reais e sem serviços pagos: sim
Cabe como script Python/planilha: JSON de vacinas fictícias, validações de lote/validade/data, geração de HTML/PDF por template com dados sintéticos,
log de auditoria local, testes unitários das regras (validade vencida, data futura, campos faltando). Assinatura digital e integração com PIMS ficam fora do MVP.

## Pendências de verificação
Normas federais/municipais de registro e atestado, requisitos de CVI/viagem, requisitos de assinatura digital, produtos de mercado, estudos sobre erros de registro vacinal.
