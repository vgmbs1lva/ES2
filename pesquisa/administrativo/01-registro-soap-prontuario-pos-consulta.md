# Registro SOAP/prontuário pós-consulta (consultas de rotina)

Data da análise: 2026-10-02. Domínio: administrativo.

## Recomendação: workflow determinístico com um passo de LLM (não agente autônomo)

Forma: **workflow** em pipeline fixo. Anotação/ditado -> transcrição -> LLM estrutura em SOAP usando só o que foi dito -> checagem determinística de campos -> revisão e assinatura do veterinário.
Não precisa de agente: o fluxo é linear e previsível. Um agente com autonomia (decidir quando gravar no prontuário, buscar histórico livremente) só amplia o risco sem ganho.

## Soluções existentes (fontes verificadas via busca; páginas de fornecedor são material comercial)

- Scribenote (voz para SOAP, integração com PIMS norte-americanos): https://scribenote.com/
- HappyDoc (escriba de IA com integração bidirecional a PIMS): https://happydoc.ai/ai-scribe
- ScribVet: https://scribvet.com/
- Comparativos (de natureza comercial/blog): https://vetclinictech.com/best-ai-soap-note-tools-veterinarians/ e https://happydoc.ai/blog/best-veterinary-ai-scribe
- Brasil: Dr. Assistente (IA veterinária para anamnese/prontuário) https://drassistente.com.br/profissoes/veterinario/ ; Laudos.AI https://www.laudos.ai/lgpd . Funcionalidades reais, preço e integração com PIMS brasileiros: **não verificado**.
- Os PIMS citados (AVImark, ezyVet, Cornerstone) são majoritariamente de mercado estrangeiro; compatibilidade com PIMS usados no Brasil: **não verificado**.
- Estudos revisados por pares sobre ganho de tempo/acurácia de escribas de IA em veterinária: **não verificado** (não encontrei na busca; as alegações de tempo economizado vêm de fornecedores).

## Fontes regulatórias (consultadas apenas por resultados de busca; leitura integral não foi possível, o acesso a crmvsp e migalhas foi bloqueado)

- Resolução CFMV 1.321/2020 (prontuário obrigatório por animal; guarda mínima de 5 anos conforme resumo da busca): https://medvep.com.br/wp-content/uploads/2021/06/1321-1.pdf
- Resolução CFMV 1.653/2025 (ampliou informações obrigatórias do prontuário): https://www.legisweb.com.br/legislacao/?id=480419 e https://crmvgo.org.br/wp-content/uploads/2025/08/1653.pdf . Lista exata de campos, vigência e exigências de assinatura: **não verificado**; ler o texto antes de definir o template.
- Resolução CFMV 1.275/2019 (estabelecimentos de pequenos animais): https://crmvmg.gov.br/ARQUIVOS/ASSTEC/1275_Clinica.pdf
- Assinatura eletrônica: a busca indica exigência de sistemas que garantam autenticidade e integridade; assinatura avançada citada para telediagnóstico. Qual nível vale para prontuário de rotina: **não verificado**.
- LGPD: dado do tutor é dado pessoal mesmo sendo o paciente um animal; IA pode estruturar, mas o conteúdo deve ser revisado pelo veterinário (https://www.flyvet.com.br/geo/melhores-praticas-conformidade-lgpd-clinica-veterinaria-brasil-2026/ , fonte de blog; a alegação de fiscalização da ANPD em clínicas veterinárias é **não verificada**).

## Human-in-the-loop

1. Veterinário revisa e edita todo o SOAP antes de assinar; sem assinatura, o registro fica como rascunho.
2. Campos numéricos (peso, TPC, FC, FR, temperatura, doses, volumes) vêm do ditado literal e aparecem destacados; o sistema não calcula nem "completa" dose.
3. Campo ausente na fala fica como "não informado", nunca preenchido por inferência.
4. Medicamentos de controle especial (receituário/notificação): o workflow apenas registra o que o veterinário declarou; não emite nem sugere receita. Regras de receituário: não verificado aqui.
5. Mantém-se o áudio/anotação original vinculado, para auditoria (retenção a definir com base na LGPD).

## Riscos

- Clínico: alucinação de achado de exame, dose ou medicação não administrada; troca de espécie/paciente; omissão de achado relevante. Mitigação: prompt restrito à fonte, saída com marcação de trecho de origem, revisão obrigatória.
- Legal CFMV: a responsabilidade pelo prontuário é do veterinário; "assinado" por automação sem revisão é inaceitável. Cumprir campos da 1.653/2025 (verificar).
- LGPD: áudio e dados do tutor enviados a API de terceiros, possivelmente com transferência internacional; exige base legal, contrato com operador, minimização e política de retenção. Para o MVP, usar apenas dados sintéticos.
- Termos de uso: não enviar dados identificáveis a serviço sem acordo adequado.

## Pontuação (1-5)

- Impacto: **4**. Tarefa diária e repetitiva, mas o ganho real depende da revisão; a economia de tempo é plausível, não demonstrada por fonte independente.
- Viabilidade: **4**. Transcrição + LLM estruturado é tecnicamente maduro; a integração com o PIMS do usuário é o ponto incerto (muitos sem API; fallback é copiar/colar).
- Risco: **3**. Moderado com revisão obrigatória; sobe para 4 sem ela.

## MVP sem dados reais e sem serviço pago

Cabe: **sim, parcialmente**. Um script que recebe texto de consulta fictícia (ditado simulado), gera SOAP em JSON conforme template, valida campos obrigatórios por regras (peso presente, unidades, campos vazios = "não informado") e produz um rascunho em Markdown com status "pendente de assinatura". Testar com casos sintéticos, incluindo armadilhas (dose ausente, espécie ambígua). A etapa de LLM exige API (custo) ou modelo local de código aberto; a transcrição pode usar Whisper local. A integração com PIMS e a assinatura digital ficam fora do MVP.
