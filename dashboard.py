import textwrap

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def exibir_painel_eleitoral_matplotlib(
    media_geral,
    partido_vencedor,
    cargo_vencedor,
    tempo_processos,
    tempo_threads
):

    from matplotlib.patches import FancyBboxPatch

    plt.style.use('dark_background')

    figura = plt.figure(
        figsize=(14, 8),
        facecolor='#0f172a'
    )

    figura.canvas.manager.set_window_title(
        "Dashboard Eleitoral TSE - Santos"
    )

    cor_do_cartao = '#1e293b'
    cor_do_texto = '#f8fafc'
    cor_secundaria = '#94a3b8'
    cor_de_destaque = '#38bdf8'

    titulo_principal = figura.suptitle(
        "DASHBOARD ELEITORAL TSE - MUNICÍPIO DE SANTOS (SP)",
        fontsize=17,
        fontweight='bold',
        color=cor_do_texto,
        y=0.96
    )

    def criar_cartao(
        titulo,
        valor,
        descricao,
        cor_do_valor,
        tamanho_da_fonte_do_valor
    ):

        eixo = figura.add_axes([0, 0, 1, 1])

        eixo.set_xlim(0, 1)
        eixo.set_ylim(0, 1)
        eixo.set_facecolor('none')
        eixo.axis('off')

        retangulo_do_cartao = FancyBboxPatch(
            (0.015, 0.04),
            0.97,
            0.92,
            boxstyle="round,pad=0.015,rounding_size=0.04",
            transform=eixo.transAxes,
            facecolor=cor_do_cartao,
            edgecolor='#334155',
            linewidth=1.5
        )

        eixo.add_patch(retangulo_do_cartao)

        texto_titulo = eixo.text(
            0.5,
            0.78,
            titulo,
            ha='center',
            va='center',
            fontsize=12,
            fontweight='bold',
            color=cor_secundaria
        )

        texto_titulo.set_clip_on(True)

        texto_valor = eixo.text(
            0.5,
            0.48,
            str(valor),
            ha='center',
            va='center',
            fontsize=tamanho_da_fonte_do_valor,
            fontweight='bold',
            color=cor_do_valor
        )

        texto_valor.set_clip_on(True)

        texto_descricao = None

        if descricao:

            texto_descricao = eixo.text(
                0.5,
                0.20,
                descricao,
                ha='center',
                va='center',
                fontsize=9,
                color='#cbd5e1'
            )

            texto_descricao.set_clip_on(True)

        return {
            'eixo': eixo,
            'titulo': texto_titulo,
            'valor': texto_valor,
            'descricao': texto_descricao
        }

    cartao_media_geral = criar_cartao(
        "MÉDIA GERAL DE VOTOS",
        f"{media_geral:.2f}",
        None,
        '#4ade80',
        23
    )

    nome_partido, media_partido = partido_vencedor

    cartao_partido = criar_cartao(
        "PARTIDO MAIOR MÉDIA",
        nome_partido,
        f"({media_partido:.2f} Média de votos/registro)",
        cor_de_destaque,
        21
    )

    nome_cargo, media_cargo = cargo_vencedor

    cartao_cargo = criar_cartao(
        "CARGO MAIOR MÉDIA",
        nome_cargo,
        f"({media_cargo:.2f} Média de votos/registro)",
        cor_de_destaque,
        19
    )

    cartoes = [
        cartao_media_geral,
        cartao_partido,
        cartao_cargo
    ]

    eixo_grafico = figura.add_axes([0, 0, 1, 1])
    eixo_grafico.set_facecolor(cor_do_cartao)

    abordagens = [
        'Multithreading\n(Threads)',
        'Multiprocessing\n(Processos)'
    ]

    tempos = [
        tempo_threads,
        tempo_processos
    ]

    cores_das_barras = [
        '#9333ea',
        '#0284c7'
    ]

    barras = eixo_grafico.barh(
        abordagens,
        tempos,
        color=cores_das_barras,
        height=0.45
    )

    eixo_grafico.set_title(
        'COMPARATIVO DE DESEMPENHO\n(MENOR TEMPO VENCE)',
        fontsize=13,
        fontweight='bold',
        color=cor_do_texto,
        pad=15
    )

    eixo_grafico.set_xlabel(
        'Tempo Total de Execução (Segundos)',
        fontsize=10,
        color=cor_secundaria,
        labelpad=8
    )

    eixo_grafico.tick_params(
        colors=cor_do_texto,
        labelsize=10,
        pad=8
    )

    eixo_grafico.grid(
        axis='x',
        linestyle='--',
        alpha=0.3,
        color='#475569'
    )

    eixo_grafico.set_axisbelow(True)

    maior_tempo = max(
        max(tempos),
        1.0
    )

    eixo_grafico.set_xlim(
        0,
        maior_tempo * 1.5
    )
    eixo_grafico.xaxis.set_major_locator(
        MaxNLocator(nbins=5, prune='upper')
    )

    textos_das_barras = []

    for barra in barras:

        largura_da_barra = barra.get_width()

        texto_da_barra = eixo_grafico.text(
            largura_da_barra + (maior_tempo * 0.015),
            barra.get_y() + barra.get_height() / 2,
            f'{largura_da_barra:.4f}s',
            va='center',
            ha='left',
            fontsize=10,
            fontweight='bold',
            color=cor_do_texto
        )

        textos_das_barras.append(texto_da_barra)

    eixo_faixa_resultado = figura.add_axes([0, 0, 1, 1])
    eixo_faixa_resultado.set_facecolor('none')
    eixo_faixa_resultado.axis('off')

    if tempo_processos < tempo_threads:

        diferenca_de_tempo = tempo_threads - tempo_processos

        percentual_de_diferenca = (
            diferenca_de_tempo / tempo_threads * 100
            if tempo_threads > 0 else 0
        )

        texto_resultado = (
            "MELHOR DESEMPENHO: MULTIPROCESSING (PROCESSOS)\n"
            f"A versão com processos executou em "
            f"{tempo_processos:.4f}s "
            f"({diferenca_de_tempo:.4f}s / {percentual_de_diferenca:.1f}% mais rápida que Threads)."
        )

        cor_da_borda_do_resultado = '#22c55e'

    elif tempo_threads < tempo_processos:

        diferenca_de_tempo = tempo_processos - tempo_threads

        percentual_de_diferenca = (
            diferenca_de_tempo / tempo_processos * 100
            if tempo_processos > 0 else 0
        )

        texto_resultado = (
            "MELHOR DESEMPENHO: MULTITHREADING (THREADS)\n"
            f"A versão com threads executou em "
            f"{tempo_threads:.4f}s "
            f"({diferenca_de_tempo:.4f}s / {percentual_de_diferenca:.1f}% mais rápida que Processos)."
        )

        cor_da_borda_do_resultado = '#22c55e'

    else:

        texto_resultado = (
            f"EMPATE: Ambas as abordagens levaram {tempo_processos:.4f}s."
        )

        cor_da_borda_do_resultado = '#eab308'

    texto_faixa_resultado = eixo_faixa_resultado.text(
        0.5,
        0.5,
        texto_resultado,
        ha='center',
        va='center',
        fontsize=11,
        fontweight='bold',
        color=cor_da_borda_do_resultado,
        transform=eixo_faixa_resultado.transAxes,
        multialignment='center',
        clip_on=True,
        bbox=dict(
            boxstyle='round,pad=0.5',
            facecolor='#0f172a',
            edgecolor=cor_da_borda_do_resultado,
            linewidth=2
        )
    )

    def ajustar_tamanho_da_fonte(
        texto,
        tamanho_base,
        largura_em_polegadas,
        fator_de_escala
    ):
        linhas_do_texto = texto.get_text().splitlines() or ['']
        quantidade_de_caracteres = max(
            len(linha) for linha in linhas_do_texto
        )
        largura_em_pontos = max(largura_em_polegadas * 72 * 0.94, 1)
        tamanho_maximo = largura_em_pontos / max(
            quantidade_de_caracteres * 0.68,
            1
        )
        texto.set_fontsize(
            max(5, min(tamanho_base * fator_de_escala, tamanho_maximo))
        )

    def ajustar_layout(evento=None):
        if evento is None:
            largura_da_janela, altura_da_janela = figura.get_size_inches()
        else:
            largura_da_janela = evento.width / figura.dpi
            altura_da_janela = evento.height / figura.dpi

        proporcao_da_janela = largura_da_janela / max(altura_da_janela, 1)
        fator_de_escala = max(
            0.4,
            min(largura_da_janela / 14, altura_da_janela / 8, 1.2)
        )
        modo_horizontal = (
            largura_da_janela >= 8.5 and proporcao_da_janela >= 1.2
        )

        if modo_horizontal:
            posicoes_dos_cartoes = [
                [0.045, 0.70, 0.29, 0.19],
                [0.355, 0.70, 0.29, 0.19],
                [0.665, 0.70, 0.29, 0.19]
            ]
            posicao_do_grafico = [
                0.12, 0.28, 0.76, 0.35
            ]
            posicao_x_do_titulo_do_grafico = 0.5
            posicao_da_faixa_resultado = [
                0.08, 0.07, 0.84, 0.13
            ]
            tamanho_fonte_titulo_principal = 17
            tamanho_fonte_titulo_cartao = 12
            tamanho_fonte_valor_cartao = 21
            tamanho_fonte_descricao_cartao = 9
            tamanho_fonte_titulo_grafico = 13
            tamanho_fonte_faixa_resultado = 11
        else:
            posicoes_dos_cartoes = [
                [0.08, 0.79, 0.84, 0.12],
                [0.08, 0.65, 0.84, 0.12],
                [0.08, 0.51, 0.84, 0.12]
            ]
            margem_esquerda_do_grafico = min(
                0.38,
                max(0.29, 1.8 / largura_da_janela)
            )
            posicao_do_grafico = [
                margem_esquerda_do_grafico,
                0.19,
                0.92 - margem_esquerda_do_grafico,
                0.26
            ]
            posicao_x_do_titulo_do_grafico = (
                (0.5 - margem_esquerda_do_grafico)
                / (0.92 - margem_esquerda_do_grafico)
            )
            posicao_da_faixa_resultado = [
                0.05, 0.025, 0.90, 0.105
            ]
            tamanho_fonte_titulo_principal = 14
            tamanho_fonte_titulo_cartao = 10
            tamanho_fonte_valor_cartao = 16
            tamanho_fonte_descricao_cartao = 8
            tamanho_fonte_titulo_grafico = 10
            tamanho_fonte_faixa_resultado = 9

        for indice, cartao in enumerate(cartoes):
            eixo_do_cartao = cartao['eixo']
            eixo_do_cartao.set_position(posicoes_dos_cartoes[indice])
            largura_do_cartao = posicoes_dos_cartoes[indice][2]
            ajustar_tamanho_da_fonte(
                cartao['titulo'],
                tamanho_fonte_titulo_cartao,
                largura_do_cartao * largura_da_janela * 0.92,
                fator_de_escala
            )
            ajustar_tamanho_da_fonte(
                cartao['valor'],
                tamanho_fonte_valor_cartao,
                largura_do_cartao * largura_da_janela * 0.92,
                fator_de_escala
            )
            if cartao['descricao'] is not None:
                ajustar_tamanho_da_fonte(
                    cartao['descricao'],
                    tamanho_fonte_descricao_cartao,
                    largura_do_cartao * largura_da_janela * 0.92,
                    fator_de_escala
                )

        eixo_grafico.set_position(posicao_do_grafico)
        ajustar_tamanho_da_fonte(
            eixo_grafico.title,
            tamanho_fonte_titulo_grafico,
            posicao_do_grafico[2] * largura_da_janela * 0.9,
            fator_de_escala
        )
        eixo_grafico.xaxis.label.set_size(
            max(5, tamanho_fonte_titulo_cartao * fator_de_escala)
        )
        eixo_grafico.tick_params(
            axis='both',
            labelsize=max(5, tamanho_fonte_titulo_cartao * fator_de_escala),
            pad=4
        )
        for texto_da_barra in textos_das_barras:
            ajustar_tamanho_da_fonte(
                texto_da_barra,
                tamanho_fonte_titulo_cartao,
                posicao_do_grafico[2] * largura_da_janela * 0.12,
                fator_de_escala
            )

        eixo_faixa_resultado.set_position(posicao_da_faixa_resultado)
        largura_maxima_da_linha_da_faixa = max(24, int(
            posicao_da_faixa_resultado[2] * largura_da_janela * 72
            / max(
                tamanho_fonte_faixa_resultado * fator_de_escala * 0.68,
                1
            )
        ))
        texto_faixa_resultado.set_text(textwrap.fill(
            texto_resultado,
            width=largura_maxima_da_linha_da_faixa,
            break_long_words=True,
            replace_whitespace=False
        ))
        ajustar_tamanho_da_fonte(
            texto_faixa_resultado,
            tamanho_fonte_faixa_resultado,
            posicao_da_faixa_resultado[2] * largura_da_janela * 0.9,
            fator_de_escala
        )

        ajustar_tamanho_da_fonte(
            titulo_principal,
            tamanho_fonte_titulo_principal,
            largura_da_janela * 0.92,
            fator_de_escala
        )

        figura.canvas.draw_idle()

    ajustar_layout()
    figura.canvas.mpl_connect(
        'resize_event',
        ajustar_layout
    )

    plt.show(block = True)