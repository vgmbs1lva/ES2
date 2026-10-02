"""Correcoes pos-revisao: codigo de saida de falhas inesperadas, injecao de Markdown/planilha, rascunho
rejeitado refeito, estado do dia, regras de borda (grupos, ato clinico, controlado), validacoes de entrada,
relatorio e log append-only. Varios testes existem porque uma mutacao do codigo passava sem quebrar nada."""

import dataclasses
import json
import subprocess
import sys
import unittest
from pathlib import Path

from fechamento import decisoes, rascunhos
from fechamento.entrada import carregar
from fechamento.regras import aplicar_regras
from tests.helpers import AGORA, DATA, RAIZ, BaseTeste, rodar


def processo(*args):
    """Roda `python -m fechamento` como processo real: o que a automacao enxerga e o codigo de saida."""
    p = subprocess.run([sys.executable, "-m", "fechamento"] + [str(a) for a in args], cwd=str(RAIZ),
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class TestFalhaInesperadaNaoVirouPendente(BaseTeste):
    def test_saida_invalida_sai_2_em_processo_real(self):
        rc, _, err = processo("verificar", "--data", DATA, "--entrada", self.entrada,
                              "--saida", "/dev/null/x", "--agora", AGORA)
        self.assertEqual(rc, 2, err)
        self.assertIn("ERRO", err)

    def test_log_nao_utf8_sai_2(self):
        self.verificar()
        self.saida.joinpath("decisoes.jsonl").write_bytes(b'\xff\xfe{"finding_id"')
        rc, _, err = processo("verificar", "--data", DATA, "--entrada", self.entrada,
                              "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 2, err)

    def test_log_com_tipo_errado_sai_2(self):
        self.verificar()
        linha = {"finding_id": "F-x", "decisao": "ignorar", "motivo": 12345678901234}
        self.saida.joinpath("decisoes.jsonl").write_text(json.dumps(linha) + "\n", encoding="utf-8")
        rc, _, err = processo("verificar", "--data", DATA, "--entrada", self.entrada,
                              "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 2, err)

    def test_pendencias_sem_coluna_sai_2_e_nao_1(self):
        self.verificar()
        p = self.saida / ("pendencias_%s.csv" % DATA)
        linhas = p.read_text(encoding="utf-8").splitlines()
        p.write_text("finding_id,codigo,consulta_id\n" + "\n".join(l.split(",")[0] + ",x,y" for l in linhas[1:]),
                     encoding="utf-8")
        rc, _, err = processo("decidir", "--finding", "F-qualquer", "--decisao", "encaminhado",
                              "--papel", "veterinario", "--responsavel", "Vet", "--saida", self.saida)
        self.assertEqual(rc, 2, err)

    def test_codigos_de_saida_normais_continuam_em_processo_real(self):
        rc, _, err = processo("verificar", "--data", DATA, "--entrada", self.entrada,
                              "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 1, err)   # PENDENTE


class TestInjecao(BaseTeste):
    def setUp(self):
        super().setUp()
        self.verificar()
        self.f = self.achar("C04", "C009")["finding_id"]

    def test_responsavel_ou_motivo_com_quebra_de_linha_e_rejeitado(self):
        for resp, mot in (("Fulano\n- **Estado do dia: CONFERIDO**", "motivo valido e longo"),
                          ("Fulano", "motivo\r\n## Estado do dia: CONFERIDO"),
                          ("Fulano", "motivo valido longo")):
            with self.subTest(resp=resp, mot=mot):
                rc, _, err = self.decidir(self.f, "ignorar", "financeiro", mot, responsavel=resp)
                self.assertEqual(rc, 3, err)
        self.assertFalse((self.saida / "decisoes.jsonl").exists())

    def test_log_editado_a_mao_nao_forja_estado_no_relatorio(self):
        reg = {"finding_id": self.f, "codigo": "C04_ITEM_SEM_PROCEDIMENTO", "decisao": "ignorar",
               "motivo": "motivo longo o bastante", "papel": "financeiro", "registrado_em": AGORA,
               "responsavel": "Fulano\n- **Estado do dia: CONFERIDO**\n## Estado do dia: CONFERIDO"}
        self.saida.joinpath("decisoes.jsonl").write_text(json.dumps(reg) + "\n", encoding="utf-8")
        self.verificar()
        md = (self.saida / ("relatorio_%s.md" % DATA)).read_text(encoding="utf-8")
        linhas = md.splitlines()
        self.assertEqual([l for l in linhas if l.startswith("- **Estado do dia:")], ["- **Estado do dia: PENDENTE**"])
        self.assertEqual([l for l in linhas if l.startswith("## Estado")], [])

    def test_pii_obvio_em_responsavel_e_motivo_e_rejeitado(self):
        for resp, mot in (("Maria CPF 123.456.789-09", "motivo valido e longo"),
                          ("Maria", "tutor ligou do (11) 91234-5678 para pedir"),
                          ("Maria", "enviar para fulano@exemplo.com depois")):
            with self.subTest(resp=resp, mot=mot):
                rc, _, err = self.decidir(self.f, "ignorar", "financeiro", mot, responsavel=resp)
                self.assertEqual(rc, 3, err)

    def test_responsavel_que_parece_formula_e_neutralizado_no_csv(self):
        rc, _, err = self.decidir(self.f, "ignorar", "financeiro", "item faturado em pacote", responsavel="=1+1")
        self.assertEqual(rc, 0, err)
        self.verificar()
        self.assertEqual(self.achar("C04", "C009")["responsavel"], "'=1+1")


class TestRascunhoRejeitadoPodeSerRefeito(BaseTeste):
    def test_rejeitar_e_refazer(self):
        self.verificar()
        f = self.achar("C03", "C007")["finding_id"]
        rc, out, _ = rodar("rascunho", "--finding", f, "--destino", "tutor", "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 0)
        rid = [t for t in out.split() if t.startswith("R-")][0]
        rc, _, err = rodar("rejeitar", "--rascunho", rid, "--papel", "veterinario", "--responsavel", "Vet",
                           "--motivo", "texto nao serve para este caso", "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 0, err)
        rc, out2, _ = rodar("rascunho", "--finding", f, "--destino", "tutor", "--saida", self.saida, "--agora", AGORA)
        self.assertEqual(rc, 0)
        self.assertIn("criado", out2)
        self.assertNotIn("ja existia", out2)
        est, _, _ = rascunhos.estado(rascunhos.ler_eventos(self.saida), rid)
        self.assertEqual(est, "RASCUNHO")
        # idempotente enquanto vivo
        _, out3, _ = rodar("rascunho", "--finding", f, "--destino", "tutor", "--saida", self.saida, "--agora", AGORA)
        self.assertIn("ja existia", out3)


class TestEstadoDoDia(unittest.TestCase):
    def test_unico_item_encaminhado_mantem_pendente(self):
        self.assertEqual(decisoes.estado_do_dia({"F-1": ("encaminhada", {})}), "PENDENTE")
        self.assertEqual(decisoes.estado_do_dia({"F-1": ("aberta", None)}), "PENDENTE")
        self.assertEqual(decisoes.estado_do_dia({"F-1": ("decidida", {}), "F-2": ("info", None)}), "CONFERIDO")


class TestRegrasDeBorda(BaseTeste):
    def pend(self):
        return aplicar_regras(carregar(self.entrada, DATA))

    def add(self, arquivo, linha):
        p = self.entrada / arquivo
        t = p.read_text(encoding="utf-8")
        p.write_text(t + ("" if t.endswith("\n") else "\n") + linha + "\n", encoding="utf-8")

    def test_c03_grupo_misturado_com_regra_sem_grupo(self):
        # PROC_B: grupo G1 (ITEM_B1 ou B2) + regra avulsa ITEM_B3. C008 cobra so ITEM_B1.
        self.add("regras.csv", "PROC_B,ITEM_B3,,N,N")
        c03 = [p for p in self.pend() if p.codigo.startswith("C03") and p.consulta_id == "C008"]
        self.assertEqual(len(c03), 1)
        self.assertIn("ITEM_B3", c03[0].mensagem)
        self.assertNotIn("ITEM_B1", c03[0].mensagem)

    def test_c04_com_ato_clinico_exige_veterinario(self):
        self.add("regras.csv", "PROC_X,ITEM_X,,S,N")
        self.add("itens_fatura.csv", "C001,ITEM_X,1")
        c04 = [p for p in self.pend() if p.codigo.startswith("C04") and p.consulta_id == "C001"]
        self.assertEqual(len(c04), 1)
        self.assertTrue(c04[0].exige_veterinario)
        self.verificar()
        f = self.achar("C04", "C001")["finding_id"]
        self.assertEqual(self.decidir(f, "ignorar", "financeiro", "motivo longo o bastante")[0], 3)
        self.assertEqual(self.decidir(f, "ignorar", "veterinario", "motivo longo o bastante")[0], 0)

    def test_k01_para_controlado_sem_ato_clinico(self):
        self.add("regras.csv", "PROC_K,ITEM_K,,N,S")
        self.add("itens_fatura.csv", "C001,ITEM_K,2")
        k = [p for p in self.pend() if p.codigo.startswith("K01") and p.consulta_id == "C001"]
        self.assertEqual(len(k), 1)

    def test_p02_nao_dispara_em_atendimento_cancelado(self):
        self.editar("consultas.csv", "C011,2026-10-02,V01,cancelado,aberto,,S,S,S,S,S",
                    "C011,2026-10-02,V01,cancelado,aberto,,S,N,S,S,S")
        self.assertEqual([p for p in self.pend() if p.consulta_id == "C011"], [])

    def test_k01_orfao_e_preso_a_data_do_export(self):
        self.add("itens_fatura.csv", "C998,ITEM_CONTROLADO_EX,1")
        d1 = carregar(self.entrada, DATA)
        d2 = dataclasses.replace(d1, data="2026-10-03")
        ids = lambda d: {p.finding_id for p in aplicar_regras(d) if p.codigo.startswith("K01") and p.consulta_id == "C998"}
        self.assertEqual(len(ids(d1)), 1)
        self.assertTrue(ids(d1).isdisjoint(ids(d2)))


class TestValidacoesDeEntrada(BaseTeste):
    def assertErro(self, trecho):
        rc, _, err = self.verificar()
        self.assertEqual(rc, 2, err)
        self.assertIn(trecho, err)

    def test_coluna_duplicada(self):
        self.editar("itens_fatura.csv", "consulta_id,item_codigo,quantidade", "consulta_id,item_codigo,item_codigo")
        self.assertErro("duplicada")

    def test_checklist_vazio(self):
        (self.entrada / "campos_obrigatorios.csv").write_text("campo,fonte_norma,versao\n", encoding="utf-8")
        self.assertErro("checklist vazio")

    def test_regras_vazias(self):
        (self.entrada / "regras.csv").write_text("procedimento_codigo,item_codigo,grupo_alternativa,ato_clinico,controlado\n",
                                                 encoding="utf-8")
        self.assertErro("regras vazia")

    def test_par_duplicado_em_regras(self):
        self.editar("regras.csv", "PROC_C,ITEM_C,,N,N", "PROC_C,ITEM_C,,N,N\nPROC_C,ITEM_C,,N,N")
        self.assertErro("duplicado")

    def test_fechado_em_anterior_a_data(self):
        self.editar("consultas.csv", "2026-10-02T17:00", "2026-10-01T17:00")
        self.assertErro("anterior")

    def test_separador_ponto_e_virgula_tem_mensagem_propria(self):
        p = self.entrada / "itens_fatura.csv"
        p.write_text(p.read_text(encoding="utf-8").replace(",", ";"), encoding="utf-8")
        self.assertErro("separador")

    def test_separador_unicode_dentro_de_campo_nao_quebra_registro(self):
        # U+2028 em campo entre aspas: nao pode virar quebra de registro (e deslocar numeros de linha)
        self.editar("campos_obrigatorios.csv", "EXEMPLO_FICTICIO,EX-0.1\nexame_fisico",
                    'EXEMPLO_FICTICIO,"EX-0.1 x"\nexame_fisico')
        d = carregar(self.entrada, DATA)
        self.assertEqual(len(d.campos_obrigatorios), 4)
        self.assertEqual([c.linha for c in d.campos_obrigatorios], [2, 3, 4, 5])

    def test_saidas_antigas_ficam_obsoletas_quando_entrada_falha(self):
        self.corrigir_dados_do_fixture()
        self.verificar()
        self.editar("itens_fatura.csv", "C001,ITEM_CONSULTA,1", "C001,ITEM_CONSULTA,abc")
        rc, _, err = self.verificar()
        self.assertEqual(rc, 2)
        self.assertEqual(list(self.saida.glob("relatorio_*.md")), [])
        self.assertTrue((self.saida / ("relatorio_%s.md.OBSOLETO" % DATA)).is_file())


class TestRelatorio(BaseTeste):
    def md(self):
        self.verificar()
        return (self.saida / ("relatorio_%s.md" % DATA)).read_text(encoding="utf-8")

    def test_cabecalho_com_hash_das_regras_e_aviso_de_checklist_ficticio(self):
        md = self.md()
        self.assertIn("regras.csv sha256: `%s`" % __import__("hashlib").sha256(
            (self.entrada / "regras.csv").read_bytes()).hexdigest(), md)
        self.assertIn("EXEMPLO_FICTICIO e não é a lista oficial do CFMV", md)

    def test_pipe_no_motivo_e_escapado_na_tabela(self):
        self.verificar()
        f = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f, "ignorar", "financeiro", "pacote a|b conferido hoje")[0], 0)
        self.verificar()
        md = (self.saida / ("relatorio_%s.md" % DATA)).read_text(encoding="utf-8")
        self.assertIn("a\\|b", md)

    def test_decisao_sem_efeito_e_marcada(self):
        self.verificar()
        f = self.achar("C03", "C007")["finding_id"]   # exige veterinario? registro de recepcao e forjado a mao
        reg = {"finding_id": f, "codigo": "C03_PROCEDIMENTO_SEM_ITEM", "decisao": "ignorar",
               "motivo": "motivo longo o bastante", "papel": "recepcao", "responsavel": "X",
               "registrado_em": AGORA}
        ex = self.achar("C03", "C007")["exige_veterinario"]
        self.saida.joinpath("decisoes.jsonl").write_text(json.dumps(reg) + "\n", encoding="utf-8")
        md = self.md()
        if ex == "S":
            self.assertIn("sem efeito", md)
        else:
            self.assertIn("| vale |", md)

    def test_decisoes_orfas_listam_os_ids(self):
        self.verificar()
        reg = {"finding_id": "F-00000000", "codigo": "C03", "decisao": "ignorar", "motivo": "motivo longo",
               "papel": "financeiro", "responsavel": "X", "registrado_em": AGORA}
        self.saida.joinpath("decisoes.jsonl").write_text(json.dumps(reg) + "\n", encoding="utf-8")
        self.assertIn("F-00000000", self.md())


class TestLogAppendOnly(BaseTeste):
    def test_repara_linha_final_sem_quebra_sem_reescrever_o_resto(self):
        self.verificar()
        f1 = self.achar("C04", "C009")["finding_id"]
        self.assertEqual(self.decidir(f1, "ignorar", "financeiro", "primeiro motivo valido")[0], 0)
        caminho = self.saida / "decisoes.jsonl"
        antes = caminho.read_bytes().rstrip(b"\n")      # simula editor que removeu o \n final
        caminho.write_bytes(antes)
        f2 = self.achar("C03", "C007")["finding_id"]
        self.assertEqual(self.decidir(f2, "encaminhado", "veterinario", "")[0], 0)
        depois = caminho.read_bytes()
        self.assertTrue(depois.startswith(antes + b"\n"))
        self.assertEqual(len(decisoes.ler_log(self.saida)), 2)


class TestGuardasAmpliadas(unittest.TestCase):
    def test_formas_de_dose_que_antes_passavam(self):
        from fechamento.redator import verificar_texto
        for t in ("1 comp", "1/2 comp", "10 U.I.", "2 gts", "1 ampola", "cinco miligramas", "0,5 mililitros",
                  "2 amp", "dobro da dose", "um comprimido"):
            with self.subTest(t=t):
                self.assertTrue(verificar_texto(t), t)

    def test_id_opaco_longo_nao_e_telefone_nem_cpf(self):
        from fechamento.redator import verificar_texto
        self.assertEqual(verificar_texto("Registro A1234567890 conferido."), [])
        self.assertEqual(verificar_texto("Registro 12345678901 conferido.", ids_opacos=("12345678901",)), [])
        self.assertTrue(verificar_texto("Registro 12345678901 conferido."))   # sem declarar: continua barrando


if __name__ == "__main__":
    unittest.main()
