# 05 - Atestados e declarações (saúde, vacinação, viagem, hospedagem, óbito)

Data da análise: 2026-10-02. Limitação: WebFetch foi bloqueado para crmvsp/crmves/manual.cfmv; o que segue vem de trechos de resultados do WebSearch. O que não pôde ser confirmado no texto integral está marcado "não verificado".

## 1. Soluções existentes
- **Norma**: Resolução CFMV 1.321/2020 define regras e modelos de atestado sanitário/de saúde, vacinação, óbito, prontuário e consentimento; atestar saúde, vacinação e óbito é ato privativo do veterinário. Atestado de saúde = documento escrito, sem rasuras, datado, assinado exclusivamente por veterinário. Texto: https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf ; modelo editável CRMV-RJ: https://www.crmvrj.org.br/wp-content/uploads/2024/12/anexos_res_1321_anexo_01_EDITAVEL.pdf ; guia CRMV-SP: https://crmvsp.gov.br/wp-content/uploads/2021/02/Guia_para_Emissao_de_Atestado_de_Saude_de_Pequenos_Animais.pdf . Resolução anterior 844/2006: https://www.legisweb.com.br/legislacao/?id=103830
- Inconsistência: a data da 1.321 aparece como 24/04/2020 e 05/06/2020 em fontes diferentes. Não verificado qual é a correta.
- **Assinatura digital ICP-Brasil** (A1, Bird ID, VIDaaS; validação em validar.iti.gov.br) e plataformas que assinam atestados/laudos: https://www.bry.com.br/blog/receita-veterinaria-digital/ ; https://www.prescreve.com/veterinarios ; VetSmart: https://pl-vetsmart.zendesk.com/hc/pt-br/articles/12476571256475-Como-utilizar-a-assinatura-digital-na-prescri%C3%A7%C3%A3o . Prontuário eletrônico exige ICP-Brasil (fonte comercial, verificar na norma): https://www.bry.com.br/blog/prontuario-eletronico-veterinario
- **Viagem internacional**: o CVI é emitido pelo MAPA/Vigiagro (não pelo clínico), conforme o país de destino; validade de 10 dias (fonte secundária) e emissão eletrônica para alguns países. https://ruralpecuaria.com.br/tecnologia-e-manejo/animais-domesticos/mapa-orienta-como-fazer-uma-viagem-internacional-com-animal-de-estimacao.html ; https://crmvms.org.br/voce-sabia-que-transporte-de-caes-e-gatos-para-o-exterior-tem-regras/ . Requisitos por país mudam; checar sempre fonte oficial do MAPA e do destino (não verificado aqui).
- Estudos sobre IA nesta tarefa específica: nenhum encontrado. Sem evidência de que haja algo além de modelos/geração de documento nos PIMS.

## 2. Forma recomendada: workflow determinístico (template + checklist)
Não é agente. O documento é padronizado por norma; o valor está em preencher campos a partir do prontuário/carteira (nome, espécie, raça, idade, microchip, vacinas e lotes, CRMV) e checar pendências. LLM, se usado, apenas para redigir observações livres, e nunca para inventar achados ou exigências de destino.
Fluxo: (1) seleciona tipo e destino; (2) formulário puxa dados cadastrados; (3) regras validam campos obrigatórios, datas (vacina antirrábica vigente, validade do atestado) e lacunas; (4) gera PDF a partir do modelo CFMV; (5) veterinário revisa, examina o animal e assina (ICP-Brasil ou manual).
Viagem: o fluxo só gera checklist e rascunho de apoio; o CVI segue no Vigiagro.

## 3. Human-in-the-loop e riscos
- Validação obrigatória: o veterinário deve ter examinado o animal; achados e declarações são dele. Nada é emitido sem assinatura dele.
- Clínico: atestar saúde sem exame ou com dado errado (vacina, microchip) -> responsabilidade ética/civil. Alucinação: IA inventando exigência de país ou achado normal; mitigar com campos obrigatórios, sem texto de achados gerado e exigências só de fonte oficial citada.
- Legal: responsabilidade do profissional (CFMV/CRMV); atestado em nome de quem não é veterinário é exercício ilegal. LGPD: dados de tutor (nome, CPF, endereço) são pessoais; minimizar, não enviar a LLM externo sem base legal/contrato. Receituário controlado: não se aplica aqui.
- Óbito: texto sensível; manter modelo fixo e revisão humana.

## 4. Pontuação
- Impacto: 2/5 (tarefa frequente, mas curta; ganho de minutos por documento e menos erros).
- Viabilidade: 5/5 (template + validação de campos).
- Risco: 3/5 (atesta fato clínico; mitigado pela assinatura humana e ausência de IA generativa nos achados).

## 5. MVP
Cabe sim, sem dados reais nem serviço pago: formulário/planilha ou script (Python/HTML) com dados fictícios, validações e geração de PDF a partir do modelo do CFMV; assinatura simulada. Assinatura ICP-Brasil real e integração com PIMS ficam fora do MVP (certificado costuma ser pago).
