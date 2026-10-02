# Redigir notas SOAP e fechar prontuários após as consultas

Domínio: apoio-clínico. Data da análise: 2026-10-02.

## Veredito

**Forma recomendada: workflow determinístico com um passo de LLM (rascunho), não um agente autônomo.**
Pipeline fixo: anotações/ditado -> transcrição -> template SOAP -> rascunho com marcação de lacunas -> revisão e assinatura do vet.
Para uso real, a opção mais simples é comprar/usar um scribe pronto ou o módulo do PIMS. Construir do zero só faz sentido como MVP de teste.

## 1. Soluções existentes (verificadas pela busca)

- ScribbleVet: grava a consulta ou aceita ditado e gera SOAP; extensão de navegador com transferência em 1 clique para DaySmart, ezyVet, Instinct, Pulse, Rhapsody, Shepherd e Vetspire. Planos citados: US$ 40/mês (150 notas) e US$ 150-200/mês por DVM. https://www.scribblevet.com/ ; https://www.vetsoftwarehub.com/article/veterinary-ai-scribe-pricing-comparison-2026
- Digitail (Tails AI Dictation): scribe ambiente nativo do PIMS, escreve o SOAP direto no prontuário aberto. https://digitail.com/blog/the-ultimate-guide-to-the-best-ai-scribes-for-veterinary-clinics/ (fonte do próprio fornecedor, viés comercial)
- Talkatoo: ditado/transcrição, mais do que geração estruturada; US$ 50/usuário/mês no plano SOAP. Mesma página de comparação acima.
- Outros listados: Scribenote, VetRec, HappyDoc, ScribVet. https://www.vetgeni.com/best-veterinary-ai-scribe (comparativo de terceiros, provável conflito de interesse)
- Evidência em medicina humana (análoga, não veterinária): RCT na UCLA com 238 médicos; Nabla reduziu tempo-em-nota em 9,5%, DAX sem efeito significativo; médicos relataram erros clinicamente relevantes (alucinação, omissão, adição) como ocorrência não nula. https://pmc.ncbi.nlm.nih.gov/articles/PMC12265753/ ; riscos: https://www.nature.com/articles/s41746-025-01895-6
- Estudo revisado por pares em veterinária sobre economia de tempo com scribe de IA: **não verificado** (só achei alegações de fornecedores).
- Disponibilidade dos produtos acima em português do Brasil e integração com PIMS brasileiros: **não verificado**.

Consequência para a estimativa: os "60-90 min/dia" são marketing; a evidência independente, em humanos, aponta ganho modesto (~10% do tempo em nota em um dos dois produtos). O ganho real depende de edição rápida do rascunho.

## 2. Por que workflow e não agente

- A tarefa é linear e de formato conhecido (SOAP). Não há decisão de rumo que exija autonomia.
- Um agente com ferramentas (gravar no prontuário, gerar receita) aumenta a superfície de erro. A gravação final deve ser sempre ato humano.
- Script/planilha sozinho não resolve ditado desestruturado; o LLM só entra em um passo (organizar texto em SOAP).
- Integração com PIMS: fazer só se o PIMS da clínica tiver API/plug-in; caso contrário, copiar e colar do rascunho.

Desenho mínimo:
1. Entrada: texto de anotações rápidas ou transcrição de ditado (campos opcionais: peso, TPR, resultados).
2. Pré-processamento determinístico: remover identificadores diretos do tutor (nome, CPF, telefone, endereço) antes de enviar a qualquer API externa.
3. LLM com prompt fixo: só reorganizar o que foi dito; campo ausente = "NÃO INFORMADO"; proibido inferir achados, doses ou diagnósticos.
4. Validações determinísticas: campos S/O/A/P presentes; unidades e valores numéricos do rascunho conferem com os da entrada (regex); lista de "itens do plano sem origem no ditado".
5. Saída: rascunho em modo "não assinado" + lista de lacunas; orientações ao tutor em linguagem simples também como rascunho.

## 3. Human-in-the-loop, riscos clínicos e legais

Validação obrigatória:
- O vet lê e edita todo o rascunho e só então assina/fecha. Nunca fechamento automático.
- Itens de revisão reforçada: doses, medicamentos, espécie/peso, lateralidade, diagnóstico, prognóstico.
- Receitas e orientações: rascunho apenas; prescrição é ato privativo do vet.

Riscos:
- Alucinação/omissão/adição de achados e doses (ver estudos acima). Mitigação: regra "só o que foi dito", marcação de lacunas, conferência numérica, diff ditado x nota.
- Viés de automação: vet assina sem ler. Mitigação: exigir confirmação por seção; amostragem de auditoria.
- CFMV: a Resolução CFMV 1.321/2020 define o prontuário como documento escrito, datado, sem rasuras, assinado exclusivamente pelo vet, com data, hora, local e identificação do responsável; cópia sob pedido em 5 dias úteis; guarda mínima de 5 anos segundo o resumo do texto. https://manual.cfmv.gov.br/arquivos/resolucao/1321.pdf (primária). Uma fonte secundária cita retenção de 20 anos e Resolução 1.653/2025 com ICP-Brasil; **não verificado** contra o texto primário, conferir antes de implantar. https://www.flyvet.com.br/geo/guia-completo-prontuario-veterinario-brasil-clinicas-cfmv/
- Norma do CFMV específica sobre uso de IA em prontuário: **não encontrada/não verificado**. A responsabilidade técnica permanece com o vet.
- LGPD: dados do tutor são pessoais; enviar áudio/texto a API em nuvem estrangeira é transferência internacional, regida pela Resolução CD/ANPD 19/2024 (cláusulas-padrão ou país adequado; exigível desde 23/08/2025). https://www.gov.br/anpd/pt-br/assuntos/noticias/resolucao-normatiza-transferencia-internacional-de-dados Exigir contrato de operador, não-treinamento com os dados e informar o tutor. Áudio de consulta pode conter voz/dados do tutor.
- Receituário controlado: **não automatizar a emissão** (talonário/notificação e regras de controlados; não pesquisei a norma vigente, **não verificado**). O sistema pode, no máximo, sinalizar "fármaco controlado mencionado, emitir manualmente".

## 4. Pontuação (1-5)

| Critério | Nota | Justificativa |
|---|---|---|
| Impacto | 3 | Tempo real (~1,5-2 h/dia na clínica por estimativa do usuário, incerta), mas só parte é raciocínio; ganho independente comprovado é modesto. |
| Viabilidade | 4 | Scribes prontos existem; protótipo simples é viável. Dificuldade: português clínico com ditado, integração com PIMS local. |
| Risco | 3 | Erro clínico mitigado por assinatura humana; risco LGPD e viés de automação permanecem. Sobe a 4-5 se automatizar receita ou fechar sem revisão. |

## 5. MVP sem dados reais e sem serviços pagos?

Parcialmente sim. Cabe um protótipo local com casos sintéticos escritos à mão: template SOAP, validadores determinísticos (campos, números, lacunas, sinalização de controlados), avaliação por comparação entrada x rascunho. Dá para testar o pipeline com um modelo local/open-source ou com um LLM mockado nos testes. Não valida: qualidade real do ditado em português, desempenho em consultas reais, integração com PIMS e economia de tempo, que exigem dados reais e piloto com consentimento. Piloto sugerido: 2 semanas, medir minutos por prontuário e erros achados na revisão.
