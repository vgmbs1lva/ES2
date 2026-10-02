# Relatório de encaminhamento, resumo de alta e comunicação ao tutor

Domínio: apoio-clinico | Data da análise: 2026-10-02

Nota de método: só consegui ler snippets de busca. WebFetch foi bloqueado pelo proxy (crmvrn.gov.br e vetgeni.com), então nada abaixo foi verificado no texto integral. Onde falta fonte, está escrito "não verificado".

## 1. Tarefa e carga
~10 min x 10-15/semana = 1,7 a 2,5 h/semana por veterinário. Âncora de carga administrativa: relatório FVE 2025 (https://fve.org/cms/wp-content/uploads/Admin-burden-report-R13-1.pdf, https://fve.org/understanding-the-growing-administrative-burden-in-veterinary-practice/). Só vi snippets, amostra pequena e contexto europeu: serve como indício, não como medida para o Brasil. A estimativa de tempo vem do usuário, não de medição.

## 2. Soluções existentes
- Scribes veterinários com resumo de alta, carta de encaminhamento e resumo ao tutor a partir da consulta: ScribbleVet, VetRec, CoVet, Coggo, PawfectNotes, Provet Clinical AI, Digitail (embutido no PIMS próprio). Fontes (snippets de busca, conteúdo majoritariamente de fornecedores/blogs comerciais):
  - https://www.provet.com/product/clinical-ai
  - https://co.vet/post/after-a-veterinary-ai-scribe-generates-the-note/
  - https://pawfectnotes.com/medical-records/discharge-note/
  - https://www.coggo.ai/
  - https://www.vetgeni.com/guides/veterinary-ai-scribe-buyers-guide-2026
  - https://ownerexchange.com/best-veterinary-ai-scribes/
  - https://www.vetsoftwarehub.com/article/veterinary-ai-scribe-pricing-comparison-2026 (preços de US$40 a 450/mês, segundo o título)
- Integrações com PIMS citadas: ezyVet, Pulse/Covetrus, Vetspire (ScribbleVet). São PIMS estrangeiros; compatibilidade com PIMS brasileiros e suporte a pt-BR: não verificado.
- Estudos: não achei estudo veterinário sobre alta/encaminhamento gerados por LLM. Em medicina humana: revisão sistemática (https://link.springer.com/article/10.1007/s13721-026-00876-3); LLMs abertos extraem bem mas alucinam, com fatos sem suporte ou incorretos (https://arxiv.org/pdf/2504.19061); GPT-3.5 em instruções pré-operatórias: 70,2% de acurácia e 1,2% de alucinação (via snippet; artigo https://mededu.jmir.org/2025/1/e70190/PDF, não conferido). Transferência para veterinária é inferência minha.
- Normas: Resolução CFMV 1.321/2020 (prontuário, atestados, termos de consentimento; guarda mínima de 5 anos; termos exigidos antes de procedimentos) e alteração pela Res. CFMV 1.653/2025, segundo snippets. Links: https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf, https://www.crmvrn.gov.br/2021/02/02/prontuarios-atestados-termos-de-consentimento-conheca-normas-sobre-documentos-medico-veterinarios/. Texto integral e o que a 1.653/2025 mudou: não verificado.

## 3. Forma recomendada: workflow (modelos + preenchimento assistido), não agente autônomo
Os três documentos são variações da mesma informação estruturada do prontuário. Caminho mais simples:
1. Modelos fixos (Markdown/Word) para encaminhamento, alta e consentimento, com campos obrigatórios (identificação, anamnese, achados, exames, diagnóstico/suspeita, tratamentos e doses dadas, pendências, sinais de alerta, retorno).
2. Um passo de LLM só para redigir narrativa e reescrever linguagem leiga, restrito aos campos fornecidos, com instrução de "não inferir; marcar [FALTA]" quando faltar dado.
3. Termos de consentimento: NÃO gerar por LLM; usar texto padrão revisado (CFMV/jurídico) e preencher só campos. Nenhum benefício em deixar o modelo redigir cláusula legal.
4. Respostas a dúvidas de tutor por mensagem: só rascunho para o veterinário aprovar; nunca envio automático.
Agente autônomo não se justifica: o ganho vem do rascunho, e autonomia só acrescenta risco. Integração com PIMS fica para depois, se o piloto funcionar.

## 4. Human-in-the-loop e riscos
Validação obrigatória do veterinário em cada documento antes de assinar/enviar: o texto é ato médico-veterinário e leva sua responsabilidade (CFMV 1.321/2020, a confirmar no texto integral). Checklist de revisão: doses, unidades, espécie/peso, nome do fármaco, datas, achados negativos omitidos, lateralidade.
- Alucinação/omissão: dose inventada, exame não feito citado, diagnóstico dado como confirmado quando era suspeita. Mitigação: saída com citação do campo de origem, marcação de lacunas, revisão lado a lado.
- Medicamentos controlados: o LLM não deve prescrever nem preencher receituário (Portaria SVS/MS 344/98 e normas do CFMV); fora do escopo. Detalhes regulatórios: não verificado.
- LGPD: dados do tutor são pessoais (nome, telefone, endereço); enviar a API externa exige base legal, contrato com operador e minimização. Dados do animal isolados não são dados pessoais, mas se ligam ao tutor. Parecer jurídico: não verificado. No MVP, só dados sintéticos.
- Prontuário: o rascunho não substitui o registro; guarda e assinatura conforme CFMV 1.321.
- Comunicação ao tutor: risco de promessa de prognóstico ou orientação de dose por mensagem; rascunhos devem incluir quando procurar emergência.
- Viés de automação: revisar só por "ok" após semanas de rascunhos corretos. Amostrar auditorias periódicas.

## 5. Pontuação (1-5)
- Impacto: 3. Economia plausível de 1-2 h/semana, mas estimativa não medida; ganho real depende de revisão rápida.
- Viabilidade: 4. Produtos prontos existem; o workflow caseiro é simples. Reduz um ponto o pouco suporte verificado a pt-BR/PIMS brasileiros.
- Risco: 3 para encaminhamento/alta com revisão; seria 4-5 se envio fosse automático ou se gerasse consentimento/receita.

## 6. MVP testável sem dados reais e sem serviço pago
Sim, em parte. Cabe um script/template com 5-10 casos sintéticos fictícios (JSON de prontuário -> documentos Markdown), com validações determinísticas: campos obrigatórios, checagem de unidades de dose e coerência dose x peso contra um limite configurável, relatório de lacunas. A parte de LLM não é gratuita por padrão (modelo local aberto é possível, qualidade em pt-BR a testar). Medir: tempo de revisão vs. redação manual, taxa de erros que escaparam, em casos sintéticos com erros plantados.
