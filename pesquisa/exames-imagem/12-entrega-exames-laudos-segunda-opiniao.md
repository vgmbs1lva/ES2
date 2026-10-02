# Entrega de exames e laudos a tutores/colegas e solicitação de segunda opinião

Domínio: exames-imagem | Data: 2026-10-02

## Aviso sobre fontes (leia primeiro)
Nesta execução o orçamento de WebSearch (200/200) estava esgotado e WebFetch foi bloqueado pelo proxy
(planalto.gov.br, cfmv.gov.br, orthanc-server.com). **Nenhuma afirmação factual abaixo foi verificada com URL.**
Tudo que depende de fonte está marcado "não verificado" e deve ser conferido antes de uso.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com portal do tutor ou envio de laudo por e-mail/WhatsApp: não verificado (nenhum nome/URL confirmado).
- Serviços de teleradiologia/telecardiologia veterinária com upload de DICOM e laudo remoto: não verificado.
- Servidores PACS/DICOM open source (ex.: Orthanc) com exportação de estudo em ZIP/visualizador web e anonimização: conheço o projeto, mas não consegui confirmar por URL nesta sessão; não verificado.
- Estudos sobre eficácia de segunda opinião em imagem veterinária: não verificado.

## 2. Forma recomendada: workflow determinístico (checklist + empacotamento), sem agente
O núcleo da tarefa é mover arquivos certos para o destinatário certo com consentimento registrado. Isso é
empacotamento e rastreio, não raciocínio clínico. Um agente LLM só agregaria valor opcional em redigir o
texto do e-mail/resumo do caso, sempre rascunho revisado.

Fluxo:
1. Veterinário abre a solicitação (tutor, destinatário, finalidade: entrega ao tutor / encaminhamento / segunda opinião).
2. Sistema exige consentimento do tutor registrado (checkbox + data) para qualquer envio a terceiro.
3. Seleção dos itens (laudo PDF, imagens JPG/PDF, DICOM) e conferência de identificação do paciente em cada arquivo.
4. Montagem do pacote: PDF do laudo + imagens legíveis + resumo clínico curto (template fixo) + link com expiração (não anexar dados sensíveis em canal aberto).
5. Veterinário revisa e aprova; só então envia.
6. Registro: o que foi enviado, a quem, quando; prazo de resposta com lembrete; resposta do especialista anexada ao prontuário como parecer, marcada com autoria.

## 3. Human-in-the-loop, riscos
- Validação humana obrigatória: (a) consentimento do tutor, (b) conferência paciente/exame, (c) aprovação do resumo clínico, (d) leitura do retorno do colega antes de alterar conduta.
- Alucinação: se houver LLM para o resumo, restringir a campos estruturados do prontuário; proibido inferir diagnóstico ou "interpretar" imagem; o veterinário compara com a fonte.
- Erro de identificação (arquivo de outro paciente enviado): risco principal; mitigar com conferência dupla de nome/ID/data em cada arquivo.
- LGPD (Lei 13.709/2018): dados do tutor são dados pessoais; envio a terceiros pede base legal/consentimento, minimização, segurança, e atenção a serviços em nuvem no exterior (transferência internacional). Artigos específicos: não verificado nesta sessão.
- CFMV: regras de prontuário, sigilo, guarda e responsabilidade técnica em telemedicina/teleconsulta veterinária: números de resoluções não verificados; consultar o site do CFMV antes de implantar. Responsabilidade pela conduta permanece com o veterinário assistente; o parecer do colega é consultivo.
- Receituário controlado: não se aplica a esta tarefa (não gera prescrição); não incluir prescrições no pacote automaticamente.
- Segurança: link expirável, senha enviada por canal separado, log de acesso; não usar e-mail pessoal sem criptografia para dados de tutor.

## 4. Pontuação (honesta)
- Impacto 3/5: economiza tempo administrativo e reduz perdas de retorno, mas não é o gargalo clínico.
- Viabilidade 4/5: tecnicamente simples (templates, formulário, armazenamento com link expirável); a dificuldade real é a integração com cada PIMS/PACS.
- Risco 3/5: baixo risco clínico direto, mas vazamento de dados e envio de arquivo errado têm risco legal real.

## 5. MVP sem dados reais e sem serviços pagos
Cabe, sim: script/formulário local que recebe pasta com arquivos sintéticos (PDF/JPG fictícios), exige checkbox de consentimento, valida convenção de nomes (ID do paciente fictício), gera ZIP + resumo a partir de template, cria registro CSV/JSON de envio e de retorno e lembrete de prazo. Envio real fica fora (simulado em pasta "outbox"). Testes: arquivo de paciente divergente deve bloquear o envio; sem consentimento deve bloquear.
