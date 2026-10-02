# Comunicar resultados de exames e orçamentos ao tutor

Domínio: atendimento-tutor | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado para planalto.gov.br. **Nenhuma fonte foi verificada.** Toda afirmação factual abaixo (produtos, estudos, normas) está marcada como "não verificado" e deve ser confirmada antes de uso. O que segue é raciocínio de desenho, não evidência.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com IA para comunicação com o tutor (resumo de resultados, mensagens): não verificado.
- Estudos sobre comunicação de custo, "financial constraints" e adesão a planos diagnósticos em veterinária: não verificado.
- Normas: CFMV (Código de Ética, resolução sobre telemedicina, prontuário), LGPD (Lei 13.709/2018, em especial art. 6 e art. 20 sobre revisão de decisões automatizadas), CDC (orçamento prévio, arts. 39-40): citados de memória, não verificado. Confirmar texto vigente.

## 2. Forma recomendada: workflow determinístico (com rascunho assistido por LLM opcional)
Não é agente autônomo. Dividir a tarefa:
1. **Determinístico (planilha/script/integração com o PIMS):** montar o pacote do caso a partir de laudo + orçamento: valores de referência, flags de alteração, itens do orçamento em opções (essencial / recomendado / ideal), total por opção, validade do orçamento. Gerar também o registro de conduta (aprovado/recusado/parcial, data, quem comunicou).
2. **LLM (opcional, só rascunho):** transformar as alterações já sinalizadas em texto leigo (mensagem WhatsApp/roteiro de ligação), em linguagem acessível, sem diagnóstico novo.
3. **Veterinário:** revisa, edita, envia/liga. A negociação por valor e a decisão de conduta são humanas.

Por que não agente: a parte de maior valor (interpretar o caso, conduzir conversa difícil sobre dinheiro e prognóstico, empatia) não deve ser delegada; o ganho real é tirar do veterinário a digitação, a formatação do orçamento em opções e o registro. Isso se resolve com template + regras. LLM só agrega no texto leigo.

## 3. Human-in-the-loop, riscos
- **Validação obrigatória** antes de qualquer envio ao tutor: veterinário lê o rascunho e confere cada valor, unidade e interpretação contra o laudo. Nada é enviado automaticamente.
- **Clínico:** alucinação (valor trocado, unidade errada, "normal" para faixa de outra espécie/idade), tranquilizar indevidamente, omitir urgência. Mitigação: números vêm do laudo por código, nunca gerados pelo modelo; o modelo só reescreve; exigir citação do campo de origem; lista de proibições (não sugerir diagnóstico, prognóstico, dose ou fármaco).
- **Legal:** responsabilidade técnica permanece do veterinário (CFMV); prontuário deve registrar o que foi informado e a decisão do tutor (não verificado o texto da norma). LGPD: dados do tutor e do paciente são pessoais; evitar enviar identificação a APIs externas (pseudonimizar), base legal, contrato com operador, retenção. Orçamento: coerência com CDC (não verificado). Receituário controlado: o fluxo não deve tocar prescrição; bloquear qualquer menção a dose/controlados.
- **Comercial/ético:** a IA não deve empurrar opções mais caras; opções sempre apresentadas com o mínimo viável incluído.
- Canal: mensagens por WhatsApp implicam consentimento do tutor para o canal (não verificado).

## 4. Pontuação (honesta)
- Impacto: **3/5**. Economiza tempo de redação e registro e padroniza orçamento em opções; o gargalo continua sendo a conversa.
- Viabilidade: **4/5**. Template + regras é trivial; integração com PIMS depende do sistema (não verificado); LLM só para texto.
- Risco: **3/5**. Moderado por erro de transcrição e dados pessoais; reduzido pelo desenho (valores por código, revisão humana).

## 5. MVP sem dados reais e sem serviços pagos
Cabe: sim, a parte determinística. Um script/planilha que recebe um JSON/CSV **sintético** de resultado (analito, valor, unidade, referência) e itens de orçamento, e gera: (a) lista de alterações por regra (alto/baixo/normal), (b) orçamento em 3 opções com totais, (c) texto leigo por template, (d) linha de registro de conduta. A camada LLM fica como etapa opcional posterior, testável com modelos locais ou gratuitos, mas sem garantia de qualidade (não verificado). Referências de faixas precisam vir de fonte do próprio laboratório, não do script.
