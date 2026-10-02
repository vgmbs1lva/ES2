# Planejamento e participação em congresso/evento

Domínio: educação e pesquisa. Data da análise: 2026-10-02.

## Tarefa
Escolher evento, inscrever-se, montar escala de cobertura na clínica, assistir e depois compartilhar o aprendizado com a equipe. Carga estimada (própria, não verificada): 2-4 dias por veterinário por ano.

## 1. Soluções existentes (pesquisadas)
- Agendas de eventos: BVS Vet (https://www.bvs-vet.org.br/agenda/) e Panorama Pet Vet (https://panoramapetvet.com.br/eventos-pet-e-veterinarios-de-2026-ja-movimentam-a-agenda-do-setor/). Exemplos de eventos 2026 listados: CBA/Anclivepa (https://www.cbago.com.br/), Vet em Foco (https://congressovetemfoco.com.br/congressovetemfoco-2026/), CVDL in Rio, 15-16/out (https://eventos.inrio.vet.br/Evento/congressocvdlinrio). Datas devem ser confirmadas no site de cada evento; a busca não retornou o calendário do Conbravet/CBMV (não verificado).
- Escala de pessoal com pedidos de folga e troca de turno: Deputy, When I Work, Shifts (Everhour), Homebase, entre outros (https://everhour.com/shifts/veterinary-scheduling-software, https://wheniwork.com/industries/veterinary-clinic-software, https://shifton.com/industries/veterinary-clinic-scheduling/). Resultados vêm de páginas dos próprios fornecedores (viés comercial); preço e aderência à CLT brasileira não verificados.
- Orientação prática para devolutiva pós-congresso (resumo de pontos-chave, recursos, ações ligadas aos objetivos): https://chcm.com/how-to-prepare-your-healthcare-team-for-a-national-conference/ e https://www.himssconference.com/blog/5-ways-attendees-turn-conference-insights-into-real-change/. São textos de blog, não estudos; evidência de efeito sobre desfecho clínico: não verificado.
- Educação continuada no CFMV: a busca não encontrou exigência de horas obrigatórias de educação continuada para médicos-veterinários (não verificado). Resolução 1.573/2023 apareceu como possível referência, mas o conteúdo não foi confirmado (https://www.legisweb.com.br/legislacao/?id=454599).
- Não encontrei plug-in de PIMS veterinário que faça planejamento de congresso (não verificado).

## 2. Forma recomendada: script/planilha (com apoio opcional de LLM em tarefa pontual)
Justificativa: a tarefa é rara (poucas vezes ao ano), de baixo volume e com decisões que são do dono/responsável técnico (orçamento, quem vai, quem cobre). Um agente autônomo não se paga. O que repete e é mecânico:
1. Comparar eventos candidatos (data, custo, tema, local) em uma planilha com pontuação simples.
2. Checar conflito de datas com a escala e calcular cobertura mínima por dia.
3. Gerar um modelo de resumo para a equipe.

Proposta: planilha com abas "Eventos", "Escala" e "Cobertura" (fórmulas de contagem de profissionais disponíveis por dia versus mínimo exigido) e um template fixo de devolutiva (3 aprendizados, 1 mudança proposta, referências). Opcionalmente, um LLM transforma anotações do próprio veterinário em rascunho do resumo; o autor revisa. Inscrição e pagamento ficam manuais.

## 3. Human-in-the-loop e riscos
Validação humana obrigatória:
- Escolha do evento, orçamento e inscrição/pagamento (decisão do veterinário ou sócio).
- Escala final e cobertura mínima, especialmente plantão, internação e responsável técnico presente (CRMV exige RT pela clínica; conferir norma vigente, não verificado aqui).
- Resumo para a equipe: o autor confere cada afirmação contra o material original antes de circular.

Riscos:
- Alucinação: o LLM pode inventar datas, preços, palestrantes ou resultados de estudos. Mitigação: dados do evento copiados da página oficial, resumo baseado só nas anotações/slides do usuário, com fonte citada.
- Clínico: um resumo que vire mudança de conduta sem leitura do trabalho original (dose, protocolo). Mitigação: marcar tudo como "a validar" e exigir referência primária antes de adotar.
- Legal: direito autoral e termos do evento (gravação/compartilhamento de slides podem ser restritos); CLT e acordo de jornada para ausências; LGPD, pois não colocar dados de pacientes/tutores em casos mostrados no congresso nem no resumo; e dados pessoais da equipe (escala, férias) em ferramentas externas exigem cuidado. Receituário controlado: sem relação direta.
- Pagamento/inscrição por agente: risco de fraude e erro financeiro; não delegar.

## 4. Pontuação (1-5)
- Impacto: 2. Libera pouco tempo (algumas horas por evento); o valor real está em fazer a devolutiva de fato, o que é disciplina e não tecnologia.
- Viabilidade: 5. Planilha e template resolvem.
- Risco clínico/legal: 2. Baixo, sobe se o resumo virar protocolo sem checagem ou se envolver dados pessoais.

## 5. MVP testável sem dados reais e sem serviços pagos?
Sim. Planilha (ou script em Python/CSV) com eventos fictícios, escala fictícia de 5 profissionais e cálculo de cobertura mínima, mais template de resumo. Não precisa de integrações nem de pagamento. Não cobre: inscrição automática, integração com PIMS, avaliação de qualidade científica do evento.
