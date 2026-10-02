# Definir e revisar regras de lembretes de vacina e retorno

Domínio: atendimento-tutor. Data da análise: 2026-10-02.

## Recomendação: workflow determinístico (tabela de regras + script/planilha), sem agente

Regras de intervalo são finitas e conhecidas: espécie, vacina, idade e última dose levam a uma data de vencimento. Isso é uma tabela de regras com cálculo de datas, não raciocínio aberto. Um LLM só traria risco de alucinar intervalo ou dose. Opcional e secundário: um LLM para redigir variações de texto da mensagem, sempre a partir de modelos já aprovados.

## Soluções existentes (o que já resolve parte do problema)
- PIMS com lembretes automáticos de vacina e vermífugo, inclusive via WhatsApp: Gvet (https://g.vet/en/whatsapp-integration), Veterian (https://veterian.com/), SimplesVet (https://simples.vet/funcionalidades/mensagens-automaticas/), Digitail (https://digitail.com/), Covetrus (https://software.covetrus.com/apac/veterinary-insights/article/practice-solutions/veterinary-reminders/). Listagens: https://sourceforge.net/software/veterinary-practice-management/brazil/
- Lembretes automáticos aumentam adesão segundo blogs de fornecedores (https://simples.vet/blog/veterinaria/lembrete-vacinacao-pet/). Isso é material de marketing; a alegação de "até 34% mais vendas de vacina" vem do fornecedor. Estudo revisado por pares sobre o efeito: não verificado.
- Se a clínica já usa um PIMS com esse módulo, o trabalho real é configurar e auditar as regras, não construir ferramenta nova.

## Base técnica dos intervalos (a clínica decide o seu calendário)
- WSAVA 2024 (https://wsava.org/wp-content/uploads/2024/04/WSAVA-Vaccination-guidelines-2024.pdf; resumo https://onlinelibrary.wiley.com/doi/10.1111/jsap.13718): vacinas essenciais em filhotes a cada 2 a 4 semanas, última dose com 16 semanas ou mais; reforço aos 6 meses (26 semanas) ou depois; em adultos, reforço de CDV/CAV/CPV não mais frequente que a cada 3 anos. O intervalo trienal já é recomendação de diretriz, não o "anual" que muitos sistemas trazem por padrão.
- Antirrábica: a periodicidade e a obrigatoriedade seguem a norma local (campanhas municipais e estaduais) e a bula do produto. Não verifiquei norma brasileira vigente: não verificado. A clínica deve conferir com a vigilância sanitária local e com o MAPA/fabricante.
- Vermifugação: ESCCAP recomenda tratar adultos pelo menos 4 vezes ao ano, ou conforme avaliação de risco (https://www.esccap.org/uploads/docs/biu0jhej_0778_ESCCAP_GL1__English_2025_v21_1p.pdf). Fontes brasileiras que encontrei são comerciais ou institucionais (ex.: a cada 3 a 4 meses em adultos); não achei diretriz brasileira revisada por pares: não verificado. A frequência deve ser individualizada por risco, como a própria WSAVA e a ESCCAP indicam.
- Retornos de doença crônica: não há intervalo universal; dependem do caso (doença renal, endocrinopatias etc.) e são definidos pelo veterinário no prontuário. Não verificado como regra geral, e não deve ser automatizado por tabela única.

## Human-in-the-loop
1. Veterinário responsável (ou RT) aprova o calendário vacinal e de vermifugação uma vez, com data e versão, e revisa a cada ano ou quando mudar a bula ou a diretriz.
2. Retornos de doença crônica: o veterinário define a data no atendimento; o sistema só repete essa data.
3. Lista semanal de vencidos: conferência humana antes do disparo, excluindo pacientes com óbito, internados, em tratamento, com reação vacinal prévia, imunossuprimidos, gestantes ou com vacinação suspensa.
4. Modelos de mensagem aprovados uma vez; mensagens não são livres e não contêm dose, diagnóstico ou conduta clínica.

## Riscos
- Clínico: lembrar vacina de animal doente, gestante ou com contraindicação; intervalo errado na tabela; dados desatualizados (animal vacinado em outra clínica).
- Legal: LGPD, com base legal e consentimento/opt-out para contato por WhatsApp, e minimização de dados nas mensagens. A Resolução CFMV 1649/2025 (publicidade, em vigor desde 17/10/2025) reforça cuidado com dados de tutores e de pacientes (https://www.legisweb.com.br/legislacao/?id=479765; https://crmvsp.gov.br/novas-regras-para-publicidade-na-medicina-veterinaria-e-zootecnia-ja-estao-vigentes/). Lembrete de saúde não é publicidade, mas promoções embutidas na mensagem podem ser; conferir com o CRMV. Receituário controlado: não se aplica a vacinas e vermífugos comuns.
- Alucinação: nula em workflow determinístico; relevante só se um LLM for usado para redigir, daí a restrição a modelos aprovados.
- Operacional: spam e bloqueio de número no WhatsApp; duplicidade de envio.

## Pontuação (1-5)
- Impacto: 3. Reduz trabalho manual semanal da recepção e melhora a retenção, mas a economia é moderada e o PIMS pode já cobrir.
- Viabilidade: 5. É uma tabela mais um filtro de datas.
- Risco: 2. Baixo se houver revisão humana; sobe para 3 se houver envio automático sem conferência.

## Cabe num MVP sem dados reais e sem serviços pagos? Sim
Planilha ou script (Python/CSV) com: (a) tabela de regras por espécie, vacina e intervalo, com campo de versão e aprovador; (b) dados sintéticos de pacientes fictícios; (c) cálculo de vencidos na semana com filtros de exclusão; (d) lista para revisão manual; (e) modelos de mensagem com variáveis. Não envia nada. O disparo real depende do PIMS ou do WhatsApp (serviço pago), fora do escopo do MVP.
