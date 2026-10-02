# Registro no prontuário da comunicação com o tutor

Domínio: atendimento-tutor | Data: 2026-10-02

## Aviso sobre fontes
Nesta execução o orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado (planalto.gov.br, cfmv.gov.br). **Nenhuma fonte foi verificada.** Tudo que é factual (produtos, estudos, normas) está como "não verificado" e precisa de confirmação antes de uso. O que segue é raciocínio de desenho.

## 1. Soluções existentes
- Scribes/IA ambientais para consulta veterinária e módulos de PIMS que resumem ligações ou mensagens e geram nota no prontuário: não verificado (nomes, preços e disponibilidade no Brasil não confirmados).
- Integrações de WhatsApp Business com PIMS que arquivam a conversa no cadastro do tutor: não verificado.
- Estudos sobre documentação de comunicação e risco de queixas/processos em veterinária: não verificado.
- Normas: Código de Ética do Médico-Veterinário e resoluções do CFMV sobre prontuário e telemedicina/orientação remota; LGPD (Lei 13.709/2018); Marco Civil/CDC como pano de fundo. Citados de memória, texto vigente não verificado.

## 2. Forma recomendada: workflow determinístico (rascunho com LLM opcional)
Não é agente. O problema é "transformar notas e conversas do dia em entrada de prontuário estruturada, ao fim do dia". Desenho mínimo:
1. **Captura durante o dia (a parte que mais agrega):** um formulário/template de 30 segundos (paciente, canal, data/hora, o que foi orientado, consentimento/recusa, retorno combinado). Registrar na hora é melhor do que reconstruir à noite, e é simples.
2. **Script/planilha:** coleta as entradas do dia, valida campos obrigatórios (ex.: recusa sem texto da orientação dada fica sinalizada), ordena por paciente e gera o texto padronizado de prontuário.
3. **LLM (opcional, só reescrita):** organiza notas soltas e exportação de conversa em texto padronizado, sem acrescentar fatos. Cada frase deve apontar para o trecho de origem.
4. **Veterinário** revisa, edita e confirma o lançamento. Nada entra no prontuário sem confirmação.

Por que não agente: não há decisão a delegar; o risco é justamente a IA "completar" o que não foi dito. Template + regras resolvem a maior parte, e o LLM entra só como organizador.

## 3. Human-in-the-loop e riscos
- **Validação:** veterinário lê cada entrada antes de salvar; campos de consentimento/recusa e orientação clínica nunca são inferidos, só transcritos do que o profissional marcou ou do texto original, e aparecem destacados para conferência.
- **Alucinação (principal risco):** o modelo pode inventar que o tutor "consentiu" ou que se orientou algo (dose, sinal de alerta) que não foi dito. Um prontuário falso é pior que um incompleto. Mitigação: saída com citação literal do trecho de origem; "não consta" como valor padrão; proibido gerar dose, diagnóstico ou conduta nova; diff visível entre nota original e texto final.
- **Legal/ético (CFMV):** a autoria e a responsabilidade pelo prontuário são do veterinário; o registro precisa refletir fielmente o ocorrido (não verificado o texto da norma). Preservar o original (conversa/áudio) além do resumo; manter data/hora e autor da edição (trilha de auditoria). Conferir exigências de guarda e prazo de prontuário (não verificado).
- **LGPD:** conversas contêm dados pessoais do tutor e informações do paciente; áudio/WhatsApp exige base legal e transparência ao tutor sobre o tratamento; evitar enviar identificação a APIs externas (pseudonimizar), contrato com operador, retenção e acesso restrito. Art. 20 (revisão de decisões automatizadas) é pouco relevante aqui por não haver decisão automatizada, mas confirmar (não verificado).
- **Receituário controlado:** se a conversa envolver prescrição, não resumir por IA; o registro de controlados segue o fluxo próprio (receita, retenção) e deve ser feito pelo veterinário.
- **Valor probatório:** nota feita muito depois e com texto "polido" por IA pode enfraquecer a prova; manter timestamp do registro bruto.

## 4. Pontuação (honesta)
- Impacto: **3/5**. Tarefa recorrente e cansativa, mas curta por caso; o ganho maior vem do hábito de registro no ato, não da IA.
- Viabilidade: **4/5**. Template e script são triviais; ingestão automática de WhatsApp/telefonia depende de integração e consentimento (não verificado).
- Risco: **3/5**. Perigo de registro falso por alucinação e exposição de dados; reduzido por revisão humana e saída com citação de origem.

## 5. MVP sem dados reais e sem serviços pagos
Cabe: sim, a parte determinística. Um script (Python) ou planilha que recebe entradas **sintéticas** (CSV/JSON: paciente fictício, canal, orientação, consentimento sim/não/recusa, retorno), valida campos, sinaliza lacunas (recusa sem orientação registrada, ausência de data/hora) e gera o texto padronizado de prontuário mais um relatório de pendências do dia. A camada LLM fica como etapa posterior, testável com modelo local/gratuito, sem garantia de qualidade (não verificado), com o teste principal sendo "o modelo nunca cria consentimento ou orientação que não está no texto de entrada".
