"""Ciclo de vida dos rascunhos de texto (tutor/prontuario) com PORTAO DE APROVACAO do veterinario.

Estados: RASCUNHO -> APROVADO | REJEITADO. Log append-only em rascunhos.jsonl.
Nada e escrito em prontuario nem enviado a tutor pela ferramenta: `exportar` so grava um arquivo
local, e somente para texto APROVADO por papel `veterinario`, sem marcadores, identico ao hash aprovado.
O papel e declarado (sem autenticacao): ver README, limitacoes.
"""

import hashlib
import json
import re
from pathlib import Path

from .erros import DecisaoRejeitada, ErroEntrada
from .redator import ContextoRascunho, redigir_com_guardas, verificar_texto

ARQ_RASCUNHOS = "rascunhos.jsonl"
PASTA_LIBERADOS = "liberados"
ESTADOS = ("RASCUNHO", "APROVADO", "REJEITADO")


def _sha(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def ler_eventos(saida):
    caminho = Path(saida) / ARQ_RASCUNHOS
    if not caminho.is_file():
        return []
    out = []
    with open(caminho, "r", encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            if not linha.strip():
                continue
            try:
                e = json.loads(linha)
                assert isinstance(e, dict) and e["evento"] in ("criado", "aprovado", "rejeitado") and e["rascunho_id"]
            except (ValueError, AssertionError, KeyError):
                raise ErroEntrada(ARQ_RASCUNHOS, n, "linha invalida no log de rascunhos")
            out.append(e)
    return out


def _acrescentar(saida, evento):
    Path(saida).mkdir(parents=True, exist_ok=True)
    caminho = Path(saida) / ARQ_RASCUNHOS
    prefixo = b""
    if caminho.is_file() and caminho.stat().st_size:
        with open(caminho, "rb") as f:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                prefixo = b"\n"
    with open(caminho, "ab") as f:
        f.write(prefixo + (json.dumps(evento, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))


def estado(eventos, rascunho_id):
    """(estado, criado, aprovado|None). Estado vem do ultimo evento; levanta se id desconhecido."""
    criado = next((e for e in eventos if e["rascunho_id"] == rascunho_id and e["evento"] == "criado"), None)
    if criado is None:
        raise DecisaoRejeitada("rascunho '%s' desconhecido" % rascunho_id)
    ultimo = [e for e in eventos if e["rascunho_id"] == rascunho_id][-1]
    if ultimo["evento"] == "aprovado":
        return "APROVADO", criado, ultimo
    if ultimo["evento"] == "rejeitado":
        return "REJEITADO", criado, None
    return "RASCUNHO", criado, None


def criar(saida, info, destino, redator, agora):
    """Gera rascunho via `redator` (com guardas) e registra como RASCUNHO. Idempotente por conteudo."""
    ctx = ContextoRascunho(info["finding_id"], info["codigo"], destino, info["consulta_id"], info["mensagem"])
    texto = redigir_com_guardas(redator, ctx)
    rid = "R-" + _sha("|".join((info["finding_id"], destino, texto)))[:8]
    eventos = ler_eventos(saida)
    if any(e["rascunho_id"] == rid and e["evento"] == "criado" for e in eventos):
        return rid, texto, False
    _acrescentar(saida, {"evento": "criado", "rascunho_id": rid, "finding_id": info["finding_id"],
                         "codigo": info["codigo"], "destino": destino, "redator": redator.nome,
                         "texto": texto, "texto_sha256": _sha(texto), "registrado_em": agora})
    return rid, texto, True


def aprovar(saida, rascunho_id, papel, responsavel, confirmo, agora, texto_final=None):
    """Aprovacao explicita. Somente papel `veterinario`; texto final sem marcadores, dose ou dado pessoal."""
    if not confirmo:
        raise DecisaoRejeitada("aprovacao exige confirmacao explicita (--confirmo)")
    if papel != "veterinario":
        raise DecisaoRejeitada("somente o papel 'veterinario' aprova texto destinado a tutor ou prontuario")
    if not (responsavel or "").strip():
        raise DecisaoRejeitada("responsavel obrigatorio")
    est, criado, _ = estado(ler_eventos(saida), rascunho_id)
    if est != "RASCUNHO":
        raise DecisaoRejeitada("rascunho %s esta %s: so RASCUNHO pode ser aprovado" % (rascunho_id, est))
    final = criado["texto"] if texto_final is None else texto_final
    problemas = verificar_texto(final, exigir_sem_marcadores=True)
    if problemas:
        raise DecisaoRejeitada("texto nao pode ser aprovado: " + "; ".join(problemas))
    ev = {"evento": "aprovado", "rascunho_id": rascunho_id, "papel": papel, "responsavel": responsavel.strip(),
          "texto_final": final, "texto_final_sha256": _sha(final), "editado": final != criado["texto"],
          "confirmacao": "o veterinario declara ter lido e aprovado este texto exato", "registrado_em": agora}
    _acrescentar(saida, ev)
    return ev


def rejeitar(saida, rascunho_id, papel, responsavel, motivo, agora):
    if papel != "veterinario":
        raise DecisaoRejeitada("somente o papel 'veterinario' rejeita rascunho")
    if not (responsavel or "").strip() or len(re.sub(r"\s", "", motivo or "")) < 10:
        raise DecisaoRejeitada("responsavel e motivo (>= 10 caracteres nao brancos) obrigatorios")
    est, _, _ = estado(ler_eventos(saida), rascunho_id)
    if est != "RASCUNHO":
        raise DecisaoRejeitada("rascunho %s esta %s: so RASCUNHO pode ser rejeitado" % (rascunho_id, est))
    ev = {"evento": "rejeitado", "rascunho_id": rascunho_id, "papel": papel, "responsavel": responsavel.strip(),
          "motivo": motivo.strip(), "registrado_em": agora}
    _acrescentar(saida, ev)
    return ev


def exportar(saida, rascunho_id):
    """Grava liberados/<id>.txt SOMENTE se APROVADO e integro. Nunca envia nem lanca em lugar nenhum."""
    est, _, aprov = estado(ler_eventos(saida), rascunho_id)
    if est != "APROVADO":
        raise DecisaoRejeitada("rascunho %s esta %s: exportacao exige aprovacao explicita do veterinario"
                               % (rascunho_id, est))
    if _sha(aprov["texto_final"]) != aprov["texto_final_sha256"]:
        raise DecisaoRejeitada("texto aprovado nao confere com o hash registrado (log adulterado?)")
    problemas = verificar_texto(aprov["texto_final"], exigir_sem_marcadores=True)
    if problemas:
        raise DecisaoRejeitada("texto aprovado reprovado nas guardas: " + "; ".join(problemas))
    pasta = Path(saida) / PASTA_LIBERADOS
    pasta.mkdir(parents=True, exist_ok=True)
    caminho = pasta / (rascunho_id + ".txt")
    caminho.write_text(aprov["texto_final"], encoding="utf-8", newline="\n")
    return caminho
