# Monitorização e registro da recuperação anestésica

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Limitação desta pesquisa (leia primeiro)
O orçamento de WebSearch da sessão está esgotado (200/200) e o WebFetch é bloqueado pelo proxy de egresso (testei aaha.org). **Nenhuma fonte foi verificada.** Toda afirmação factual está marcada "não verificado". Nenhuma dose ou valor de corte clínico é fixado aqui: limiares (temperatura, escore de dor que dispara resgate) devem ser definidos pelo veterinário/protocolo da clínica a partir de fontes conferidas.

Referências apenas citadas (não abertas): AAHA 2020 Anesthesia and Monitoring Guidelines for Dogs and Cats: https://www.aaha.org/resources/2020-aaha-anesthesia-and-monitoring-guidelines-for-dogs-and-cats/ (conteúdo não verificado). A menção do enunciado de que o ACVAA 2025 pede registro da recuperação vem do enunciado, não verificada por mim.

## 1. Soluções existentes (não verificado)
Hipóteses a confirmar numa próxima rodada:
- Escalas de dor validadas: Glasgow Composite Measure Pain Scale (forma curta, cães), Feline Grimace Scale, UNESP-Botucatu (validada no Brasil, felinos e cães): existência conhecida, URLs e detalhes não verificados.
- Módulos de ficha anestésica/recuperação em PIMS (Simples Vet, Vetus, SoftVet; ezyVet, Digitail, Cornerstone): não verificado se têm campos de recuperação ou lembretes.
- Monitores multiparamétricos com registro automático (SpO2, temperatura, FC): existem, mas o foco aqui é a recuperação pós-extubação, frequentemente sem monitor: não verificado.
- Apps de escala de dor (ex.: apps das escalas acima): não verificado.
- Estudos sobre hipotermia pós-anestésica, disforia e dor na recuperação em cães e gatos: não verificado; buscar no PubMed.
- Estudos de LLM/visão computacional para avaliação de dor por face (ex.: Feline Grimace por IA): literatura existe (não verificado), ainda de pesquisa, não confiável para decisão clínica.

## 2. Forma recomendada: workflow determinístico (formulário estruturado com cronômetro e lembretes). Sem agente.
Justificativa:
- A tarefa é medir à beira da baia (mão e olho do profissional): extubação, temperatura, escore de dor, náusea, vocalização. O gargalo é registro consistente e no tempo certo, não raciocínio. Um formulário com horários e campos fixos resolve.
- Decisão de analgesia de resgate é julgamento clínico; a ferramenta pode apenas sinalizar "escore acima do limiar definido pela clínica" por regra fixa, nunca prescrever.
- Dispensa LLM no MVP. Opcional futuro: redigir o resumo narrativo a partir dos campos, sem inventar valores.

Componentes do MVP:
1. Formulário (CSV/JSON ou planilha/script CLI) por paciente (ID fictício): hora da extubação, tempo até deglutição/decúbito esternal (opcional), série de medições em intervalos configuráveis (temperatura, FC, FR, escala de dor escolhida, náusea/vômito, vocalização/disforia, observações).
2. Intervalos de lembrete configuráveis pela clínica (padrão placeholder).
3. Regras por código com limiares configuráveis e sem valores clínicos embutidos como verdade: alerta de temperatura fora da faixa, escore de dor acima do corte, ausência de medição no intervalo, campo obrigatório faltando.
4. Critérios de alta para internação como checklist preenchido pelo veterinário (extubado, temperatura aceitável, dor controlada, sem vômito ativo), nunca decisão automática.
5. Saída: registro de recuperação com autor, horários e assinatura/confirmação do veterinário; trilha de edição (quem alterou o quê).
6. Registro de analgesia de resgate como campo livre/estruturado de dose administrada pelo veterinário; a ferramenta não calcula nem sugere dose (ou, se integrada à calculadora da tarefa 02, só exibe números do formulário curado).

## 3. Human-in-the-loop
- Técnico/auxiliar mede e registra; veterinário revisa a série, decide ajuste analgésico e assina a liberação para internação.
- Alertas por regra são avisos, não ordens. Silenciar alerta exige justificativa registrada.
- Escolha e treino na escala de dor: concordância entre avaliadores varia (não verificado); padronizar uma escala por espécie.

## Riscos
- Clínico: atraso na detecção de dor, hipotermia ou obstrução de vias aéreas por falso conforto na ferramenta; fadiga de alertas; escala aplicada de modo inconsistente. Mitigação: alertas simples e poucos, lembretes visíveis, treino, a ferramenta não substitui observação contínua.
- Alucinação: inexistente se sem LLM. Se resumo por LLM entrar, risco de inventar achados ou omitir alerta; mitigar com texto gerado só dos campos e revisão.
- Legal: o prontuário é responsabilidade do médico-veterinário; normas do CFMV sobre prontuário/ficha e guarda: não verificado nesta rodada. Registro deve ter autoria, data/hora e não ser apagável sem trilha.
- Receituário controlado: analgésicos de resgate frequentes (opioides) são controlados no Brasil (Portaria SVS/MS 344/98, não verificado). A ferramenta não emite receita nem substitui livro/escrituração de controlados; apenas sinaliza "controlado".
- LGPD: dados de tutor e paciente identificável são dados pessoais; no MVP só dados sintéticos; em produção, armazenamento local/controlado, sem envio a APIs externas sem base legal (não verificado).
- Dispositivo/software como produto de saúde animal: enquadramento regulatório não verificado.

## 4. Pontuação (1-5, sem inflar)
- Impacto: 3. O tempo de 30-45 min é de observação à beira da baia, que não some; o ganho é no registro completo, no padrão e na conformidade documental (ACVAA conforme enunciado, não verificado), economizando talvez alguns minutos de digitação/papel por paciente (estimativa própria).
- Viabilidade: 5 para formulário com regras; 1-2 para avaliação autônoma de dor por IA.
- Risco: 3 com formulário e alertas simples e validação humana; 4 se alguém passar a confiar nos alertas em vez de observar.
- Incerteza geral: alta (nenhuma fonte verificada).

## 5. Cabe num MVP testável sem dados reais e sem serviços pagos?
Sim. Script Python (ou planilha) com pacientes sintéticos, limiares placeholder configuráveis, testes unitários de regras (intervalo perdido, escore acima do corte, campos obrigatórios) e geração do registro em Markdown/CSV. Sem API paga. A validação dos limiares e da escala de dor adotada exige veterinário e fontes conferidas antes de uso real.

## Próximos passos de verificação
Ler AAHA 2020 e ACVAA 2025 (seção de recuperação/registro); validação das escalas (Glasgow CMPS-SF, UNESP-Botucatu, Feline Grimace); estudos de hipotermia pós-anestésica; normas CFMV sobre prontuário; Portaria 344/98 e orientação MAPA; levantar recursos de recuperação em PIMS brasileiros.
