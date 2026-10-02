"""AC-01 a AC-05: regras deterministicas no fixture."""

import re
import unittest

from fechamento.entrada import carregar
from fechamento.regras import aplicar_regras
from tests.helpers import DATA, FIXTURE, BaseTeste

ESPERADO = {
    ("P01_PRONTUARIO_ABERTO", "C002"), ("P02_PRONTUARIO_INCOMPLETO", "C003"),
    ("P02_PRONTUARIO_INCOMPLETO", "C004"), ("P03_FECHADO_RETROATIVO", "C005"),
    ("C01_CONSULTA_SEM_FATURA", "C006"), ("C03_PROCEDIMENTO_SEM_ITEM", "C007"),
    ("C04_ITEM_SEM_PROCEDIMENTO", "C009"), ("C05_CANCELADA_COM_ITENS", "C010"),
    ("K01_CONTROLADO_CONFERIR", "C012"), ("P01_PRONTUARIO_ABERTO", "C013"),
    ("C01_CONSULTA_SEM_FATURA", "C013"), ("C02_FATURA_SEM_CONSULTA", "C999"),
}


class TestRegras(unittest.TestCase):
    def setUp(self):
        self.dados = carregar(FIXTURE, DATA)
        self.pend = aplicar_regras(self.dados)

    def test_ac01_conjunto_exato(self):
        obtido = {(p.codigo, p.consulta_id) for p in self.pend}
        self.assertEqual(obtido, ESPERADO)
        self.assertEqual(len(self.pend), len(ESPERADO), "pendencia duplicada")

    def test_ac02_sem_falso_positivo(self):
        for cid in ("C001", "C008", "C011"):
            self.assertEqual([p for p in self.pend if p.consulta_id == cid], [], cid)

    def test_ac03_c013_gera_p01_e_c01_separados(self):
        cods = sorted(p.codigo for p in self.pend if p.consulta_id == "C013")
        self.assertEqual(cods, ["C01_CONSULTA_SEM_FATURA", "P01_PRONTUARIO_ABERTO"])
        ids = {p.finding_id for p in self.pend if p.consulta_id == "C013"}
        self.assertEqual(len(ids), 2)

    def test_ac04_p02_lista_todos_os_campos(self):
        c004 = next(p for p in self.pend if p.codigo.startswith("P02") and p.consulta_id == "C004")
        self.assertIn("conduta", c004.mensagem)
        self.assertIn("exame_fisico", c004.mensagem)
        c003 = next(p for p in self.pend if p.codigo.startswith("P02") and p.consulta_id == "C003")
        self.assertIn("conduta", c003.mensagem)
        self.assertNotIn("exame_fisico", c003.mensagem)

    def test_ac05_evidencia_cita_arquivo_e_linha_com_o_consulta_id(self):
        for p in self.pend:
            self.assertTrue(p.evidencia, p.codigo)
            for parte in p.evidencia.split("; "):
                m = re.fullmatch(r"([a-z_]+\.csv):L(\d+)", parte)
                self.assertIsNotNone(m, parte)
                linhas = (FIXTURE / m.group(1)).read_text(encoding="utf-8").splitlines()
                self.assertIn(p.consulta_id, linhas[int(m.group(2)) - 1].split(","),
                              "%s %s: linha citada nao contem o consulta_id" % (p.codigo, parte))

    def test_severidades_e_papeis(self):
        por = {(p.codigo, p.consulta_id): p for p in self.pend}
        self.assertEqual(por[("P03_FECHADO_RETROATIVO", "C005")].severidade, "info")
        self.assertEqual(por[("C03_PROCEDIMENTO_SEM_ITEM", "C007")].severidade, "atencao")
        self.assertTrue(por[("C03_PROCEDIMENTO_SEM_ITEM", "C007")].exige_veterinario)   # ato_clinico=S
        self.assertFalse(por[("C04_ITEM_SEM_PROCEDIMENTO", "C009")].exige_veterinario)
        self.assertIn("possivel item nao cobrado", por[("C03_PROCEDIMENTO_SEM_ITEM", "C007")].mensagem.lower())
        self.assertIn("possivel cobranca indevida", por[("C04_ITEM_SEM_PROCEDIMENTO", "C009")].mensagem.lower())

    def test_finding_id_estavel_entre_execucoes(self):
        outra = aplicar_regras(carregar(FIXTURE, DATA))
        self.assertEqual([p.finding_id for p in self.pend], [p.finding_id for p in outra])


class TestRegrasConfiguraveis(BaseTeste):
    def test_ac18_checklist_do_arquivo_muda_p02_sem_mudar_codigo(self):
        self.assertEqual(self.verificar()[0], 1)
        antes = self.linhas_csv()
        self.assertFalse([x for x in antes if x["consulta_id"] == "C001"])
        rel_antes = (self.saida / ("relatorio_%s.md" % DATA)).read_text(encoding="utf-8")
        with open(self.entrada / "campos_obrigatorios.csv", "a", encoding="utf-8") as f:
            f.write("observacoes_extra,EXEMPLO_FICTICIO,EX-0.2\n")
        self.assertEqual(self.verificar()[0], 1)
        c001 = [x for x in self.linhas_csv() if x["consulta_id"] == "C001"]
        self.assertEqual([x["codigo"] for x in c001], ["P02_PRONTUARIO_INCOMPLETO"])
        self.assertIn("observacoes_extra", c001[0]["mensagem"])
        rel_depois = (self.saida / ("relatorio_%s.md" % DATA)).read_text(encoding="utf-8")
        self.assertNotEqual(rel_antes, rel_depois)
        self.assertIn("EX-0.2", rel_depois)
        import hashlib
        novo_hash = hashlib.sha256((self.entrada / "campos_obrigatorios.csv").read_bytes()).hexdigest()
        self.assertIn(novo_hash, rel_depois)

    def test_regras_do_arquivo_mudam_c03(self):
        # alternativas no mesmo grupo: com ITEM_EXAME_LAB2 em G, C007 continua pendente mas o conteudo muda
        antes = self.achar_c03()
        self.editar("regras.csv", "PROC_EXAME_LAB,ITEM_EXAME_LAB,,S,N",
                    "PROC_EXAME_LAB,ITEM_EXAME_LAB,G9,S,N\nPROC_EXAME_LAB,ITEM_EXAME_LAB2,G9,S,N")
        depois = self.achar_c03()
        self.assertNotEqual(antes, depois)

    def achar_c03(self):
        self.verificar()
        return self.achar("C03", "C007")["finding_id"]


if __name__ == "__main__":
    unittest.main()
