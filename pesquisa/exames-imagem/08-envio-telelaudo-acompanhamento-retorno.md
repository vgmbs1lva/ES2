# Envio de estudos para telelaudo e acompanhamento do retorno

Data: 2026-10-02. Domínio: exames-imagem.

## Aviso sobre fontes
Nesta execução o WebSearch estava com o limite da sessão esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída (www.cfmv.gov.br). Nenhuma afirmação factual abaixo tem URL verificada. Tudo que depende de fonte está marcado "não verificado". Revisar com busca antes de citar.

## 1. Soluções existentes
- Plataformas/serviços de teleradiologia veterinária (laudo por radiologista/ultrassonografista remoto, com portal de upload e SLA): não verificado (sem URLs). Os prazos de mercado citados na tarefa (2-4 h rotina, 1-2 h urgente) vêm da descrição da tarefa, não confirmados.
- Integração de PIMS/PACS com teleradiologia (envio direto do estudo DICOM, retorno do laudo ao prontuário): não verificado.
- Servidor PACS open source (ex.: Orthanc) com API REST para envio e consulta de estudos: não verificado.
- Estudos sobre concordância entre laudo remoto e presencial, ou tempo de resposta: não verificado.
- Norma do CFMV sobre telemedicina veterinária e laudo à distância: não verificado (existe regulamentação do CFMV sobre o tema segundo conhecimento prévio, mas número, data e conteúdo não foram confirmados).

## 2. Forma recomendada: workflow determinístico (planilha/script), sem agente
O trabalho é preencher um formulário padronizado, enviar, e controlar prazo e pendências. Isso é regra fixa; julgamento clínico fica com o laudador.
- Modelo de solicitação com campos obrigatórios (espécie, raça, idade, peso, região/modalidade, histórico, pergunta diagnóstica, urgência). Bloqueia envio com campo vazio.
- Planilha/tabela de controle: id do estudo, data/hora de envio, urgência, prazo-alvo calculado (ex.: +4 h rotina, +2 h urgente, parametrizável), status (enviado, em laudo, pedido de informação, recebido, validado), alerta de atraso.
- Rascunho do histórico a partir do prontuário: pode ser template preenchido por campos; LLM só como opção para resumir texto livre, sempre com revisão. Não recomendado como parte central.
- Se a plataforma tiver API/e-mail estruturado, o script pode enviar e ler status; senão, o envio permanece manual e o script só controla o prazo.
- Agente de IA não se justifica: não há decisão aberta que regras não resolvam.

## 3. Human-in-the-loop e riscos
- O veterinário solicitante revisa e aprova histórico e pergunta diagnóstica antes do envio, escolhe a urgência e responde pedidos de informação. Ao receber o laudo, confere se corresponde ao paciente/estudo correto e se responde à pergunta, e só então vincula ao prontuário.
- Clínico: troca de paciente/lado, urgência subestimada e laudo atrasado sem alerta. O alerta de prazo mitiga o último. Achado crítico exige contato direto, não só e-mail.
- Alucinação: nula em workflow determinístico; se LLM resumir histórico, pode omitir ou inventar dado clínico, então revisão humana obrigatória e proibição de acrescentar informação não presente no prontuário.
- LGPD: nome/telefone do tutor são dados pessoais; enviar ao laudador apenas dados mínimos (identificador do caso, espécie, histórico), anonimizar cabeçalho DICOM/imagens quando possível, e ter contrato com a plataforma. Enquadramento da LGPD ao contexto veterinário: não verificado.
- CFMV: responsabilidade final pelo atendimento permanece do clínico; exigências para telelaudo (identificação do laudador, CRMV, assinatura): não verificado.
- Receituário controlado: não se aplica.

## 4. Pontuação
- Impacto: 2/5. Poupa minutos por caso e evita estudos esquecidos, mas o tempo principal é a espera do laudador.
- Viabilidade: 4/5. Planilha com prazos é trivial; integração real depende da plataforma.
- Risco: 2/5. Baixo se houver revisão humana e dados mínimos; sobe com LLM ou envio externo automático.

## 5. MVP sem dados reais e sem serviços pagos
Sim. Script Python (ou planilha) com casos fictícios: valida o formulário, calcula prazo por urgência, simula estados e gera lista de pendências/atrasos. Não cobre integração com plataforma ou PACS reais.
