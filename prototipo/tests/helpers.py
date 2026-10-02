"""Utilidades de teste: copia do fixture em pasta temporaria e execucao da CLI com captura."""

import contextlib
import hashlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from fechamento import cli  # noqa: E402

FIXTURE = RAIZ / "exemplos" / "dados_ficticios"
DATA = "2026-10-02"
AGORA = "2026-10-02T19:00:00"
ARQUIVOS_ENTRADA = ("consultas.csv", "procedimentos_realizados.csv", "itens_fatura.csv",
                    "regras.csv", "campos_obrigatorios.csv")


def sha(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def hashes_entrada(pasta):
    return {n: sha(Path(pasta) / n) for n in ARQUIVOS_ENTRADA}


def rodar(*args):
    """Roda a CLI em processo; devolve (codigo, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cli.main([str(a) for a in args])
    return rc, out.getvalue(), err.getvalue()


class BaseTeste(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        self.entrada = self.tmp / "entrada"
        shutil.copytree(FIXTURE, self.entrada)
        self.saida = self.tmp / "saida"

    # ---- atalhos
    def editar(self, arquivo, antigo, novo):
        p = self.entrada / arquivo
        t = p.read_text(encoding="utf-8")
        self.assertIn(antigo, t, "trecho a editar nao encontrado em %s" % arquivo)
        p.write_text(t.replace(antigo, novo, 1), encoding="utf-8")

    def verificar(self, entrada=None, saida=None):
        return rodar("verificar", "--data", DATA, "--entrada", entrada or self.entrada,
                     "--saida", saida or self.saida, "--agora", AGORA)

    def linhas_csv(self, saida=None):
        import csv
        with open(Path(saida or self.saida) / ("pendencias_%s.csv" % DATA), newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def achar(self, codigo, consulta, saida=None):
        r = [x for x in self.linhas_csv(saida) if x["codigo"].startswith(codigo) and x["consulta_id"] == consulta]
        self.assertEqual(len(r), 1, "esperava 1 %s em %s, achei %d" % (codigo, consulta, len(r)))
        return r[0]

    def decidir(self, finding, decisao, papel, motivo="", responsavel="Responsavel Ficticio"):
        return rodar("decidir", "--finding", finding, "--decisao", decisao, "--motivo", motivo,
                     "--papel", papel, "--responsavel", responsavel, "--saida", self.saida, "--agora", AGORA)

    def corrigir_dados_do_fixture(self):
        """Corrige no 'PIMS' o que so se resolve no dado (P01/P02). Sobram C01, C02, C03, C04, C05, K01."""
        self.editar("consultas.csv", "C002,2026-10-02,V01,realizado,aberto,,",
                    "C002,2026-10-02,V01,realizado,fechado,2026-10-02T18:30,")
        self.editar("consultas.csv", "C013,2026-10-02,V01,realizado,aberto,,",
                    "C013,2026-10-02,V01,realizado,fechado,2026-10-02T18:40,")
        self.editar("consultas.csv", "S,S,N,S,S\n", "S,S,S,S,S\n")                    # C003
        self.editar("consultas.csv", "S,N,N,S,S\n", "S,S,S,S,S\n")                    # C004


class RedatorDoseRuim:
    """Redator de teste que 'alucina' uma dose: as guardas devem barrar."""
    nome = "dose_ruim"

    def redigir(self, contexto):
        return "Aplicar 5 mg/kg do medicamento. [PREENCHER: assinatura]"


class RedatorLimpo:
    nome = "limpo"

    def redigir(self, contexto):
        return "RASCUNHO. Registro %s: divergencia administrativa. [PREENCHER: detalhes]" % contexto.consulta_id
