import os

CAMINHO_DO_ARQUIVO_CSV = os.path.join(
    "dados",
    "votacao_candidato_munzona_2026_SP.csv"
)

CIDADE_PARA_FILTRAR = "SANTOS"

TAMANHO_DO_BLOCO_DE_LINHAS = 100000

COLUNAS_NECESSARIAS = [
    'NM_MUNICIPIO',
    'QT_VOTOS_NOMINAIS_VALIDOS',
    'SG_PARTIDO',
    'DS_CARGO'
]