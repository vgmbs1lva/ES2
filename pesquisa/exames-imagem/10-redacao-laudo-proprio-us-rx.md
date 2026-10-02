# Redação de laudo próprio de ultrassonografia/radiografia (imagem interna)

Data: 2026-10-02. Domínio: exames-imagem.

## Aviso sobre verificação de fontes
A cota de WebSearch da sessão estava esgotada (200/200) e o egress bloqueou WebFetch (vetology.ai, signalpet.com, planalto.gov.br). Nenhuma afirmação factual abaixo foi verificada com URL. Tudo o que depende de fonte está marcado "não verificado". Antes de usar este documento para decidir, refazer a pesquisa.

## 1. Soluções existentes
- Produtos de IA de leitura de radiografia veterinária (Vetology, SignalPET, Radimal e similares): existência e funcionamento exato "não verificado" (sem URL nesta sessão). Esses produtos, em geral, geram uma triagem/interpretação da imagem, que é um problema diferente de redigir o laudo a partir da interpretação do próprio veterinário.
- Módulos de laudo com modelos, medidas e imagens-chave dentro de PIMS e softwares de ultrassom/PACS (Simples Vet, SoftVet, etc.): "não verificado".
- Estudos sobre desempenho de IA em radiografia veterinária e sobre laudo estruturado: "não verificado".
- Normas: Resolução CFMV sobre responsabilidade em laudos/exames de imagem, LGPD (Lei 13.709/2018, art. 20 sobre revisão de decisões automatizadas e art. 46 sobre segurança): "não verificado" nesta sessão, conferir o texto vigente.

## 2. Forma recomendada: workflow determinístico (modelo + formulário), com LLM opcional apenas para texto
Justificativa: o ato central (interpretar a imagem e concluir) é do veterinário. O que consome tempo é a montagem: cabeçalho, identificação, técnica, achados por órgão, tabela de medidas, imagens-chave, conclusão, assinatura, PDF, entrega e arquivamento. Isso resolve com modelos por tipo de exame, campos estruturados, valores de referência pré-cadastrados (a revisar pelo clínico) e geração de PDF. Um agente que "olha a imagem e conclui" aumenta risco e não é necessário.

Camada opcional (fase 2): LLM que apenas reescreve ditado/notas do veterinário em prosa técnica padronizada e uma versão em linguagem leiga para o tutor, sem acesso à imagem e sem inventar achados.

Fluxo:
1. Veterinário escolhe o modelo (abdome, ecocardio, tórax RX, etc.).
2. Preenche achados e medidas (campos com "normal/alterado/não avaliado"; padrão é "não avaliado", nunca "normal").
3. Sistema monta o texto, calcula razões simples (ex.: relações entre medidas) e sinaliza valores fora do intervalo de referência configurado.
4. Veterinário seleciona imagens-chave, revisa o texto completo e a conclusão.
5. Assinatura (nome, CRMV; assinatura digital ICP-Brasil se a clínica adotar: "não verificado" quanto à exigência), PDF, anexo ao prontuário, envio ao tutor.

## 3. Human-in-the-loop, riscos
Validação obrigatória: o veterinário revisa e assina; nada é emitido sem ato explícito de assinatura. Todo texto gerado por IA fica marcado como rascunho até a revisão.

Riscos clínicos/alucinação:
- LLM inventando achado, medida ou lateralidade. Mitigação: sem acesso à imagem, saída limitada aos campos preenchidos, diff visível entre notas e texto final, campos não preenchidos saem como "não avaliado".
- Erro de paciente/lado/unidade de medida: exibir identificação e conferir lateralidade antes da assinatura; validar unidades.
- Valores de referência errados por espécie/raça/porte: tabela curada e revisada pelo clínico responsável, com fonte citada (não verificado aqui).
- Viés de automação: o texto "pronto" faz o profissional aceitar sem ler. Mitigação: conclusão em campo próprio escrito pelo veterinário.

Legais:
- CFMV: o laudo é ato privativo do médico-veterinário, que responde por ele; delegar a IA não transfere responsabilidade (norma exata: não verificado).
- LGPD: dados de tutor são pessoais; imagem do animal vinculada ao tutor também fica sob a mesma base. Se usar LLM em nuvem, enviar apenas texto sem identificadores (sem nome/CPF/telefone do tutor), checar contrato de processamento e transferência internacional (não verificado).
- Receituário controlado: fora do escopo do laudo; o sistema não deve sugerir prescrição.
- Guarda do prontuário/laudo e retenção: prazo e forma "não verificado".

## 4. Pontuação
- Impacto: 3. Redação e entrega são parte relevante do tempo pós-exame, mas a interpretação continua manual; ganho depende do volume da clínica.
- Viabilidade: 5 para o workflow determinístico (formulário, modelo, PDF); 3 se incluir LLM com controles.
- Risco: 2 no workflow sem IA; sobe para 3 a 4 se a IA interpretar imagem. Recomendado não fazer isso.

## 5. Cabe num MVP testável sem dados reais e sem serviços pagos?
Sim. MVP: script Python (ou planilha com modelo) que lê um JSON/YAML de achados e medidas fictícios, aplica um modelo de laudo em Markdown/HTML, valida campos obrigatórios e intervalos de referência fictícios, marca "não avaliado" por padrão e gera PDF com bloco de assinatura. Testes: campos vazios, valor fora do intervalo, lateralidade ausente, unidade inconsistente. Imagens-chave: placeholders. Sem integração com PIMS, sem LLM, sem dados reais.
