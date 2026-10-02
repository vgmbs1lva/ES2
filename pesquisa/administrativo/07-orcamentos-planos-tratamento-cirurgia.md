# Orçamentos e planos de tratamento/cirurgia

Domínio: administrativo. Data da análise: 2026-10-02.

## Recomendação
**Workflow determinístico (planilha/script) com redação opcional por LLM.** Não é caso para agente autônomo. O cálculo (itens x preço x quantidade, faixa mín-máx, margem de variação) deve ser código ou planilha, nunca LLM. O LLM, se usado, só redige a explicação ao tutor a partir do orçamento já calculado.

## Soluções existentes
- Digitail: PIMS com estimativas, plano de tratamento e consentimento integrados; IA gera estimativas a partir do prontuário. https://digitail.com/
- Shepherd: estimativas aprovadas vão direto ao plano de tratamento. https://www.shepherd.vet/
- Bittsi: PIMS "AI-native" com rascunho de estimativa em tempo real. https://bittsi.com/
- Brasil: SimplesVet tem módulo de orçamentos com acompanhamento de orçamentos em análise (https://simples.vet/clinica-veterinaria/); Vetsmart (https://plano.vetsmart.com.br/divulgacao); VetSoft (https://www.vetsoft.com.br/). Preços de planos: https://blog.flyvet.com.br/quanto-custa-software-gestao-clinica-veterinaria-2026/ (fonte de blog de concorrente, tratar com cautela).
- Boas práticas: estimativa com faixa baixa/alta, aviso de variação de 15 a 20% e opções alternativas (https://todaysveterinarybusiness.com/estimates-take-charge-0823/ ; https://todaysveterinarybusiness.com/craft-treatment-plan-game-plan/). Fontes de divulgação comercial, não revisadas por pares.
- Evidência: a discussão de custo é incomum nas consultas (JAVMA 2022, https://avmajournals.avma.org/view/journals/javma/260/14/javma.22.06.0268.xml). Levantamento Gallup/PetSmart Charities: custo é o principal motivo de recusa; 73% dos tutores que recusaram por custo disseram não ter recebido opção mais barata (https://news.gallup.com/poll/700115/veterinarians-say-cost-main-driver-declined-care.aspx ; https://petsmartcharities.org/press-releases/cost-of-care-continues-to-strain-veterinary-care-access-new-study-finds). Dados dos EUA, resumidos por busca; não li os estudos completos. Estudos sobre eficácia de IA gerando orçamento veterinário: não verificado.

## Valor real
O ganho está em padronizar (templates por procedimento), oferecer sempre opções (ideal/intermediária/mínima), registrar aceite/recusa e revisar após intercorrências. Isso o PIMS que a clínica já usa muitas vezes faz; verificar antes de construir algo.

## Human-in-the-loop
1. Veterinário define o plano clínico e as opções; o sistema não sugere conduta.
2. Veterinário revisa o orçamento final e a faixa de variação antes do envio.
3. Revisão pós-intercorrência: sistema calcula a diferença, veterinário decide e comunica; tutor aprova o acréscimo.
4. Registro de aceite/recusa por pessoa, com data.

## Riscos
- Legal (CDC art. 40): orçamento prévio discriminando mão de obra, materiais, condições de pagamento e datas; validade de 10 dias salvo estipulação; alteração só por livre negociação; tutor não paga acréscimos não previstos. https://www.legjur.com/legislacao/art/lei_00080781990-40 ; https://www.procon.sc.gov.br/orcamento-para-servicos-e-obrigatorio-gratuito-e-deve-conter-gastos-discriminados/ . A faixa de variação deve estar no documento e ser explicada.
- CFMV (Res. 1138/2016): consentimento formal do tutor para atos profissionais (exceto risco iminente) e critérios para honorários (art. 12). https://manual.cfmv.gov.br/arquivos/resolucao/1138.pdf . Confirmar os artigos exatos no texto; só li o resumo da busca.
- LGPD: dados de tutor (nome, contato, financeiro) são dados pessoais. Enviar a API externa de LLM exige base legal, minimização e contrato; no MVP usar apenas dados fictícios. Fonte primária da lei não consultada nesta rodada: não verificado.
- Receituário controlado: orçamento não deve prescrever nem listar controlados além de custo de item; prescrição segue regras próprias (não pesquisado: não verificado).
- Alucinação: preços e quantidades jamais gerados por LLM; vêm só da tabela. Doses e condutas não saem do sistema.
- Operacional: tabela de preços e estoque desatualizados geram orçamento errado; validar data da tabela.

## Pontuação
- Impacto: 3 (poupa tempo moderado e melhora aceite; muitas clínicas já têm módulo no PIMS)
- Viabilidade: 5 (planilha/script simples)
- Risco: 2 (baixo clínico; moderado legal/financeiro se faixa mal comunicada)

## MVP sem dados reais e sem serviços pagos
Sim. Planilha ou script Python: tabela de preços fictícia (CSV), templates de procedimento com itens e quantidades mín/máx, cálculo de faixa e variação, geração de PDF/Markdown com validade de 10 dias e campos de data, e log CSV de aceite/recusa e de revisão pós-intercorrência (delta). Redação ao tutor via LLM é opcional e fora do núcleo.
