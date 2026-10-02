# Aquisição, registro e organização do estudo de imagem (radiografia/US)

Data: 2026-10-02. Domínio: exames-imagem.

## Aviso sobre fontes
A pesquisa web não pôde ser feita nesta execução: o limite de WebSearch da sessão estava esgotado e o WebFetch foi bloqueado pelo proxy de saída (orthanc-server.com, dicomstandard.org). Portanto nenhuma afirmação factual abaixo tem URL verificada. Tudo que depende de fonte está marcado "não verificado". Revisar com busca antes de citar.

## 1. Soluções existentes
- Servidor DICOM/PACS open source (Orthanc): não verificado nesta execução. Conhecimento prévio sugere que suporta worklist, API REST e plugins, mas é preciso confirmar na documentação oficial.
- PACS/PIMS veterinários comerciais com integração a radiologia digital e teleradiologia: não verificado (sem URLs).
- Atributos DICOM para espécie/raça/responsável (Patient Species, Breed, Responsible Person): não verificado; checar no DICOM PS3.3.
- Estudos sobre erros de identificação em imagem: não verificado.
- Normas CFMV/MAPA/ANVISA sobre laudo, guarda de imagens e prontuário: não verificado.

## 2. Forma recomendada: workflow determinístico (script), sem agente
O trabalho é padronizar nome, identificador e destino, e fazer envio. Isso é regra fixa, não exige julgamento.
- Script que lê o pedido (CSV/planilha) e gera um identificador de estudo no padrão `AAAAMMDD_ID-paciente_modalidade_seq`.
- Renomeia/organiza a pasta, confere se há JPEG/DICOM esperados, gera checklist e manifesto (hash dos arquivos).
- Preferir worklist DICOM (equipamento puxa os dados do cadastro) a digitação manual, se o equipamento suportar: não verificado.
- LLM só se justifica opcionalmente para ler texto de etiqueta/queimado na imagem; não recomendado (risco de erro de identificação).

## 3. Human-in-the-loop e riscos
- O veterinário (ou auxiliar treinado) confere identidade do paciente, lateralidade/marcadores e qualidade antes de fechar o estudo. A conferência é obrigatória, não amostral.
- Clínico: troca de paciente ou de lado (D/E) é o erro grave. Automação nunca deve corrigir marcadores sozinha.
- LGPD: imagens com nome do tutor são dados pessoais; evitar enviar a serviços de nuvem/LLM sem base legal e contrato. Aplicação ao contexto veterinário: não verificado.
- CFMV: responsabilidade técnica pelo laudo e guarda do prontuário/imagens permanecem do médico-veterinário; requisitos exatos de prazo de guarda: não verificado.
- Receituário controlado: não se aplica diretamente (sedação com controlados tem registro próprio, fora do escopo da automação).
- Alucinação: nula num script determinístico; relevante apenas se usar LLM.

## 4. Pontuação
- Impacto: 2/5. Economiza minutos por estudo e reduz erros de arquivo, mas a parte clínica não é automatizada.
- Viabilidade: 4/5. Script simples; a integração real com equipamento/PACS depende do fabricante.
- Risco: 3/5. Baixo se determinístico, mas erro de identificação é grave e o risco sobe se houver automação de envio externo.

## 5. MVP sem dados reais e sem serviços pagos
Sim. Um script Python que usa pastas de arquivos sintéticos e um CSV de pedidos fictícios, gera identificadores, valida nomenclatura, produz manifesto e checklist. Pode-se usar DICOM sintético (biblioteca pydicom, não verificada aqui). Não cobre a integração com PACS real.
