# Consulta a especialista / segunda opinião por mensagem

Domínio: educação/pesquisa. Data da análise: 2026-10-02.

## Tarefa
Enviar caso anonimizado (imagens, hemograma, ECG, resumo clínico) a radiologista, cardiologista, patologista ou grupo de colegas e acompanhar a resposta. Saída: parecer, ajuste de conduta, eventual encaminhamento. Tempo gasto: não verificado.

## Soluções existentes (fontes verificadas via busca)
- IDEXX Telemedicine Consultants: radiologia, cardiologia e outras especialidades; a página informa radiologistas 24/7 e laudos em até 60 min (alegação do fabricante). https://www.idexx.com/en/veterinary/diagnostic-imaging-telemedicine-consultants/telemedicine-consultants/
- DVM STAT (teleconsulta com especialistas certificados): https://www.dvmstat.com/
- Golden Hour (teleradiologia/cardiologia): https://goldenhourvet.com/
- AxisVet: https://axisvet.com/
- VVS (Virtual Veterinary Specialists), começou como segunda opinião em cardiologia: https://www.vvs.vet/
- Diretório da Veterinary Virtual Care Association: https://vvca.org/directory/
- Todos são serviços pagos, em geral dos EUA/Reino Unido. Disponibilidade, preço e atendimento em português no Brasil: não verificado. Integração com PIMS brasileiros: não verificado.
- Estudos sobre LLM para redigir/estruturar consultas a especialistas em veterinária: não verificado.

## Normas e requisitos (verificados)
- Resolução CFMV nº 1.465/2022 define a teleinterconsulta como modalidade exclusivamente entre médicos-veterinários, para troca de informações e opiniões com finalidade de auxílio diagnóstico ou terapêutico; o consultor decide se pode opinar com segurança conforme a qualidade e a quantidade das informações recebidas. Texto: https://jornal.unesp.br/wp-content/uploads/2022/08/Resolucao_TelemedicinaVeterinaria-1.pdf ; resumo CFMV: https://www.cfmv.gov.br/resolucao-do-cfmv-regulamenta-a-telemedicina-veterinaria/comunicacao/noticias/2022/06/29/
- Responsabilidade permanece com o médico-veterinário que assiste o animal presencialmente (consultor responde na medida de sua atuação); imagens e informações trocadas integram o prontuário; dados do responsável só podem ser transmitidos com consentimento livre e esclarecido e protocolos de segurança (segundo resumo secundário em https://noticias.agencia.pet/telemedicina-veterinaria/ e buscas; conferir no texto da resolução antes de usar como base formal).
- LGPD art. 12: dado anonimizado não é dado pessoal, exceto se a anonimização for reversível com meios próprios ou esforço razoável. https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm . Na prática, imagem com nome do tutor/clínica, data e microchip é reidentificável.
- DICOM PS3.15: o perfil básico de confidencialidade não limpa texto gravado nos pixels (burned-in) sem a opção "Clean Pixel Data". https://dicom.nema.org/medical/dicom/current/output/html/part15.html

## Forma recomendada: workflow determinístico simples (checklist + template + planilha de acompanhamento), com integração opcional de anonimização
Não é caso para agente autônomo. O gargalo não é raciocínio, é padronizar, desidentificar e acompanhar. Proposta:
1. Template fixo de consulta (espécie, idade em faixa, sinais, exames, pergunta objetiva, urgência).
2. Etapa de desidentificação por script: remover/limpar metadados DICOM (nomes, IDs, datas, instituição), recortar/apagar texto gravado na imagem, remover EXIF de fotos, e checar texto livre contra lista de termos (nome do tutor/paciente, telefone, CPF, clínica) com regex.
3. Planilha de acompanhamento: caso (código interno), especialista, data de envio, prazo, status, resposta, decisão do veterinário.
4. Envio manual por canal seguro (plataforma do especialista ou e-mail/mensageiro acordado). Chave de reidentificação fica só na clínica.
Um LLM é opcional e só para rascunhar o resumo clínico a partir de texto já desidentificado, ou resumir a resposta recebida; nunca para interpretar imagem/ECG nem sugerir conduta.

## Human-in-the-loop
- O veterinário revisa o pacote anonimizado antes de enviar (checagem visual de cada imagem, inclusive pixels).
- Obtém consentimento do tutor quando houver dado do responsável ou risco de reidentificação.
- Avalia o parecer do especialista com o quadro presencial e decide a conduta; registra no prontuário.
- Qualquer receita (inclusive controlada) é feita pelo veterinário assistente, nunca derivada de texto automático.

## Riscos
- Legal/LGPD/CFMV: principal risco é vazamento por anonimização falha (metadados, texto na imagem, data, localidade rara). Envio a serviço estrangeiro implica transferência internacional de dados; adequação jurídica: não verificado. Mitigar com checklist, saída revisada e contrato/termos do serviço.
- Clínico: parecer baseado em dados incompletos ou imagens de baixa qualidade; resposta mal interpretada. Mitigar com template e pergunta objetiva. Receituário controlado: não se aplica à automação.
- Alucinação: só se usar LLM; resumo pode omitir achado relevante. Mitigar usando LLM apenas para formatar, com conferência contra os dados originais; ou não usar.
- Dependência: prazo de resposta de especialista variável (não verificado para o Brasil); em urgência, não esperar.

## Pontuação (1-5)
- Impacto: 3 (poupa tempo de montagem e acompanhamento e reduz erros de anonimização; frequência real do uso: não verificado)
- Viabilidade: 4 (anonimização DICOM e templates com ferramentas livres; o envio e o especialista continuam humanos)
- Risco: 3 (dado sensível e anonimização imperfeita; cai para 2 se o script ficar local e houver checagem humana)

## MVP sem dados reais e sem serviços pagos
Sim. Script Python local (por exemplo, pydicom, que é livre) que: apaga tags identificadoras de DICOM sintéticos de teste, remove EXIF, varre texto livre sintético por padrões de identificadores e gera o template de consulta e uma linha na planilha CSV de acompanhamento. Testar com arquivos DICOM/texto fictícios. Limpeza de texto gravado na imagem exige conferência humana (o padrão DICOM não define como localizar). Não construído nesta análise.
