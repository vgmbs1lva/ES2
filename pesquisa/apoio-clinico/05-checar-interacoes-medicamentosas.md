# Checar interações medicamentosas e contraindicações

Domínio: apoio-clinico. Data: 2026-10-02. Volume estimado: ~5 min x 10-15 casos/semana (~1 h/semana; estimativa própria, não verificada).

## Recomendação

**Forma: integração/consulta a base curada, com workflow determinístico leve para montar o caso. Não usar LLM como fonte da interação.**

- A parte que importa (a interação existe? qual gravidade?) é consulta a base curada. Gerar isso com LLM é o ponto de maior risco de alucinação.
- O que sobra de automatizável é organizar a entrada: normalizar nomes (comercial para princípio ativo), listar pares, checar espécie/peso/comorbidade e produzir um checklist.
- LLM entra, no máximo, como redator opcional do parecer a partir de dados já recuperados da base (RAG estrito), citando o trecho da fonte. Ele não acrescenta interações por conta própria.

## Soluções existentes (verificadas por busca)

- Plumb's (Instinct): checador de interações veterinário, classificação contraindicado/maior/moderada/menor/sem interação, >25.000 interações, apps iOS/Android. https://plumbs.com/ e https://instinct.vet/products/plumbs/ , https://plumbs.com/blog/plumbs-veterinary-drugs-launches-new-features-and-a-first-of-its-kind-industry-tool/ . Preço/disponibilidade/idioma no Brasil: não verificado. Integração via API com PIMS brasileiros: não verificado.
- Estudos de LLM em interações (humanos, não veterinário): acurácia geral 54,1% a 83,7%, pior em interações menos graves, desempenho cai com mais fármacos. https://pmc.ncbi.nlm.nih.gov/articles/PMC12772686/ , https://pmc.ncbi.nlm.nih.gov/articles/PMC13505366/ . Estudo equivalente em veterinária: não verificado (não encontrei).
- Plug-ins de PIMS brasileiros com alerta de interação: não verificado.

## Human-in-the-loop

- O veterinário é o responsável pela prescrição (ato técnico e ético exclusivo do médico-veterinário, Res. CFMV 1.318/2020): https://revista.cfmv.gov.br/prescricao-de-medicamentos-veterinarios-e-um-ato/ . A ferramenta só sugere; nunca prescreve nem altera receita.
- Validação obrigatória: o veterinário confere cada alerta contra a fonte citada, decide substituir/monitorar/manter e registra no prontuário (Res. CFMV 1.321/2020, alterada pela 1.653/2025): https://www.migalhas.com.br/depeso/435877/resolucao-1-653-25-do-cfmv-na-visao-do-prontuario-medico-veterinario .
- Ausência de alerta não significa ausência de interação: a tela deve dizer isso explicitamente.

## Riscos

- Clínico: falso negativo (pior caso); doses, espécie (gato vs cão), insuficiência renal/hepática e suplementos fitoterápicos geralmente mal cobertos. Extrapolação de dados humanos.
- Alucinação: LLM inventa interação ou nega uma real; mitigação: só base curada, citação obrigatória, "não encontrado na base" em vez de resposta livre.
- Legal: responsabilidade permanece do veterinário. Receituário controlado (Portaria SVS/MS 344/98): regras específicas não verificadas aqui; a ferramenta não emite nem substitui receita. LGPD (Lei 13.709/2018): dados do tutor são pessoais; evitar enviar identificação a serviços externos, enviar apenas fármacos, espécie, peso e condição, sem nome do tutor/paciente. Detalhes de enquadramento não verificados.
- Licença: raspar ou redistribuir conteúdo do Plumb's viola direitos autorais; usar apenas via licença/produto oficial.

## Pontuação (honesta)

- Impacto: 2/5. ~1 h/semana, mas o ganho de segurança é qualitativo; o tempo liberado é pequeno.
- Viabilidade: 3/5. Consulta a base curada é simples; o gargalo é obter base de interações veterinária licenciável/estruturada (não verificado), não a tecnologia.
- Risco: 4/5. Falso negativo em decisão de prescrição.

## MVP sem dados reais e sem serviços pagos

**Cabe parcialmente (prototype_in_repo = true), com ressalvas.** Um script/planilha com:
1. Tabela própria de exemplo de pares de classes (ex.: AINE + corticoide, IECA + diurético, tramadol + ISRS/antidepressivos) preenchida manualmente com citação de fonte pública verificada pelo autor; os exemplos acima vêm da descrição da tarefa, não foram validados por mim.
2. Normalizador de nomes (comercial para princípio ativo) e checagem de pares.
3. Saída: lista de pares com gravidade, fonte e campo "decisão do veterinário".
Dados sintéticos apenas. Não valida cobertura clínica real; serve para testar o fluxo e o formato do parecer. Cobertura útil exigiria base licenciada (Plumb's ou equivalente), paga.
