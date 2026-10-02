"""Relatorio Markdown e CSV de pendencias. Saida deterministica (RF-01, RF-11, RF-12).

Imprime apenas codigos opacos. Nada aqui escreve em prontuario ou fatura.
"""

import csv
import io
import os
from collections import defaultdict
from pathlib import Path

from .decisoes import situacao
from .regras import CODIGOS

COLUNAS_CSV = ("finding_id", "codigo", "severidade", "consulta_id", "veterinario_id", "evidencia",
               "mensagem", "regra_ref", "exige_veterinario", "status", "decisao", "papel",
               "responsavel", "hash_regras", "hash_campos")


def _md(texto):
    return str(texto).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def gravar_atomico(caminho, texto):
    caminho = Path(caminho)
    tmp = caminho.with_name(caminho.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    os.replace(tmp, caminho)


def gerar_csv(dados, pendencias, status):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUNAS_CSV)
    for p in pendencias:
        st, reg = status[p.finding_id]
        w.writerow([p.finding_id, p.codigo, p.severidade, p.consulta_id, p.veterinario_id, p.evidencia,
                    p.mensagem, p.regra_ref, "S" if p.exige_veterinario else "N", st,
                    reg["decisao"] if reg else "", reg["papel"] if reg else "",
                    reg["responsavel"] if reg else "", dados.hash_regras, dados.hash_campos])
    return buf.getvalue()


def gerar_md(dados, pendencias, registros, estado, agora):
    status = situacao(pendencias, registros)
    por_id = {p.finding_id: p for p in pendencias}
    contagem = defaultdict(lambda: defaultdict(int))
    for p in pendencias:
        st, reg = status[p.finding_id]
        c = contagem[p.codigo]
        c["total"] += 1
        c[st] += 1
        if reg and reg["decisao"] == "ignorar":
            c["ignorada"] += 1
    n = lambda st: sum(1 for s, _ in status.values() if s == st)
    versoes = sorted({c.versao for c in dados.campos_obrigatorios})
    fontes = sorted({c.fonte_norma for c in dados.campos_obrigatorios})

    L = []
    L.append("# Fechamento do dia %s" % dados.data)
    L.append("")
    L.append("> Dados fictícios / de exemplo. Este relatório é só leitura: a ferramenta não escreve em "
             "prontuário nem em fatura. Não use com dados reais de pacientes ou tutores.")
    L.append("")
    L.append("- Gerado em: %s" % agora)
    L.append("- **Estado do dia: %s**" % estado)
    L.append("- Pendências abertas: %d (sem decisão: %d; encaminhadas, ainda não resolvidas no dado: %d)"
             % (n("aberta") + n("encaminhada"), n("aberta"), n("encaminhada")))
    L.append("- Pendências decididas (terminal, com motivo): %d" % n("decidida"))
    L.append("- Informativas (não bloqueiam): %d" % n("info"))
    L.append("- regras.csv sha256: `%s`" % dados.hash_regras)
    L.append("- campos_obrigatorios.csv sha256: `%s` (versão do checklist: %s; fonte_norma: %s)"
             % (dados.hash_campos, ", ".join(versoes), ", ".join(fontes)))
    L.append("- Consultas lidas: %d; procedimentos: %d; itens de fatura: %d"
             % (len(dados.consultas), len(dados.procedimentos), len(dados.itens)))
    if "EXEMPLO_FICTICIO" in fontes:
        L.append("- Aviso: o checklist em uso é EXEMPLO_FICTICIO e não é a lista oficial do CFMV.")
    L.append("")
    L.append("## Totais por código")
    L.append("")
    L.append("| Código | Total | Abertas | Decididas | Ignoradas | % ignoradas |")
    L.append("|---|---|---|---|---|---|")
    for cod in CODIGOS:
        if cod not in contagem:
            continue
        c = contagem[cod]
        ab = c["aberta"] + c["encaminhada"]
        pct = "%d%%" % round(100 * c["ignorada"] / c["total"])
        L.append("| %s | %d | %d | %d | %d | %s |" % (cod, c["total"], ab, c["decidida"], c["ignorada"], pct))
    if not contagem:
        L.append("| (nenhuma pendência) | 0 | 0 | 0 | 0 | - |")
    L.append("")

    por_vet = defaultdict(list)
    for p in pendencias:
        por_vet[p.veterinario_id].append(p)
    for vet in sorted(por_vet):
        L.append("## Veterinário %s" % vet)
        L.append("")
        for p in por_vet[vet]:
            st, reg = status[p.finding_id]
            rotulo = {"aberta": "ABERTA", "encaminhada": "ENCAMINHADA (não resolvida)",
                      "decidida": "DECIDIDA", "info": "INFO"}[st]
            L.append("- **%s** `%s` consulta `%s` [%s | %s]" % (p.codigo, p.finding_id, p.consulta_id,
                                                              p.severidade, rotulo))
            L.append("  - %s" % p.mensagem)
            L.append("  - Evidência: %s" % p.evidencia)
            if p.regra_ref:
                L.append("  - Regra: %s" % p.regra_ref)
            if p.exige_veterinario and p.severidade != "info":
                L.append("  - Decisão restrita ao papel `veterinario`.")
            if reg:
                L.append("  - Última decisão: %s por %s (%s) em %s%s"
                         % (reg["decisao"], reg["responsavel"], reg["papel"], reg["registrado_em"],
                            (" — motivo: " + reg["motivo"]) if reg.get("motivo") else ""))
        L.append("")
    if not por_vet:
        L.append("Nenhuma pendência.")
        L.append("")

    L.append("## Decisões registradas")
    L.append("")
    aplicaveis = [r for r in registros if r["finding_id"] in por_id]
    if aplicaveis:
        L.append("| Finding | Código | Consulta | Decisão | Papel | Responsável | Registrado em | Motivo |")
        L.append("|---|---|---|---|---|---|---|---|")
        for r in aplicaveis:
            p = por_id[r["finding_id"]]
            L.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % tuple(_md(x) for x in (
                r["finding_id"], p.codigo, p.consulta_id, r["decisao"], r["papel"], r["responsavel"],
                r["registrado_em"], r.get("motivo", ""))))
    else:
        L.append("Nenhuma decisão registrada para as pendências desta execução.")
    orfas = len(registros) - len(aplicaveis)
    if orfas:
        L.append("")
        L.append("%d decisão(ões) do log não se aplicam a nenhuma pendência atual (o dado foi corrigido "
                 "ou o conteúdo da pendência mudou: decisão presa à evidência)." % orfas)
    L.append("")
    return "\n".join(L)
