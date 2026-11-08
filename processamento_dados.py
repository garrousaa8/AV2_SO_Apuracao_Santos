import os
import pandas as pandas

from collections import defaultdict
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor
)

from config import (
    CIDADE_PARA_FILTRAR,
    TAMANHO_DO_BLOCO_DE_LINHAS,
    COLUNAS_NECESSARIAS
)

def processar_bloco_de_dados(bloco_de_dados):
    if 'NM_MUNICIPIO' not in bloco_de_dados.columns:
        return 0, 0, {}, {}, {}, {}

    filtro_santos = (
        bloco_de_dados['NM_MUNICIPIO']
        .astype(str)
        .str.strip()
        .str.upper() == CIDADE_PARA_FILTRAR
    )

    dados_filtrados_santos = bloco_de_dados[
        filtro_santos
    ].copy()

    if dados_filtrados_santos.empty:
        return 0, 0, {}, {}, {}, {}

    coluna_votos = pandas.to_numeric(
        dados_filtrados_santos[
            'QT_VOTOS_NOMINAIS_VALIDOS'
        ],
        errors='coerce'
    ).fillna(0)

    dados_filtrados_santos[
        'QT_VOTOS_NOMINAIS_VALIDOS'
    ] = coluna_votos

    total_de_votos_no_bloco = float(
        coluna_votos.sum()
    )

    quantidade_de_registros_no_bloco = int(
        len(dados_filtrados_santos)
    )

    agrupamento_partido = dados_filtrados_santos.groupby(
        'SG_PARTIDO'
    )['QT_VOTOS_NOMINAIS_VALIDOS']

    soma_votos_por_partido = (
        agrupamento_partido.sum().to_dict()
    )

    quantidade_registros_por_partido = (
        agrupamento_partido.count().to_dict()
    )

    agrupamento_cargo = dados_filtrados_santos.groupby(
        'DS_CARGO'
    )['QT_VOTOS_NOMINAIS_VALIDOS']

    soma_votos_por_cargo = (
        agrupamento_cargo.sum().to_dict()
    )

    quantidade_registros_por_cargo = (
        agrupamento_cargo.count().to_dict()
    )

    return (
        total_de_votos_no_bloco,
        quantidade_de_registros_no_bloco,
        soma_votos_por_partido,
        quantidade_registros_por_partido,
        soma_votos_por_cargo,
        quantidade_registros_por_cargo
    )

def consolidar_resultados_finais(
    lista_de_resultados_dos_blocos
):
    soma_total_de_votos_global = 0.0
    quantidade_total_de_registros_global = 0

    soma_acumulada_por_partido = defaultdict(float)
    quantidade_acumulada_por_partido = defaultdict(int)

    soma_acumulada_por_cargo = defaultdict(float)
    quantidade_acumulada_por_cargo = defaultdict(int)

    for (
        votos_bloco,
        registros_bloco,
        soma_partidos_bloco,
        qtd_partidos_bloco,
        soma_cargos_bloco,
        qtd_cargos_bloco
    
    ) in lista_de_resultados_dos_blocos:

        soma_total_de_votos_global += votos_bloco

        quantidade_total_de_registros_global += registros_bloco

        for partido, soma_votos in soma_partidos_bloco.items():

            soma_acumulada_por_partido[partido] += soma_votos

            quantidade_acumulada_por_partido[partido] += (
                qtd_partidos_bloco[partido]
            )

        for cargo, soma_votos in soma_cargos_bloco.items():

            soma_acumulada_por_cargo[cargo] += soma_votos

            quantidade_acumulada_por_cargo[cargo] += (
                qtd_cargos_bloco[cargo]
            )

    if quantidade_total_de_registros_global == 0:
        return (
            0.0,
            ("Sem registros", 0.0),
            ("Sem registros", 0.0)
        )

    media_geral_do_municipio = (
        soma_total_de_votos_global /
        quantidade_total_de_registros_global
    )

    medias_por_partido = {
        partido:
        soma_acumulada_por_partido[partido] /
        quantidade_acumulada_por_partido[partido]

        for partido in soma_acumulada_por_partido

        if quantidade_acumulada_por_partido[partido] > 0
    }

    partido_com_maior_media = max(
        medias_por_partido.items(),
        key = lambda par_nome_e_media : par_nome_e_media[1]
    )

    medias_por_cargo = {
        cargo:
        soma_acumulada_por_cargo[cargo] / quantidade_acumulada_por_cargo[cargo]

        for cargo in soma_acumulada_por_cargo

        if quantidade_acumulada_por_cargo[cargo] > 0
    }

    cargo_com_maior_media = max(
        medias_por_cargo.items(),
        key = lambda par_nome_e_media: par_nome_e_media[1]
    )

    return (
        media_geral_do_municipio,
        partido_com_maior_media,
        cargo_com_maior_media
    )

def ler_blocos_do_arquivo(caminho_do_arquivo):

    leitor_de_blocos_csv = pandas.read_csv(
        caminho_do_arquivo,
        sep=';',
        encoding='iso-8859-1',
        usecols=COLUNAS_NECESSARIAS,
        chunksize=TAMANHO_DO_BLOCO_DE_LINHAS,
        low_memory=False
    )

    return list(leitor_de_blocos_csv)

def executar_com_multiprocessing(caminho_do_arquivo):

    lista_de_blocos = ler_blocos_do_arquivo(
        caminho_do_arquivo
    )

    quantidade_de_nucleos = os.cpu_count() or 4

    with ProcessPoolExecutor(
        max_workers=quantidade_de_nucleos
    ) as executor_de_processos:

        resultados_dos_blocos = list(
            executor_de_processos.map(
                processar_bloco_de_dados,
                lista_de_blocos
            )
        )

    return consolidar_resultados_finais(resultados_dos_blocos)

def executar_com_multithreading(caminho_do_arquivo):

    lista_de_blocos = ler_blocos_do_arquivo(
        caminho_do_arquivo
    )

    quantidade_de_threads = (os.cpu_count() or 4) * 2

    with ThreadPoolExecutor(
        max_workers=quantidade_de_threads
    ) as executor_de_threads:

        resultados_dos_blocos = list(
            executor_de_threads.map(
                processar_bloco_de_dados,
                lista_de_blocos
            )
        )

    return consolidar_resultados_finais(resultados_dos_blocos)