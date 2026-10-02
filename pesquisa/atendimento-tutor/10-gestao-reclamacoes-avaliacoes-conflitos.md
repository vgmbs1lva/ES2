# Gestão de reclamações, avaliações e conflitos com tutores

Domínio: atendimento-tutor. Data: 2026-10-02.

## Aviso de verificação

Nesta rodada o orçamento de WebSearch estava esgotado (200/200) e o proxy bloqueou WebFetch para planalto.gov.br e cfmv.gov.br. **Nenhuma afirmação abaixo tem URL verificada.** Tudo que depende de fonte está marcado como "não verificado" e deve ser conferido antes de uso.

## 1. Soluções existentes
- Produtos de gestão de reputação/resposta a avaliações (Google Business Profile, ferramentas de CRM de clínicas, plug-ins de PIMS): não verificado. Nenhum produto específico veterinário brasileiro foi confirmado.
- Estudos sobre comunicação em eutanásia/luto do tutor e satisfação: não verificado.
- Normas: Código de Ética do Médico-Veterinário (CFMV; número da resolução e artigos sobre sigilo e publicidade): não verificado. LGPD (Lei 13.709/2018; dados pessoais, art. 20 sobre revisão de decisões automatizadas): não verificado nesta rodada. Código de Defesa do Consumidor (relação de consumo em clínicas): não verificado.
- Ação sugerida: conferir esses pontos em fontes primárias (CFMV, Planalto) antes de qualquer implantação.

## 2. Forma recomendada: workflow determinístico com rascunho por LLM (sem agente autônomo)
Parcialmente "não automatizar".

- **Automatizar (workflow simples):** triagem e classificação da reclamação (preço, espera, resultado, atendimento), montagem de dossiê do caso (linha do tempo a partir do prontuário e política da clínica), rascunho de resposta a avaliação online e a e-mail, registro do caso em planilha e sugestão de ajuste de processo (padrões recorrentes). Uma planilha com categorias + modelos de resposta + um prompt já resolve 80%.
- **Não automatizar:** conversa de eutanásia, óbito e prognóstico. É relacional e de alta carga emocional; no máximo, checklist de preparo e roteiro para o veterinário (ferramenta de apoio, não de envio). Acordos financeiros/indenizações e respostas a notificações jurídicas/CRMV também ficam fora.
- Agente autônomo que responde sozinho: não recomendado.

## 3. Human-in-the-loop e riscos
- Todo texto sai como rascunho; o veterinário/gestor aprova antes de publicar ou enviar. Sem envio automático.
- **Sigilo/LGPD:** responder publicamente a avaliação sem expor dados do paciente/tutor ou do atendimento (princípio geral; fundamento normativo exato não verificado). Não colar prontuário real em LLM de terceiros sem base legal, contrato e anonimização.
- **Alucinação:** o modelo pode inventar fatos clínicos, desculpas ou promessas de reembolso; mitigar usando apenas campos fornecidos, proibir citação de dose/diagnóstico e exigir revisão.
- **Legal/ético:** admissão de culpa, tom defensivo e publicidade indevida em resposta pública; encaminhar casos com ameaça jurídica ao responsável técnico/advogado.
- **Receituário controlado:** não deve entrar na resposta automática; qualquer menção a medicamentos controlados é bloqueada para revisão humana.
- **Viés/escalada:** reclamações com risco (óbito, ameaça, denúncia ao CRMV) são sinalizadas por regras determinísticas (palavras-chave) para o humano.

## 4. Pontuação (honesta)
- Impacto: 3 (ganho moderado de tempo; valor maior em consistência e aprendizado de processo).
- Viabilidade: 4 (rascunho e triagem são triviais com LLM; integração com PIMS é dispensável no começo).
- Risco: 3 (reputacional/ético, sigilo; mitigável com humano na aprovação e dados anonimizados).

## 5. MVP sem dados reais e sem serviço pago
Cabe: planilha/CSV com casos sintéticos, regras de triagem (palavras-chave + categorias), modelos de resposta com campos preenchíveis e script que gera o dossiê e o rascunho. A parte de LLM pode ser simulada com modelos de texto; teste com 20 a 30 reclamações fictícias, avaliando tom, ausência de dados sensíveis e correta escalada. Não cabe testar integração com PIMS nem eficácia real sem dados reais.
