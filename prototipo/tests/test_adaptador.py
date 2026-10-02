"""Adaptador Anthropic testado OFFLINE com cliente falso (nenhuma chamada de rede)."""

import sys
import unittest
from types import SimpleNamespace

from adaptadores.anthropic_redator import MODELO_PADRAO, AnthropicRedator
from fechamento.erros import DecisaoRejeitada
from fechamento.redator import ContextoRascunho, redigir_com_guardas
from tests.helpers import BaseTeste  # noqa: F401  (garante sys.path)


class ClienteFalso:
    def __init__(self, texto="RASCUNHO - nao enviar sem aprovacao. [PREENCHER: detalhes]", stop="end_turn"):
        self.chamadas = []
        self._texto, self._stop = texto, stop
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kw):
        self.chamadas.append(kw)
        blocos = [SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=self._texto)]
        return SimpleNamespace(content=blocos, stop_reason=self._stop)


CTX = ContextoRascunho("F-12345678", "C03_PROCEDIMENTO_SEM_ITEM", "tutor", "C007", "mensagem opaca")


class TestAdaptador(unittest.TestCase):
    def test_nao_importa_sdk_ao_ser_carregado(self):
        self.assertNotIn("anthropic", sys.modules)

    def test_chamada_e_extracao_de_texto(self):
        c = ClienteFalso()
        texto = redigir_com_guardas(AnthropicRedator(client=c), CTX)
        self.assertIn("RASCUNHO", texto)
        kw = c.chamadas[0]
        self.assertEqual(kw["model"], MODELO_PADRAO)
        self.assertIn("NUNCA inclua doses", kw["system"])
        corpo = kw["messages"][0]["content"]
        self.assertIn("C007", corpo)
        self.assertNotIn("temperature", kw)

    def test_saida_com_dose_e_barrada_pelas_guardas(self):
        with self.assertRaises(DecisaoRejeitada):
            redigir_com_guardas(AnthropicRedator(client=ClienteFalso(texto="Dar 10 mg/kg. [PREENCHER: x]")), CTX)

    def test_recusa_e_truncamento_viram_falha_sem_texto(self):
        for stop in ("refusal", "max_tokens"):
            with self.subTest(stop=stop):
                with self.assertRaises(DecisaoRejeitada):
                    redigir_com_guardas(AnthropicRedator(client=ClienteFalso(stop=stop)), CTX)

    def test_sem_sdk_instalado_erro_claro_na_cli_de_carga(self):
        from fechamento.redator import obter_redator
        try:
            import anthropic  # noqa: F401
            self.skipTest("SDK instalado neste ambiente")
        except ImportError:
            with self.assertRaises(DecisaoRejeitada):
                obter_redator("adaptadores.anthropic_redator:AnthropicRedator")


if __name__ == "__main__":
    unittest.main()
