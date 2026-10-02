# Prontuário de internados e retornos (evolução, fichas, prescrição interna)

Data da pesquisa: 2026-10-02. Domínio: administrativo. Afirmações sem fonte estão marcadas "não verificado".

## 1. Soluções existentes

PIMS com ficha digital de internação (substituem a ficha em papel; não geram a evolução sozinhos):
- Instinct Treatment Plan: ficha de tratamento com sinais vitais, tarefas e medicações. https://instinct.vet/products/instinct-treatment-plan/
- Vet Radar / ezyVet, "patient sheets": registro de tratamentos e vitais; ao concluir a ficha, sincroniza com o prontuário. https://docs.ezyvet.com/en/browse-documentation/vet-radar/patient-whiteboard/patient-sheets/about-patient-sheets e https://www.vetradar.com/
- Bitts: treatment sheet e software de hospitalização. https://bittsi.com/solutions/treatment-sheet
- Modelos de ficha com grade de vitais, fluidoterapia (tipo, taxa, volume e total acumulado), dor e entradas/saídas: https://vetvisitai.com/resources/veterinary-treatment-sheet e https://vcahospitals.com/-/media/2/vca/documents/hospitals/wisconsin/veterinary-specialty-center-middleton/overnight-monitoring---updated.ashx

Escribas de IA (focados em consulta/SOAP por áudio, não em evolução de internado):
- ScribbleVet: SOAP por paciente, envio ao PIMS. https://www.scribblevet.com/ e https://instinct.vet/products/scribblevet/
- Digitail (Tails AI) e Shepherd (TranscribeAI): IA nativa do PIMS. Visão geral: https://vetclinictech.com/best-ai-soap-note-tools-veterinarians/ e https://www.nectarvet.com/post/veterinary-ai-products
- Não encontrei fonte de que algum desses gere evolução diária de internado a partir de vitais e labs. Não verificado; o resumo da busca só citou SOAP de consulta.
- Contexto geral: https://www.aaha.org/trends-magazine/trends-may-2024/applications-of-ai-in-veterinary-practice/

Evidência sobre alucinação:
- Estrutura de avaliação de segurança clínica e alucinação em sumarização médica; relata taxa de alucinação de 1,47% e de omissão de 3,45% em geração de notas clínicas: https://www.nature.com/articles/s41746-025-01670-7
- JAMA Netw Open sobre acurácia, consistência e alucinação de LLMs em notas clínicas não estruturadas: https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2822301
- Avaliação de três ferramentas veterinárias de sumarização em registros de oncologia (fatos, completude, ordem cronológica): https://arxiv.org/pdf/2510.01224 (pré-print; os dados são de medicina humana e de oncologia veterinária, não de internação).
- Não encontrei estudo veterinário validado sobre geração de evolução diária de internados. Não verificado.

Brasil: não encontrei produto brasileiro específico para este fim na busca. Não verificado.

## 2. Forma recomendada

**Workflow determinístico + rascunho assistido por LLM opcional (integração leve), não agente autônomo.**

Justificativa:
- O maior ganho está em consolidar dados estruturados (vitais, entradas e saídas, medicações administradas, labs) em uma ficha única com cálculos. Balanço hídrico, tendência de peso/temperatura/FC e doses em mg/kg por peso atual são aritmética, e planilha ou script resolve sem risco de alucinação.
- Um LLM só entra para redigir o texto da evolução (S/O) a partir desses campos estruturados, em formato fechado. A avaliação (A) e o plano (P) ficam com o veterinário.
- Prescrição interna: o sistema só carrega a prescrição vigente, confere dose contra faixa cadastrada e sinaliza divergências. Não prescreve.
- Agente autônomo que altera prontuário ou prescrição: não recomendado. Há risco clínico, e a Res. CFMV 1.321/2020 define o prontuário como documento assinado privativamente por médico-veterinário.

## 3. Human-in-the-loop e riscos

Validação obrigatória:
1. O veterinário lê, edita e assina cada evolução antes de ela entrar no prontuário (assinatura e CRMV, conforme https://www.normasbrasil.com.br/norma/resolucao-1321-2020_480427.html). Rascunho da IA fica marcado como "não validado".
2. Toda mudança de prescrição (dose, fluido, suspensão) é criada e confirmada por humano. O sistema apenas alerta.
3. Alertas de valores críticos (por exemplo, queda de temperatura ou aumento de FC fora de limites configurados pela própria clínica) vão para a equipe. Os limites são parâmetros da clínica, não inventados pelo sistema.
4. O balanço hídrico é recalculado a partir dos registros brutos e conferido pela enfermagem.

Riscos:
- Clínicos: copiar e colar de dias anteriores, omissão (a literatura acima aponta omissões), erro de dose por peso desatualizado, unidade errada.
- Alucinação: o LLM pode inventar parâmetros ou exames. Mitigação: o modelo só recebe campos estruturados, a saída cita o campo de origem e valores numéricos são inseridos por código, não pelo modelo.
- Legais (CFMV): o prontuário deve ser escrito e datado, sem rasuras ou emendas, com data, horário, local e identificação do veterinário atendente, e arquivado por no mínimo 5 anos (Res. 1.321/2020, fontes acima). Requer trilha de auditoria e versionamento (correção por adendo, não sobrescrita). A Res. 1.275/2019 exige veterinário presente enquanto houver animal internado: https://abmes.org.br/arquivos/legislacoes/Resolucao-CFMV-1275-2019-07-25.pdf
- Receituário controlado: a Portaria SVS/MS 344/98 se aplica à prescrição veterinária de medicamentos de controle especial (https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf). A ficha interna não substitui a notificação/receita de controle especial. O sistema não deve emitir nem preencher esses documentos automaticamente. Requisitos atuais de receita eletrônica e SNCR para uso veterinário: não verificado, consultar CRMV.
- LGPD: dados de tutor são dados pessoais. Enviar a API de LLM externa exige minimização (sem nome, CPF, telefone ou endereço) e contrato com o operador. Texto da lei e orientação da ANPD: não verificado nesta pesquisa.

## 4. Pontuação

- Impacto: 4. A tarefa é diária e repetitiva, e o balanço e a consolidação são onde mais se ganha tempo.
- Viabilidade: 4 para a parte estruturada (ficha, cálculos, alertas). 3 para o rascunho de texto por LLM.
- Risco: 3 se o sistema só consolida e rascunha com validação. Subiria para 5 se alterasse prescrição de forma autônoma.

## 5. MVP sem dados reais e sem serviços pagos

Cabe: sim. Escopo sugerido:
- Planilha ou script (Python/CSV) com pacientes fictícios: entrada de vitais, fluidos e medicações por horário.
- Cálculo automático de balanço hídrico (entradas menos saídas), dose em mg/kg a partir do peso e tendências por parâmetro.
- Geração por template de um rascunho de evolução (S/O) marcado "RASCUNHO - requer validação veterinária", com campos A/P em branco.
- Teste: casos sintéticos com erros plantados (peso desatualizado, unidade errada, omissão) para medir se o sistema os sinaliza.
- Fora do MVP: LLM (pode usar modelo local gratuito depois), integração com PIMS, receituário controlado.
