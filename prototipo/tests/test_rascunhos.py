"""Etapa de redacao (stub offline), guardas e PORTAO DE APROVACAO do veterinario."""

import json
import unittest

from fechamento import rascunhos
from fechamento.erros import DecisaoRejeitada
from fechamento.redator import (ContextoRascunho, RedatorStub, obter_redator,
                                redigir_com_guardas, verificar_texto)
from tests.helpers import AGORA, BaseTeste, rodar


class TestGuardas(unittest.TestCase):
    def test_barra_doses_e_dados_pessoais(self):
        for texto in ("aplicar 5 mg/kg", "usar 10 ml agora", "concentracao de 50%", "dar 2 comprimidos",
                      "1,5 mL IV", "300 UI", "CPF 123.456.789-09", "fulano@exemplo.com", "(11) 91234-5678",
                      "11 91234-5678"):
            with self.subTest(texto=texto):
                self.assertTrue(verificar_texto(texto), texto)

    def test_nao_barra_texto_administrativo(self):
        for texto in ("Registro C002, pendencia P01_PRONTUARIO_ABERTO em 2026-10-02T17:00 (F-b43d2caf).",
                      "Item ITEM_B1 e ITEM_C, grupo G1, quantidade 2 itens.", "Atendimento do dia 02/10."):
            with self.subTest(texto=texto):
                self.assertEqual(verificar_texto(texto), [])

    def test_marcador_so_incomoda_na_aprovacao(self):
        t = "texto [PREENCHER: algo]"
        self.assertEqual(verificar_texto(t), [])
        self.assertTrue(verificar_texto(t, exigir_sem_marcadores=True))

    def test_stub_passa_nas_guardas_para_todos_os_codigos(self):
        from fechamento.redator import DESTINOS_POR_CODIGO
        for cod, destinos in DESTINOS_POR_CODIGO.items():
            for d in destinos:
                ctx = ContextoRascunho("F-12345678", cod, d, "C002", "mensagem opaca da regra")
                texto = redigir_com_guardas(RedatorStub(), ctx)
                self.assertIn("RASCUNHO", texto)
                self.assertIn("[PREENCHER", texto)

    def test_destino_incompativel_com_codigo(self):
        ctx = ContextoRascunho("F-12345678", "C03_PROCEDIMENTO_SEM_ITEM", "prontuario", "C007", "m")
        with self.assertRaises(DecisaoRejeitada):
            redigir_com_guardas(RedatorStub(), ctx)

    def test_obter_redator(self):
        self.assertEqual(obter_redator("stub").nome, "stub")
        self.assertEqual(obter_redator("tests.helpers:RedatorLimpo").nome, "limpo")
        with self.assertRaises(DecisaoRejeitada):
            obter_redator("modulo_que_nao_existe:X")
        with self.assertRaises(DecisaoRejeitada):
            obter_redator("sem_dois_pontos")


class TestPortaoDeAprovacao(BaseTeste):
    def setUp(self):
        super().setUp()
        self.verificar()
        self.finding = self.achar("C03", "C007")["finding_id"]
        rc, out, err = rodar("rascunho", "--finding", self.finding, "--destino", "tutor",
                             "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 0, err)
        self.assertIn("NAO ENVIAR", out)
        self.rid = [e for e in rascunhos.ler_eventos(self.saida) if e["evento"] == "criado"][0]["rascunho_id"]

    def aprovar(self, papel="veterinario", confirmo=True, final=None, responsavel="Vet Ficticio"):
        args = ["aprovar", "--rascunho", self.rid, "--papel", papel, "--responsavel", responsavel,
                "--saida", self.saida, "--agora", AGORA]
        if confirmo:
            args.append("--confirmo")
        if final is not None:
            arq = self.tmp / "final.txt"
            arq.write_text(final, encoding="utf-8")
            args += ["--texto-final", arq]
        return rodar(*args)

    def exportar(self):
        return rodar("exportar", "--rascunho", self.rid, "--saida", self.saida)

    TEXTO_OK = "Prezado tutor, identificamos divergencia administrativa no registro C007. Atenciosamente, Vet Ficticio."

    def test_verificar_e_decidir_nao_geram_texto_para_tutor(self):
        self.assertFalse((self.saida / "liberados").exists())
        self.assertEqual(self.decidir(self.finding, "encaminhado", "veterinario")[0], 0)
        self.assertFalse((self.saida / "liberados").exists())

    def test_rascunho_fica_em_estado_rascunho_e_nao_exporta(self):
        est, _, _ = rascunhos.estado(rascunhos.ler_eventos(self.saida), self.rid)
        self.assertEqual(est, "RASCUNHO")
        rc, _, err = self.exportar()
        self.assertEqual(rc, 3)
        self.assertIn("aprovacao explicita", err)
        self.assertFalse((self.saida / "liberados").exists())

    def test_aprovacao_exige_confirmacao_explicita(self):
        rc, _, err = self.aprovar(confirmo=False, final=self.TEXTO_OK)
        self.assertEqual(rc, 3)
        self.assertIn("--confirmo", err)

    def test_somente_veterinario_aprova(self):
        for papel in ("recepcao", "financeiro"):
            self.assertEqual(self.aprovar(papel=papel, final=self.TEXTO_OK)[0], 3)
        self.assertEqual(self.exportar()[0], 3)

    def test_nao_aprova_texto_com_marcador_pendente(self):
        rc, _, err = self.aprovar()               # texto original do stub tem [PREENCHER ...]
        self.assertEqual(rc, 3)
        self.assertIn("PREENCHER", err)

    def test_nao_aprova_texto_com_dose_ou_dado_pessoal(self):
        self.assertEqual(self.aprovar(final="Aplicar 5 mg/kg do farmaco.")[0], 3)
        self.assertEqual(self.aprovar(final="Fale com fulano@exemplo.com sobre a cobranca.")[0], 3)
        self.assertEqual(self.exportar()[0], 3)

    def test_fluxo_completo_aprovar_e_exportar_texto_exato(self):
        self.assertEqual(self.aprovar(final=self.TEXTO_OK)[0], 0)
        rc, out, _ = self.exportar()
        self.assertEqual(rc, 0, out)
        self.assertEqual((self.saida / "liberados" / (self.rid + ".txt")).read_text(encoding="utf-8"), self.TEXTO_OK)
        ev = [e for e in rascunhos.ler_eventos(self.saida) if e["evento"] == "aprovado"][0]
        self.assertEqual((ev["papel"], ev["responsavel"], ev["editado"]), ("veterinario", "Vet Ficticio", True))
        self.assertEqual(self.aprovar(final=self.TEXTO_OK)[0], 3)       # nao aprova duas vezes

    def test_log_adulterado_apos_aprovacao_bloqueia_exportacao(self):
        self.assertEqual(self.aprovar(final=self.TEXTO_OK)[0], 0)
        p = self.saida / "rascunhos.jsonl"
        linhas = p.read_text(encoding="utf-8").splitlines()
        ev = json.loads(linhas[-1])
        ev["texto_final"] = ev["texto_final"] + " Pague para outra conta."
        linhas[-1] = json.dumps(ev, ensure_ascii=False)
        p.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        self.assertEqual(self.exportar()[0], 3)
        self.assertFalse((self.saida / "liberados").exists())

    def test_rejeitar_impede_aprovar_e_exportar(self):
        rc, _, _ = rodar("rejeitar", "--rascunho", self.rid, "--papel", "veterinario", "--responsavel", "Vet Ficticio",
                         "--motivo", "texto nao se aplica ao caso", "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 0)
        self.assertEqual(self.aprovar(final=self.TEXTO_OK)[0], 3)
        self.assertEqual(self.exportar()[0], 3)

    def test_rejeitar_exige_motivo_e_papel(self):
        base = ["rejeitar", "--rascunho", self.rid, "--responsavel", "Vet Ficticio", "--saida", self.saida]
        self.assertEqual(rodar(*base, "--papel", "veterinario", "--motivo", "curto")[0], 3)
        self.assertEqual(rodar(*base, "--papel", "recepcao", "--motivo", "motivo bem longo aqui")[0], 3)

    def test_rascunho_idempotente(self):
        rc, out, _ = rodar("rascunho", "--finding", self.finding, "--destino", "tutor", "--saida", self.saida)
        self.assertEqual(rc, 0)
        self.assertIn("ja existia", out)
        self.assertEqual(len([e for e in rascunhos.ler_eventos(self.saida) if e["evento"] == "criado"]), 1)

    def test_destino_invalido_para_o_codigo_na_cli(self):
        rc, _, err = rodar("rascunho", "--finding", self.finding, "--destino", "prontuario", "--saida", self.saida)
        self.assertEqual(rc, 3)

    def test_saida_do_redator_com_dose_e_barrada_e_nada_e_gravado(self):
        antes = (self.saida / "rascunhos.jsonl").read_bytes()
        rc, _, err = rodar("rascunho", "--finding", self.finding, "--destino", "tutor", "--saida", self.saida,
                           "--redator", "tests.helpers:RedatorDoseRuim")
        self.assertEqual(rc, 3)
        self.assertIn("guardas", err)
        self.assertEqual((self.saida / "rascunhos.jsonl").read_bytes(), antes)

    def test_redator_plugavel_limpo(self):
        rc, out, _ = rodar("rascunho", "--finding", self.finding, "--destino", "tutor", "--saida", self.saida,
                           "--redator", "tests.helpers:RedatorLimpo")
        self.assertEqual(rc, 0)
        self.assertIn("(limpo)", out)


if __name__ == "__main__":
    unittest.main()
