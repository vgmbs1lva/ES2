"""Etapa de redacao: interface plugavel + implementacao STUB offline + guardas deterministicas.

Este e o UNICO ponto onde um LLM poderia entrar, e apenas para redigir RASCUNHOS de texto.
Regras de projeto:
  * O redator recebe so dados opacos (codigo da regra, consulta_id, mensagem da regra). Nada de nome,
    CPF, telefone, texto livre de prontuario.
  * Toda saida do redator passa por `verificar_texto` (deterministico) antes de ser guardada.
  * Nenhum texto sai do rascunho sem aprovacao explicita do veterinario (ver rascunhos.py).
  * O pacote `fechamento` nao importa SDK de LLM (RF-10). Adaptadores reais ficam fora do pacote,
    em `adaptadores/`, e sao carregados por nome (`--redator modulo:Classe`).
"""

import importlib
import re
from dataclasses import dataclass
from typing import List

try:  # Protocol existe desde Python 3.8
    from typing import Protocol
except ImportError:  # pragma: no cover
    Protocol = object

from .erros import DecisaoRejeitada

DESTINOS = ("tutor", "prontuario")

# Destino permitido por codigo: cobranca -> comunicado ao tutor; prontuario/controlado -> nota ao prontuario.
DESTINOS_POR_CODIGO = {
    "P01_PRONTUARIO_ABERTO": ("prontuario",),
    "P02_PRONTUARIO_INCOMPLETO": ("prontuario",),
    "P03_FECHADO_RETROATIVO": ("prontuario",),
    "K01_CONTROLADO_CONFERIR": ("prontuario",),
    "C01_CONSULTA_SEM_FATURA": ("tutor",),
    "C02_FATURA_SEM_CONSULTA": ("tutor",),
    "C03_PROCEDIMENTO_SEM_ITEM": ("tutor",),
    "C04_ITEM_SEM_PROCEDIMENTO": ("tutor",),
    "C05_CANCELADA_COM_ITENS": ("tutor",),
}

MARCADOR = "[PREENCHER"


@dataclass(frozen=True)
class ContextoRascunho:
    """Tudo que o redator pode ver. Somente dados opacos produzidos pelas regras."""
    finding_id: str
    codigo: str
    destino: str
    consulta_id: str
    mensagem: str


class Redator(Protocol):
    """Contrato de um redator. Implemente `nome` e `redigir`."""
    nome: str

    def redigir(self, contexto: ContextoRascunho) -> str:
        """Devolve o texto do RASCUNHO. Deve manter marcadores `[PREENCHER ...]` para o que so o
        veterinario pode afirmar. Nao pode incluir doses, diagnosticos ou condutas."""
        ...


class RedatorStub:
    """Modelo fixo, offline e deterministico. Nao usa LLM. Serve de referencia e para testes."""
    nome = "stub"

    def redigir(self, contexto):
        if contexto.destino == "tutor":
            return (
                "RASCUNHO - nao enviar sem aprovacao do medico-veterinario.\n"
                "\n"
                "Prezado(a) tutor(a) %s],\n"
                "\n"
                "Ao conferir o atendimento de registro %s, identificamos uma possivel divergencia "
                "administrativa na cobranca (referencia interna: %s).\n"
                "\n"
                "%s: detalhes da divergencia e providencia, a criterio do medico-veterinario. "
                "Nao incluir doses nem condutas clinicas sem fonte e revisao do veterinario.]\n"
                "\n"
                "Atenciosamente,\n"
                "%s: nome e identificacao do medico-veterinario]\n"
                % (MARCADOR + ": forma de tratamento", contexto.consulta_id, contexto.codigo,
                   MARCADOR + " pelo veterinario", MARCADOR))
        return (
            "RASCUNHO - nota administrativa; so vale apos aprovacao e lancamento manual no PIMS pelo "
            "medico-veterinario.\n"
            "\n"
            "Registro %s. Pendencia %s: %s\n"
            "\n"
            "%s: providencia tomada no PIMS, data e hora. Nao incluir doses, diagnosticos ou condutas "
            "sem fonte e revisao do veterinario.]\n"
            "Responsavel: %s: nome e identificacao do medico-veterinario]\n"
            % (contexto.consulta_id, contexto.codigo, contexto.mensagem, MARCADOR + " pelo veterinario",
               MARCADOR))


# ------------------------------------------------------------------ Guardas
_UNIDADES = (r"(?:mg|mcg|ug|µg|g|kg|ml|ui|u\.i\.?|iu|cp|comps?|comprimidos?|gts?|gotas?|amp|ampolas?|"
             r"capsulas?|cápsulas?|mililitros?|miligramas?|microgramas?|gramas?)")
_NUMEROS = (r"(?:um|uma|dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|meio|meia|"
            r"vinte|trinta|quarenta|cinquenta|cem)")
_RE_DOSE = re.compile(r"(?<![\w.,])(?:\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?|" + _NUMEROS + r")\s*(?:%|" + _UNIDADES
                      + r"(?:/(?:kg|dia|h|ml|kg/dia))?(?![A-Za-zÀ-ÿ]))", re.IGNORECASE)
_RE_DOSE_VAGA = re.compile(r"(?<![A-Za-zÀ-ÿ])(?:dobro|metade|triplo)\s+d[ao]\s+dose", re.IGNORECASE)
# (?<![\w]) / (?![\w]): um consulta_id opaco como A1234567890 nao e telefone nem CPF.
_RE_CPF = re.compile(r"(?<![\w])\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?![\w])")
_RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_RE_FONE = re.compile(r"(?<![\w])(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}(?![\w])")


def verificar_pii(texto) -> List[str]:
    """Padroes de dado pessoal obvios (CPF, e-mail, telefone). Nao detecta nomes nem enderecos."""
    problemas = []
    for rotulo, rx in (("CPF", _RE_CPF), ("e-mail", _RE_EMAIL), ("telefone", _RE_FONE)):
        m = rx.search(texto or "")
        if m:
            problemas.append("padrao de %s detectado ('%s')" % (rotulo, m.group(0).strip()))
    return problemas


def verificar_texto(texto, exigir_sem_marcadores=False, ids_opacos=()) -> List[str]:
    """Guardas deterministicas sobre qualquer texto de rascunho/aprovado. Lista de problemas (vazia = ok).

    Nao e prova de seguranca clinica: apenas barra padroes obvios (dose, dado pessoal) e, na
    aprovacao, marcadores ainda nao preenchidos.
    """
    problemas = []
    if not (texto or "").strip():
        problemas.append("texto vazio")
        return problemas
    # ids opacos (consulta_id) nao sao dado pessoal, mesmo que parecam CPF/telefone (ex.: 12345678901)
    analisado = texto
    for i in sorted((x for x in ids_opacos if x), key=len, reverse=True):
        analisado = analisado.replace(i, " ")
    m = _RE_DOSE.search(analisado) or _RE_DOSE_VAGA.search(analisado)
    if m:
        problemas.append("padrao de dose/quantidade clinica detectado ('%s'; ex.: mg, ml, comp, gts, %%, UI, "
                         "numero por extenso): a ferramenta nao embute nem aceita doses; o veterinario deve "
                         "tratar fora do texto" % m.group(0).strip())
    problemas.extend(verificar_pii(analisado))
    if exigir_sem_marcadores and MARCADOR in texto:
        problemas.append("ainda ha marcador(es) '%s ...]' nao preenchido(s)" % MARCADOR)
    return problemas


def redigir_com_guardas(redator, contexto):
    if contexto.destino not in DESTINOS_POR_CODIGO.get(contexto.codigo, ()):
        raise DecisaoRejeitada("destino '%s' nao permitido para %s (permitido: %s)" % (
            contexto.destino, contexto.codigo, ", ".join(DESTINOS_POR_CODIGO.get(contexto.codigo, ())) or "nenhum"))
    try:
        texto = redator.redigir(contexto)
    except Exception as e:  # falha de rede/credencial/recusa no adaptador: nada e guardado
        raise DecisaoRejeitada("redator '%s' falhou: %s: %s" % (getattr(redator, "nome", "?"), type(e).__name__, e))
    if not isinstance(texto, str):
        raise DecisaoRejeitada("redator '%s' nao devolveu texto" % getattr(redator, "nome", "?"))
    problemas = verificar_texto(texto, ids_opacos=(contexto.consulta_id,))
    if problemas:
        raise DecisaoRejeitada("saida do redator '%s' barrada pelas guardas: %s"
                               % (getattr(redator, "nome", "?"), "; ".join(problemas)))
    return texto


def obter_redator(especificacao="stub"):
    """'stub' ou 'pacote.modulo:Classe' (importado sob demanda, instanciado sem argumentos)."""
    if especificacao in (None, "", "stub"):
        return RedatorStub()
    if ":" not in especificacao:
        raise DecisaoRejeitada("redator '%s' invalido: use 'stub' ou 'modulo:Classe'" % especificacao)
    modulo, _, classe = especificacao.partition(":")
    try:
        cls = getattr(importlib.import_module(modulo), classe)
        return cls()
    except Exception as e:  # modulo ausente, SDK nao instalado, sem credencial...
        raise DecisaoRejeitada("nao foi possivel carregar o redator '%s': %s: %s"
                               % (especificacao, type(e).__name__, e))
