"""Decisoes humanas em log append-only (decisoes.jsonl). RF-04, RF-05, RF-06, RF-08, RF-09.

A ferramenta nunca "resolve" uma pendencia: so o dado corrigido no PIMS (proximo export)
ou uma decisao humana valida e terminal encerra. `encaminhado` nao e terminal.
"""

import csv
import json
import re
from pathlib import Path

from .erros import DecisaoRejeitada, ErroEntrada
from .modelos import SEV_INFO
from .regras import NAO_IGNORAVEIS

ARQ_LOG = "decisoes.jsonl"
DECISOES = ("ignorar", "encaminhado", "conferido_manual")
PAPEIS = ("veterinario", "recepcao", "financeiro")
TERMINAIS = ("ignorar", "conferido_manual")
MIN_MOTIVO = 10  # caracteres nao brancos


def caracteres_uteis(texto):
    return len(re.sub(r"\s", "", texto or ""))


def validar_decisao(codigo, severidade, exige_veterinario, decisao, motivo, papel, responsavel):
    """Aplica RF-05/RF-06. Levanta DecisaoRejeitada com a razao. Nao grava nada."""
    if decisao not in DECISOES:
        raise DecisaoRejeitada("decisao '%s' invalida (use: %s)" % (decisao, ", ".join(DECISOES)))
    if papel not in PAPEIS:
        raise DecisaoRejeitada("papel '%s' invalido (use: %s)" % (papel, ", ".join(PAPEIS)))
    if not (responsavel or "").strip():
        raise DecisaoRejeitada("responsavel obrigatorio")
    if severidade == SEV_INFO:
        raise DecisaoRejeitada("%s e informativa: nao exige nem aceita decisao" % codigo)
    if decisao == "conferido_manual" and not codigo.startswith("K01"):
        raise DecisaoRejeitada("conferido_manual so se aplica a K01")
    if codigo.startswith("K01") and decisao == "ignorar":
        raise DecisaoRejeitada("K01 so pode ser encerrada com conferido_manual (papel veterinario, com motivo)")
    if decisao == "ignorar" and codigo in NAO_IGNORAVEIS:
        raise DecisaoRejeitada("%s nao pode ser ignorada: so se resolve fechando/completando o prontuario no PIMS" % codigo)
    if decisao in TERMINAIS and caracteres_uteis(motivo) < MIN_MOTIVO:
        raise DecisaoRejeitada("motivo obrigatorio com ao menos %d caracteres nao brancos para '%s'" % (MIN_MOTIVO, decisao))
    if (codigo.startswith(("P", "K")) or exige_veterinario) and papel != "veterinario":
        raise DecisaoRejeitada("%s so aceita decisao de papel 'veterinario'" % codigo)


def ler_log(saida):
    caminho = Path(saida) / ARQ_LOG
    if not caminho.is_file():
        return []
    registros = []
    with open(caminho, "r", encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            if not linha.strip():
                continue
            try:
                r = json.loads(linha)
                assert isinstance(r, dict) and "finding_id" in r and "decisao" in r
            except (ValueError, AssertionError):
                raise ErroEntrada(ARQ_LOG, n, "linha invalida no log de decisoes")
            registros.append(r)
    return registros


def registrar(saida, info, decisao, motivo, papel, responsavel, agora):
    """Valida e acrescenta UMA linha ao log (nunca reescreve). `info` = dict da pendencia."""
    validar_decisao(info["codigo"], info["severidade"], info["exige_veterinario"] == "S",
                    decisao, motivo, papel, responsavel)
    reg = {"finding_id": info["finding_id"], "codigo": info["codigo"], "decisao": decisao,
           "motivo": (motivo or "").strip(), "papel": papel, "responsavel": responsavel.strip(),
           "registrado_em": agora, "hash_regras": info["hash_regras"], "hash_campos": info["hash_campos"]}
    Path(saida).mkdir(parents=True, exist_ok=True)
    caminho = Path(saida) / ARQ_LOG
    prefixo = b""
    if caminho.is_file() and caminho.stat().st_size:
        with open(caminho, "rb") as f:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                prefixo = b"\n"
    with open(caminho, "ab") as f:
        f.write(prefixo + (json.dumps(reg, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
    return reg


def localizar_finding(saida, finding_id):
    """Busca a pendencia nos pendencias_*.csv ja gerados por `verificar` (mais recente vence)."""
    achado = None
    for caminho in sorted(Path(saida).glob("pendencias_*.csv")):
        with open(caminho, newline="", encoding="utf-8") as f:
            for linha in csv.DictReader(f):
                if linha["finding_id"] == finding_id:
                    achado = linha
    return achado


def situacao(pendencias, registros):
    """Para cada pendencia: (status, registro|None). status: aberta | encaminhada | decidida | info.

    Vale a ultima decisao registrada para o finding_id. Registros que nao passam de novo
    pelas regras (ex.: log editado a mao) nao contam.
    """
    por_id = {p.finding_id: p for p in pendencias}
    ultima = {}
    for r in registros:
        p = por_id.get(r["finding_id"])
        if p is None:
            continue
        try:
            validar_decisao(p.codigo, p.severidade, p.exige_veterinario, r.get("decisao"),
                            r.get("motivo", ""), r.get("papel"), r.get("responsavel", ""))
        except DecisaoRejeitada:
            continue
        ultima[p.finding_id] = r
    out = {}
    for p in pendencias:
        if p.severidade == SEV_INFO:
            out[p.finding_id] = ("info", None)
            continue
        r = ultima.get(p.finding_id)
        if r is None:
            out[p.finding_id] = ("aberta", None)
        elif r["decisao"] in TERMINAIS:
            out[p.finding_id] = ("decidida", r)
        else:
            out[p.finding_id] = ("encaminhada", r)
    return out


def estado_do_dia(status_por_id):
    abertas = [s for s, _ in status_por_id.values() if s in ("aberta", "encaminhada")]
    return "PENDENTE" if abertas else "CONFERIDO"
