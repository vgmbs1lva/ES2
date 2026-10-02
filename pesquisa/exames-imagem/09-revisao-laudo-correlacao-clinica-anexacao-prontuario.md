# Revisão do laudo de imagem, correlação clínica e anexação ao prontuário

Data: 2026-10-02. Domínio: exames-imagem.

## Aviso sobre fontes
Nesta execução o limite de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy (in.gov.br). Nenhuma afirmação factual abaixo tem URL verificada. O que veio do enunciado da tarefa (Resolução CFMV 1.465/2022: assinatura eletrônica avançada e RT no CRMV para telediagnóstico) está tratado como premissa do usuário, "não verificado" por mim. Revisar com busca antes de citar.

## 1. Soluções existentes
- Plataformas de teleradiologia veterinária com IA e laudo em PDF (ex.: Vetology, SignalPET, Antech RapidRead): existência conhecida por memória, mas características, integração com PIMS e validação científica: não verificado (sem URL).
- Plug-ins/integrações de PIMS que anexam laudo PDF ao prontuário: não verificado.
- Estudos sobre LLM em revisão de laudos radiológicos (erros de lateralidade, alucinação): não verificado para veterinária.
- Texto da Resolução CFMV 1.465/2022 e requisitos de assinatura (ICP-Brasil ou equivalente): não verificado.
- Guarda de prontuário/imagens e LGPD aplicada à veterinária: não verificado.

## 2. Forma recomendada: workflow determinístico (checklist + script), com LLM opcional e restrito
A tarefa mistura duas partes:
1. Verificação formal, que é regra fixa: o PDF tem assinatura digital válida? Nome do paciente/ID do laudo bate com o cadastro? Identificação do prestador e RT/CRMV presentes? Data do exame confere? Lateralidade citada no laudo aparece nas imagens/metadados? Isso se resolve com script (extração de texto do PDF, regex, comparação com o cadastro, checagem da assinatura PDF, nomeação padronizada e arquivamento).
2. Correlação clínica e conduta, que é julgamento do veterinário. Não automatizar.

Um LLM, se usado, apenas como segunda leitura: resumir o laudo, listar achados e sinalizar divergências com o texto do prontuário (ex.: "laudo diz membro D, prontuário diz E"). Não decide conduta e não escreve no prontuário sem aprovação. Agente autônomo não se justifica: o fluxo é curto, linear e de alto risco.

## 3. Human-in-the-loop e riscos
- Veterinário valida: (a) identidade do paciente e lateralidade olhando a imagem, não só o texto; (b) cada discrepância sinalizada; (c) a correlação clínica e a conduta; (d) a anexação final. Revisão é obrigatória em todo laudo, não amostral.
- Clínico: laudo de outro paciente ou lado trocado levando a procedimento errado. Alucinação do LLM (achado inventado ou omitido). Falso conforto de um "OK" automático.
- Legal/CFMV: responsabilidade pelo ato permanece do médico-veterinário; telediagnóstico exige prestador com RT e assinatura eletrônica avançada (premissa do enunciado, não verificado). O script deve apenas sinalizar ausência, nunca "validar" juridicamente.
- LGPD: laudo contém nome/contato do tutor. Evitar enviar a LLM em nuvem sem base legal, contrato e minimização (pseudonimizar antes). Aplicação exata: não verificado.
- Receituário controlado: não se aplica diretamente; se a conduta envolver controlados, o receituário segue fluxo próprio, fora da automação.
- Integridade: guardar hash do PDF original e trilha de quem anexou e quando.

## 4. Pontuação
- Impacto: 3/5. Poupa conferências repetitivas e padroniza arquivamento, mas a parte demorada (raciocínio clínico) fica com o veterinário.
- Viabilidade: 4/5 para o workflow determinístico; 2/5 para qualquer integração real com PIMS (depende de API do fornecedor, não verificado).
- Risco: 4/5. Erro de paciente/lateralidade é grave; a automação pode induzir complacência. Cai para 3/5 se for só checklist sem LLM.

## 5. MVP sem dados reais e sem serviços pagos
Sim, parcialmente. Um script Python local com PDFs sintéticos (laudos fictícios, alguns com troca de nome, lateralidade divergente, sem assinatura ou sem RT), um CSV/JSON de prontuário fictício, que gera relatório de conferência (aprovado/divergente/ausente), nomeia e arquiva com hash. Camada de LLM opcional e testável com modelo local ou stub. Não cobre: validação criptográfica real de assinatura ICP-Brasil (exige certificados), integração com PIMS e conferência da imagem em si.
