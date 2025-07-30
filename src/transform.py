def aggregate(df):
    """
    Agrupa por Market, Channel, SKU y Date,
    sumando Sales y promediando Price.
    """
    return (
        df
        .groupby(['Market', 'Channel', 'SKU', 'Date'])
        .agg({'Sales': 'sum', 'Price': 'mean'})
        .reset_index()
    )

def merge_with_input(agg_df, input_df):
    """
    Hace left merge con el input de comerciales
    para añadir sus valores de forecast.
    """
    return agg_df.merge(
        input_df,
        how='left',
        on=['Market', 'Channel', 'SKU', 'Date']
    )

