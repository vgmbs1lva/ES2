# Documentação fora do expediente (finalizar fichas, relatórios e prontuários pendentes)

Domínio: hospital-cirurgia. Data: 2026-10-02.

## Aviso sobre evidências
Nesta execução o orçamento de WebSearch estava esgotado (200/200) e WebFetch foi bloqueado pelo proxy (woovet.com, scribblevet.com, planalto.gov.br, cfmv.gov.br). **Nenhuma afirmação abaixo foi verificada com fonte nesta sessão. Tudo marcado "não verificado" deve ser conferido antes de uso.**

## 1. Soluções existentes
- Dado de ~6,2 h/semana fora do horário: citado em https://www.woovet.com/blog/how-much-time-vets-spend-on-medical-records (fornecedor; fonte primária VIN 2024 não localizada). **Não verificado.**
- Categoria "AI scribe veterinário" (ditado/gravação da consulta gera SOAP): existem produtos comerciais (por exemplo ScribbleVet, Talkatoo, entre outros), mas **não verificado** nesta sessão: funcionalidades, idioma português do Brasil, integração com PIMS brasileiros, preço e política de dados. Conferir nos sites dos fornecedores.
- PIMS brasileiros com prontuário eletrônico e modelos/atalhos de texto: existência provável, **não verificado**.
- Estudos revisados por pares sobre ganho de tempo com scribe em veterinária: **não verificado / não localizado**.

## 2. Forma recomendada: workflow determinístico + assistente de rascunho opcional (não agente autônomo)
Justificativa: o gargalo principal é a organização do trabalho (pendências espalhadas), não falta de inteligência. O mais simples que resolve:
1. **Checklist/planilha de pendências** (script): lista de prontuários abertos por paciente/data, campos obrigatórios faltantes (anamnese, exame físico, diagnóstico/suspeita, procedimento, anestesia, conduta, medicação com dose/via/frequência, retorno, assinatura).
2. **Validador de completude** determinístico (regras): aponta lacunas sem inventar conteúdo.
3. **Opcional, fase 2:** LLM que reformata anotações-rascunho em SOAP, com regra estrita de "só reorganizar o que está escrito; lacuna = [PREENCHER]".
Não recomendo agente autônomo que feche prontuário: o fechamento é ato do médico-veterinário.

## 3. Human-in-the-loop e riscos
- O veterinário revisa e fecha cada prontuário; a IA nunca assina nem fecha. Diff entre rascunho original e texto reformatado visível.
- Clínico: alucinação de dose, peso, achado de exame ou procedimento não realizado. Mitigação: não gerar valores; campos numéricos e medicamentos só copiados do original; lacunas marcadas.
- Legal (CFMV): responsabilidade técnica e conteúdo do prontuário são do veterinário; exigências de guarda/assinatura/prazo conforme resoluções do CFMV. **Não verificado** (número e texto da resolução não consultados).
- Receituário controlado: o sistema não deve gerar nem preencher receitas de controle especial (Portaria SVS/MS 344/98, **não verificado** nesta sessão); só sinalizar que há medicamento controlado sem registro.
- LGPD (Lei 13.709/2018): dados do tutor são pessoais; usar LLM em nuvem implica operador, possível transferência internacional e necessidade de minimização/anonimização. **Não verificado** artigo a artigo.
- Risco de viés de automação: revisão apressada à noite. Mitigação: destacar trechos gerados vs. originais.
- Imputação de horas extras/tempo: não somar com tarefas anteriores (já contadas).

## 4. Pontuação (honesta)
- Impacto: 3. O número de 6,2 h/semana não é verificado e parte se sobrepõe a outras tarefas; ganho real provavelmente é fração disso.
- Viabilidade: 4 para checklist/validador; 3 para rascunho com LLM integrado a PIMS (dependência de API).
- Risco: 3 (rebaixa a 2 se só validador sem LLM; sobe a 4 se IA escrever conteúdo clínico).

## 5. MVP sem dados reais e sem serviços pagos
Sim para o núcleo: script Python que lê prontuários **sintéticos** (JSON/CSV), aplica regras de completude e gera lista de pendências priorizada. Testável com casos fictícios (faltando dose, sem peso, controlado sem registro). O módulo LLM exige serviço pago ou modelo local e fica fora do MVP.
