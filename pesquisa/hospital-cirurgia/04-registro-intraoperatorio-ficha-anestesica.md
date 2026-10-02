# Registro intraoperatório da ficha anestésica (sinais vitais a cada 5 min, eventos, fármacos)

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Limitação desta pesquisa (leia primeiro)
O orçamento de WebSearch da sessão está esgotado (200/200) e o WebFetch é bloqueado pelo proxy (testei acvaa.org: EGRESS_BLOCKED). **Nenhuma fonte foi verificada por mim.** O que está abaixo vem do enunciado da tarefa (citado como tal) ou é marcado "não verificado".

Fontes citadas no enunciado, não abertas por mim:
- ACVAA 2025, diretrizes de monitoração em pequenos animais: https://www.vaajournal.org/article/S1467-2987(25)00071-6/fulltext e https://acvaa.org/updated-acvaa-small-animal-anesthesia-monitoring-guidelines-are-available/ (afirmação do enunciado: FC, PA, SpO2 e EtCO2 geralmente a cada 5 min; demais variáveis ao menos a cada 15 min; não verificado).
- Tempo: 45-90 min por procedimento x 8-15 procedimentos/semana é estimativa própria do enunciado. Parte desse tempo é presença de monitoração (obrigatória), não digitação; o que se economiza é só a transcrição.

## 1. Soluções existentes (não verificado)
Hipóteses a confirmar numa próxima rodada:
- Monitores multiparamétricos veterinários com saída de dados/registro de tendências (memória interna, USB, serial) e softwares de registro anestésico eletrônico ligados a eles: existência plausível, produtos e modelos não verificados.
- Módulos de ficha anestésica em PIMS (Simples Vet, Vetus, SoftVet no Brasil; ezyVet, Digitail, Cornerstone fora): não verificado se têm ficha intraoperatória ou importam dados do monitor.
- Sistemas de registro anestésico automatizado em medicina humana (AIMS) e estudos comparando registro manual vs automático (humana e veterinária): não verificado; buscar no PubMed. A literatura humana costuma descrever que registro automático tem artefatos (leituras espúrias por movimento/eletrocautério) que exigem revisão: não verificado.
- Planilha ou ficha de papel padronizada: solução mais comum na prática (não verificado).

## 2. Forma recomendada: integração/script determinístico (captura de dados do monitor) + formulário para eventos. Sem agente.
Justificativa:
- Os sinais vitais já existem digitalmente no monitor; a tarefa é copiar números em intervalos fixos. Isso é problema de captura de dados, não de raciocínio. LLM não acrescenta nada e introduz risco de número inventado.
- Eventos e fármacos (bolus, mudança de plano, intercorrência) são observações e ações do anestesista/técnico: devem ser registradas por entrada direta (botão/formulário com carimbo de hora), não inferidas.
- Caminho mais simples em ordem crescente de esforço:
  1. Ficha de papel/planilha padronizada com intervalos de 5 min e campos pré-impressos (zero tecnologia).
  2. Formulário/planilha com carimbo de hora automático por clique para eventos e fármacos (script/web local).
  3. Importação do log do monitor (CSV/serial), quando o modelo exportar: depende do equipamento e do fabricante (não verificado), pode ser integração proprietária ou inexistente.
- Camada de LLM opcional e fora do MVP: apenas redigir o resumo narrativo pós-operatório a partir dos registros já confirmados, sem alterar valores. Também não indicada para "interpretar" tendências em tempo real.

Componentes do MVP:
1. Linha do tempo por procedimento (paciente fictício): campos FC, PAS/PAM/PAD, SpO2, EtCO2, temperatura, FR, plano/CAM/agente, fluido, com lembrete visual a cada 5 min.
2. Registro de eventos e fármacos com hora automática (fármaco, dose em mg ou mL, via; flag "controlado").
3. Importador de CSV simulado de monitor com validação: faixas fisiológicas plausíveis, valores nulos, saltos bruscos; leituras suspeitas marcadas, não corrigidas.
4. Alertas por regra (limiares configuráveis pelo veterinário, por exemplo SpO2 baixa, PAM baixa, temperatura): apenas destacar na tela, nunca decidir. Valores-limite devem ser definidos pelo anestesista (não cito números; não verificado).
5. Gráfico da ficha e exportação PDF/Markdown com campo de assinatura e log de alterações (quem editou o quê e quando).

## 3. Human-in-the-loop
- Anestesista/técnico presente junto ao paciente: dados importados do monitor são rascunho até alguém conferir; artefatos (movimento, eletrocautério, sensor mal posicionado) devem ser descartados ou anotados por humano.
- O veterinário responsável revisa e assina a ficha ao final; edições posteriores ficam em trilha de auditoria.
- Alertas não substituem a observação clínica nem a monitoração contínua do paciente. A automação do registro não pode reduzir a vigilância; risco de "automation complacency" (não verificado).

## Riscos
- Clínico: registro automático de valor artefatual tomado como real; atraso/falha de importação sem o operador perceber (lacuna silenciosa na ficha); alarme falso ou ausente criando falsa segurança. Mitigação: indicador de última leitura recebida, aviso de lacuna maior que o intervalo, confirmação humana, papel como contingência.
- Alucinação: nula se não houver LLM no registro; se houver no resumo, ele pode inventar eventos ou trocar valores. Mitigação: LLM só reformata dados estruturados e mostra os campos de origem; revisão obrigatória.
- Legal: a ficha anestésica integra o prontuário e é responsabilidade do médico-veterinário (normas CFMV sobre prontuário e responsabilidade técnica: não verificado). Exige identificação do autor, data/hora e imutabilidade/trilha de alterações. Assinatura eletrônica válida: não verificado.
- Receituário controlado: opioides, cetamina e benzodiazepínicos são controlados no Brasil (Portaria SVS/MS 344/98, não verificado nesta rodada). A ficha apenas registra uso e sinaliza "controlado"; não gera receita nem substitui livro/escrituração de controlados, nem baixa de estoque sem desenho regulatório adicional (não verificado).
- LGPD: nome de tutor, paciente identificável e imagens são dados pessoais; no MVP usar somente dados fictícios; em produção, armazenar localmente/em provedor com base legal e não enviar a APIs externas sem avaliação (não verificado).
- Dependência de fornecedor: protocolos proprietários de monitores podem impedir integração ou violar termos de uso (não verificado).

## 4. Pontuação (1-5, sem inflar)
- Impacto: 3. O tempo de transcrição existe, mas é só parte do 45-90 min (estimativa do enunciado, não verificada), pois a monitoração em si não é eliminável. Ganho maior em legibilidade, completude e menos erro de transcrição; para quem já usa PIMS, menor.
- Viabilidade: 4 para formulário com carimbo de hora e ficha estruturada; 2-3 para importação automática do monitor (depende do modelo); 1-2 para qualquer abordagem baseada em LLM.
- Risco: 3 (clínico e legal moderados: artefatos, lacunas e responsabilidade do prontuário). Sobe para 4 se houver alarmes ou sugestões automáticas ao paciente.
- Incerteza geral: alta (nenhuma fonte verificada).

## 5. Cabe num MVP testável sem dados reais e sem serviços pagos?
Sim, em parte. Cabe: formulário/script local (Python ou planilha), eventos com carimbo de hora, importador de CSV sintético de monitor, validação de plausibilidade, gráfico e exportação com trilha de auditoria, testes unitários com procedimentos fictícios. Não cabe: integração real com monitor/capnógrafo (depende de equipamento e protocolo) e validação clínica; ambos exigem teste com veterinário em ambiente real.

## Próximos passos de verificação
Abrir o texto completo ACVAA 2025 (links acima) e confirmar intervalos e itens obrigatórios do registro; levantar modelos de monitores com exportação de dados e PIMS com ficha anestésica; buscar estudos de registro anestésico manual vs automatizado; checar normas CFMV (prontuário, responsabilidade) e Portaria 344/98 / orientação MAPA para controlados.
