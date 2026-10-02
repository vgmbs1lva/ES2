"""Regras deterministicas (uma funcao por codigo). Sem LLM, sem rede, sem escrita (RF-01, RF-02, RF-10).

Cada funcao recebe `Dados` (+ indices) e devolve uma lista de `Pendencia`.
O conteudo das regras (checklist, tabela item x procedimento) vem so dos CSVs (RF-07).
"""

import hashlib
from collections import defaultdict

from .erros import ErroEntrada
from .entrada import ARQ_CONSULTAS, ARQ_ITENS, ARQ_PROCEDIMENTOS, ARQ_REGRAS
from .modelos import SEV_ACAO, SEV_ATENCAO, SEV_INFO, Pendencia

SEM_CONSULTA = "SEM_CONSULTA"

CODIGOS = ("P01_PRONTUARIO_ABERTO", "P02_PRONTUARIO_INCOMPLETO", "P03_FECHADO_RETROATIVO",
           "C01_CONSULTA_SEM_FATURA", "C02_FATURA_SEM_CONSULTA", "C03_PROCEDIMENTO_SEM_ITEM",
           "C04_ITEM_SEM_PROCEDIMENTO", "C05_CANCELADA_COM_ITENS", "K01_CONTROLADO_CONFERIR")

# Codigos cujas pendencias nunca podem ser ignoradas (RF-06).
NAO_IGNORAVEIS = ("P01_PRONTUARIO_ABERTO", "P02_PRONTUARIO_INCOMPLETO")


def finding_id(codigo, consulta_id, data, chave):
    """Id estavel: hash curto de codigo + consulta_id + chave (+ data do export). RF-09."""
    bruto = "|".join((codigo, consulta_id, data, chave))
    return "F-" + hashlib.sha256(bruto.encode("utf-8")).hexdigest()[:8]


def _ev(*pares):
    return "; ".join("%s:L%d" % (arq, lin) for arq, lin in pares)


class _Indice:
    def __init__(self, dados):
        self.dados = dados
        self.consulta = {c.consulta_id: c for c in dados.consultas}
        self.procs = defaultdict(list)
        for p in dados.procedimentos:
            self.procs[p.consulta_id].append(p)
        self.itens = defaultdict(list)
        for i in dados.itens:
            self.itens[i.consulta_id].append(i)
        self.regras_por_proc = defaultdict(list)
        self.regras_por_item = defaultdict(list)
        for r in dados.regras:
            self.regras_por_proc[r.procedimento_codigo].append(r)
            self.regras_por_item[r.item_codigo].append(r)
        self.controlados = {r.item_codigo for r in dados.regras if r.controlado}


def _pend(codigo, sev, c_id, vet, chave, data, evid, msg, exige_vet, regra_ref=""):
    return Pendencia(finding_id(codigo, c_id, data, chave), codigo, sev, c_id, vet, evid, msg,
                     exige_vet, regra_ref)


# ---------------------------------------------------------------- Prontuario
def p01_prontuario_aberto(ix):
    out = []
    for c in ix.dados.consultas:
        if c.status_atendimento == "realizado" and c.status_prontuario == "aberto":
            out.append(_pend("P01_PRONTUARIO_ABERTO", SEV_ACAO, c.consulta_id, c.veterinario_id,
                             "aberto", c.data, _ev((ARQ_CONSULTAS, c.linha)),
                             "Atendimento realizado com prontuario ainda aberto. Fechar/completar no PIMS "
                             "(a ferramenta nao preenche, nao fecha e nao assina).", True))
    return out


def p02_prontuario_incompleto(ix):
    out = []
    obrigatorios = [c.campo for c in ix.dados.campos_obrigatorios]
    for c in ix.dados.consultas:
        # Atendimento cancelado nao tem prontuario a completar; sem este filtro o dia ficaria bloqueado
        # (P02 nao e ignoravel) por uma consulta que nao aconteceu. Mesmo criterio de P01.
        if c.status_atendimento != "realizado":
            continue
        valores = dict(c.campos)
        faltantes = sorted(n for n in obrigatorios if valores.get(n) == "N")
        if faltantes:
            out.append(_pend("P02_PRONTUARIO_INCOMPLETO", SEV_ACAO, c.consulta_id, c.veterinario_id,
                             ",".join(faltantes), c.data, _ev((ARQ_CONSULTAS, c.linha)),
                             "Prontuario com campo(s) do checklist nao preenchido(s): %s." % ", ".join(faltantes),
                             True))
    return out


def p03_fechado_retroativo(ix):
    out = []
    for c in ix.dados.consultas:
        if c.status_prontuario == "fechado" and c.fechado_em[:10] > c.data:
            out.append(_pend("P03_FECHADO_RETROATIVO", SEV_INFO, c.consulta_id, c.veterinario_id,
                             c.fechado_em, c.data, _ev((ARQ_CONSULTAS, c.linha)),
                             "Informativo: prontuario fechado em %s, depois da data do atendimento (%s)."
                             % (c.fechado_em, c.data), True))
    return out


# ------------------------------------------------------------------ Cobranca
def c01_consulta_sem_fatura(ix):
    out = []
    for c in ix.dados.consultas:
        if c.status_atendimento == "realizado" and not ix.itens.get(c.consulta_id):
            out.append(_pend("C01_CONSULTA_SEM_FATURA", SEV_ACAO, c.consulta_id, c.veterinario_id,
                             "", c.data, _ev((ARQ_CONSULTAS, c.linha)),
                             "Atendimento realizado sem nenhum item de fatura.", False))
    return out


def c02_fatura_sem_consulta(ix):
    out = []
    for cid in sorted(k for k in ix.itens if k not in ix.consulta):
        itens = ix.itens[cid]
        chave = ",".join(sorted("%s*%d" % (i.item_codigo, i.quantidade) for i in itens))
        out.append(_pend("C02_FATURA_SEM_CONSULTA", SEV_ACAO, cid, SEM_CONSULTA, chave,
                         ix.dados.data,
                         _ev(*[(ARQ_ITENS, i.linha) for i in itens]),
                         "Item(ns) de fatura (%s) com consulta_id inexistente em %s."
                         % (", ".join(sorted({i.item_codigo for i in itens})), ARQ_CONSULTAS), False))
    return out


def c03_procedimento_sem_item(ix):
    out = []
    for c in ix.dados.consultas:
        if c.status_atendimento != "realizado":
            continue
        cobrados = {i.item_codigo for i in ix.itens.get(c.consulta_id, [])}
        procs = defaultdict(list)
        for p in ix.procs.get(c.consulta_id, []):
            procs[p.procedimento_codigo].append(p)
        for proc in sorted(procs):
            grupos = defaultdict(list)
            for r in ix.regras_por_proc.get(proc, []):
                chave_grupo = ("g:" + r.grupo_alternativa) if r.grupo_alternativa else ("r:" + r.item_codigo)
                grupos[chave_grupo].append(r)
            for g in sorted(grupos):
                regras = grupos[g]
                if any(r.item_codigo in cobrados for r in regras):
                    continue
                esperados = sorted(r.item_codigo for r in regras)
                out.append(_pend(
                    "C03_PROCEDIMENTO_SEM_ITEM", SEV_ATENCAO, c.consulta_id, c.veterinario_id,
                    proc + "|" + ",".join(esperados), c.data,
                    _ev((ARQ_CONSULTAS, c.linha), *[(ARQ_PROCEDIMENTOS, p.linha) for p in procs[proc]]),
                    "Possivel item nao cobrado: procedimento %s realizado, sem item esperado na fatura (%s)."
                    % (proc, " ou ".join(esperados)),
                    any(r.ato_clinico for r in regras),
                    _ev(*[(ARQ_REGRAS, r.linha) for r in regras])))
    return out


def c04_item_sem_procedimento(ix):
    out = []
    for c in ix.dados.consultas:
        if c.status_atendimento != "realizado":
            continue
        realizados = {p.procedimento_codigo for p in ix.procs.get(c.consulta_id, [])}
        por_item = defaultdict(list)
        for i in ix.itens.get(c.consulta_id, []):
            por_item[i.item_codigo].append(i)
        for item in sorted(por_item):
            regras = ix.regras_por_item.get(item, [])
            if not regras:
                continue
            associados = sorted({r.procedimento_codigo for r in regras})
            if realizados.intersection(associados):
                continue
            qtd = sum(i.quantidade for i in por_item[item])
            out.append(_pend(
                "C04_ITEM_SEM_PROCEDIMENTO", SEV_ATENCAO, c.consulta_id, c.veterinario_id,
                "%s*%d|%s" % (item, qtd, ",".join(associados)), c.data,
                _ev((ARQ_CONSULTAS, c.linha), *[(ARQ_ITENS, i.linha) for i in por_item[item]]),
                "Possivel cobranca indevida: item %s cobrado sem o procedimento associado (%s) nos realizados."
                % (item, " ou ".join(associados)),
                any(r.ato_clinico for r in regras),
                _ev(*[(ARQ_REGRAS, r.linha) for r in regras])))
    return out


def c05_cancelada_com_itens(ix):
    out = []
    for c in ix.dados.consultas:
        itens = ix.itens.get(c.consulta_id, [])
        if c.status_atendimento == "cancelado" and itens:
            chave = ",".join(sorted("%s*%d" % (i.item_codigo, i.quantidade) for i in itens))
            out.append(_pend("C05_CANCELADA_COM_ITENS", SEV_ACAO, c.consulta_id, c.veterinario_id,
                             chave, c.data,
                             _ev((ARQ_CONSULTAS, c.linha), *[(ARQ_ITENS, i.linha) for i in itens]),
                             "Atendimento cancelado com item(ns) de fatura: %s."
                             % ", ".join(sorted({i.item_codigo for i in itens})), False))
    return out


# --------------------------------------------------------------- Controlados
def k01_controlado_conferir(ix):
    out = []
    por_chave = defaultdict(list)
    for i in ix.dados.itens:
        if i.item_codigo in ix.controlados:
            por_chave[(i.consulta_id, i.item_codigo)].append(i)
    for (cid, item) in sorted(por_chave):
        itens = por_chave[(cid, item)]
        c = ix.consulta.get(cid)
        vet = c.veterinario_id if c else SEM_CONSULTA
        data = c.data if c else ix.dados.data   # orfa: data do export, para a decisao nao valer em outro dia
        qtd = sum(i.quantidade for i in itens)
        evid = [(ARQ_CONSULTAS, c.linha)] if c else []
        evid += [(ARQ_ITENS, i.linha) for i in itens]
        out.append(_pend("K01_CONTROLADO_CONFERIR", SEV_ACAO, cid, vet, "%s*%d" % (item, qtd), data,
                         _ev(*evid),
                         "Item controlado %s na fatura: conferencia manual obrigatoria contra o livro/sistema "
                         "de controle (a ferramenta nao registra baixa nem escrituracao)." % item, True))
    return out


FUNCOES = (p01_prontuario_aberto, p02_prontuario_incompleto, p03_fechado_retroativo,
           c01_consulta_sem_fatura, c02_fatura_sem_consulta, c03_procedimento_sem_item,
           c04_item_sem_procedimento, c05_cancelada_com_itens, k01_controlado_conferir)


def aplicar_regras(dados):
    """Executa todas as regras e devolve as pendencias em ordem deterministica."""
    ix = _Indice(dados)
    todas = []
    for fn in FUNCOES:
        todas.extend(fn(ix))
    vistos = {}
    for p in todas:
        if p.finding_id in vistos:  # colisao de hash (32 bits): falhar alto em vez de sobrescrever em silencio
            raise ErroEntrada("regras", None, "finding_id duplicado %s (%s e %s): decisoes poderiam valer "
                              "para a pendencia errada" % (p.finding_id, vistos[p.finding_id], p.codigo))
        vistos[p.finding_id] = p.codigo
    todas.sort(key=lambda p: (p.veterinario_id, p.consulta_id, p.codigo, p.finding_id))
    return todas
