# 05 - Revisão e aprovação de agenda e encaixes

Domínio: atendimento-tutor. Data da pesquisa: 2026-10-02.

Nota de método: WebSearch funcionou; WebFetch foi bloqueado pelo proxy (simples.vet, getoliver.com, planalto.gov.br). Afirmações abaixo baseiam-se nos resumos de busca, não na leitura das páginas. Onde isso importa, marquei "não verificado".

## 1. Soluções existentes

Produtos (todos materiais de fornecedor, sem evidência independente de eficácia):
- Agenda de PIMS brasileiros: SimplesVet (visão por profissional por dia/semana/mês, tempo de espera e duração média de atendimento) https://simples.vet/funcionalidades/agenda/ ; VetSoft Web https://www.vetsoft.com.br/ ; VetBase https://www.vetbase.com.br/ ; Vetus https://vetus.com.br/new/
- Agendamento online/IA (EUA/UE): Vetstoria https://www.vetstoria.com/blog/why-your-veterinary-practice-needs-real-time-online-booking/ ; PetDesk https://petdesk.com/products/veterinary-online-booking-system ; Oliver (waitlist com preenchimento automático) https://getoliver.com/veterinary-appointment-scheduling ; Puppilot https://www.puppilot.co/product/scheduling ; Whippy https://www.whippy.ai/blog/automate-veterinary-appointment-scheduling ; Vetspire https://www.vetspire.ai/features/scheduler ; comparativo https://ownerexchange.com/veterinary-online-scheduling-software/
- Recurso comum relatado: triagem por palavras-chave de emergência que dispara alerta ao tutor, e IA que lê a mesma agenda da recepção e casa tipo de consulta com profissional (resumo de busca; não verificado nas páginas).

Literatura/guias:
- Modelos de duração por tipo de consulta (retorno rápido 10-20 min, exame completo 30-45 min) e agenda por horário marcado vs. por ondas: https://amerivet.com/blog/veterinary-appointment-scheduling e https://www.jotform.com/blog/veterinary-appointment-scheduling/ (blogs comerciais, não revisados por pares; durações são referência genérica, não norma).
- AAHA, guia de forward booking (Felsted e Gavzer): http://www.aaha.org/wp-content/uploads/globalassets/04-practice-resources/Forward-booking (link retornado pela busca; conteúdo não lido).
- Pesquisa operacional sobre templates de agenda em ambulatório humano (reservar capacidade para casos não agendados): https://arxiv.org/pdf/1911.05129 e https://arxiv.org/pdf/2511.06557 (preprints; transferência para veterinária não verificada).
- Estudo de coorte em atenção primária humana sobre duração de consulta: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8900401/ (humana, apenas contexto).

Lacuna: não encontrei estudo revisado por pares mostrando que IA melhora encaixe de agenda em clínica veterinária brasileira. Não verificado.

## 2. Forma recomendada: workflow determinístico (regras + planilha/script), com LLM opcional só para redigir mensagem

Justificativa: o problema central é restrição e prioridade (quem tem vaga, quanto dura cada tipo, bloqueios cirúrgicos, ordem da lista de espera). Isso é resolvível com regras explícitas e auditáveis, sem generalização por LLM. Um agente autônomo que mexe na agenda traz risco sem ganho. A decisão "este caso agudo entra?" é clínica e fica com o vet.

Desenho:
1. Tabela de tipos de consulta com duração, vet/sala elegíveis e buffer (configurável pela clínica).
2. Blocos fixos protegidos (cirurgia, retornos longos) e quota diária de encaixes.
3. Motor de regras responde "cabe?": lista de slots candidatos ordenados, conflitos entre vets sinalizados com motivo.
4. Pedido de encaixe entra com campos estruturados (espécie, queixa em texto livre, sinal de alerta marcado pela recepção). Triagem só por checklist fixo definido pelo vet, sem diagnóstico.
5. Sugestão de proposta de agenda gerada; vet/responsável aprova; só então a recepção confirma ou remarca com o tutor (modelo de mensagem pronto).
6. LLM opcional: redigir a mensagem ao tutor e resumir a lista de espera. Nunca decide prioridade clínica.

Se a clínica já usa PIMS com agenda (ex.: SimplesVet), o caminho mais simples é configurar tipos/durações/bloqueios nativos antes de construir algo. Integração/API: não verificada para os PIMS brasileiros.

## 3. Human-in-the-loop, riscos e conformidade

Validação humana:
- Vet responsável (ou plantonista) aprova todo encaixe de caso agudo e qualquer redução de duração padrão.
- Recepção não recebe "negado" automático para queixas com sinal de alerta: o sistema escala ao vet.
- Conflito entre vets: resolvido pelo responsável técnico; o sistema só lista as opções.
- Cirurgias e bloqueios: alteração só por humano autorizado, com log.

Riscos clínicos:
- Subestimar urgência (ex.: tutor descreve mal; dispneia, trauma, obstrução urinária em felino, intoxicação) e empurrar para data distante. Mitigação: qualquer sinal de alerta ou dúvida vai para o vet; texto ao tutor orienta buscar atendimento imediato conforme definido pela clínica. Não usar o sistema para orientar conduta.
- Duração subdimensionada gera atraso em cascata; monitorar duração real versus prevista.
- Alucinação: se houver LLM, restringir a texto de mensagem com modelo e dados vindos da agenda; sem inventar horários, preços ou recomendações clínicas. Validar horário contra a agenda antes de enviar.

Legais:
- LGPD (Lei 13.709/2018): dados do tutor (nome, telefone) e do animal; base legal provável é execução de contrato/procedimentos preliminares (art. 7, V) ou legítimo interesse; para marketing, consentimento. Art. 20 prevê revisão de decisões automatizadas, mais um motivo para decisão final humana. Texto do artigo não verificado (planalto.gov.br bloqueado). Minimizar dados, operador/fornecedor de IA em contrato, atenção a transferência internacional se a IA estiver fora do Brasil. Fonte geral de WhatsApp e LGPD: https://lgpdbrasil.com.br/whatsapp-nas-empresas-e-a-adequacao-da-lgpd/
- CFMV: a decisão de atender, priorizar e encaminhar é ato do médico-veterinário (responsabilidade técnica); a normativa específica sobre uso de IA em veterinária: não verificado.
- Receituário controlado: fora do escopo desta tarefa; o sistema não deve gerar, renovar ou prometer prescrição ao confirmar retornos.

## 4. Pontuação (1-5)

- Impacto: 3. Reduz idas e vindas da recepção e conflitos, mas a agenda já existe nos PIMS e o ganho de tempo é moderado. Sem evidência quantitativa.
- Viabilidade: 4 para regras/planilha; 2 para integração automática com PIMS (API não verificada).
- Risco: 3 (por urgência subestimada e LGPD), caindo para 2 com aprovação humana obrigatória e sem decisão clínica automática.

## 5. MVP sem dados reais e sem serviço pago

Cabe. Protótipo em repositório: planilha/script (Python ou JS) com agenda sintética (vets fictícios, tipos de consulta, bloqueios cirúrgicos, lista de espera), função "cabe?" que devolve slots e conflitos, e fila de aprovação do vet. Testes unitários com casos: encaixe em bloco cirúrgico, dois vets disputando a mesma sala, caso com sinal de alerta escalado. Sem LLM no MVP (templates de mensagem fixos). Não inclui integração com PIMS real nem WhatsApp.
