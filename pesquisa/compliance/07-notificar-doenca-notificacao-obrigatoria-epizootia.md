# 07 - Notificar doença de notificação obrigatória / epizootia (raiva, leishmaniose visceral)

Domínio: compliance | Data: 2026-10-02

## Aviso de verificação (leia primeiro)
Nesta execução o WebFetch foi bloqueado pelo proxy de saída (crmvsp.gov.br, crmves.org.br, bvsms.saude.gov.br) e o limite de WebSearch da sessão estava esgotado (200/200). Portanto **nenhuma afirmação abaixo foi verificada em fonte nesta rodada**. Tudo que é factual está marcado "não verificado" e deve ser conferido antes de uso.

Fontes indicadas na tarefa (não abertas por mim, apenas citadas como ponto de partida):
- https://crmvsp.gov.br/saiba-mais-sobre-a-notificacao-obrigatoria-de-epizootias-ao-ministerio-da-saude/
- https://www.crmves.org.br/as-doencas-de-notificacao-obrigatoria-medico-veterinario-sua-notificacao-faz-a-diferenca/

Fontes primárias a conferir (URL candidata, não verificada): Portaria GM/MS nº 217/2023 (lista nacional de notificação compulsória; minha memória diz que inclui epizootias e raiva, prazos imediatos e semanais - não verificado), https://bvsms.saude.gov.br/bvs/saudelegis/gm/2023/prt0217_04_05_2023.html ; Guia de Vigilância em Saúde do MS; manuais de raiva e LV do MS; fluxo municipal/estadual (CCZ/vigilância).

## 1. Soluções existentes
Não verificado (sem busca possível). Hipóteses a pesquisar: sistemas oficiais de notificação (SINAN/e-SUS VS, formulários estaduais/municipais de epizootia), módulos de PIMS veterinários com notificação (não sei de nenhum no Brasil - não verificado). Não afirmo existência de produto algum.

## 2. Forma recomendada: workflow determinístico (checklist + gerador de rascunho), não agente autônomo
Justificativa:
- Evento raro (estimativa do usuário: média semanal diluída) -> baixo volume, ROI de automação complexa é pequeno; o valor está em **não esquecer/atrasar** e em reduzir fricção quando o caso acontece.
- Fluxo varia por município (não verificado para cada) -> regras por município devem ser tabela configurável, não "conhecimento" do LLM.
- A notificação em si é ato do profissional e envolve dados pessoais; envio automático sem revisão é inadequado.

Desenho: formulário/checklist guiado (planilha ou script) que (a) lista doenças/eventos e critérios de caso suspeito/confirmado conforme tabela mantida por humano com fonte citada; (b) pré-preenche texto de ficha e registro de prontuário a partir de campos digitados; (c) mostra o contato do CCZ/vigilância do município vindo de tabela configurável; (d) gera lembrete de prazo; (e) gera texto de orientação ao tutor a partir de modelo fixo revisado. LLM opcional apenas para redigir o resumo clínico a partir de campos, nunca para decidir se é notificável nem prazo.

## 3. Human-in-the-loop e riscos
- Veterinário decide: se o caso preenche definição de suspeito/confirmado, conteúdo da ficha, envio e conduta com o tutor (isolamento, observação, eutanásia/vacinação etc.).
- Clínico: falso negativo (não notificar) atrasa resposta de saúde pública; falso positivo gera alarme e exposição indevida do tutor/clínica. Orientação ao tutor (ex.: exposição humana na raiva) deve vir de texto oficial, não gerado livremente.
- Legal: obrigação e prazos de notificação, e eventual responsabilidade ética (CFMV) - não verificado; confirmar na portaria e no código de ética. LGPD: dados do tutor/endereço são pessoais; base legal plausível é cumprimento de obrigação legal/tutela da saúde (art. 7 e 11 da Lei 13.709/2018 - não verificado), minimizar dados, não enviar a LLM externo sem controle. Receituário controlado: não aplicável diretamente.
- Alucinação: LLM pode inventar prazo, critério ou contato do CCZ. Mitigação: regras e contatos em tabela com URL de fonte e data de revisão; saída do LLM restrita a redação.

## 4. Pontuação
- Impacto: 2/5 (evento raro; ganho pequeno em tempo, ganho maior em conformidade/prevenção de esquecimento)
- Viabilidade: 4/5 (checklist + modelos é simples; difícil é a variação municipal e integração oficial)
- Risco: 4/5 (clínico/legal se errar critério, prazo ou vazar dados; reduz a 2-3 com HITL e sem envio automático)

## 5. MVP sem dados reais e sem serviço pago
Sim, parcial: planilha/script local com tabela de doenças (preenchida com fontes após verificação), gerador de rascunho de ficha e de nota de prontuário a partir de campos fictícios, e tabela de contatos por município vazia/exemplo. Não cabe integrar ao sistema oficial nem validar fluxos municipais sem dados e acesso reais.
