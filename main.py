import os
import time

from config import CAMINHO_DO_ARQUIVO_CSV
from processamento_dados import (
    executar_com_multiprocessing,
    executar_com_multithreading
)

if __name__ == "__main__":

    if not os.path.exists(CAMINHO_DO_ARQUIVO_CSV):

        print(
            f"[ERRO] O arquivo '{CAMINHO_DO_ARQUIVO_CSV}' "
            f"não foi encontrado."
        )

        exit(1)

    print("Processando dados de Santos(SP)...")

    instante_inicial = time.perf_counter()

    (
        media_geral,
        partido_vencedor,
        cargo_vencedor
    ) = executar_com_multiprocessing(
        CAMINHO_DO_ARQUIVO_CSV
    )

    tempo_processos = time.perf_counter() - instante_inicial

    instante_inicial = time.perf_counter()

    executar_com_multithreading(
        CAMINHO_DO_ARQUIVO_CSV
    )

    tempo_threads = time.perf_counter() - instante_inicial

    print(
        "Processamento concluído! "
        "Exibindo o Dashboard Matplotlib..."
    )

    