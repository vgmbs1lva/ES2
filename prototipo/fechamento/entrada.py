"""Leitura e validacao dos CSVs de entrada. Falha alto (ErroEntrada) antes de qualquer saida (RF-03).

Somente leitura (RF-02). Somente codigos opacos sao aceitos como identificadores (RF-12).
"""

import csv
import hashlib
import io
import re
from datetime import datetime
from pathlib import Path

from .erros import ErroEntrada
from .modelos import (CampoObrigatorio, Consulta, Dados, ItemFatura,
                      Procedimento, Regra)

ARQ_CONSULTAS = "consultas.csv"
ARQ_PROCEDIMENTOS = "procedimentos_realizados.csv"
ARQ_ITENS = "itens_fatura.csv"
ARQ_REGRAS = "regras.csv"
ARQ_CAMPOS = "campos_obrigatorios.csv"

COLUNAS_CONSULTAS = ("consulta_id", "data", "veterinario_id", "status_atendimento",
                     "status_prontuario", "fechado_em")
COLUNAS_PROCEDIMENTOS = ("consulta_id", "procedimento_codigo")
COLUNAS_ITENS = ("consulta_id", "item_codigo", "quantidade")
COLUNAS_REGRAS = ("procedimento_codigo", "item_codigo", "grupo_alternativa",
                  "ato_clinico", "controlado")
COLUNAS_CAMPOS = ("campo", "fonte_norma", "versao")
PREFIXO_CAMPO = "campo_"

# Cabecalhos que sugerem dado pessoal sao recusados (RF-12, AC-20).
FRAGMENTOS_PROIBIDOS = ("cpf", "telefone", "celular", "email", "tutor", "endereco", "cnpj")
TOKENS_PROIBIDOS = ("nome", "fone", "rg")

_RE_ID = re.compile(r"^[A-Za-z0-9_-]{1,32}$")
_RE_CAMPO = re.compile(r"^[a-z0-9_]{1,40}$")


def sha256_arquivo(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def _valida_cabecalho(arquivo, cab, obrigatorias, aceita_campo_prefixo=False):
    if len(set(cab)) != len(cab):
        raise ErroEntrada(arquivo, 1, "coluna duplicada no cabecalho")
    for col in cab:
        baixo = col.lower()
        tokens = [t for t in re.split(r"[^a-z0-9]+", baixo) if t]
        if any(f in baixo for f in FRAGMENTOS_PROIBIDOS) or any(t in TOKENS_PROIBIDOS for t in tokens):
            raise ErroEntrada(arquivo, 1, "coluna '%s' sugere dado pessoal; o MVP aceita so codigos opacos" % col)
    faltando = [c for c in obrigatorias if c not in cab]
    if faltando:
        raise ErroEntrada(arquivo, 1, "coluna(s) faltando: %s" % ", ".join(faltando))
    extras = [c for c in cab if c not in obrigatorias
              and not (aceita_campo_prefixo and c.startswith(PREFIXO_CAMPO) and len(c) > len(PREFIXO_CAMPO))]
    if extras:
        raise ErroEntrada(arquivo, 1, "coluna(s) nao aceita(s): %s" % ", ".join(extras))


def _ler_csv(pasta, arquivo, obrigatorias, aceita_campo_prefixo=False):
    caminho = Path(pasta) / arquivo
    if not caminho.is_file():
        raise ErroEntrada(arquivo, None, "arquivo ausente em %s" % pasta)
    try:
        texto = caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as e:
        raise ErroEntrada(arquivo, None, "nao esta em UTF-8 (%s)" % e.reason)
    # newline="": quebras DENTRO de campo entre aspas (e U+2028/U+0085) nao viram registros nem somem
    leitor = csv.reader(io.StringIO(texto, newline=""), delimiter=",")
    try:
        cab = [c.strip() for c in next(leitor)]
    except StopIteration:
        raise ErroEntrada(arquivo, 1, "arquivo vazio (sem cabecalho)")
    if len(cab) == 1 and ";" in cab[0]:
        raise ErroEntrada(arquivo, 1, "o separador parece ser ';' (comum em CSV do Excel pt-BR); "
                                      "o esperado e ',' (exporte como CSV UTF-8 separado por virgula)")
    _valida_cabecalho(arquivo, cab, obrigatorias, aceita_campo_prefixo)
    linhas = []
    for valores in leitor:
        n = leitor.line_num
        if not valores or all(not v.strip() for v in valores):
            continue
        if len(valores) != len(cab):
            raise ErroEntrada(arquivo, n, "esperadas %d colunas, encontradas %d" % (len(cab), len(valores)))
        linhas.append((n, dict(zip(cab, (v.strip() for v in valores)))))
    return cab, linhas


def _id(arquivo, n, linha, coluna):
    v = linha[coluna]
    if not _RE_ID.match(v):
        raise ErroEntrada(arquivo, n, "%s='%s' invalido: use codigo opaco (letras, digitos, _ ou -, ate 32)" % (coluna, v))
    return v


def _sn(arquivo, n, linha, coluna):
    v = linha[coluna]
    if v not in ("S", "N"):
        raise ErroEntrada(arquivo, n, "%s='%s' invalido: esperado S ou N" % (coluna, v))
    return v


def _data(arquivo, n, linha, coluna):
    v = linha[coluna]
    try:
        datetime.strptime(v, "%Y-%m-%d")
    except ValueError:
        raise ErroEntrada(arquivo, n, "%s='%s' invalida: esperado YYYY-MM-DD" % (coluna, v))
    if len(v) != 10:
        raise ErroEntrada(arquivo, n, "%s='%s' invalida: esperado YYYY-MM-DD" % (coluna, v))
    return v


def validar_data_cli(valor):
    try:
        if len(valor) != 10:
            raise ValueError
        datetime.strptime(valor, "%Y-%m-%d")
    except ValueError:
        raise ErroEntrada("--data", None, "'%s' invalida: esperado YYYY-MM-DD" % valor)
    return valor


def carregar(pasta, data):
    """Le os 5 CSVs, valida tudo e devolve Dados. Levanta ErroEntrada no primeiro problema."""
    validar_data_cli(data)

    # checklist (versionado) primeiro: define quais colunas campo_* sao exigidas
    _, lin = _ler_csv(pasta, ARQ_CAMPOS, COLUNAS_CAMPOS)
    campos = []
    vistos = set()
    for n, r in lin:
        c = r["campo"]
        if not _RE_CAMPO.match(c):
            raise ErroEntrada(ARQ_CAMPOS, n, "campo='%s' invalido (use [a-z0-9_], sem o prefixo 'campo_')" % c)
        if c in vistos:
            raise ErroEntrada(ARQ_CAMPOS, n, "campo '%s' duplicado" % c)
        vistos.add(c)
        if not r["fonte_norma"] or not r["versao"]:
            raise ErroEntrada(ARQ_CAMPOS, n, "fonte_norma e versao sao obrigatorias")
        campos.append(CampoObrigatorio(c, r["fonte_norma"], r["versao"], n))
    if not campos:
        raise ErroEntrada(ARQ_CAMPOS, None, "checklist vazio (desligaria P02 em silencio)")

    cab, lin = _ler_csv(pasta, ARQ_CONSULTAS, COLUNAS_CONSULTAS, aceita_campo_prefixo=True)
    colunas_campo = [c for c in cab if c.startswith(PREFIXO_CAMPO)]
    for c in campos:
        if PREFIXO_CAMPO + c.campo not in cab:
            raise ErroEntrada(ARQ_CONSULTAS, 1, "coluna '%s%s' faltando (exigida por %s:L%d)"
                              % (PREFIXO_CAMPO, c.campo, ARQ_CAMPOS, c.linha))
    consultas = []
    ids = {}
    for n, r in lin:
        cid = _id(ARQ_CONSULTAS, n, r, "consulta_id")
        if cid in ids:
            raise ErroEntrada(ARQ_CONSULTAS, n, "consulta_id '%s' duplicado (primeira ocorrencia na linha %d)" % (cid, ids[cid]))
        ids[cid] = n
        d = _data(ARQ_CONSULTAS, n, r, "data")
        if d != data:
            raise ErroEntrada(ARQ_CONSULTAS, n, "data=%s difere de --data %s (um export por dia)" % (d, data))
        vet = _id(ARQ_CONSULTAS, n, r, "veterinario_id")
        sa = r["status_atendimento"]
        if sa not in ("realizado", "cancelado"):
            raise ErroEntrada(ARQ_CONSULTAS, n, "status_atendimento='%s' invalido: esperado realizado ou cancelado" % sa)
        sp = r["status_prontuario"]
        if sp not in ("aberto", "fechado"):
            raise ErroEntrada(ARQ_CONSULTAS, n, "status_prontuario='%s' invalido: esperado aberto ou fechado" % sp)
        fe = r["fechado_em"]
        if sp == "aberto" and fe:
            raise ErroEntrada(ARQ_CONSULTAS, n, "prontuario aberto nao pode ter fechado_em ('%s')" % fe)
        if sp == "fechado":
            if not fe:
                raise ErroEntrada(ARQ_CONSULTAS, n, "prontuario fechado exige fechado_em")
            try:
                datetime.strptime(fe, "%Y-%m-%dT%H:%M")
            except ValueError:
                raise ErroEntrada(ARQ_CONSULTAS, n, "fechado_em='%s' invalido: esperado YYYY-MM-DDTHH:MM" % fe)
            if len(fe) != 16:
                raise ErroEntrada(ARQ_CONSULTAS, n, "fechado_em='%s' invalido: esperado YYYY-MM-DDTHH:MM" % fe)
            if fe[:10] < d:
                raise ErroEntrada(ARQ_CONSULTAS, n, "fechado_em=%s e anterior a data do atendimento (%s): "
                                  "dado inconsistente" % (fe, d))
        campos_linha = tuple((c[len(PREFIXO_CAMPO):], _sn(ARQ_CONSULTAS, n, r, c)) for c in colunas_campo)
        consultas.append(Consulta(cid, d, vet, sa, sp, fe, campos_linha, n))

    _, lin = _ler_csv(pasta, ARQ_PROCEDIMENTOS, COLUNAS_PROCEDIMENTOS)
    procs = []
    for n, r in lin:
        cid = _id(ARQ_PROCEDIMENTOS, n, r, "consulta_id")
        if cid not in ids:
            raise ErroEntrada(ARQ_PROCEDIMENTOS, n, "consulta_id '%s' nao existe em %s" % (cid, ARQ_CONSULTAS))
        procs.append(Procedimento(cid, _id(ARQ_PROCEDIMENTOS, n, r, "procedimento_codigo"), n))

    _, lin = _ler_csv(pasta, ARQ_ITENS, COLUNAS_ITENS)
    itens = []
    for n, r in lin:
        cid = _id(ARQ_ITENS, n, r, "consulta_id")  # inexistente => C02, nao erro
        item = _id(ARQ_ITENS, n, r, "item_codigo")
        q = r["quantidade"]
        if not re.match(r"^[0-9]+$", q) or int(q) <= 0:
            raise ErroEntrada(ARQ_ITENS, n, "quantidade='%s' invalida: esperado inteiro > 0" % q)
        itens.append(ItemFatura(cid, item, int(q), n))

    _, lin = _ler_csv(pasta, ARQ_REGRAS, COLUNAS_REGRAS)
    if not lin:
        raise ErroEntrada(ARQ_REGRAS, None, "tabela de regras vazia (desligaria C03, C04 e K01 em silencio)")
    regras = []
    pares = {}
    for n, r in lin:
        proc = _id(ARQ_REGRAS, n, r, "procedimento_codigo")
        item = _id(ARQ_REGRAS, n, r, "item_codigo")
        grupo = r["grupo_alternativa"]
        if grupo and not _RE_ID.match(grupo):
            raise ErroEntrada(ARQ_REGRAS, n, "grupo_alternativa='%s' invalido" % grupo)
        if (proc, item) in pares:
            raise ErroEntrada(ARQ_REGRAS, n, "par (%s, %s) duplicado (linha %d)" % (proc, item, pares[(proc, item)]))
        pares[(proc, item)] = n
        regras.append(Regra(proc, item, grupo, _sn(ARQ_REGRAS, n, r, "ato_clinico") == "S",
                            _sn(ARQ_REGRAS, n, r, "controlado") == "S", n))

    return Dados(tuple(consultas), tuple(procs), tuple(itens), tuple(regras), tuple(campos),
                 sha256_arquivo(Path(pasta) / ARQ_REGRAS), sha256_arquivo(Path(pasta) / ARQ_CAMPOS), data)
