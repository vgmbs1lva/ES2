"""CLI. Codigos de saida: verificar 0=CONFERIDO 1=PENDENTE 2=erro de entrada;
decidir/aprovar/rejeitar/exportar/rascunho 0=ok 2=erro de entrada 3=rejeitado por regra."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from . import decisoes, rascunhos, relatorio
from .entrada import carregar
from .erros import DecisaoRejeitada, ErroEntrada
from .redator import DESTINOS, obter_redator
from .regras import aplicar_regras

PAPEIS = decisoes.PAPEIS


def _agora(valor):
    if valor is None:
        return datetime.now().isoformat(timespec="seconds")
    try:
        datetime.fromisoformat(valor)
    except ValueError:
        raise ErroEntrada("--agora", None, "'%s' invalido: esperado data-hora ISO" % valor)
    return valor


def _parser():
    ap = argparse.ArgumentParser(
        prog="python -m fechamento",
        description="Fechamento do dia (prontuario x cobranca). MVP local e offline; so dados ficticios. "
                    "A ferramenta nunca escreve em prontuario nem em fatura.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verificar", help="cruza consultas x fatura x regras e gera relatorio + pendencias")
    v.add_argument("--data", required=True, help="YYYY-MM-DD")
    v.add_argument("--entrada", required=True, help="pasta com os 5 CSVs")
    v.add_argument("--saida", required=True, help="pasta de saida (relatorio, pendencias, decisoes)")
    v.add_argument("--agora", help="data-hora ISO fixa (determinismo)")

    d = sub.add_parser("decidir", help="registra decisao humana sobre uma pendencia (log append-only)")
    d.add_argument("--finding", required=True)
    d.add_argument("--decisao", required=True, choices=decisoes.DECISOES)
    d.add_argument("--motivo", default="")
    d.add_argument("--papel", required=True, choices=PAPEIS)
    d.add_argument("--responsavel", required=True)
    d.add_argument("--saida", required=True)
    d.add_argument("--agora")

    r = sub.add_parser("rascunho", help="gera RASCUNHO de texto (tutor/prontuario); nada sai sem aprovacao")
    r.add_argument("--finding", required=True)
    r.add_argument("--destino", required=True, choices=DESTINOS)
    r.add_argument("--saida", required=True)
    r.add_argument("--redator", default="stub", help="'stub' (padrao, offline) ou 'modulo:Classe'")
    r.add_argument("--agora")

    a = sub.add_parser("aprovar", help="aprovacao explicita do veterinario sobre um rascunho")
    a.add_argument("--rascunho", required=True)
    a.add_argument("--papel", required=True, choices=PAPEIS)
    a.add_argument("--responsavel", required=True)
    a.add_argument("--confirmo", action="store_true", help="declara que leu e aprova o texto exato")
    a.add_argument("--texto-final", help="arquivo UTF-8 com o texto final (obrigatorio se houver [PREENCHER ...])")
    a.add_argument("--saida", required=True)
    a.add_argument("--agora")

    j = sub.add_parser("rejeitar", help="rejeita um rascunho (motivo obrigatorio)")
    j.add_argument("--rascunho", required=True)
    j.add_argument("--papel", required=True, choices=PAPEIS)
    j.add_argument("--responsavel", required=True)
    j.add_argument("--motivo", required=True)
    j.add_argument("--saida", required=True)
    j.add_argument("--agora")

    e = sub.add_parser("exportar", help="grava arquivo local do texto APROVADO (nao envia nem lanca em lugar nenhum)")
    e.add_argument("--rascunho", required=True)
    e.add_argument("--saida", required=True)
    return ap


def _cmd_verificar(args):
    agora = _agora(args.agora)
    dados = carregar(args.entrada, args.data)          # falha alto: nada e escrito antes disto
    pendencias = aplicar_regras(dados)
    registros = decisoes.ler_log(args.saida)
    status = decisoes.situacao(pendencias, registros)
    estado = decisoes.estado_do_dia(status)
    md = relatorio.gerar_md(dados, pendencias, registros, estado, agora)
    csv_txt = relatorio.gerar_csv(dados, pendencias, status)
    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)
    relatorio.gravar_atomico(saida / ("pendencias_%s.csv" % args.data), csv_txt)
    relatorio.gravar_atomico(saida / ("relatorio_%s.md" % args.data), md)
    abertas = sum(1 for s, _ in status.values() if s in ("aberta", "encaminhada"))
    print("Estado do dia %s: %s (%d pendencia(s) aberta(s), %d total)" % (args.data, estado, abertas, len(pendencias)))
    print("Relatorio: %s" % (saida / ("relatorio_%s.md" % args.data)))
    print("Pendencias: %s" % (saida / ("pendencias_%s.csv" % args.data)))
    return 0 if estado == "CONFERIDO" else 1


def _info(saida, finding):
    info = decisoes.localizar_finding(saida, finding)
    if info is None:
        raise ErroEntrada(finding, None, "finding desconhecido em %s/pendencias_*.csv: rode 'verificar' antes" % saida)
    return info


def _cmd_decidir(args):
    agora = _agora(args.agora)
    info = _info(args.saida, args.finding)
    try:
        reg = decisoes.registrar(args.saida, info, args.decisao, args.motivo, args.papel, args.responsavel, agora)
    except DecisaoRejeitada as e:
        print("DECISAO REJEITADA: %s" % e, file=sys.stderr)
        return 3
    print("Decisao registrada em %s: %s %s por %s (%s)" % (decisoes.ARQ_LOG, reg["decisao"], reg["finding_id"],
                                                          reg["responsavel"], reg["papel"]))
    if reg["decisao"] == "encaminhado":
        print("Nota: 'encaminhado' NAO encerra a pendencia; ela some quando o dado for corrigido no PIMS "
              "e um novo 'verificar' for rodado.")
    else:
        print("Rode 'verificar' de novo para atualizar o estado do dia.")
    return 0


def _cmd_rascunho(args):
    agora = _agora(args.agora)
    info = _info(args.saida, args.finding)
    try:
        redator = obter_redator(args.redator)
        rid, texto, novo = rascunhos.criar(args.saida, info, args.destino, redator, agora)
    except DecisaoRejeitada as e:
        print("RASCUNHO REJEITADO: %s" % e, file=sys.stderr)
        return 3
    print("Rascunho %s (%s) %s. ESTADO: RASCUNHO - NAO ENVIAR, NAO LANCAR NO PRONTUARIO." % (
        rid, redator.nome, "criado" if novo else "ja existia"))
    print("Para liberar: o veterinario revisa/edita e roda 'aprovar --confirmo'; depois 'exportar'.")
    print("-----")
    print(texto)
    return 0


def _cmd_aprovar(args):
    agora = _agora(args.agora)
    final = None
    if args.texto_final:
        p = Path(args.texto_final)
        if not p.is_file():
            raise ErroEntrada(args.texto_final, None, "arquivo ausente")
        try:
            final = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ErroEntrada(args.texto_final, None, "nao esta em UTF-8")
    try:
        ev = rascunhos.aprovar(args.saida, args.rascunho, args.papel, args.responsavel, args.confirmo, agora, final)
    except DecisaoRejeitada as e:
        print("APROVACAO REJEITADA: %s" % e, file=sys.stderr)
        return 3
    print("Rascunho %s APROVADO por %s (%s). Use 'exportar' para gravar o arquivo local." % (
        ev["rascunho_id"], ev["responsavel"], ev["papel"]))
    return 0


def _cmd_rejeitar(args):
    agora = _agora(args.agora)
    try:
        rascunhos.rejeitar(args.saida, args.rascunho, args.papel, args.responsavel, args.motivo, agora)
    except DecisaoRejeitada as e:
        print("REJEICAO RECUSADA: %s" % e, file=sys.stderr)
        return 3
    print("Rascunho %s REJEITADO." % args.rascunho)
    return 0


def _cmd_exportar(args):
    try:
        caminho = rascunhos.exportar(args.saida, args.rascunho)
    except DecisaoRejeitada as e:
        print("EXPORTACAO RECUSADA: %s" % e, file=sys.stderr)
        return 3
    print("Texto aprovado gravado em %s. Envio ao tutor / lancamento no prontuario continuam MANUAIS." % caminho)
    return 0


_CMDS = {"verificar": _cmd_verificar, "decidir": _cmd_decidir, "rascunho": _cmd_rascunho,
         "aprovar": _cmd_aprovar, "rejeitar": _cmd_rejeitar, "exportar": _cmd_exportar}


def main(argv=None):
    try:
        args = _parser().parse_args(argv)
    except SystemExit as e:  # argparse: 0 em --help, 2 em uso invalido
        return e.code if isinstance(e.code, int) else 2
    try:
        return _CMDS[args.cmd](args)
    except ErroEntrada as e:
        print("ERRO DE ENTRADA: %s" % e, file=sys.stderr)
        return 2
