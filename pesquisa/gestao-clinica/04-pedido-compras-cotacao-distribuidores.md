# Pedido de compras e cotação com distribuidores

Domínio: gestão clínica. Data: 2026-10-02.

## Aviso sobre fontes
Nesta rodada o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de egress (simplesvet.com.br, sebrae.com.br). Portanto **nenhuma afirmação factual abaixo tem URL verificada**. Tudo que cita produto, estudo ou norma está marcado "não verificado" e precisa ser conferido antes de ser usado como fato.

## 1. Soluções existentes
- Sistemas de gestão veterinária brasileiros (ex.: SimplesVet, Vetsoft e similares): costumam ter estoque mínimo, entrada por XML de NF-e e contas a pagar. Não verificado (sem URL; nenhuma funcionalidade confirmada).
- PIMS internacionais (ex.: Covetrus/Provet, ezyVet, IDEXX Cornerstone): têm reposição automática e pedido ao distribuidor. Não verificado.
- ERPs genéricos (Bling, Omie, Tiny, Conta Azul): importação de XML, pedido de compra, contas a pagar. Não verificado.
- Estudos sobre gestão de estoque em clínicas veterinárias: não verificado, nada localizado.
- Conceito: ponto de reposição = consumo médio diário x prazo de entrega + estoque de segurança. É fórmula padrão de gestão de estoques; fonte não verificada nesta rodada.

Ação sugerida: antes de construir, conferir se o PIMS atual da clínica já faz ponto de pedido e entrada por XML. Se fizer, a melhor ação é configurar, não construir.

## 2. Forma recomendada: script/planilha (workflow determinístico simples)
Não precisa de agente. As etapas são aritmética e comparação de tabelas:
1. Ponto de reposição por item = consumo médio (últimos 1-3 meses) x lead time + estoque de segurança. Cálculo em planilha.
2. Lista de itens abaixo do mínimo, com quantidade sugerida até o estoque-alvo.
3. Comparação de 2-3 tabelas de preço de fornecedores (menor preço unitário, considerando embalagem, frete, prazo, validade mínima).
4. Geração de rascunho de pedido por fornecedor.
5. Conferência de recebimento: itens, quantidades, lote e validade da NF-e (XML) contra o pedido; divergências listadas.
6. Exportação de contas a pagar para o financeiro/contador.

LLM é opcional e só útil para casar nomes de produtos diferentes entre tabelas (ex.: mesma apresentação com descrições distintas). Mesmo assim, o casamento deve ser aprovado por humano e fixado numa tabela de equivalência (de-para) para não depender do modelo toda vez. Um agente autônomo que emite pedidos é desproporcional ao problema e arriscado (compra errada, valor financeiro).

## 3. Human-in-the-loop, riscos
Validação humana:
- Aprovar parâmetros de mínimo/alvo por item (veterinário/gestor conhece sazonalidade, campanhas, surtos).
- Aprovar o pedido antes do envio; o sistema nunca envia sozinho.
- Aprovar o de-para de produtos equivalentes. Substituição de marca/princípio ativo/concentração é decisão clínica.
- Conferir fisicamente o recebimento (lote, validade, cadeia de frio) e decidir sobre divergências.

Riscos:
- Clínico: substituir medicamento/vacina por apresentação diferente; ruptura de itens críticos (emergência, anestésicos); produto próximo da validade; quebra de cadeia de frio (vacinas, insulina). Mitigação: lista de itens críticos com estoque de segurança maior; de-para somente aprovado.
- Legal: medicamentos controlados (portaria SVS/MS 344/98, receituário e livro de registro) exigem escrituração própria e não devem ser comprados/baixados por fluxo automático; manter fora do escopo ou com fluxo manual. Produtos de uso veterinário têm regras do MAPA; distribuidor deve ser regular. Não verificado (sem URL nesta rodada; conferir texto vigente).
- Fiscal: NF-e e contas a pagar devem seguir a contabilidade da clínica; o script gera lançamento sugerido, não substitui o contador.
- LGPD: baixo. Dados de fornecedores e estoque não são dados pessoais do tutor; não usar dados de pacientes/tutores no fluxo.
- Alucinação: nula se for determinístico; se houver LLM no casamento de nomes, risco de par errado, mitigado por aprovação humana e por nunca deixar o LLM calcular quantidades ou preços.

## 4. Pontuação
- Impacto: 3. Economiza horas por mês e reduz ruptura e compra em excesso, mas é tarefa semanal/mensal, não diária. Ganho financeiro não quantificado (sem estudo verificado).
- Viabilidade: 5. Planilha/script com CSV e XML de NF-e; sem serviço pago.
- Risco: 2. Principalmente financeiro e de substituição de produto; mitigado por aprovação humana e exclusão de controlados.

## 5. Cabe em MVP sem dados reais e sem serviço pago? Sim
Script Python (ou planilha) com dados sintéticos:
- CSV de estoque (item, saldo, mínimo, consumo mensal, lead time).
- 3 CSVs de tabelas de preço de fornecedores fictícios.
- XML de NF-e sintético para teste de conferência de recebimento.
- Saídas: lista de reposição, pedido rascunho por fornecedor, relatório de divergências, CSV de contas a pagar.
Itens controlados ficam sinalizados e excluídos do pedido automático.
Nesta rodada o protótipo não foi implementado; esta é só a análise.

## Pendências de verificação
Funcionalidades dos PIMS/ERPs, portaria 344/98 e normas do MAPA, fórmula de ponto de pedido e estudos sobre estoque veterinário: todos "não verificados".
