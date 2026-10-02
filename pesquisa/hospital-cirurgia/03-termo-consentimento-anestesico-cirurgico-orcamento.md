# Termo de consentimento anestésico-cirúrgico e estimativa de custo

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Limitação desta pesquisa (leia primeiro)
O orçamento de WebSearch da sessão estava esgotado (200/200) e o WebFetch foi bloqueado pelo proxy de saída (planalto.gov.br, cfmv.gov.br). Portanto **nenhuma afirmação abaixo foi verificada com fonte e URL**. Tudo que é factual (normas, produtos, estudos) está marcado "não verificado" e deve ser conferido antes de uso. As recomendações de arquitetura são raciocínio de engenharia, não achados de pesquisa.

## 1. Soluções existentes
- Produtos/plug-ins de PIMS com termos e assinatura digital e orçamento: não verificado (nenhum produto confirmado por URL). Hipótese a conferir: PIMS veterinários brasileiros e internacionais costumam ter modelos de termo, assinatura em tablet e estimativa. Pesquisar o PIMS usado na clínica antes de construir qualquer coisa.
- Estudos sobre consentimento informado em veterinária e compreensão do tutor: não verificado.
- Norma CFMV sobre exigência e conteúdo do termo, e sobre prontuário: não verificado; conferir a Resolução CFMV vigente e o Código de Ética (portal cfmv.gov.br).
- Base legal geral a conferir: LGPD (Lei 13.709/2018), CDC art. 40 (orçamento prévio), Marco Civil/ICP-Brasil e Lei 14.063/2020 (assinaturas eletrônicas). Todos não verificados nesta sessão.

## 2. Forma recomendada: workflow determinístico (template + planilha), sem agente
Justificativa: o conteúdo jurídico do termo deve ser fixo, revisado uma vez por responsável técnico/jurídico, e não gerado livremente por LLM. O que varia é preenchimento de campos (procedimento, espécie, jejum, risco ASA, itens do orçamento).
- Modelos de termo versionados por procedimento (castração, ortopedia, etc.), com campos de mesclagem.
- Planilha de orçamento com tabela de preços da clínica (honorários, anestesia, internação, exames, materiais) e faixa mínimo-máximo, com cláusula de que valores são estimativa.
- Geração de PDF para assinatura (tablet, ou assinatura eletrônica simples/avançada); arquivo anexado ao prontuário.
- Checklist automático: termo assinado? jejum explicado? orçamento aceito? bloqueia agendamento sem termo.
- LLM opcional e restrito: apenas reescrever a explicação ao tutor em linguagem leiga ou traduzir, a partir de texto já aprovado, com revisão do veterinário. Não é necessário no MVP.

Não automatizar: a conversa de explicação e o julgamento dos riscos individuais do paciente.

## 3. Human-in-the-loop e riscos
- Veterinário responsável valida: modelo-base (uma vez, e a cada mudança), riscos específicos do paciente (comorbidades, classe ASA), jejum, estimativa final, e conduz a explicação antes da assinatura.
- Clínico: jejum errado ou risco subestimado em texto genérico; LLM poderia omitir ou inventar riscos/doses. Mitigação: texto fixo, sem dose gerada.
- Legal: validade do termo e conteúdo exigido (CFMV: não verificado); termo não substitui informação adequada; orçamento como estimativa (CDC: não verificado); guarda do prontuário (prazo: não verificado).
- LGPD: dados do tutor (nome, CPF, contato, assinatura) são dados pessoais; manter no sistema da clínica, base legal de execução de contrato/obrigação (não verificado), não enviar a LLM externo sem anonimização e contrato.
- Receituário controlado: fora do escopo; o fluxo não deve gerar ou sugerir prescrição de controlados.
- Alucinação: eliminada por design se o termo é template fixo; só reaparece na camada LLM opcional.

## 4. Pontuação
- Impacto: 3 (economiza minutos por cirurgia e reduz esquecimentos, mas o tempo principal é a explicação, que não se automatiza).
- Viabilidade: 5 (templates, planilha e PDF com ferramentas comuns).
- Risco: 3 (consequência jurídica de termo mal redigido ou incompleto; baixo risco clínico se texto fixo).

## 5. MVP sem dados reais e sem serviços pagos
Sim. Repositório pode conter: template Markdown/HTML do termo com campos fictícios, planilha/CSV de preços fictícia, script (Python) que mescla e gera PDF/HTML, e checklist de pendências, testado com tutores e pacientes sintéticos. Assinatura digital válida e integração com PIMS ficam fora do MVP.

## Pendências de verificação
1. Resolução CFMV vigente sobre termo/prontuário e Código de Ética.
2. Produtos de PIMS que já oferecem termo e orçamento.
3. Requisitos de assinatura eletrônica aceitos e prazo de guarda.
