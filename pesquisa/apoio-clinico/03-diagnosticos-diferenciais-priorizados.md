# Apoio clínico: lista de diagnósticos diferenciais priorizada

Data da análise: 2026-10-02. Tarefa: a partir de sinalmento, queixa, exame físico e exames iniciais, listar diferenciais por probabilidade e propor testes escalonados para separá-los.

Volume (estimativa própria, não verificada em fonte): ~10 min/caso x 6-10 casos/semana = 1 a 1,7 h/semana.

## Recomendação curta

**Workflow semi-determinístico com o veterinário no centro, não agente autônomo.** Entrada estruturada, base curada de "síndromes" (vômito crônico felino, PU/PD canino etc.) com diferenciais e plano escalonado baseados em consensos citados caso a caso, e um LLM opcional apenas para (a) ampliar a lista com diferenciais não previstos e (b) redigir o racional. O ranking final e o plano são sempre do veterinário.

## 1. Soluções existentes (o que foi encontrado)

Evidência científica:
- Veterinária, GPT-4 em casos clínicos: o diagnóstico principal coincidiu com o final em 39% e o diagnóstico final estava entre os diferenciais em 64% dos casos (segundo o resumo retornado pela busca; não abri o artigo completo para conferir a amostra). https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2024.1395934/full
- Veterinária, avaliação oral de cães: veterinários novatos tiveram maior consistência que todos os LLMs avaliados; os autores concluem que LLMs ainda são insuficientes para uso diagnóstico independente. https://pubmed.ncbi.nlm.nih.gov/41740881/
- Veterinária, oftalmologia felina: veterinários experientes 96,7%, ChatGPT-4.5 90%, ChatGPT-4o 83,3% (apenas resumo da busca). https://onlinelibrary.wiley.com/doi/10.1111/vop.70052
- Medicina humana (AMIE, Nature 2025): LLM otimizado teve top-10 de 59,1% contra 33,6% de clínicos sem auxílio; clínicos assistidos 51,7%. Mostra potencial, mas é medicina humana e modelo especializado. https://www.nature.com/articles/s41586-025-08869-4
- Avaliação de geradores de DDx com casos reais (humana): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9509605/

Produtos:
- Isabel DDx (humana, não veterinária; a busca não encontrou ferramenta veterinária equivalente com esse nome): https://www.isabelhealthcare.com/ . Alegações de acurácia são do próprio fornecedor.
- Digitail (Tails AI) e DeepCura (modo CDS) anunciam diferenciais a partir de sinais. Fontes são blogs/comparativos de terceiros e vendors, de baixa qualidade; **não verificado** em documentação oficial nem em estudo independente. https://www.deepcura.com/resources/best-ai-scribe-for-veterinarians , https://www.unite.ai/best-ai-veterinary-tools/
- Scribenote, VetRec, ezyVet (notas assistidas): focam em documentação, não em DDx (mesmos comparativos).
- Disponibilidade em português, preço e integração com PIMS brasileiros: **não verificado**.

Lacuna: não encontrei estudo prospectivo veterinário mostrando que DDx por IA muda desfecho ou poupa tempo. **Não verificado.**

## 2. Forma recomendada: workflow

Por que não agente: a tarefa é de uma passada (entrada, lista, plano), sem necessidade de ferramentas externas ou loops. Agente autônomo adiciona risco sem ganho.

Por que não só planilha: a planilha serve de base (a curadoria dos diferenciais por síndrome), mas não cobre casos fora do roteiro, que são justamente os "complexos".

Por que não integração agora: sem dado real e sem PIMS definido, integrar é prematuro.

Desenho:
1. Formulário estruturado (espécie, idade, raça, queixa, achados, exames já feitos), sem nome de tutor/paciente.
2. Passo determinístico: casa a queixa com a síndrome curada (YAML/planilha) e devolve diferenciais-base e plano escalonado (nível 1 barato e não invasivo, nível 2, nível 3), cada item com referência de consenso preenchida pelo próprio veterinário na curadoria.
3. Passo LLM opcional: recebe o caso e a lista-base, sugere diferenciais adicionais e justifica, em formato JSON fixo, marcando o que veio da base curada e o que veio do modelo.
4. Veterinário revisa, reordena, descarta e assina. Saída vira rascunho de texto para o prontuário.

## 3. Human-in-the-loop e riscos

Validação obrigatória: (a) o veterinário confere cada diferencial e a ordem; (b) escolhe quais testes pedir (custo, risco anestésico, condição do paciente); (c) nada entra no prontuário sem aceite explícito; (d) ferramenta nunca emite diagnóstico nem conduta ao tutor.

Riscos clínicos:
- Viés de ancoragem: lista da IA pode induzir a parar na primeira hipótese. Mitigação: mostrar a lista sem probabilidades numéricas falsamente precisas, usar faixas (provável/possível/menos provável) e incluir sempre "o que descartaria".
- Omissão de diferenciais graves, mas raros. Mitigação: seção fixa "não perder" por síndrome.
- Alucinação de estudo, dose ou ponto de corte. Mitigação: o modelo não cita literatura nem doses; referências só da base curada; qualquer número exige conferência.
- Dados de espécie errados (extrapolação de humana ou entre espécies): a evidência acima mostra desempenho variável.

Riscos legais (verificação parcial):
- CFMV: a Resolução 1.321/2020, alterada pela 1.653/2025, amplia o conteúdo obrigatório do prontuário e exige identificação do profissional responsável com CRMV. https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ . A busca **não encontrou norma do CFMV específica sobre IA**; assumo que a responsabilidade técnica permanece do médico-veterinário (Res. 1.562/2023, consolidação de responsabilidade técnica, https://manual.cfmv.gov.br/arquivos/resolucao/1562.pdf ), mas isso é inferência, **não verificado** como posição formal do CFMV sobre IA.
- LGPD: dados de tutores são dados pessoais; enviar casos a API de terceiros exige base legal, minimização e, provavelmente, contrato de operador e atenção a transferência internacional. **Não verificado** nesta pesquisa (não consultei o texto da Lei 13.709/2018); validar com assessoria jurídica.
- Receituário controlado: esta tarefa não prescreve; o plano deve ficar restrito a testes diagnósticos e não sugerir fármacos controlados (Portaria SVS/MS 344/98, não consultada: **não verificado**).

## 4. Pontuação (1-5)

| Critério | Nota | Justificativa |
|---|---|---|
| Impacto | 3 | Valor real em casos complexos e como "checklist anti-omissão", mas só ~1 a 1,7 h/semana (estimativa própria) e o ganho principal é qualidade, não tempo. |
| Viabilidade | 4 | Base curada + LLM com saída estruturada é tecnicamente simples; a dificuldade é a curadoria e a qualidade. |
| Risco (5 = pior) | 3 | Sem prescrição e com revisão obrigatória, mas há ancoragem, alucinação e questão de LGPD se usar API externa. |

## 5. MVP sem dados reais e sem serviços pagos

**Cabe.** Escopo sugerido:
- 2 síndromes: vômito crônico em gato idoso e PU/PD em cão.
- Base em YAML/planilha com diferenciais, "não perder" e plano em 3 níveis; as referências a consensos (ACVIM etc.) devem ser preenchidas e conferidas pelo veterinário com URL; sem isso o campo fica "não verificado".
- 10 a 20 casos **sintéticos** escritos à mão, sem qualquer dado de paciente/tutor.
- Script local (Python) que casa a síndrome e imprime a lista e o plano; o passo LLM fica como interface plugável (stub) para testar depois com um modelo local gratuito ou API, fora do MVP.
- Métrica de teste: o veterinário diz, para cada caso sintético, se a lista cobre o que ele listaria (cobertura) e quanto tempo economizou. Isso só valida o fluxo, não a acurácia clínica.
