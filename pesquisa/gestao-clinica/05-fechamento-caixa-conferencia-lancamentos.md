# Fechamento de caixa diário e conferência de lançamentos

Domínio: gestão clínica. Data: 2026-10-02.

## Aviso sobre fontes
Nesta rodada o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy (bcb.gov.br e simplesvet.com.br). **Nenhuma afirmação factual externa foi verificada.** Tudo abaixo que depende de fonte está marcado "não verificado". Antes de decidir compra ou investimento, repetir a pesquisa.

## 1. Soluções existentes
- Sistemas de gestão veterinária brasileiros (ex.: Simples Vet, Vetsystem e similares): têm módulo financeiro/caixa. Se conciliam cartão/PIX automaticamente com atendimentos: **não verificado**.
- Adquirentes (Stone, Cielo, Rede etc.) e ERPs financeiros: oferecem conciliação de vendas por arquivo/API. Formatos, custos e disponibilidade: **não verificado**.
- Pix (Banco Central): extrato bancário com identificação do pagador e, em cobrança por QR dinâmico, identificador da transação. Detalhes técnicos: **não verificado**.
- Estudos sobre perda de receita por cobranças não lançadas em clínicas veterinárias: **não verificado**; não citar percentuais de mercado sem fonte.

## 2. Forma recomendada: script/planilha (workflow determinístico)
A conciliação em si é correspondência de valores, datas e identificadores entre três listas (caixa/PIX, maquininha, atendimentos lançados). É problema determinístico: script (Python/pandas) ou planilha com regras fixas resolve, é auditável e não alucina. Agente LLM só se justifica numa camada opcional e posterior: sugerir "procedimento descrito no prontuário sem item cobrado" por leitura de texto livre, sempre como sugestão.

Pipeline proposto:
1. Importar CSV/XLSX exportado do sistema, da maquininha e do extrato bancário.
2. Normalizar (valor em centavos, data, forma de pagamento, taxa/MDR).
3. Casar por valor+data+bandeira/NSU/identificador; tolerância configurável; casos 1:N e N:1 (parcelado, pagamento dividido).
4. Gerar lista de divergências: recebido sem lançamento, lançado sem recebimento, valor diferente, duplicidade.
5. Cruzar atendimentos/procedimentos do dia (campo estruturado) com itens cobrados: regra "procedimento X exige item financeiro Y" (tabela de equivalência mantida pela clínica).
6. (Opcional) LLM lê texto livre do prontuário para sugerir cobranças esquecidas, marcadas como "sugestão, baixa confiança".

## 3. Human-in-the-loop e riscos
- Veterinário/gestor valida: toda divergência antes de corrigir lançamento; toda sugestão de cobrança extra (quem realizou o ato confirma que foi feito); fechamento final. O sistema nunca altera lançamento sozinho nem cobra tutor.
- Clínico: baixo; não decide conduta. Risco indireto: cobrar procedimento não realizado ou pressionar a conduta por receita.
- Legal/fiscal: cobrança indevida a tutor (CDC); estorno/ajuste deve ser rastreável; guardar log de alterações. Regras fiscais e de nota: **não verificado**, consultar contador.
- LGPD: dados de tutor (nome, CPF, pagamentos) são pessoais; minimizar (usar ID do atendimento, mascarar CPF), processar localmente, não enviar prontuário a LLM externa sem base legal e contrato. Detalhe normativo: **não verificado**.
- CFMV: prontuário é documento do médico-veterinário; o script só lê. Receituário controlado: fora do escopo; não tocar. Normas específicas: **não verificado**.
- Alucinação: nula na parte determinística; relevante apenas na camada LLM (inventar procedimento). Mitigar exigindo citação do trecho do prontuário e confirmação humana.

## 4. Pontuação (1-5)
- Impacto: 3. Fechamento diário consome tempo e vazamento de receita é plausível, mas magnitude **não verificada**.
- Viabilidade: 4. Depende de exportação de dados do PIMS; se só houver tela sem export, cai para 2.
- Risco (5 = pior): 2. Dados financeiros pessoais e cobrança indevida, sem risco clínico direto.

## 5. MVP sem dados reais e sem serviço pago
Sim. Gerar dados sintéticos (CSV de atendimentos, maquininha, extrato PIX) com divergências plantadas (esquecido, duplicado, valor trocado, parcelado) e implementar o conciliador em Python/pandas, medindo precisão/recall das divergências detectadas. Fica fora do MVP: integração real com PIMS/adquirente e a camada LLM sobre prontuário.
