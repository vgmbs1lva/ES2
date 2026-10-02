# Resumir histórico do paciente antes de retorno/encaminhamento

Domínio: apoio-clinico. Data: 2026-10-02. Fontes lidas apenas em nível de resultado de busca (trechos), não integralmente; ressalvas marcadas.

## 1. Soluções existentes
Todas são comerciais, em PIMS majoritariamente estrangeiros; funcionalidades vêm de páginas dos próprios fornecedores (alegação de marketing, sem validação independente):
- Provet Clinical AI, resumo de até 10 anos de histórico: https://www.provet.com/product/clinical-ai
- Vetspire AI Patient Summary (até 3 anos, inclui PDFs enviados): https://manual.vetspire.com/vetspire-user-manual/ok/Commercial/about-ai-patient-summary
- Shepherd SummarizeAI: https://www.shepherd.vet/aitools/summarizeai/
- VetRecap (standalone): https://vetrecap.com/
- NectarVet (IA no PIMS): https://www.nectarvet.com/ai-suite
- Instinct EMR: https://instinct.vet/blog/instinct-emr-ai-features/
- Comparativo geral: https://www.signalpet.com/articles/the-top-10-veterinary-software-tools/
- Disponibilidade no Brasil, em português e integração com PIMS nacionais: não verificado.

Evidência sobre risco (medicina humana, por analogia; não encontrei estudo veterinário):
- Framework de segurança/alucinação em sumarização, npj Digital Medicine 2025: omissões 3,45% vs alucinações 1,47% das frases; alucinações mais frequentemente "maiores" (44% vs 16,7%); mais comuns na seção Plano. https://www.nature.com/articles/s41746-025-01670-7
- Outro estudo citado nos resultados (GPT-4, resumos): 42% com alucinações e 47% com omissão relevante; origem exata não verificada (ver https://arxiv.org/pdf/2407.16905).

Normas brasileiras:
- CFMV Res. 1321/2020 (prontuário é documento assinado privativamente por médico-veterinário; cópia só ao responsável ou autorizado): https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf. Li só o resumo da busca.
- LGPD (dados do tutor são dados pessoais; envio a API externa = tratamento/possível transferência internacional): não verificado nesta busca; checar texto da Lei 13.709/2018.
- Receituário controlado (Portaria SVS/MS 344/98): não verificado aqui.

## 2. Forma recomendada: workflow semi-determinístico (não agente autônomo)
Pipeline fixo: (a) extração determinística, via script, de campos estruturados do PIMS (medicações ativas, exames com data/valor, vacinas, alergias); (b) LLM apenas para condensar texto livre em um modelo fixo de resumo, com cada item citando a data/consulta de origem; (c) revisão do veterinário.
Justificativa: a parte de maior risco (lista de medicações e doses) deve vir do dado estruturado, copiada literalmente, sem passar pelo LLM. Um agente com autonomia e ferramentas não agrega valor aqui. Se o PIMS do usuário já tem esse recurso embutido (ver lista acima), usar o nativo é mais simples que construir.

## 3. Human-in-the-loop e riscos
- Validação: o veterinário responsável lê e assina o resumo antes de uso; o resumo é rascunho, nunca substitui o prontuário (que é documento privativo do MV, CFMV 1321).
- Interface: cada afirmação com link/data para o trecho de origem; campos "não encontrado" explícitos em vez de preenchimento; destaque de divergências (ex.: medicação citada no texto mas ausente da lista).
- Riscos clínicos: omissão de alergia, medicação suspensa listada como ativa, dose errada, plano inventado (a seção Plano foi a mais alucinada no estudo acima). Mitigação: doses só por cópia literal; resumo sem recomendações de conduta.
- Legais: LGPD (minimização, anonimizar tutor, contrato/localização do provedor de LLM; não verificado); sigilo (CFMV 1321); receituário controlado: não resumir/regerar dados de notificação/receita, apenas referenciar.
- Viés de automação: revisão superficial é o risco real; amostrar auditoria periódica contra o prontuário.

## 4. Pontuação
- Impacto 3: ~5 min x 15-20 casos/semana = ~1,3-1,7 h/semana (estimativa do usuário, incerteza ±50%); a âncora de 30-40% do tempo em documentação não é verificada em fonte primária. Ganho real é reduzido pelo tempo de revisão.
- Viabilidade 4: LLMs resumem bem texto; integração com o PIMS real é o gargalo.
- Risco 3: baixo se com revisão e dados estruturados copiados; omissões silenciosas e LGPD pesam.

## 5. MVP sem dados reais e sem serviço pago?
Sim, em parte. Cabe um protótipo no repositório: dados sintéticos (JSON de prontuário fictício), script que extrai medicações/exames/pendências de forma determinística, gera o modelo de resumo e checa que cada item tem origem citada; etapa LLM pode ser simulada ou usar modelo local gratuito (qualidade não verificada). Avaliar com casos sintéticos com erros plantados (alergia omitida, medicação suspensa). Não valida desempenho em prontuários reais.
