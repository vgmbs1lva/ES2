# 09 - Gerenciar RSS, perfurocortantes e biossegurança do dia a dia

Domínio: compliance | Data: 2026-10-02

## Aviso de verificação (leia primeiro)

Nesta rodada o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída para gov.br, bvsms.saude.gov.br e in.gov.br. Portanto **nenhuma afirmação normativa ou de mercado abaixo foi confirmada com URL**. Tudo o que depende de norma está marcado "não verificado". Não há citações inventadas; onde falta fonte, a lacuna está declarada.

## 1. Soluções existentes

- Normas a conferir (não verificado, sem URL acessada): RDC ANVISA 222/2018 (RSS), CONAMA 358/2005, exigências do CRMV/CFMV para estabelecimentos veterinários, legislação estadual/municipal de PGRSS e de MTR (manifesto de transporte de resíduos), NR-32 (aplicabilidade a veterinária: não verificado).
- Produtos/plug-ins de PIMS veterinário com módulo de RSS: não verificado. Existem, em geral, sistemas de gestão ambiental/MTR para geradores (órgãos estaduais têm MTR eletrônico), mas não confirmei nomes nem URLs.
- Estudos/artigos sobre automação por IA em PGRSS veterinário: não verificado.
- Prática comum (conhecimento geral, sem fonte): planilha/checklist de PGRSS, contrato com empresa licenciada, guarda de manifestos/certificados de destinação, registro de treinamento.

## 2. Forma recomendada: script/planilha (workflow determinístico leve)

Não é agente. O problema é de calendário e registro, não de interpretação aberta:
- Cadastro de obrigações com validade: contrato de coleta, licença da empresa coletora, certificado de destinação final, treinamentos, vacinação/EPI, manutenção de autoclave (se houver).
- Alertas de vencimento (30/15/7 dias) e checklist diário/semanal de limpeza e segregação.
- Conferência cruzada simples: coleta realizada (data/peso/manifesto) x contrato x certificado de destinação; sinaliza lacuna.
- Registro de treinamento (data, tema, lista de presença, instrutor).

LLM só tem papel opcional e secundário: rascunhar POPs a partir de modelo, ou resumir o PGRSS para treinamento, sempre revisado. Segregação de resíduo físico (lixeira certa) e descarte de perfurocortante não são automatizáveis por software: é comportamento da equipe.

## 3. Human-in-the-loop e riscos

- O responsável técnico / responsável pelo PGRSS valida: classificação de grupos, PGRSS, POPs, contrato e licenças da coletora, cada manifesto/certificado.
- Veterinário/RT assina treinamentos e checklists; ferramenta nunca "aprova" conformidade sozinha.
- Risco legal: autuação por vigilância sanitária/ambiental e CRMV se registros faltarem. Exigências exatas e prazos de guarda: não verificado (conferir norma e legislação local).
- Risco de alucinação: alto se LLM responder "qual a regra" sem texto da norma; mitigar usando só texto oficial anexado e exibindo o trecho.
- LGPD: baixo; dados são de empresa e funcionários (listas de presença, nomes). Sem dados de pacientes/tutores. Resíduos de medicamentos controlados/receituário: tratamento específico, não verificado; fora do escopo do MVP.
- Risco clínico direto: baixo; risco ocupacional (acidente perfurocortante) é o relevante, e a ferramenta só ajuda em lembretes.

## 4. Pontuação

- Impacto: 3. Tarefa recorrente e com risco de multa, mas o ganho de tempo é modesto; o valor é não esquecer prazos.
- Viabilidade: 5. Planilha com datas e checklists; sem integração.
- Risco: 2. Falha típica é falso conforto por alerta ausente; sem dado sensível.

## 5. MVP sem dados reais e sem serviço pago

Cabe. Planilha (ou script Python/CSV) com abas: Obrigações e vencimentos, Coletas, Checklist de limpeza, Treinamentos; gerador de alerta por data; dados fictícios. Interface/lembrete: Google Planilhas ou calendário (gratuito). Não requer PIMS.

## Pendências para verificar

1. Texto da RDC 222/2018 (escopo para veterinária, conteúdo do PGRSS, capacitação, registros e prazos de guarda).
2. Norma do CRMV/CFMV sobre estabelecimentos e PGRSS.
3. Regras estaduais/municipais de MTR e licenciamento.
4. Existência de módulos de RSS em PIMS veterinários brasileiros.
