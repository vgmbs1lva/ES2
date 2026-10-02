# 10 - Controle documental e conformidade (livro de controlados, vacinas, notificações, arquivamento)

Data da análise: 2026-10-02. Domínio: administrativo.

## 1. Tarefa
Conferir registros de controlados, lançar vacinas/certificados e arquivar documentos assinados. Entradas: receitas retidas, estoque, fichas de vacinação. Saídas: livros/planilhas atualizados, arquivo organizado.

## 2. O que a pesquisa encontrou (com fontes)

Normas (verificadas só via resultados de busca; os textos integrais não puderam ser abertos, pois legisweb, flyvet e migalhas foram bloqueados pelo proxy):
- Portaria MAPA nº 837, de 23/09/2025: regime de controle especial para substâncias controladas de uso veterinário (aquisição, escrituração, prescrição, dispensação, rotulagem). Exige livro próprio com entrada, saída, uso e perda; prescrição via sistema do MAPA (SIPEAGRO); aquisição por notificação. Fontes: https://www.legisweb.com.br/legislacao/?id=488965 ; https://www.agricultura.rs.gov.br/upload/arquivos/202602/19162152-portaria-mapa-837-2025-subst-controladas.pdf ; ofício circular MAPA 6/2026 (gov.br, listado na busca). Prazos de escrituração, tempo de guarda e relatórios periódicos: NÃO VERIFICADO (ler o PDF oficial).
- Portaria SVS/MS 344/98 (humano): livro de registro específico, uma página por substância, manual ou informatizado, atualização semanal (modelo Anexo XVIII); medicamentos veterinários seguem legislação específica. Fonte: https://antigo.anvisa.gov.br/documents/10181/2718376/PRT_SVS_344_1998_COMP.pdf . Serve de referência, mas a base para clínica veterinária é a 837/2025; confirmar com o CRMV qual regime vale no seu caso (inclusive se SNGPC se aplica; resultados de busca sobre SNGPC veterinário vieram de fontes secundárias, NÃO VERIFICADO).
- Prontuário: Resolução CFMV 1.321/2020, alterada pela 1.653/2025; guarda de ao menos 5 anos após o último atendimento; cópia ao tutor em até 5 dias úteis (até 30 em casos justificados). Fontes secundárias: https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ ; https://www.crmvrj.org.br/prontuarios-medico-veterinarios-quando-solicitados-pelos-clientes-deverao-ser-entregues-em-ate-cinco-dias-uteis-e-nao-mais-de-forma-imediata/ . Texto oficial: não verificado.
- Guia de prescrição (CRMV-MG/PR): https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf

Soluções existentes (todas só vistas em resultados de busca, sem avaliação de qualidade):
- PIMS/apps com carteira de vacinação, lembretes, estoque: TG Pet https://tgpet.com.br/funcionalidades/controle-vacinas ; Anota Pet https://www.anotapet.com/ ; Simples.vet (prescrição de controlados) https://suporte.simples.vet/pt-BR/articles/3293097-como-criar-prescricao-de-medicamentos-sujeitos-ao-controle-especial ; Vetnaut https://vetnaut.com/blog/modelo-prontuario-veterinario/
- Projeto open source de vacinas/estoque/lembretes WhatsApp: https://github.com/carlosdsaquino-sys/Sistema-de-vacina-o-de-pets (não auditado).
- Estudos/artigos sobre IA nessa tarefa: não encontrei. Não verificado.

## 3. Forma recomendada: workflow determinístico + planilha (sem agente)
Justificativa: a tarefa é regra fixa (saldo = saldo anterior + entradas - saídas - perdas; receita sem lançamento; vacina com data/lote/validade faltando; vencimentos). Isso é script/planilha com validações, não exige LLM. O custo de erro (fiscalização, livro de controlado) é alto e o LLM pode alucinar números. Uso opcional de LLM restrito a extrair campos de foto/PDF de receita ou de ficha de vacina para pré-preencher uma linha, sempre com conferência humana.

Componentes:
1. Planilha/CSV de livro por substância (colunas: data, DCB/nome comercial, lote, validade, entrada, saída, perda, saldo, nº notificação, tutor/paciente por ID interno).
2. Script de conferência: recalcula saldos, acusa divergência com contagem física, itens sem notificação vinculada, lançamentos atrasados, lotes vencidos/próximos do vencimento.
3. Registro de vacinas: tabela com campos obrigatórios e checagem de lote/validade/próxima dose; geração de lembretes.
4. Arquivamento: convenção de nomes e pastas (ano/tipo/ID), checklist de assinatura, cópia de segurança e verificação de integridade (hash).

## 4. Human-in-the-loop e riscos
- O veterinário (RT) assina e valida: todo lançamento no livro de controlados, contagem física periódica contra saldo, qualquer divergência, emissão de receita/notificação (sistema oficial do MAPA, nunca pelo script), e certificados de vacina. A automação só sinaliza, não escritura sozinha.
- Legal: o livro é documento fiscalizável; o script não substitui o livro oficial se a norma exigir formato específico (verificar 837/2025). Assinatura digital: usar ICP-Brasil/sistema oficial; validade de documento eletrônico para cada caso não verificada.
- LGPD: dados de tutores são pessoais; minimizar (usar IDs), armazenamento com acesso restrito, sem enviar a LLM de terceiros sem base legal e contrato. Base normativa LGPD (Lei 13.709/2018) citada de memória; não verificada nesta pesquisa.
- Alucinação: LLM nunca calcula saldo nem preenche lote/dose; extração de imagem deve mostrar o original ao lado e exigir confirmação.
- Clínico: erro de lote/validade de vacina ou de controlado afeta rastreabilidade e segurança do paciente.

## 5. Pontuação (1-5)
- Impacto: 3 (trabalho recorrente e chato, evita autuação, mas não é gargalo clínico)
- Viabilidade: 5 para o workflow determinístico; 2 para extração por LLM de documentos manuscritos
- Risco: 3 (legal alto se mal feito; mitigado por validação humana e por não automatizar a escrituração/assinatura)

## 6. MVP sem dados reais e sem serviços pagos
Cabe. Um script Python local lendo CSVs sintéticos (livro, receitas, vacinas), com testes: recalcular saldo, detectar divergências, itens sem notificação, vacinas com campos faltando ou vencidas, e relatório em Markdown. Sem LLM no MVP.
