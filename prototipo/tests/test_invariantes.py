"""AC-19 e AC-20: sem rede/SDK no pacote; sem dado pessoal nas entradas e no relatorio."""

import ast
import re
import unittest
from pathlib import Path

from fechamento import entrada
from tests.helpers import DATA, FIXTURE, RAIZ, BaseTeste

PROIBIDOS = {"socket", "urllib", "http", "requests", "anthropic", "openai", "httpx", "ssl", "ftplib",
             "smtplib", "aiohttp"}


def importados(arquivo):
    arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
    achados = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            achados.update(a.name.split(".")[0] for a in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module and no.level == 0:
            achados.add(no.module.split(".")[0])
    return achados


class TestSemRedeNemSdk(unittest.TestCase):
    def test_ac19_nenhum_modulo_do_pacote_importa_rede_ou_sdk_de_llm(self):
        arquivos = sorted((RAIZ / "fechamento").glob("*.py"))
        self.assertGreaterEqual(len(arquivos), 8)
        for arq in arquivos:
            with self.subTest(modulo=arq.name):
                self.assertEqual(importados(arq) & PROIBIDOS, set())

    def test_adaptador_anthropic_so_importa_o_sdk_sob_demanda(self):
        arq = RAIZ / "adaptadores" / "anthropic_redator.py"
        arvore = ast.parse(arq.read_text(encoding="utf-8"))
        topo = {a.name.split(".")[0] for n in arvore.body if isinstance(n, ast.Import) for a in n.names}
        self.assertNotIn("anthropic", topo)
        self.assertIn("anthropic", importados(arq))  # mas existe, dentro de funcao


class TestPrivacidade(BaseTeste):
    PESSOAIS = ("nome", "cpf", "telefone", "fone", "email", "tutor", "endereco")

    def test_ac20_colunas_aceitas_nao_incluem_dado_pessoal(self):
        aceitas = (entrada.COLUNAS_CONSULTAS + entrada.COLUNAS_PROCEDIMENTOS + entrada.COLUNAS_ITENS
                   + entrada.COLUNAS_REGRAS + entrada.COLUNAS_CAMPOS)
        for col in aceitas:
            self.assertFalse(any(p in col.lower() for p in self.PESSOAIS), col)

    def test_ac20_fixture_so_tem_codigos_opacos_e_relatorio_sem_padroes_pessoais(self):
        for csv_ in sorted(FIXTURE.glob("*.csv")):
            cab = csv_.read_text(encoding="utf-8").splitlines()[0].lower()
            self.assertFalse(any(p in cab for p in self.PESSOAIS), csv_.name)
        self.verificar()
        texto = (self.saida / ("relatorio_%s.md" % DATA)).read_text(encoding="utf-8")
        texto += (self.saida / ("pendencias_%s.csv" % DATA)).read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto))      # CPF
        self.assertIsNone(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", texto))        # e-mail
        self.assertIsNone(re.search(r"\(?\d{2}\)?\s?9?\d{4}-\d{4}", texto))    # telefone
        self.assertIn("EXEMPLO_FICTICIO", texto)


if __name__ == "__main__":
    unittest.main()
