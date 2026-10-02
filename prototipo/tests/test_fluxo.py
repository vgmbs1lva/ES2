"""AC-06, AC-07, AC-09 a AC-17: determinismo, somente leitura, decisoes e estado do dia."""

import json
import socket
import unittest
from unittest import mock

from tests.helpers import AGORA, DATA, BaseTeste, hashes_entrada, sha

REL = "relatorio_%s.md" % DATA
CSV = "pendencias_%s.csv" % DATA


class TestDeterminismoELeitura(BaseTeste):
    def test_ac06_relatorio_e_csv_identicos_com_agora_fixo(self):
        s1, s2 = self.tmp / "s1", self.tmp / "s2"
        self.verificar(saida=s1)
        self.verificar(saida=s2)
        self.assertEqual(sha(s1 / REL), sha(s2 / REL))
        self.assertEqual(sha(s1 / CSV), sha(s2 / CSV))

    def test_ac07_entradas_intactas_apos_verificar_e_decidir(self):
        antes = hashes_entrada(self.entrada)
        self.verificar()
        self.assertEqual(hashes_entrada(self.entrada), antes)
        f = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f, "ignorar", "financeiro", "item faturado a parte, conferido")[0], 0)
        self.verificar()
        self.assertEqual(hashes_entrada(self.entrada), antes)

    def test_funciona_sem_rede(self):
        def proibido(*a, **k):
            raise AssertionError("tentativa de usar rede")
        with mock.patch.object(socket, "socket", proibido), \
                mock.patch.object(socket, "create_connection", proibido):
            self.assertEqual(self.verificar()[0], 1)


class TestEstadoDoDia(BaseTeste):
    def test_ac09_pendente_com_pendencias_sem_decisao(self):
        rc, out, _ = self.verificar()
        self.assertEqual(rc, 1)
        self.assertIn("PENDENTE", out)
        self.assertIn("**Estado do dia: PENDENTE**", (self.saida / REL).read_text(encoding="utf-8"))

    def test_ac09_conferido_quando_tudo_tratado(self):
        self.corrigir_dados_do_fixture()
        self.verificar()
        tratar = [("C01", "C006", "ignorar", "financeiro"), ("C01", "C013", "ignorar", "recepcao"),
                  ("C02", "C999", "ignorar", "financeiro"), ("C03", "C007", "ignorar", "veterinario"),
                  ("C04", "C009", "ignorar", "financeiro"), ("C05", "C010", "ignorar", "recepcao"),
                  ("K01", "C012", "conferido_manual", "veterinario")]
        for cod, cid, dec, papel in tratar:
            f = self.achar(cod, cid)["finding_id"]
            rc, _, err = self.decidir(f, dec, papel, "conferido com a escala do dia, sem erro")
            self.assertEqual(rc, 0, "%s %s: %s" % (cod, cid, err))
        rc, out, _ = self.verificar()
        self.assertEqual(rc, 0, out)
        self.assertIn("CONFERIDO", out)
        rel = (self.saida / REL).read_text(encoding="utf-8")
        self.assertIn("**Estado do dia: CONFERIDO**", rel)
        self.assertIn("## Decisões registradas", rel)
        self.assertIn("conferido com a escala do dia, sem erro", rel)
        self.assertIn("P03_FECHADO_RETROATIVO", rel)  # info continua listada e nao bloqueia

    def test_info_nao_aceita_decisao(self):
        self.verificar()
        f = self.achar("P03", "C005")["finding_id"]
        self.assertEqual(self.decidir(f, "ignorar", "veterinario", "motivo bem longo aqui")[0], 3)


class TestDecisoes(BaseTeste):
    def setUp(self):
        super().setUp()
        self.verificar()

    def log(self):
        p = self.saida / "decisoes.jsonl"
        return p.read_bytes() if p.exists() else b""

    def test_ac10_ignorar_sem_motivo_ou_motivo_curto(self):
        f = self.achar("C04", "C009")["finding_id"]
        for motivo in ("", "   ", "curto", "  a b c d e  f  ", "123456789"):
            with self.subTest(motivo=motivo):
                rc, _, err = self.decidir(f, "ignorar", "financeiro", motivo)
                self.assertEqual(rc, 3)
                self.assertIn("motivo", err)
                self.assertEqual(self.log(), b"")
        self.assertEqual(self.decidir(f, "ignorar", "financeiro", "1234567890")[0], 0)

    def test_ac11_p01_e_p02_nao_sao_ignoraveis(self):
        for cod, cid in (("P01", "C002"), ("P02", "C003"), ("P02", "C004"), ("P01", "C013")):
            with self.subTest(cod=cod, cid=cid):
                f = self.achar(cod, cid)["finding_id"]
                rc, _, err = self.decidir(f, "ignorar", "veterinario", "tentativa de ignorar com motivo longo")
                self.assertEqual(rc, 3)
                self.assertIn("nao pode ser ignorada", err)
                self.assertEqual(self.log(), b"")

    def test_p01_aceita_encaminhado_do_veterinario_mas_nao_de_outro_papel(self):
        f = self.achar("P01", "C002")["finding_id"]
        self.assertEqual(self.decidir(f, "encaminhado", "recepcao")[0], 3)
        self.assertEqual(self.decidir(f, "encaminhado", "veterinario")[0], 0)

    def test_ac12_k01(self):
        f = self.achar("K01", "C012")["finding_id"]
        motivo = "conferido contra o livro de controle do dia"
        self.assertEqual(self.decidir(f, "conferido_manual", "recepcao", motivo)[0], 3)
        self.assertEqual(self.decidir(f, "conferido_manual", "financeiro", motivo)[0], 3)
        self.assertEqual(self.decidir(f, "ignorar", "veterinario", motivo)[0], 3)
        self.assertEqual(self.decidir(f, "conferido_manual", "veterinario", "")[0], 3)
        self.assertEqual(self.log(), b"")
        self.assertEqual(self.decidir(f, "conferido_manual", "veterinario", motivo)[0], 0)
        self.verificar()
        self.assertEqual(self.achar("K01", "C012")["status"], "decidida")

    def test_conferido_manual_so_vale_para_k01(self):
        f = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f, "conferido_manual", "veterinario", "motivo suficientemente longo")[0], 3)

    def test_ac13_c03_com_ato_clinico_exige_veterinario(self):
        f = self.achar("C03", "C007")["finding_id"]
        motivo = "exame nao realizado nesta clinica, conferido"
        for papel in ("financeiro", "recepcao"):
            self.assertEqual(self.decidir(f, "ignorar", papel, motivo)[0], 3)
        self.assertEqual(self.log(), b"")
        self.assertEqual(self.decidir(f, "ignorar", "veterinario", motivo)[0], 0)

    def test_c03_sem_ato_clinico_aceita_recepcao(self):
        self.editar("regras.csv", "PROC_EXAME_LAB,ITEM_EXAME_LAB,,S,N", "PROC_EXAME_LAB,ITEM_EXAME_LAB,,N,N")
        self.verificar()
        f = self.achar("C03", "C007")["finding_id"]
        self.assertEqual(self.decidir(f, "encaminhado", "recepcao")[0], 0)

    def test_ac14_encaminhado_nao_encerra(self):
        f = self.achar("C03", "C007")["finding_id"]
        self.assertEqual(self.decidir(f, "encaminhado", "veterinario", "vou lancar no PIMS")[0], 0)
        rc, out, _ = self.verificar()
        self.assertEqual(rc, 1)
        self.assertEqual(self.achar("C03", "C007")["status"], "encaminhada")
        self.assertIn("ENCAMINHADA", (self.saida / REL).read_text(encoding="utf-8"))
        with open(self.entrada / "itens_fatura.csv", "a", encoding="utf-8") as fh:
            fh.write("C007,ITEM_EXAME_LAB,1\n")
        self.verificar()
        self.assertEqual([x for x in self.linhas_csv() if x["finding_id"] == f], [])

    def test_ac15_ignorar_c04_vira_decidida_com_motivo_responsavel_e_papel(self):
        f = self.achar("C04", "C009")["finding_id"]
        motivo = "item faturado em pacote, conferido com o financeiro"
        self.assertEqual(self.decidir(f, "ignorar", "financeiro", motivo, "Fulano Ficticio")[0], 0)
        self.verificar()
        linha = self.achar("C04", "C009")
        self.assertEqual((linha["status"], linha["decisao"], linha["papel"], linha["responsavel"]),
                         ("decidida", "ignorar", "financeiro", "Fulano Ficticio"))
        rel = (self.saida / REL).read_text(encoding="utf-8")
        self.assertIn(motivo, rel)
        self.assertIn("Fulano Ficticio", rel)
        self.assertRegex(rel, r"Abertas \| Decididas \| Ignoradas \| % ignoradas")
        self.assertIn("| C04_ITEM_SEM_PROCEDIMENTO | 1 | 0 | 1 | 1 | 100% |", rel)

    def test_ac16_decisao_presa_a_evidencia_c04(self):
        f = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f, "ignorar", "financeiro", "item faturado em pacote, conferido")[0], 0)
        self.editar("itens_fatura.csv", "C009,ITEM_C,1", "C009,ITEM_C,2")   # conteudo da pendencia muda
        self.verificar()
        nova = self.achar("C04", "C009")
        self.assertNotEqual(nova["finding_id"], f)
        self.assertEqual(nova["status"], "aberta")
        self.assertIn("não se aplicam a nenhuma pendência atual", (self.saida / REL).read_text(encoding="utf-8"))

    def test_ac16_decisao_presa_a_evidencia_c03(self):
        f = self.achar("C03", "C007")["finding_id"]
        self.assertEqual(self.decidir(f, "ignorar", "veterinario", "exame nao foi realizado, confirmado")[0], 0)
        self.editar("regras.csv", "PROC_EXAME_LAB,ITEM_EXAME_LAB,,S,N",
                    "PROC_EXAME_LAB,ITEM_EXAME_LAB,G9,S,N\nPROC_EXAME_LAB,ITEM_EXAME_LAB2,G9,S,N")
        self.verificar()
        nova = self.achar("C03", "C007")
        self.assertNotEqual(nova["finding_id"], f)
        self.assertEqual(nova["status"], "aberta")

    def test_decisao_invalida_editada_a_mao_no_log_nao_encerra_p02(self):
        f = self.achar("P02", "C003")
        reg = {"finding_id": f["finding_id"], "decisao": "ignorar", "motivo": "x" * 20, "papel": "veterinario",
               "responsavel": "Alguem Ficticio", "registrado_em": AGORA, "hash_regras": "", "codigo": f["codigo"]}
        with open(self.saida / "decisoes.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(reg) + "\n")
        self.verificar()
        self.assertEqual(self.achar("P02", "C003")["status"], "aberta")

    def test_ac17_log_append_only(self):
        f1 = self.achar("C04", "C009")["finding_id"]
        f2 = self.achar("C05", "C010")["finding_id"]
        self.assertEqual(self.decidir(f1, "ignorar", "financeiro", "item faturado em pacote, conferido")[0], 0)
        antes = self.log()
        self.assertEqual(self.decidir(f2, "encaminhado", "financeiro", "vou corrigir")[0], 0)
        self.verificar()
        depois = self.log()
        self.assertTrue(depois.startswith(antes))
        self.assertGreater(len(depois), len(antes))
        self.assertEqual(len(depois.splitlines()), 2)
        reg = json.loads(depois.splitlines()[0])
        for campo in ("finding_id", "decisao", "motivo", "papel", "responsavel", "registrado_em", "hash_regras"):
            self.assertIn(campo, reg)
        self.assertEqual(reg["hash_regras"], sha(self.entrada / "regras.csv"))

    def test_finding_desconhecido_e_erro_de_entrada(self):
        self.assertEqual(self.decidir("F-00000000", "encaminhado", "veterinario")[0], 2)

    def test_papel_invalido_e_erro_de_uso(self):
        f = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f, "encaminhado", "estagiario")[0], 2)

    def test_responsavel_em_branco(self):
        f = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f, "encaminhado", "financeiro", responsavel="  ")[0], 3)
        self.assertEqual(self.log(), b"")


if __name__ == "__main__":
    unittest.main()
