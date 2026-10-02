# Contas a pagar, repasses e conferência de notas fiscais

Domínio: gestao-clinica | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch bloqueou os domínios oficiais (nfe.fazenda.gov.br, planalto.gov.br). Nenhuma afirmação factual externa foi verificada. Tudo que depende de fonte está marcado como "não verificado" e deve ser confirmado antes de uso.

## 1. Soluções existentes
- Produtos de PIMS/ERP veterinário com módulo financeiro e comissão por profissional: não verificado (nenhuma URL confirmada). Procurar na documentação do PIMS usado na clínica.
- ERPs financeiros genéricos com leitura de XML de NF-e e agenda de contas a pagar: não verificado.
- Padrão técnico: NF-e tem XML estruturado com chave de acesso de 44 dígitos, que permite conferência determinística (CNPJ, valor, itens, vencimento das duplicatas). Portal oficial: https://www.nfe.fazenda.gov.br (não foi possível acessar; não verificado).
- Regras de repasse a veterinário autônomo/parceiro (contrato de parceria, retenções, tributos): não verificado. Conferir com contador e com legislação aplicável (a lei do salão-parceiro costuma ser citada por analogia, mas não confirmei se se aplica a clínicas veterinárias).

## 2. Forma recomendada: workflow determinístico / script-planilha
Justificativa:
- Os cálculos (repasse = produção x percentual contratado - descontos/retenções; vencimentos; fluxo de caixa) são aritmética com regras fixas. LLM não agrega valor nem deve calcular dinheiro.
- Parsing de XML de NF-e e comparação com boleto/pedido é determinístico.
- Único uso opcional de IA: extrair campos de boletos/PDFs sem XML (OCR), sempre com dupla conferência pelo código (linha digitável tem dígito verificador).
- Não é caso de agente autônomo: pagar dinheiro é ação irreversível.

Pipeline: (a) importar XML/CSV de produção por veterinário; (b) validar chaves e totais; (c) tabela de regras de repasse por profissional (percentual, tabela de serviços, deduções); (d) gerar calendário de pagamentos e fluxo de caixa; (e) relatório de divergências.

## 3. Human-in-the-loop, riscos
- Validação obrigatória: dono/gestor aprova cada lote de pagamento e cada demonstrativo de repasse antes de enviar ao profissional. O sistema nunca executa pagamento nem acessa banco com poder de transferência.
- Veterinário (profissional) confere seu demonstrativo de produção; contestação gera ajuste manual registrado.
- Risco clínico: baixo/indireto. O relatório de produção não precisa de dados clínicos; usar apenas código de serviço, valor e identificador interno, sem nome de tutor/paciente.
- Legal: natureza do vínculo (autônomo x empregado x sócio) e tributação do repasse são questões contábeis/trabalhistas, não verificadas aqui; o contador define as regras que a planilha apenas executa. LGPD: minimizar dados pessoais (dados bancários e fiscais dos profissionais são dados pessoais; acesso restrito). CFMV/receituário controlado: sem relação direta; não incluir dados de receitas.
- Alucinação: eliminada para cálculos se feitos por código; se OCR/LLM for usado, valores extraídos devem ser conferidos contra linha digitável/XML e destacados quando divergirem.

## 4. Pontuação
- Impacto: 3 (economiza horas por mês e reduz erros e multas por atraso, mas é tarefa mensal de volume modesto em clínica pequena)
- Viabilidade: 5 (regras determinísticas, ferramentas simples)
- Risco: 2 (financeiro/legal moderado se regras de repasse errarem; clínico nulo)

## 5. MVP sem dados reais e sem serviço pago
Sim. Um script Python (stdlib) ou planilha que: lê CSV sintético de produção e XML de NF-e fictício, aplica percentuais configuráveis, valida dígito de linha digitável, gera calendário de vencimentos e fluxo de caixa projetado e lista de divergências. Testável com dados fictícios e testes unitários. Fora do MVP: integração bancária, emissão fiscal, PIMS real.
