# Redação de relato de caso ou resumo de congresso

Domínio: educação/pesquisa. Data da análise: 2026-10-02.

## Resumo da recomendação

**Forma recomendada: workflow determinístico (checklist + scripts), com LLM apenas como assistente opcional de rascunho/revisão, sempre sob o veterinário.** Não recomendo um agente autônomo que redija o manuscrito a partir do prontuário.

Motivo: o trabalho é esporádico (poucos meses/ano; frequência "não verificado"), o gargalo real é organizacional (consentimento, desidentificação, aderência à checklist e às normas da revista, referências corretas) e o risco de alucinação de referências é bem documentado. Um script/planilha cobre a parte mecânica; a redação científica e a interpretação clínica são do autor.

## Soluções existentes (fontes)

- Diretrizes de relato: CARE (https://www.care-statement.org/checklist), com SCARE 2020 como adaptação cirúrgica (https://www.equator-network.org/reporting-guidelines/the-scare-statement-consensus-based-surgical-case-report-guidelines/). Não encontrei, na busca, extensão veterinária específica da CARE: não verificado. Servem de base para a checklist.
- Políticas de revistas veterinárias exigem consentimento do tutor: JAVMA (https://avmajournals.avma.org/page/41), Veterinary Record Case Reports, que pede formulário de consentimento por participante identificável (https://bvajournals.onlinelibrary.wiley.com/hub/journal/20526121/author-guidelines), e Irish Veterinary Journal, que exige consentimento para publicação em relatos de caso (https://irishvetjournal.biomedcentral.com/submission-guidelines/preparing-your-manuscript/case-report). Cada revista tem texto próprio: o fluxo deve ler as normas da revista-alvo.
- IA na redação: ICMJE exige declarar o uso de IA, proíbe listar IA como autora e responsabiliza os autores humanos pelo conteúdo (https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html).
- Alucinação de referências: estudo relatou 41 de 59 referências geradas pelo ChatGPT como fabricadas (descrito em https://www.explorationpub.com/Journals/em/Article/1001385; ver também https://www.sciencedirect.com/science/article/abs/pii/S0165178123002846). Auditoria entre modelos: https://arxiv.org/pdf/2603.03299 (preprint, não revisado por pares).
- Verificação de referências: API REST aberta do Crossref, sem cadastro (https://www.crossref.org/documentation/retrieve-metadata/rest-api/). Cobre só o que tem DOI no Crossref; periódicos sem DOI exigem conferência manual.
- Plug-ins de PIMS que gerem relato de caso: não encontrei nenhum. Não verificado.

## Normas e riscos legais

- Sigilo/ética: o Código de Ética do Médico-Veterinário veda referência a casos clínicos identificáveis em divulgação e acesso a prontuário sem autorização ou obrigação legal (https://www.crmv-pr.org.br/uploads/documentos/codeticacfmv.pdf; resumo via busca, conferir o artigo exato antes de citar). Prontuário: guarda mínima de 5 anos, Res. CFMV 1.275/2019 (https://crmvmg.gov.br/ARQUIVOS/ASSTEC/1275_Clinica.pdf).
- LGPD: dados do tutor (nome, contato, endereço, às vezes imagem) são dados pessoais; dado anonimizado só sai do escopo se a reversão não for razoavelmente possível (art. 5 e 12, https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). Enviar prontuário com identificadores a LLM em nuvem é tratamento/transferência de dados do tutor: exige desidentificação prévia e, se houver processador externo, base legal e contrato. Interpretação jurídica final: consultar profissional de direito, não verificado por mim.
- Receituário controlado: relato pode citar fármacos controlados; não incluir número de receita/notificação nem dados do prescritor/tutor. Doses citadas devem ser conferidas na bula/fonte primária (MAPA/literatura), nunca vir só do LLM.
- Consentimento: AVMA usa o termo "owner consent" e recomenda documentar o consentimento (https://www.avma.org/javma-news/2007-05-15/avma-adopts-policy-informed-consent). Termo deve cobrir publicação, imagens e apresentação em congresso.

## Fluxo proposto (workflow)

1. Cadastro do caso (planilha): ID interno, revista/evento alvo, prazo, status do consentimento (anexo arquivado), checklist CARE.
2. Termo de consentimento: modelo em texto (revisado pelo veterinário/jurídico) + campo de data/arquivo. Bloqueia as etapas seguintes sem consentimento.
3. Desidentificação (script): sinaliza nomes, telefones, CPF, e-mails, endereços, datas exatas, nome de clínica/tutor por regex e lista de termos informados; o humano revisa e aprova.
4. Esqueleto CARE preenchido pelo veterinário (linha do tempo, achados, diagnóstico, tratamento, desfecho). LLM opcional só para ajustar linguagem e adequar ao limite de palavras, apenas sobre texto já desidentificado.
5. Referências: veterinário escolhe as fontes (PubMed/Scholar); script confere DOI no Crossref (título, ano, autores) e marca divergências. Nenhuma referência gerada por LLM entra sem verificação.
6. Formatação: checklist das normas da revista (limite de palavras, seções, figuras) e verificação de contagem; submissão manual.
7. Declaração de uso de IA (se usada) na carta e no manuscrito, conforme ICMJE.

## Human-in-the-loop

O veterinário valida: escolha do caso e relevância; consentimento assinado; desidentificação final (inclusive imagens e metadados de exames); todos os fatos clínicos contra o prontuário; cada referência e dose; conclusões/discussão; declaração de IA; submissão. O LLM nunca decide, nunca cita sem fonte verificada.

## Riscos

- Alucinação de referências e de dados clínicos (alto sem verificação; mitigado por conferência Crossref e revisão ponto a ponto).
- Vazamento de dados do tutor/paciente via ferramenta externa (LGPD, sigilo CFMV).
- Má-conduta por não declarar IA ou plágio (ICMJE).
- Consentimento insuficiente para imagens/congresso.
- Falsa sensação de segurança de regex: desidentificação automática não é garantia.

## Pontuação (1-5)

- Impacto: **2**. Tarefa pouco frequente; o ganho é de horas por caso (formatação, referências, checklist), não da redação em si. Estimativa de tempo não verificada.
- Viabilidade técnica: **4** para checklist/desidentificação/verificação de DOI; 2 para redação autônoma confiável.
- Risco clínico/legal: **3** para o workflow proposto (4 se um agente receber prontuário real em nuvem).

## MVP testável sem dados reais e sem serviços pagos?

**Sim.** Cabe num repositório: script Python (stdlib + requests) que (a) lê um caso sintético em texto/JSON, (b) sinaliza identificadores por regex, (c) valida estrutura contra a checklist CARE e contagem de palavras de uma norma fictícia, (d) consulta a API gratuita do Crossref para conferir referências (requer acesso à internet; testes podem usar respostas gravadas). Modelo de termo de consentimento e planilha de acompanhamento como arquivos de texto/CSV. Sem LLM no MVP.
