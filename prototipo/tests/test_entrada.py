"""AC-08: falha alto com arquivo e linha, sem relatorio parcial. Mais RF-12/AC-20."""

import re
import unittest

from tests.helpers import DATA, BaseTeste, rodar


class TestEntradaInvalida(BaseTeste):
    def assertErro(self, arquivo, com_linha=True):
        rc, out, err = self.verificar()
        self.assertEqual(rc, 2, err)
        self.assertIn(arquivo, err)
        if com_linha:
            self.assertRegex(err, re.escape(arquivo) + r":L\d+")
        self.assertEqual(list(self.saida.glob("relatorio_*.md")) if self.saida.exists() else [], [])
        self.assertEqual(list(self.saida.glob("pendencias_*.csv")) if self.saida.exists() else [], [])

    def test_arquivo_ausente(self):
        (self.entrada / "itens_fatura.csv").unlink()
        self.assertErro("itens_fatura.csv", com_linha=False)

    def test_coluna_faltando(self):
        self.editar("itens_fatura.csv", "consulta_id,item_codigo,quantidade", "consulta_id,item_codigo")
        self.assertErro("itens_fatura.csv")

    def test_consulta_id_duplicado(self):
        self.editar("consultas.csv", "C002,2026-10-02", "C001,2026-10-02")
        self.assertErro("consultas.csv")

    def test_valor_sn_invalido(self):
        self.editar("consultas.csv", "S,S,S,S,N\n", "S,S,X,S,N\n")
        self.assertErro("consultas.csv")

    def test_quantidade_zero(self):
        self.editar("itens_fatura.csv", "C001,ITEM_CONSULTA,1", "C001,ITEM_CONSULTA,0")
        self.assertErro("itens_fatura.csv")

    def test_quantidade_nao_inteira(self):
        self.editar("itens_fatura.csv", "C001,ITEM_CONSULTA,1", "C001,ITEM_CONSULTA,1.5")
        self.assertErro("itens_fatura.csv")

    def test_aberto_com_fechado_em(self):
        self.editar("consultas.csv", "C002,2026-10-02,V01,realizado,aberto,,",
                    "C002,2026-10-02,V01,realizado,aberto,2026-10-02T18:00,")
        self.assertErro("consultas.csv")

    def test_fechado_sem_fechado_em(self):
        self.editar("consultas.csv", "2026-10-02T17:00", "")
        self.assertErro("consultas.csv")

    def test_dominio_de_status(self):
        self.editar("consultas.csv", "C001,2026-10-02,V01,realizado", "C001,2026-10-02,V01,feito")
        self.assertErro("consultas.csv")

    def test_data_diferente_do_parametro(self):
        self.editar("consultas.csv", "C001,2026-10-02", "C001,2026-10-01")
        self.assertErro("consultas.csv")

    def test_procedimento_de_consulta_inexistente(self):
        self.editar("procedimentos_realizados.csv", "C001,PROC_CONSULTA", "C777,PROC_CONSULTA")
        self.assertErro("procedimentos_realizados.csv")

    def test_coluna_do_checklist_ausente_em_consultas(self):
        with open(self.entrada / "campos_obrigatorios.csv", "a", encoding="utf-8") as f:
            f.write("campo_inexistente,EXEMPLO_FICTICIO,EX-0.2\n")
        self.assertErro("consultas.csv")

    def test_ac20_colunas_de_dado_pessoal_sao_recusadas(self):
        for coluna in ("nome_tutor", "cpf", "telefone", "email", "nome"):
            with self.subTest(coluna=coluna):
                self.setUp()
                self.editar("itens_fatura.csv", "consulta_id,item_codigo,quantidade",
                            "consulta_id,item_codigo,quantidade,%s" % coluna)
                rc, _, err = self.verificar()
                self.assertEqual(rc, 2)
                self.assertIn("dado pessoal", err)

    def test_identificador_nao_opaco_e_recusado(self):
        self.editar("consultas.csv", "C001,2026-10-02,V01", "C001,2026-10-02,Maria Silva")
        self.assertErro("consultas.csv")

    def test_data_cli_invalida(self):
        rc, _, err = rodar("verificar", "--data", "02/10/2026", "--entrada", self.entrada, "--saida", self.saida)
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
