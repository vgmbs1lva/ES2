# Acompanhamento pós-consulta / pós-cirúrgico (24-72h)

Domínio: atendimento-tutor. Data da análise: 2026-10-02.

## Recomendação: workflow determinístico (lista diária + mensagem padronizada + checklist), com IA opcional só para rascunho/triagem

Não precisa de agente autônomo. O gargalo real é lembrar de quem chamar e registrar o resultado, não raciocinar clinicamente. Um workflow simples resolve: (1) gera diariamente a lista de pacientes elegíveis a partir de altas/cirurgias; (2) dispara/oferece mensagem-modelo por protocolo (castração, dentística, gastroenterite); (3) coleta respostas estruturadas do tutor (checklist de sinais de alerta); (4) classifica por regras fixas (verde/amarelo/vermelho); (5) o veterinário decide e registra.

## 1. Soluções existentes (evidência)

- Produtos de comunicação integrados a PIMS com follow-ups automatizados por SMS/e-mail/app: PetDesk (https://petdesk.com/veterinary-client-engagement-software), Digitail (https://digitail.com/blog/best-software-for-a-mobile-veterinary-clinic/). Comparativos de blogs comerciais: https://emitrr.com/blog/texting-software-for-veterinary-practices/. São fontes de fornecedor/marketing; disponibilidade no Brasil, idioma e WhatsApp: não verificado.
- Prática recomendada de ligação de retorno pós-cirúrgico: Veterinary Practice News (https://www.veterinarypracticenews.com/how-to-make-surgical-recovery-a-success/) e Today's Veterinary Nurse (https://todaysveterinarynurse.com/practice-management/postoperative-discharges-improving-owner-education/). Material de divulgação/prática, não ensaio clínico veterinário.
- Expectativa do tutor: dvm360, "Post-appointment follow-up: What veterinary clients say they want" (https://www.dvm360.com/view/post-appointment-follow-what-veterinary-clients-say-they-want). O resumo de busca cita pesquisa em que mais de um terço dos clientes agiria mais sobre recomendações se a equipe fizesse check-in; o número de adesão de 17-35% (AAHA 2003) é citado de segunda mão. Não li o texto completo.
- Evidência em medicina humana/odontologia (analogia, não veterinária): ligação de retorno melhorou adesão a instruções pós-exodontia (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9750235/ e https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7600202/). Não extrapolar para desfecho clínico veterinário.
- Estudo veterinário controlado mostrando redução de complicações por ligação de acompanhamento: não verificado (não encontrei).
- Produto específico para o Brasil com esse fluxo em PIMS nacional: não verificado.

## 2. Forma recomendada e justificativa

Workflow determinístico/planilha. Por quê:
- Entrada estruturada (data de alta/procedimento + tipo) permite regra simples: D+1 e D+3 para cirúrgicos, D+1 para gastroenterite.
- Perguntas de triagem são fechadas e conhecidas (apetite, vômito, dor, ferida, urina/fezes, medicação). Não exige LLM.
- LLM só agrega valor em: redigir mensagem em tom humano e resumir resposta livre do tutor para o prontuário. Ambos como rascunho.
- Agente autônomo que decide conduta: não recomendado (risco clínico e regulatório, ver abaixo).

## 3. Human-in-the-loop, riscos

Onde o veterinário valida:
1. Aprova protocolo e modelos de mensagem uma vez (por tipo de procedimento).
2. Toda resposta classificada amarelo/vermelho vai para o veterinário, que liga/decide retorno antecipado.
3. Nenhuma alteração de conduta, dose ou prescrição sai sem ato do veterinário.
4. Registro no prontuário revisado e assinado pelo veterinário.

Riscos:
- Clínico: tutor minimiza sinais; classificação automática falso-negativo atrasa retorno (ex.: gastroenterite com desidratação, deiscência, dor mal controlada). Mitigar: regra conservadora (qualquer dúvida sobe de nível), mensagem sempre com sinais de alerta e canal de urgência, sem "tudo ok" automático sem revisão.
- Alucinação (se usar LLM): pode inventar orientação ou dose. Mitigar: LLM não responde ao tutor sozinho; só resume e rascunha; textos clínicos vêm de modelos aprovados.
- Legal/CFMV: contato do veterinário com paciente após procedimento se enquadra no que a regulamentação de telemedicina veterinária chama de telemonitoramento (permitido só após atendimento presencial, em recuperação de procedimentos) e teleorientação (sem diagnóstico, exames ou prescrição) segundo resumos do CRMV-SP/CFMV: https://crmvsp.gov.br/resolucao-que-regulamenta-a-telemedicina-veterinaria-e-publicada-entenda-como-funciona/ e https://www.cfmv.gov.br/resolucao-do-cfmv-regulamenta-a-telemedicina-veterinaria/comunicacao/noticias/2022/06/29/. O número da resolução e exigências exatas (consentimento, registro) não pude verificar no texto primário (site do CFMV bloqueado nesta sessão); conferir antes de implantar. Documentação do prontuário: Resolução CFMV 1321/2020 (https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf), não relida em detalhe.
- Receituário controlado: o fluxo não deve emitir, renovar ou alterar prescrição; se o tutor pedir (ex.: analgésico opioide), encaminhar ao veterinário e seguir portaria do MAPA/ANVISA aplicável (não verificado aqui).
- LGPD: telefone, nome do tutor e dados do animal associados são dados pessoais; base legal provável: execução de contrato/cuidado do serviço contratado, com aviso na ficha de admissão; consentimento específico para canais como WhatsApp é recomendado por fontes de mercado (https://www.socialhub.pro/blog/lgpd-clinica-whatsapp-consentimento-obrigatorio/, fonte comercial). Orientação ANPD sobre legítimo interesse: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_legitimo_interesse.pdf/@@display-file/file. Se usar LLM em nuvem, enviar dados minimizados/pseudonimizados e checar transferência internacional. Validar com assessoria jurídica.

## 4. Pontuação (1-5)

- Impacto: 3. Valor real em segurança do paciente, retenção e adesão, mas ganho de tempo moderado (ligações curtas) e evidência veterinária forte de desfecho: não verificada.
- Viabilidade técnica: 5 para o workflow; 3 se incluir IA com integração a PIMS/WhatsApp.
- Risco clínico/legal: 3 (workflow com revisão); subiria para 4-5 com agente autônomo decidindo conduta.

## 5. MVP sem dados reais e sem serviços pagos: sim

Cabe no repositório: script/planilha (CSV sintético com paciente fictício, procedimento, data) que (a) gera a fila D+1/D+3 por regras, (b) preenche mensagem-modelo por protocolo, (c) recebe respostas do checklist (formulário ou CSV) e classifica verde/amarelo/vermelho por regras, (d) gera nota de prontuário em rascunho para o veterinário assinar. Sem envio real de mensagens, sem LLM obrigatório, sem integrações pagas. Envio por WhatsApp/SMS e integração com PIMS ficam fora do MVP.
