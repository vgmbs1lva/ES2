# Lançamento/padronização de resultados no prontuário (domínio: exames-imagem)

Data: 2026-10-02

## Aviso de verificação

Nesta execução o WebSearch estava com a cota esgotada (200/200) e o WebFetch foi bloqueado pelo proxy de saída (idexx.com, loinc.org, planalto.gov.br). Não consegui abrir nenhuma fonte. Por isso, nenhuma afirmação factual abaixo tem URL e todas estão marcadas como "não verificado". Antes de decidir qualquer coisa, vale conferir os itens da seção "Pendências de verificação".

## 1. Soluções existentes (todas: não verificado)

- Portais de laboratórios de referência com exportação (por exemplo VetConnect PLUS da IDEXX, portais da Antech/Synlab): não verificado se oferecem integração com PIMS no Brasil nem quais PIMS brasileiros são compatíveis. Âncora da tarefa diz que a lacuna de integração existe (fonte vendor, baixa confiança).
- Padrões de terminologia: LOINC (códigos de analito) e UCUM (unidades) são os padrões usuais em medicina humana; não verificado o uso/cobertura em veterinária. VeNom e SNOMED CT Veterinary Extension existem como terminologias veterinárias, não verificado o escopo para exames laboratoriais.
- Extração de PDF por LLM/OCR: não verificado estudo de acurácia para laudos veterinários. Não afirmo números.
- Plug-ins de PIMS brasileiros (Simples Vet, SoftVet, Vetsoft etc.): não verificado se algum faz importação automática de PDF de laudos.

## 2. Forma recomendada: workflow determinístico com extração assistida (script), sem agente autônomo

Recomendação: **workflow** (script + tabela de mapeamento), com LLM opcional apenas para ler PDFs fora do padrão, sempre com conferência humana.

Justificativa:
- O problema central é de regras fixas: mapear nome do analito de cada laboratório para um nome canônico, converter unidades (ex.: creatinina mg/dL para umol/L, fator 88,4; glicose mg/dL para mmol/L, fator 0,0555 — fatores a conferir), guardar o intervalo de referência do laboratório junto ao resultado e nomear arquivos. Isso é tabela + função, não raciocínio aberto.
- Agente autônomo não se justifica: o ganho extra do LLM é só ler layouts inconsistentes, e é exatamente onde há risco de alucinação numérica.
- Princípio clínico chave: não "normalizar" o intervalo de referência para um único; manter o valor original, a unidade original e o intervalo do laboratório de origem, e acrescentar o valor convertido como campo adicional. Comparar com histórico exige mesma unidade, mas a interpretação (alto/baixo) deve usar o intervalo do laboratório que gerou o resultado, pois métodos e analisadores diferem (afirmação de bom senso técnico, não verificada com fonte).
- Observação de escopo: o domínio é "exames-imagem", mas a tarefa trata de resultados laboratoriais em PDF. Laudos de imagem (texto livre do radiologista) não têm valores numéricos a converter; para eles só cabe a nomeação uniforme e anexação, não extração. Isso reduz a utilidade da automação neste domínio.

## 3. Human-in-the-loop, riscos

Validação do veterinário:
1. Tela de conferência lado a lado: imagem do PDF original e valores extraídos; o veterinário confirma ou corrige cada linha antes de gravar.
2. Campos fora de faixa plausível ou com unidade desconhecida ficam bloqueados até decisão humana (nunca preencher por inferência).
3. Os valores só entram no prontuário após aceite explícito; o PDF original sempre anexado como documento-fonte.

Riscos clínicos:
- Troca ou arredondamento de unidade (ordem de grandeza) gerando conduta errada; alucinação de número se usar LLM; associação do resultado ao paciente errado (mitigar com conferência de identificador/ data da coleta no laudo); perda do intervalo de referência original.
- Receituário controlado: não é afetado diretamente por este fluxo; não deve haver geração de prescrição. Não verificado nenhum requisito específico.

Riscos legais:
- CFMV: o prontuário é responsabilidade do médico-veterinário; a norma específica sobre prontuário e guarda (número da resolução, prazos, exigências de assinatura/ integridade para registros digitais) não foi verificada. Conferir no site do CFMV antes de adotar.
- LGPD (Lei 13.709/2018): dados do tutor são dados pessoais; enviar PDFs com nome/CPF/endereço do tutor a uma API de LLM externa seria transferência a operador/ possível transferência internacional. Não verificado em fonte nesta execução. Mitigação: processamento local, ou remoção de campos identificadores antes de qualquer envio, e contrato com o operador.
- Alteração do registro: manter log de quem validou e quando, sem sobrescrever o original.

## 4. Pontuação (honesta)

- Impacto: 3/5. Economiza digitação repetitiva e padroniza histórico, mas o ganho depende de volume de laudos em PDF; para imagem quase nulo.
- Viabilidade: 4/5. Tabelas de mapeamento e conversão são simples; a parte frágil é parsing de PDFs de layouts variados e a integração com o PIMS específico (não verificado).
- Risco: 3/5. Erro numérico silencioso é perigoso, mas o controle humano e a manutenção do original reduzem muito.

## 5. MVP sem dados reais e sem serviço pago: sim

Cabe no repositório:
- Arquivo `mapeamento.csv` (analito por laboratório, nome canônico, unidade canônica, fator de conversão).
- Script (Python) que lê laudos sintéticos em CSV/JSON (ou PDFs gerados artificialmente com texto selecionável) e produz tabela padronizada com: valor original, unidade original, intervalo de referência original, valor convertido, flag de revisão.
- Nomeação de arquivo: `AAAA-MM-DD_<idPaciente>_<tipoExame>_<laboratorio>.pdf` (id fictício).
- Testes com casos de unidade ambígua e analito não mapeado (devem ir para revisão).
- Fora do MVP: OCR de papel e integração real com PIMS.

## Pendências de verificação

1. Normas CFMV vigentes sobre prontuário/guarda e documentos eletrônicos (cfmv.gov.br).
2. Texto da LGPD (planalto.gov.br) e orientação da ANPD sobre operadores e transferência internacional.
3. Fatores de conversão de unidades por analito (fonte: literatura clínica ou laboratório).
4. Integrações reais dos laboratórios e PIMS usados no Brasil.
5. Estudos de acurácia de extração de laudos por LLM/OCR.
