# Rastreio de resultados pendentes e atrasados de laboratórios externos

Domínio: exames-imagem | Data: 2026-10-02

## Aviso de verificação

Nesta execução o limite de WebSearch (200/200) estava esgotado e o WebFetch foi bloqueado pelo proxy (idexx.com e ncbi.nlm.nih.gov). Nenhuma fonte foi consultada. Toda afirmação factual externa abaixo está marcada como **não verificado**. Não há URLs citadas de propósito, para não inventar referências.

## 1. Soluções existentes

- Portais de grandes laboratórios veterinários (por exemplo IDEXX VetConnect PLUS, Antech) e integrações com PIMS: não verificado. Em geral costumam oferecer status do pedido e notificação de resultado; confirmar com o laboratório que você usa.
- Laboratórios brasileiros costumam ter portal web ou e-mail com status: não verificado, depende de cada um.
- Literatura sobre erros pré-analíticos (hemólise, volume insuficiente, identificação) em medicina veterinária: não verificado. Pesquisar em PubMed/Vet Clin Pathol quando houver acesso.
- Normas CFMV/MAPA/ANVISA aplicáveis a envio de amostras e responsabilidade técnica: não verificado.

## 2. Forma recomendada: workflow determinístico (planilha + lembretes)

O problema é de controle de prazo, não de raciocínio. Regras simples resolvem:

1. Planilha/tabela de envios: ID interno (sem nome de tutor), espécie, exame, laboratório, data de envio, prazo de entrega (TAT) prometido, status, data de retorno.
2. Regra: hoje > data de envio + TAT (+ tolerância) e sem resultado => status "atrasado".
3. Fila diária de pendências ordenada por atraso e urgência clínica (campo marcado pelo veterinário).
4. Modelos de mensagem (e-mail/WhatsApp) ao laboratório com campos preenchidos automaticamente; envio só após clique humano.
5. Checklist de causa de rejeição (hemolisada, volume insuficiente, anticoagulante errado, identificação) que leva a "solicitar nova coleta" com texto padrão para o tutor, revisado pela clínica.

Agente de IA só agregaria valor opcional: ler e-mails/laudos do laboratório e classificar ("amostra rejeitada por hemólise") para preencher o status. Isso pode vir depois, como extração com revisão humana. Não é necessário para o MVP. Ligações telefônicas não devem ser automatizadas.

## 3. Human-in-the-loop e riscos

- Veterinário/recepção valida: envio de qualquer mensagem externa, decisão de nova coleta (custo e estresse do animal, jejum, sedação), priorização clínica de casos urgentes.
- Resultado crítico: o sistema nunca interpreta o valor do exame; só rastreia presença/ausência e status.
- Clínico: risco principal é atraso de diagnóstico se uma pendência passar despercebida; o sistema reduz esse risco, mas uma falha no alerta pode gerar falsa segurança. Mitigar com revisão diária obrigatória da fila.
- Legal/LGPD: dados de tutor são pessoais; usar apenas ID interno e telefone/e-mail do laboratório na planilha. Se usar IA externa, não enviar dados do tutor. Obrigações do CFMV sobre prontuário e guarda de laudos: não verificado.
- Receituário controlado: não se aplica.
- Alucinação (se usar IA para classificar e-mails): pode inventar status ou causa de rejeição; mitigar exigindo citação do trecho original e confirmação humana.

## 4. Pontuação

- Impacto: 3. Reduz perda de resultados e retrabalho, mas o volume depende da clínica; em clínica pequena é modesto.
- Viabilidade: 5 para workflow/planilha; 3 para extração por IA de e-mails/laudos.
- Risco: 2 (somente rastreio, sem decisão clínica; risco residual de falha de alerta e de privacidade).

## 5. MVP sem dados reais e sem serviços pagos

Cabe. Um script Python (ou planilha com fórmulas) com dados sintéticos: CSV de envios, cálculo de atraso por TAT, fila ordenada, gerador de modelos de mensagem, e teste com casos de amostra hemolisada/insuficiente. Sem integração com PIMS nem laboratório. Integração real com portais/PIMS: não verificado e provavelmente dependente de contrato.
