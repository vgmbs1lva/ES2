# Compliance 05: Coletar e arquivar termos de consentimento (cirurgia, anestesia, eutanásia, internação)

Data da análise: 2026-10-02

## Limitação desta pesquisa (leia primeiro)
Nesta execução o orçamento de WebSearch estava esgotado (200/200) e o proxy bloqueou WebFetch para crmvsp.gov.br e planalto.gov.br. Portanto NENHUMA afirmação abaixo foi verificada nesta sessão. Tudo que é factual está marcado "não verificado" ou aponta para a única URL fornecida no enunciado, que não consegui abrir.

- Res. CFMV 1.653/2025 e a exigência de termos associada ao prontuário: citada no enunciado com https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ . Conteúdo exato (quais termos, prazo de guarda, aceitação de meio digital): não verificado. Ler o texto da resolução antes de implementar.
- Validade de assinatura eletrônica (Lei 14.063/2020; MP 2.200-2/2001): não verificado aqui. Hipótese de trabalho a confirmar: assinatura eletrônica simples/avançada costuma ser aceita entre particulares quando as partes assim admitem; exigir ICP-Brasil só se a norma específica pedir.
- LGPD (Lei 13.709/2018): dados do tutor são dados pessoais comuns; base legal provável é execução de contrato/obrigação regulatória. Não verificado.
- Soluções existentes: não pesquisadas por esgotamento do orçamento. Sabe-se de forma geral que PIMS veterinários e plataformas de assinatura eletrônica (ex.: Autentique, ClickSign, D4Sign, Gov.br assinatura) oferecem coleta de assinatura e anexação a cadastro; não verificado, sem URL. Não afirmo funcionalidades específicas de nenhum produto.

## Forma recomendada: workflow determinístico (integração simples), sem agente de IA

Justificativa:
- O texto jurídico do termo deve ser fixo, revisado pelo responsável técnico. Não há tarefa que exija raciocínio aberto: escolher modelo por procedimento, preencher campos (tutor, paciente, procedimento, data, riscos padrão), coletar assinatura, gerar PDF, gravar hash, vincular ao prontuário, lembrar pendências.
- Um LLM gerando ou "explicando" riscos ao tutor introduz risco de alucinação em documento com valor probatório. Se usado, apenas para sugerir rascunho de linguagem leiga em modelo que o veterinário aprova uma vez, nunca por paciente.
- Explicar riscos e colher o consentimento é ato humano e não deve ser automatizado.

Desenho:
1. Biblioteca de modelos versionados (cirurgia, anestesia, eutanásia, internação), aprovados pelo RT.
2. Ao abrir o procedimento/internação no PIMS, o workflow mescla campos no modelo (template com placeholders, sem IA).
3. Tutor assina (tablet na clínica ou link de assinatura eletrônica) após o veterinário explicar verbalmente.
4. Geração do PDF, SHA-256, nome padronizado, armazenamento e vínculo ao prontuário (ID do paciente + procedimento + versão do modelo).
5. Painel de pendências: procedimento agendado sem termo assinado bloqueia/avisa antes da indução anestésica.
6. Retenção conforme prazo da resolução (não verificado) e LGPD (acesso restrito, log).

## Human-in-the-loop
- Veterinário: explica riscos, escolhe o modelo, confere campos mesclados, confirma que o tutor entendeu antes da assinatura.
- RT/gestor: aprova e versiona os modelos; revisa exceções (tutor ausente, assinatura por terceiro, urgência, eutanásia).
- Conferência final: o veterinário marca o termo como "válido" no prontuário; o sistema nunca marca sozinho.

## Riscos
- Legal/CFMV: exigência exata e forma de guarda não verificadas; risco de modelo desatualizado. Mitigar com versionamento e leitura da resolução.
- Prova: assinatura eletrônica simples pode ser contestada; registrar data/hora, IP/dispositivo, identificação do tutor e hash. Nível de assinatura adequado: não verificado.
- LGPD: dados pessoais do tutor e documentos de identidade; minimizar, criptografar, controle de acesso, política de retenção.
- Receituário controlado: não faz parte deste fluxo; não misturar (termo não substitui receita nem notificação).
- Alucinação: nula se não houver LLM; se houver, restrita a rascunho revisado.
- Clínico: urgências sem tutor presente precisam de fluxo de exceção documentado, não de bloqueio rígido.

## Pontuação
- Impacto: 3 (reduz papel, extravio e retrabalho; ganho por consulta pequeno, mas valor defensivo em litígio)
- Viabilidade: 5 (template + assinatura + armazenamento são tecnologia madura)
- Risco clínico/legal: 2 (baixo se determinístico e com revisão humana; sobe para 4 se IA redigir termos)

## MVP em repositório, sem dados reais e sem serviços pagos
Cabe: sim. Escopo sugerido:
- Modelos em Markdown/HTML com placeholders; script Python (Jinja2 + biblioteca de PDF gratuita) que mescla dados fictícios e gera PDF.
- Assinatura simulada (imagem de assinatura desenhada em canvas HTML local), cálculo de SHA-256 e registro em SQLite/CSV com vínculo "prontuário" fictício.
- Verificador de pendências (procedimento sem termo) e testes automatizados.
- Fora do MVP: assinatura com validade jurídica (ICP-Brasil/gov.br), integração com PIMS real, armazenamento em nuvem.

## Fontes
- Enunciado: https://crmvsp.gov.br/nova-resolucao-do-cfmv-amplia-informacoes-obrigatorias-nos-prontuarios/ (acesso bloqueado, não lida)
- Demais: não verificado.
