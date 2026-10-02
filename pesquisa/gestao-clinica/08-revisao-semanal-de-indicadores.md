# Revisão semanal de indicadores

Domínio: gestão clínica. Data: 2026-10-02.

## Aviso sobre fontes
Nesta rodada o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy (www.aaha.org). **Nenhuma afirmação factual externa foi verificada; não há URLs citadas.** O que depende de fonte está marcado "não verificado". Repetir a pesquisa antes de decidir compra.

## 1. Soluções existentes
- Módulos de relatório/dashboard dos PIMS brasileiros (Simples Vet, Vetsystem e similares): provavelmente trazem ticket médio, faturamento por profissional e agenda. Quais indicadores exatos, se exportam CSV/API: **não verificado**.
- Ferramentas de BI (Looker Studio, Power BI, Metabase) conectadas a planilha/exportação: existem, mas o plano gratuito, os conectores e o custo para este caso: **não verificado**.
- Benchmarks de KPIs de clínicas veterinárias (AAHA, associações brasileiras): **não verificado**; não usar números de mercado como meta sem fonte. A meta deve vir da própria planilha de metas da clínica e do histórico dela.
- Estudos sobre efeito de revisão periódica de KPIs em resultado de clínicas: **não verificado**.

## 2. Forma recomendada: script/planilha (workflow determinístico)
Os indicadores são aritmética sobre exportações: ticket médio = faturamento / atendimentos pagos; consultas; faturamento por veterinário; taxa de retorno (definição fixa, ex.: retorno agendado compareceu / retornos agendados); faltas / agendados; margem = (preço - custo) / preço; giro = custo das saídas / estoque médio. Planilha com fórmulas ou script Python/pandas que lê os CSV, compara com a meta e a semana anterior e marca desvios (regra: fora de ±X% da meta ou da média das 4 semanas) resolve de forma auditável e sem alucinação. Agente LLM não é necessário; no máximo uma camada opcional que redige em linguagem natural as 1-3 ações a partir dos desvios já calculados, usando só números fornecidos, ou melhor, ações de uma tabela de regras ("faltas acima da meta -> reforçar confirmação").

Pipeline:
1. Exportar relatórios do sistema (CSV/XLSX) e carregar a planilha de metas.
2. Normalizar e calcular indicadores com definições escritas e fixas (glossário na própria planilha).
3. Comparar com meta e histórico; sinalizar desvios; alertar amostra pequena (poucos atendimentos por veterinário).
4. Gerar painel de uma página (tabela com setas/semáforo) e rascunho de 1-3 ações.
5. Gestor escolhe as ações.

## 3. Human-in-the-loop e riscos
- Valida: gestor/veterinário responsável confere os números (batem com o sistema?), escolhe as ações e decide. Nada é aplicado automaticamente.
- Clínico: baixo direto. Risco indireto relevante: faturamento por veterinário e ticket médio podem virar pressão para vender mais exames/procedimentos e distorcer conduta clínica. Mitigar: não usar ranking individual como meta de desempenho; ler junto a desfechos e satisfação.
- Legal: LGPD, pois dados por veterinário são dados pessoais de funcionários/colaboradores e os de origem são de tutores; trabalhar com agregados, sem nome de tutor/paciente; processar localmente. Uso de métricas individuais na relação de trabalho: consultar advogado trabalhista (**não verificado**). CFMV/receituário controlado: fora do escopo; o painel não deve tocar prontuário nem controlados (o giro de estoque pode incluir controlados só como quantidade; normas de controle de estoque desses itens: **não verificado**).
- Alucinação: nula no cálculo; só na camada de texto, mitigada gerando ações de regras e exibindo os números ao lado.
- Risco de qualidade de dados: definições inconsistentes (o que é "retorno", consulta cancelada, desconto) geram conclusões erradas. Documentar definições.

## 4. Pontuação (1-5)
- Impacto: 3. Poupa uma ou duas horas semanais e dá consistência de acompanhamento, mas o ganho vem da decisão, não do painel; magnitude **não verificada**.
- Viabilidade: 4. Fácil se o PIMS exporta CSV; cai para 2 se só tiver tela/PDF.
- Risco (5 = pior): 2. Sem risco clínico direto; viés de incentivo e dados pessoais de equipe.

## 5. MVP sem dados reais e sem serviço pago
Sim. Gerar CSV sintéticos (atendimentos, agenda com faltas/retornos, vendas e estoque com custo) e uma planilha de metas fictícia; script Python/pandas (ou planilha) que calcula os sete indicadores, compara com meta/semana anterior, produz painel em HTML/Markdown e 1-3 ações por regras. Teste: conferir os indicadores contra valores calculados à mão nos dados sintéticos e verificar que os desvios plantados são sinalizados. Fora do MVP: integração real com PIMS e camada LLM.
