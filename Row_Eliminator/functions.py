# Functions for the Row Eliminator Site
from flask import flash


#  Define and Display Columns for user selection
def def_cols(df) -> list:
    """Define and Display Columns for user selection"""
    # -- Select all columns that have offensive values: --
    victor_df, elim_df, col_sel = df.copy(), df.copy(), []
    for i in range(len(df.columns)):
        if len(df) > df[df.columns[i]].nunique() > 1:
            x = f'[{i}]{df.columns[i]} -- {df[df.columns[i]].nunique()} ' \
                f'Unique Values!'
            col_sel.append(x)
            flash(x, 'cols')
    return [i for i in col_sel]
