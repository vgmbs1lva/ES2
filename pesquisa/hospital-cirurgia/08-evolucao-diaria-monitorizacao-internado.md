# Evolução diária e ficha de monitorização do internado

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Aviso sobre fontes (leia primeiro)

Nesta execução o limite de buscas web da sessão (200/200) estava esgotado e o WebFetch foi bloqueado pelo proxy para cfmv.gov.br e vet.cornell.edu. Portanto **nenhuma afirmação factual externa foi verificada com URL**. Tudo abaixo marcado "não verificado" precisa de checagem antes de ser usado. Não inclui URLs inventadas.

## 1. Soluções existentes

- Scribes de IA para SOAP veterinário e módulos de IA em PIMS (ex.: ferramentas de ditado/ambient scribe): não verificado (sem busca possível). Sei, de conhecimento geral, que esse mercado existe, mas não confirmo produtos, preços, suporte a PT-BR nem hospedagem de dados.
- Fichas de internamento em PIMS brasileiros (grade de parâmetros por horário, tarefas de tratamento): não verificado.
- Escalas de dor validadas (Glasgow CMPS-SF canina, escala felina da UNESP-Botucatu): existem na literatura, mas link e versão atual não verificados.
- Estudos sobre eficácia/segurança de LLM gerando notas clínicas veterinárias: não verificado.
- Normas: Resolução CFMV sobre prontuário/registro clínico (número e texto exatos não verificados), LGPD (Lei 13.709/2018), Código de Ética do médico-veterinário: não verificados nesta execução.

## 2. Forma recomendada: workflow determinístico / script-planilha (com rascunho de texto opcional)

Justificativa:
- Os dados de entrada são estruturados (FC, FR, T, PA, glicemia, diurese, dor) e o valor está em organizar, sinalizar tendência e listar pendências, não em "raciocinar".
- Parte 1 (determinística, sem IA): ficha por horário, validação de entrada (faixas plausíveis, unidades), cálculo de tendência e alertas por limiares configuráveis definidos pelo veterinário da casa, diurese em mL/kg/h, lista de pendências (exame não aferido no horário, medicação não registrada).
- Parte 2 (opcional): montar o rascunho SOAP por template preenchendo S/O/A/P com os dados registrados; o campo "Avaliação" e "Plano" ficam em branco ou apenas com sugestão marcada como tal. Um LLM só entra para redigir texto do S/O a partir de campos estruturados, nunca para decidir conduta.
- Agente autônomo não se justifica: o risco clínico e a baixa tolerância a erro superam o ganho; o mais simples (formulário + regras) resolve a maior parte do tempo gasto.

## 3. Human-in-the-loop, riscos

Validação: enfermagem registra os valores; o veterinário responsável revisa, edita e assina a evolução. Nada é gravado no prontuário como final sem assinatura/aceite explícito. Alertas são apoio, não substituem avaliação.

Riscos clínicos: alucinação de valores ou tendências (mitigar: o texto só cita números vindos dos campos, com diff visível); viés de automação (copiar nota do dia anterior); limiares inadequados por espécie/porte/idade/neonato (limiares vêm do veterinário, não do sistema); falso conforto por ausência de alerta.
Riscos legais (todos não verificados quanto ao texto exato): prontuário é responsabilidade do médico-veterinário (CFMV); LGPD aplica-se a dados do tutor (nome, contato) mesmo em contexto veterinário: minimizar, pseudonimizar e evitar enviar identificáveis a API externa; medicamentos controlados: o sistema não deve gerar nem sugerir doses/receituário (portaria SVS/MS 344/98 e normas CFMV, não verificadas), apenas registrar administração conforme prescrição humana.

## 4. Pontuação (1-5)

- Impacto: 3. Estimativa própria ~10 min x 3-5 internados x 5-7 dias é plausível, mas boa parte do tempo é exame físico, que não se automatiza; economia real talvez 30-40% (estimativa minha, sem fonte).
- Viabilidade: 4 para a parte determinística; 2-3 para texto por LLM com qualidade e privacidade adequadas.
- Risco: 3 (clínico moderado se houver sugestão de conduta; baixo se só organização e redação a partir de dados).

## 5. MVP sem dados reais e sem serviços pagos

Sim. Um script Python/planilha com ficha de parâmetros sintéticos, validação de faixa, tendência, cálculo de diurese, lista de pendências e gerador de template SOAP em texto, testado com casos fictícios. Sem LLM no MVP; LLM local ou API pode ser avaliado depois.
