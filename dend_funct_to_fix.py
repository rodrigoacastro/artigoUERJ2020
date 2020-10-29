def plot_dendrogram(df_for_dendogram,show=True):
    # make dendrogram
    # https://plotly.com/python/dendrogram/
    import scipy
    import plotly.figure_factory as ff
    import numpy as np
    # np.random.seed(1)

    # X = np.random.rand(15, 12) # 15 samples, with 12 dimensions each
    # df_counts_dend
    fig = ff.create_dendrogram(df_for_dendogram)
    fig.update_layout(width=800, height=500)

    if show:
        fig.show()
    else:
        plt.savefig('Results/Dendrogram.tiff',dpi=300)


plot_dendrogram(df_counts_dend,show=False)
