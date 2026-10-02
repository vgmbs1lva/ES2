"""Estruturas de dados imutaveis usadas pelo nucleo deterministico."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

SEV_ACAO = "acao"
SEV_ATENCAO = "atencao"
SEV_INFO = "info"


@dataclass(frozen=True)
class Consulta:
    consulta_id: str
    data: str
    veterinario_id: str
    status_atendimento: str
    status_prontuario: str
    fechado_em: str
    campos: Tuple[Tuple[str, str], ...]  # (nome_do_campo, "S"|"N"), ordem do arquivo
    linha: int


@dataclass(frozen=True)
class Procedimento:
    consulta_id: str
    procedimento_codigo: str
    linha: int


@dataclass(frozen=True)
class ItemFatura:
    consulta_id: str
    item_codigo: str
    quantidade: int
    linha: int


@dataclass(frozen=True)
class Regra:
    procedimento_codigo: str
    item_codigo: str
    grupo_alternativa: str
    ato_clinico: bool
    controlado: bool
    linha: int


@dataclass(frozen=True)
class CampoObrigatorio:
    campo: str
    fonte_norma: str
    versao: str
    linha: int


@dataclass(frozen=True)
class Dados:
    consultas: Tuple[Consulta, ...]
    procedimentos: Tuple[Procedimento, ...]
    itens: Tuple[ItemFatura, ...]
    regras: Tuple[Regra, ...]
    campos_obrigatorios: Tuple[CampoObrigatorio, ...]
    hash_regras: str
    hash_campos: str
    data: str = ""


@dataclass(frozen=True)
class Pendencia:
    finding_id: str
    codigo: str
    severidade: str
    consulta_id: str
    veterinario_id: str
    evidencia: str  # "arquivo:Lnn; arquivo:Lnn" (so arquivos de dados que contem o consulta_id)
    mensagem: str
    exige_veterinario: bool = False  # RF-06: so decisao de papel veterinario
    regra_ref: str = ""  # "regras.csv:Lnn" (referencia a regra que originou, quando houver)
