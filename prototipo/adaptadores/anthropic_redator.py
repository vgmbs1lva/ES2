"""Redator que usa a API da Anthropic (Claude) para redigir RASCUNHOS. OPCIONAL e NAO usado por padrao.

Uso (a partir da pasta prototipo/):
    pip install anthropic
    export ANTHROPIC_API_KEY=...        # ou `ant auth login`; nunca grave a chave no codigo
    python -m fechamento rascunho --finding F-xxxxxxxx --destino tutor --saida saida/ \
        --redator adaptadores.anthropic_redator:AnthropicRedator

Garantias que NAO dependem do modelo (estao no nucleo, em fechamento/redator.py e rascunhos.py):
  * o modelo so recebe dados opacos (codigo da regra, consulta_id, mensagem da regra);
  * a saida passa pelas guardas deterministicas (dose, CPF, e-mail, telefone) antes de ser guardada;
  * o texto continua RASCUNHO ate aprovacao explicita do veterinario (comando `aprovar --confirmo`).

ATENCAO (LGPD/privacidade): usar esta classe envia texto a um servico externo. O MVP so tem dados
ficticios. Antes de qualquer uso com dados reais, e preciso avaliacao de base legal/minimizacao
(nao verificado nesta spec). Dados reais NAO devem ser usados com este MVP.

Detalhes da API conferidos na documentacao da skill claude-api (Python): `anthropic.Anthropic()` resolve a
credencial do ambiente; `client.messages.create(model=..., max_tokens=..., system=..., messages=...)`;
`output_config={"effort": ...}` controla o esforco; a resposta e uma lista de blocos em `response.content`
(usar so os de `type == "text"`); `stop_reason == "refusal"` indica recusa de seguranca (HTTP 200).
O modelo padrao abaixo e o recomendado pela skill; altere conforme custo/qualidade. Esta classe NAO foi
exercitada contra a API real neste ambiente (sem rede/credencial); os testes usam um cliente falso.
"""

import json

MODELO_PADRAO = "claude-opus-5-5"

SISTEMA = (
    "Voce redige RASCUNHOS curtos, em portugues do Brasil, de texto administrativo para um "
    "medico-veterinario revisar. Regras obrigatorias: (1) use somente os fatos do JSON recebido; "
    "(2) nao invente fatos, nomes, datas, valores ou fontes; (3) NUNCA inclua doses, diagnosticos, "
    "prognosticos, condutas clinicas, numeros com unidade (mg, ml, %, UI) nem dados pessoais; "
    "(4) onde faltar informacao que so o veterinario pode afirmar, escreva um marcador no formato "
    "'[PREENCHER: o que falta]'; (5) comece com a linha 'RASCUNHO - nao enviar sem aprovacao do "
    "medico-veterinario.'; (6) destino 'tutor' = mensagem cordial sobre divergencia administrativa de "
    "cobranca, sem termos internos; destino 'prontuario' = nota administrativa objetiva, a ser lancada "
    "manualmente pelo veterinario. Responda apenas com o texto do rascunho."
)


class AnthropicRedator:
    nome = "anthropic"

    def __init__(self, client=None, modelo=MODELO_PADRAO, max_tokens=2000, esforco="low"):
        if client is None:
            import anthropic  # importado so aqui: o nucleo nunca depende do SDK
            client = anthropic.Anthropic()
        self._client = client
        self.modelo = modelo
        self.max_tokens = max_tokens
        self.esforco = esforco
        self.nome = "anthropic:" + modelo

    def redigir(self, contexto):
        entrada = {"destino": contexto.destino, "codigo_regra": contexto.codigo,
                   "registro": contexto.consulta_id, "mensagem_da_regra": contexto.mensagem}
        resposta = self._client.messages.create(
            model=self.modelo,
            max_tokens=self.max_tokens,
            output_config={"effort": self.esforco},
            system=SISTEMA,
            messages=[{"role": "user", "content": json.dumps(entrada, ensure_ascii=False)}],
        )
        if getattr(resposta, "stop_reason", None) == "refusal":
            raise RuntimeError("o modelo recusou a requisicao (stop_reason=refusal); redija manualmente")
        if getattr(resposta, "stop_reason", None) == "max_tokens":
            raise RuntimeError("resposta truncada (max_tokens); aumente max_tokens")
        texto = "".join(b.text for b in resposta.content if getattr(b, "type", None) == "text").strip()
        if not texto:
            raise RuntimeError("resposta sem bloco de texto")
        return texto
