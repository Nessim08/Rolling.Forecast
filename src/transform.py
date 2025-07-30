def aggregate(df):
    return (
      df
      .groupby(['Market','Channel','SKU','Date'])
      .agg({'Sales':'sum','Price':'mean'})
      .reset_index()
    )

def merge_with_input(agg_df, input_df):
    return agg_df.merge(input_df, how='left', on=['Market','Channel','SKU','Date'])

