"""Excecoes do dominio. Cada uma mapeia para um codigo de saida da CLI."""


class ErroEntrada(Exception):
    """Entrada invalida (arquivo, coluna, valor). Saida 2. Sempre cita arquivo e linha quando possivel."""

    def __init__(self, arquivo, linha, mensagem):
        self.arquivo = arquivo
        self.linha = linha
        self.mensagem = mensagem
        local = str(arquivo) if linha is None else "%s:L%s" % (arquivo, linha)
        super().__init__("%s: %s" % (local, mensagem))


class DecisaoRejeitada(Exception):
    """Decisao humana recusada por regra (RF-05/RF-06) ou rascunho recusado por guarda. Saida 3."""
