# 03 - Emissão de receitas (simples, controladas, antimicrobianos) e orientações de uso

Domínio: administrativo. Data da análise: 2026-10-02.

Nota de método: WebSearch funcionou; WebFetch foi bloqueado pelo proxy de saída para quase todos os domínios (CRMV, CFMV, NCBI, Wiley, LegisWeb). Portanto, as afirmações abaixo vêm de resumos de resultados de busca, não de leitura do texto integral das normas. Onde isso importa, está marcado "conferir no texto oficial".

## Recomendação

**Forma: workflow determinístico (template + regras + calculadora de dose a partir de formulário curado pelo veterinário), com LLM opcional apenas para redigir o texto de orientação ao tutor. Não é um agente autônomo.**

Justificativa:
- A parte de maior risco (dose, tipo de receituário, campos obrigatórios) é regra e aritmética (mg/kg x peso, arredondamento por apresentação, cálculo de quantidade total = dose x frequência x dias). Isso é determinístico, auditável e testável; LLM aqui só adiciona risco de alucinação.
- O tipo de receituário (simples / notificação de receita veterinária MAPA / controle especial humano 344/98 / antimicrobiano) é uma tabela de decisão por princípio ativo, que pode ser mantida em planilha/JSON versionado.
- A emissão de controlados depende de numeração e sistema oficial (MAPA/SNCR, ver abaixo) e assinatura; isso é integração, não geração de texto.
- O LLM só se justifica na camada de linguagem: transformar a prescrição JÁ validada em instruções claras ao tutor (horários, "com alimento", sinais de alerta), sempre revisadas.

## Normas relevantes (fontes; conferir texto integral)

- Resolução CFMV 1.318/2020: prescrição é ato privativo, de responsabilidade técnica e ética do médico-veterinário; regula prescrição, guarda e uso de produtos. https://manual.cfmv.gov.br/arquivos/resolucao/1318.pdf e https://www.cfmv.gov.br/cfmv-regulamenta-assistencia-veterinaria-e-o-uso-de-produtos-em-animais/comunicacao/noticias/2020/04/08/ (resumo via busca; não li o texto).
- Notificação de Receita Veterinária: documento padronizado, emitido e numerado em sistema do MAPA, para produto veterinário registrado no MAPA sujeito a controle especial (IN MAPA 35/2017 citada em resultado de busca). Fonte secundária: https://revista.cfmv.gov.br/prescricao-de-medicamentos-veterinarios-e-um-ato/
- Portaria SVS/MS 344/98: veterinário pode prescrever controlados de uso humano apenas para uso veterinário; exige identificação do emitente com CRMV-UF e endereço; notificações A/B assinadas por profissional registrado no conselho. https://antigo.anvisa.gov.br/documents/10181/2718376/PRT_SVS_344_1998_COMP.pdf . Há alteração recente pela RDC 873/2024 (citada em busca; conteúdo não verificado).
- Antimicrobianos de uso humano prescritos para animais: RDC 471/2021 (critérios de prescrição, dispensação, retenção de receita), com assinatura eletrônica avançada ou qualificada permitida (segundo resultado de busca; conferir). Fontes: https://crfrs.org.br/noticias/ot-informa-esclareca-suas-duvidas-sobre-a-prescricao-de-antimicrobianos-e-de-medicamentos-sujeitos-a-controle-especial-por-medico-veterinario e https://portal.crmvmg.gov.br/2026/03/12/prescricao-de-medicamentos-3/
- Portaria MAPA 837/2025 (23/09/2025): aparece nos resultados ligada a ajustes de numeração via SNCR e impressão em gráfica pelo prescritor; conteúdo exato não verificado. https://www.legisweb.com.br/legislacao/?id=488965
- Guia de prescrição CRMV-MG (controlados e antimicrobianos): https://www.crmv-pr.org.br/uploads/pagina/arquivos/Guia-de-Prescricao-Veterinaria_-Medicamentos-Controlados-e-Antimicrobianos-CRMV-MG.pdf
- Manual de orientações técnicas CRMV-RJ 2026: https://www.crmvrj.org.br/wp-content/uploads/2026/07/manual_orientacoes_tecnicas_crmv_rj_2026_07_29.pdf.pdf

Importante: o quadro normativo mudou várias vezes (2025-2026) e o marco depende do tipo de produto (registrado no MAPA vs. de uso humano). Qualquer regra codificada no MVP deve citar a norma e ter data de revisão; pendência: validar com o CRMV da UF.

## Soluções existentes

- Plataformas de prescrição digital veterinária com certificado ICP-Brasil: Meu Receituário Digital (https://www.meureceituariodigital.com.br/prescricao-digital-veterinarios/), Receita Digital (https://www.bemparana.com.br/saude/receita-digital-inova-e-lanca-sua-plataforma-de-prescricao-digital-para-medicos-veterinarios/), Prescreve (https://www.prescreve.com/veterinarios), BRy (explicação do marco: https://www.bry.com.br/blog/receita-veterinaria-digital/). Preços e cobertura de controlados MAPA: não verificado.
- PIMS/ERP veterinários nacionais costumam ter módulo de receituário (ex.: Vetzco, https://blog.vetzco.com.br/receita-digital-veterinaria/). Detalhes de funcionalidades: não verificado, e são materiais de marketing.
- Modelos PDF de receituário (fonte secundária, não oficial): https://vetagora.online/modelo-receituario-veterinario-pdf/
- Evidência sobre LLM em dose/clínica veterinária: estudo de protocolos anestésicos com ChatGPT-4o/5 e Gemini 2.5 Pro relatou respostas com fármaco inadequado, dose incorreta e jejum inadequado (Okur, Vet Record, https://bvajournals.onlinelibrary.wiley.com/doi/10.1002/vetr.70741; só li o resumo da busca). Guia de uso de IA generativa em veterinária: https://arxiv.org/pdf/2403.14654. Revisão sobre IA generativa e dano por medicação em humanos: https://www.nature.com/articles/s41746-025-01565-7. Conclusão honesta: LLM sozinho não é confiável para dose; sem estudo veterinário específico sobre receituário encontrado ("não verificado").

Lacuna: não encontrei estudo comparando prescrição eletrônica com CDS vs. manual em veterinária brasileira. Não verificado.

## Human-in-the-loop

1. Veterinário escolhe o fármaco e confirma diagnóstico/peso/espécie (entrada dele, nunca inferida).
2. Sistema propõe dose a partir do formulário curado; veterinário revisa dose, via, frequência, duração e quantidade final, que aparecem lado a lado com a fonte do formulário.
3. Bloqueios duros: dose fora da faixa do formulário, espécie contraindicada, peso ausente/implausível, controlado sem dados obrigatórios, antimicrobiano sem justificativa/duração.
4. Texto ao tutor (se gerado por LLM) só é gerado a partir da prescrição aprovada e fica em rascunho até aprovação.
5. Assinatura (ICP-Brasil/avançada, conforme o tipo) e numeração oficial sempre pelo veterinário; o sistema nunca assina nem emite número de notificação por conta própria.

## Riscos

- Clínicos: erro de dose (toxicidade em gatos, raças sensíveis, pediatria/geriatria, insuficiência renal/hepática), erro de unidade (mg vs mL vs comprimido), interação medicamentosa.
- Legais: tipo de receituário errado; numeração/notificação fora do sistema oficial; retenção de via; responsabilidade é do prescritor (CFMV 1.318/2020), então a ferramenta não pode "decidir". Antimicrobianos: risco regulatório e de resistência; justificar e limitar duração.
- LGPD: dados do tutor (nome, endereço, CPF) são pessoais; minimizar, armazenar com controle de acesso, não enviar a API de LLM externa sem base legal/contrato; no MVP usar apenas dados fictícios.
- Alucinação: fármaco, dose ou norma inventados. Mitigação: LLM não calcula nem cita normas; dose sai de tabela; saída do LLM validada por esquema e checagem de que só repete campos da prescrição.
- Desatualização normativa: regras em arquivo versionado com data e fonte.

## Pontuação (1-5)

- Impacto: 3. Tarefa frequente e repetitiva, mas o ganho vem de template/CDS e já existe em plataformas; o tempo liberado por receita é pequeno, embora cumulativo.
- Viabilidade: 4 para o workflow determinístico; 2 para emissão oficial de controlados (depende de MAPA/SNCR/certificado, sem API pública verificada).
- Risco: 4 (clínico/legal alto se dose/tipo errados; mitigado por determinismo e validação humana).

## Cabe num MVP sem dados reais e sem serviços pagos? Sim, parcialmente.

MVP em repositório: script Python/planilha com (a) formulário fictício de ~10 fármacos (dose mg/kg min/max por espécie, apresentações, categoria de receituário); (b) calculadora de dose, quantidade e arredondamento; (c) regras de decisão do tipo de receituário e checagem de campos obrigatórios; (d) geração de PDF/HTML da receita e de texto ao tutor por template (sem LLM); (e) testes com casos limite (gato, peso extremo, controlado, antimicrobiano). Fora do MVP: assinatura ICP-Brasil, numeração MAPA/SNCR, integração com PIMS e qualquer LLM com dados reais.
