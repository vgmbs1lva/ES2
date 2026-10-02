# Relatório cirúrgico / descrição da técnica no prontuário

Domínio: hospital-cirurgia. Data: 2026-10-02.

## Aviso sobre evidências
Nesta execução o limite de WebSearch (200) estava esgotado e o proxy bloqueou WebFetch (woovet.com, in.gov.br). Nada abaixo foi pesquisado nesta rodada. Tudo que é fato externo está marcado "não verificado" e deve ser conferido antes de uso.

Única fonte citada, já dada na tarefa (comercial, baixa confiança, não reaberta por mim):
- https://tandemhealth.ai/resources/knowledge/documentation-cost-per-veterinarian-a-european-perspective
- https://www.woovet.com/blog/how-much-time-vets-spend-on-medical-records

## 1. Soluções existentes
Não verificado. Existem, pelo meu conhecimento prévio, scribes de IA veterinários e módulos de PIMS que geram notas a partir de ditado, mas não confirmei produto, preço, suporte a português nem a cirurgia. Pesquisar depois: "AI scribe veterinário", plug-ins dos PIMS usados no Brasil, estudos de laudo operatório gerado por LLM em medicina humana.

## 2. Forma recomendada: workflow determinístico (template estruturado), com LLM opcional
Justificativa: o relatório cirúrgico é quase todo dado já conhecido (paciente, procedimento, material, amostras). O ganho vem de um formulário/checklist por tipo de cirurgia (OSH, orquiectomia, cistotomia, mastectomia etc.) com campos pré-preenchidos e texto-base da técnica padrão, em que o veterinário só ajusta desvios. Isso é o mais simples que resolve, não alucina e é auditável. Um LLM só entra, se entrar, para transformar notas livres/ditado em texto corrido a partir dos campos, sem inventar conteúdo. Agente autônomo não se justifica.

Fluxo:
1. Veterinário preenche campos curtos (técnica escolhida, achados, fios/calibres, complicações S/N, amostras).
2. Script monta o relatório a partir de modelos de técnica.
3. Campo ausente aparece como "NÃO INFORMADO", nunca preenchido por suposição.
4. Gera também a requisição de histopatologia (identificação, sítio, fixador, suspeita clínica).
5. Veterinário revisa, edita e assina.

## 3. Human-in-the-loop e riscos
- Validação: o cirurgião revisa e assina todo relatório; nada entra no prontuário sem esse aceite. Revisar especialmente lateralidade, fios, contagem de compressas, complicações, amostras enviadas.
- Alucinação: risco de LLM completar técnica "padrão" que não foi feita (ex.: citar sutura não usada). Mitigação: modelo só reformata campos fornecidos, diff entre entrada e saída, sem texto extra.
- Legal/CFMV: o prontuário/ficha clínica é responsabilidade do médico-veterinário; a resolução do CFMV sobre prontuário e guarda é a referência, mas não consegui verificar número, texto nem prazos. Não verificado.
- LGPD: dados de tutor são pessoais. Evitar enviar identificação a APIs externas; usar apenas dados mínimos/pseudonimizados. Detalhes de enquadramento: não verificado.
- Receituário controlado: o relatório pode citar anestésicos/opioides controlados; não deve substituir registro/escrituração específica (Portaria SVS/MS 344/98, não verificado nesta rodada). Não automatizar esse registro no MVP.

## 4. Pontuação
- Impacto: 3. A tarefa dura ~10 min por cirurgia (estimativa da tarefa); o ganho é real mas limitado ao volume cirúrgico, e os 25-40% de documentação vêm de fonte comercial.
- Viabilidade: 5. Template + script é trivial.
- Risco: 2 com template e revisão obrigatória; subiria a 4 com LLM sem revisão.

## 5. MVP
Sim, cabe: gerador em script/planilha (Python ou formulário) com templates de técnica e dados fictícios, sem serviços pagos e sem dados reais. Teste: comparar saída com relatórios sintéticos escritos à mão e checar que campos vazios saem como "NÃO INFORMADO". Camada LLM fica fora do MVP.
