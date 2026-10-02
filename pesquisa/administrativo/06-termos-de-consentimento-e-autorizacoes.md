# Termos de consentimento (anestesia, cirurgia, internação, eutanásia) e autorizações

Domínio: administrativo | Data: 2026-10-02

## Recomendação
**Workflow determinístico (gerador de termo por template + checklist), com IA opcional só para reescrever a explicação em linguagem leve. Não é agente.**
Os termos são documentos jurídicos; o conteúdo de risco deve vir de blocos de texto pré-aprovados pelo veterinário, não gerado livremente por LLM.

## Fontes (acessadas via busca em 2026-10-02)
- Resolução CFMV 1.275/2019 (estabelecimentos para pequenos animais): define os termos de consentimento (internação/tratamento clínico ou pós-cirúrgico, procedimentos anestésicos, eutanásia, pesquisa clínica); exige prontuário físico e/ou informatizado; em recusa ou impossibilidade de obter consentimento com risco de morte/incapacidade, registrar no prontuário. https://manual.cfmv.gov.br/arquivos/resolucao/1275.pdf e https://abmes.org.br/arquivos/legislacoes/Resolucao-CFMV-1275-2019-07-25.pdf
- Aviso: não consegui abrir o texto integral (domínios bloqueados pelo proxy). Números de artigos e prazo de guarda do prontuário: **não verificado**. O resumo acima vem de snippets de busca; conferir no texto oficial.
- Artigo geral sobre termos na veterinária: https://www.jusbrasil.com.br/artigos/os-termos-de-consentimento-na-medicina-veterinaria/1345229137 (não lido na íntegra; fonte secundária).
- Lei 14.063/2020 (assinaturas eletrônicas simples/avançada/qualificada): https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14063.htm
- Assinatura digital em clínica vet (blog de fornecedor, BRy; fonte comercial): https://www.bry.com.br/blog/assinatura-clinica-veterinaria/ — afirma que assinatura simples costuma bastar para termos do tutor com identificação, prova de aceite e trilha de auditoria. Interpretação de fornecedor; **validar com jurídico**.
- Resolução CFMV 1.465/2022 (telemedicina): https://www.legisweb.com.br/legislacao/?id=433219 (relevante se o consentimento for remoto; detalhes não verificados).
- LGPD (Lei 13.709/2018): dados do tutor (CPF, endereço, telefone) são dados pessoais. Fonte secundária: https://www.flyvet.com.br/geo/melhores-praticas-conformidade-lgpd-clinica-veterinaria-brasil-2026/ (blog comercial). Texto legal primário não consultado: não verificado.
- Estudo sobre legibilidade/compreensão de termos de anestesia (humana, Espanha), sugere que compreensão depende também de fatores socioculturais, não só de leitura fácil: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11206610/ (evidência indireta, não veterinária).
- FDA CVM GFI #282, consentimento em estudos com animais de tutores, recomenda linguagem acessível (contexto de pesquisa, não clínica): https://www.fda.gov/media/172056/download

## Soluções existentes
- PIMS com prontuário eletrônico e assinatura de termos: SimplesVet (https://simples.vet/, https://simples.vet/blog/veterinaria/prontuario-veterinario/), VetSoft (https://www.vetsoft.com.br/). Funcionalidades descritas por resultados de busca; não testei os produtos.
- Modelos gratuitos de formulário (consentimento de cirurgia/anestesia): https://emitrr.com/medical-forms/anesthesia-consent-form/ , https://forms.app/en/templates/veterinary-anesthesia-consent-form (modelos genéricos, não adequados à norma brasileira sem adaptação).
- Não encontrei estudo que avalie IA gerando termos veterinários: não verificado.

## Por que workflow e não agente
- Entrada é estruturada (procedimento, espécie, ASA, tutor); saída é um documento com cláusulas fixas por tipo de procedimento.
- Alucinação em cláusula de risco tem consequência legal; template versionado e aprovado elimina isso.
- Se o PIMS da clínica já tem assinatura de termos, o melhor é usá-lo (integração zero). Só justifica construir se não tiver.

## Desenho do workflow
1. Veterinário escolhe tipo de termo e procedimento, espécie, porte, classificação ASA, riscos específicos (seleção de biblioteca de blocos).
2. Sistema monta o termo preenchendo campos (tutor, paciente, procedimento, data, responsável técnico com CRMV) a partir de blocos aprovados.
3. Checklist de campos obrigatórios; bloqueia se faltar item (ex.: contato de emergência, decisão sobre RCP/reanimação, autorização de transfusão).
4. (Opcional) Resumo em linguagem simples para a conversa, gerado por LLM sobre os blocos, sempre revisado pelo veterinário e rotulado como apoio, nunca substituindo o termo.
5. Tutor assina (papel digitalizado ou assinatura eletrônica com trilha de auditoria); PDF anexado ao prontuário com hash, data/hora.
6. Registro de recusa ou impossibilidade de consentimento em emergência.

## Human-in-the-loop
- Veterinário valida: escolha dos riscos específicos, o texto final, e conduz a explicação verbal ao tutor (consentimento é processo, não só assinatura).
- Veterinário/responsável técnico aprova a biblioteca de blocos e suas revisões.
- Assinatura sempre pelo tutor ou representante identificado; sistema nunca assina nem marca "ciente" sozinho.

## Riscos
- Clínico: termo que subestima risco específico (braquicefálico, idoso, ASA alto); explicação superficial. Mitigar com campos de risco obrigatórios vinculados ao pré-anestésico.
- Legal CFMV: termo ausente ou incompleto frente à Res. 1.275 (conteúdo mínimo e guarda: conferir no texto oficial).
- Legal assinatura: validade de assinatura simples em eventual litígio; menor/incapaz como signatário; assinatura de terceiro não identificado como tutor.
- LGPD: CPF, endereço, telefone e imagem de documento; base legal (execução de contrato/obrigação legal), minimização, controle de acesso, retenção, operador/fornecedor em nuvem, evitar enviar dados identificados a LLM externo. Detalhes da lei: não verificado em fonte primária.
- Receituário controlado: fora do escopo deste termo; não misturar com autorização de uso de controlados (portaria MAPA/ANVISA não pesquisada: não verificado).
- Alucinação: eliminada nas cláusulas por template; resta no resumo opcional, mitigada por revisão e proibição de inventar números de risco/mortalidade (não citar percentuais sem fonte).

## Pontuação (honesta)
- Impacto: 3. Poupa minutos por procedimento e reduz omissões, mas já existe em PIMS e modelos Word resolvem boa parte.
- Viabilidade: 5. Template + formulário + geração de PDF.
- Risco: 3. Baixo em tecnologia, moderado no jurídico se o conteúdo for mal adaptado.

## MVP sem dados reais e sem serviço pago
Cabe. Proposta: script Python/HTML local que lê um YAML de blocos de risco (anestesia, cirurgia, internação, eutanásia), recebe campos fictícios de paciente/tutor, valida checklist e gera PDF/Markdown com campos de assinatura e hash. Teste com casos sintéticos; sem LLM no núcleo. Fora do MVP: assinatura eletrônica com validade, integração a PIMS e armazenamento em nuvem.

## Pendências
- Ler o texto oficial da Res. 1.275/2019 (artigos, conteúdo mínimo, guarda) e normas atuais do CFMV/CRMV.
- Parecer jurídico sobre assinatura simples vs. ICP-Brasil e cláusulas.
