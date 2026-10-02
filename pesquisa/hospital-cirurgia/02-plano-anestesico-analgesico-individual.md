# Plano anestésico e analgésico individual (MPA, indução, manutenção, bloqueios, fluidos)

Domínio: hospital-cirurgia. Data da análise: 2026-10-02.

## Limitação desta pesquisa (leia primeiro)
O orçamento de WebSearch da sessão está esgotado (200/200) e o WebFetch é bloqueado pelo proxy (tentei aaha.org e europepmc.org). **Nenhuma fonte foi verificada.** Tudo que é factual abaixo está marcado "não verificado". Nenhuma dose é citada neste documento de propósito: doses devem vir de bula/formulário que a clínica escolher e conferir.

Referência apenas citada (não aberta por mim): AAHA 2020 Anesthesia and Monitoring Guidelines for Dogs and Cats: https://www.aaha.org/resources/2020-aaha-anesthesia-and-monitoring-guidelines-for-dogs-and-cats/ (conteúdo não verificado).

## 1. Soluções existentes (não verificado)
Hipóteses a confirmar numa próxima rodada:
- Calculadoras/apps de doses anestésicas veterinárias e formulários de fármacos (a buscar: "veterinary anesthesia drug calculator", Veterinary Anesthesia & Analgesia Support Group, formulários tipo Plumb's): não verificado.
- Módulos de ficha anestésica em PIMS (Simples Vet, Vetus, SoftVet no Brasil; ezyVet, Digitail, Cornerstone fora): não verificado se calculam doses.
- Estudos sobre erros de medicação/cálculo em anestesia veterinária e sobre LLMs dando doses: não verificado; buscar no PubMed.
- Planilhas internas de clínicas (mg/kg para mL) são provavelmente a solução mais comum: não verificado.

## 2. Forma recomendada: script/planilha determinístico (calculadora com formulário de fármacos curado pela clínica). Sem agente.
Justificativa:
- O núcleo é aritmético: dose (mg/kg) x peso / concentração (mg/mL) = volume; taxa de fluido (mL/kg/h) x peso. Isso é determinístico, testável e não precisa de LLM. LLM calcula errado ou inventa dose com risco real de dano.
- A escolha do protocolo (qual fármaco para qual ASA/comorbidade) é julgamento clínico. A ferramenta pode oferecer "protocolos-modelo" cadastrados e aprovados pela própria clínica, nunca gerados livremente.
- Prefira o mais simples: planilha ou script com tabela de fármacos (nome, concentração, faixa de dose mín/máx por espécie, via, observações, controlado sim/não) preenchida e referenciada pelo veterinário a partir de bula/formulário.

Componentes do MVP:
1. Tabela de fármacos editável (CSV/JSON) com fonte da faixa de dose por linha (campo obrigatório) e data da revisão.
2. Entradas: espécie, peso, ASA (informado pelo veterinário, ver tarefa 01), procedimento, estoque disponível (flag por fármaco/concentração).
3. Cálculo: volume por fármaco, volume de bloqueio, taxa de fluido, com arredondamento para seringa e unidade explícita.
4. Travas por código: alerta se dose fora da faixa cadastrada, peso fora de plausibilidade para a espécie, concentração ausente, fármaco sem estoque, combinação marcada como incompatível pela clínica.
5. Saída: plano em Markdown/PDF com fármaco, dose mg/kg, mg totais, mL, via, fonte da faixa, e campo de assinatura.
6. Camada de LLM opcional e fora do MVP: apenas redigir o texto do plano a partir dos números já calculados, sem alterar valores.

## 3. Human-in-the-loop
- O veterinário anestesista escolhe o protocolo, confirma ASA e comorbidades, revisa cada dose/volume e assina. Nada é liberado sem confirmação ativa.
- Dupla checagem na hora do preparo (seringa rotulada vs plano impresso), prática comum em segurança de medicação (não verificado).
- Ajustes por comorbidade (cardiopata, hepatopata, nefropata, filhote, geriátrico, braquicefálico, gato) são decisão do veterinário; a ferramenta no máximo exibe lembretes cadastrados.

## Riscos
- Clínico: erro de decimal ou unidade (mg vs mcg, mg/mL vs %), peso errado, concentração errada do frasco, overdose. Mitigação: unidades explícitas, faixa mín/máx, exibir conta passo a passo, reconfirmar concentração do frasco em uso, testes unitários.
- Viés de ancoragem: aceitar protocolo sugerido sem pensar. Mitigação: não pré-selecionar, mostrar fonte.
- Alucinação (se LLM entrar): doses inventadas ou espécie trocada (cão vs gato). Mitigação: LLM proibido de gerar números; só formata. Tabela de doses é a única fonte numérica.
- Tabela desatualizada ou com erro de digitação: risco persistente; exige responsável e revisão periódica.
- Legal: o ato anestésico e a prescrição são responsabilidade do médico-veterinário (CFMV; normativas específicas: não verificado). Registro com autor, versão e horário. Ferramenta não substitui o profissional nem deve ser apresentada como tal.
- Receituário controlado: opioides e cetamina etc. são controlados no Brasil (Portaria SVS/MS 344/98, não verificado nesta rodada). A ferramenta não gera receita nem controla livro de registro; apenas sinaliza "controlado" para o profissional. Integração com estoque de controlados exigiria cuidado regulatório adicional (não verificado).
- LGPD: dados de tutor e paciente identificável são dados pessoais; no MVP usar apenas dados fictícios; em produção, evitar enviar a APIs externas sem base legal (não verificado).

## 4. Pontuação (1-5, sem inflar)
- Impacto: 3. Cálculo é fonte de erro e retrabalho (afirmação do enunciado, estimativa própria, não verificada), mas um anestesista experiente já calcula rápido; o ganho é segurança e padronização, mais que tempo. Para equipe júnior, valor maior.
- Viabilidade: 5 para calculadora determinística; 2 para geração autônoma de protocolo por LLM.
- Risco: 4 (erro de dose é de dano direto). Cai para 3 com travas, faixas cadastradas e dupla checagem.
- Incerteza geral: alta (nenhuma fonte verificada).

## 5. Cabe num MVP testável sem dados reais e sem serviços pagos?
Sim. Python ou planilha com tabela de fármacos fictícia/placeholder (marcando que as faixas devem ser substituídas por valores conferidos em bula), pacientes sintéticos e testes unitários de aritmética, arredondamento, unidade e travas. Não depende de API paga nem de dados reais. A validação clínica das doses reais não cabe no MVP e deve ser feita por veterinário antes de qualquer uso.

## Próximos passos de verificação
Ler as diretrizes AAHA 2020 e documentos de segurança de medicação em anestesia; buscar estudos de erro de medicação perioperatória veterinária; checar normas CFMV sobre prontuário/responsabilidade, Portaria 344/98 e orientação MAPA para uso de controlados em veterinária; levantar calculadoras e PIMS existentes.
