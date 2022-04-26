# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
try:
    import squarify
except ModuleNotFoundError:
    print('Import Squarify package: conda install -c conda-forge squarify')
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.colors import ListedColormap

def get_date_range(df: pd.DataFrame,start:str,end:str)-> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe where the index is in datetime format.
    start : str
        start for the date range.
    end : str
        end of the date range.

    Returns
    -------
    pd.DataFrame
        The dataframe with the datetime specified.

    """
    df.index = pd.to_datetime(df.index)
    date_range = pd.date_range(start,end,freq='D')
    common_dates = set(df.index).intersection(date_range)
    df = df.loc[common_dates]
    df = df.sort_index()
    return df

def calculate_percentage(x, y):
    return round((100 * x / y), 2)


def preprocess_daily_data_for_plotting(df: pd.DataFrame,
                                       total_col: str = 'Total tests',
                                       positive_col: str = 'Positive tests',
                                       country: str = None,
                                       date_start: str = '2020-06-15',
                                       date_end: str = '2022-03-14',
                                       groupby_Monthly=False):
    """
    

    Parameters
    ----------
    df : pd.DataFrame
        a dataframe where index is a daily.
    total_col : str, optional
        the name of the total tests column. The default is 'Total tests'.
    positive_col : str, optional
        the name of the positive column. The default is 'Positive tests'.
    country : str, optional
        the name of the country. The default is None.
    date_start : str, optional
        DESCRIPTION. The default is '2020-06-15'.
    date_end : str, optional
        DESCRIPTION. The default is '2022-03-14'.
    groupby : TYPE, optional
        If not None, will be groupby by Month. The default is None.

    Returns
    -------
    df : DataFrame
        Get a new data frame preprocessed for plotting.

    """
    
    all_dates = pd.date_range(date_start, date_end, freq='D')
    all_dates.name = 'Date'
    if isinstance(df.index, pd.MultiIndex):
        index_levels = dict()
        index_levels[0] = all_dates
        for level in range(1, df.index.nlevels):
            index_levels[level] = df.index.get_level_values(level).unique()
        all_dates = pd.MultiIndex.from_product(index_levels.values(),names=['Date']+df.index.names[1:])
        df.index = df.index.set_levels(pd.DatetimeIndex(df.index.levels[0]), level=0)
    else:
        df.index = pd.DatetimeIndex(df.index)
    df = df.reindex(all_dates)
    df.index.name = all_dates.names
    df.rename(columns={
        total_col: 'Total tests',
        positive_col: 'Positive tests'
    },
              inplace=True)
    if groupby_Monthly:
        df['Month'] = df.index.get_level_values(0).strftime('%b-%Y')
        index_names = df.index.names[1:]
        df = df.reset_index()
        
        df['Month'] = pd.Categorical(
            df['Month'],
            categories=pd.date_range(date_start, date_end, freq='D').strftime('%b-%Y').unique(),
            ordered=True)
        df = df.sort_values(by='Month')
        df = df.groupby(['Month']+index_names).sum()
        df['positive percentage'] = calculate_percentage(
            df['Positive tests'], df['Total tests'])
        
    if country is not None:
        df['Country'] = country
    return df

def calculate_positive_2W_incidence_per_100k_inhabitant(df: pd.DataFrame, population:int):
    """
    

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of daily positive cases.
    population : int
        population of a country.

    Returns
    -------
    resampled_df : TYPE
        Resampled dataframe.

    """
    
    df.index = pd.DatetimeIndex(df.index)
    resampled_df = df.resample('2W').mean()
    resampled_df['incidence'] = round(
        ((resampled_df['positive'] / population) * 100000), 2)
    return resampled_df

def plot_bar_plot(ax, *dfs,**kwargs):
    """
    

    Parameters
    ----------
    ax : TYPE
        axes from plt.subplots().
    *dfs : TYPE
        list of dataframes. Input from the preprocess_daily_data_for_plotting.
    **kwargs : TYPE
        bar_annotate - annotate on the top of the bar.
        title - name of the plot

    Returns
    -------
    None.

    """
    if kwargs.get('hue'):
        hue = kwargs.get('hue')
    else:
        hue = None
    combined_df = pd.concat([*dfs], join='inner')
    combined_df.index.name = 'Date'
    g = sns.barplot(x=combined_df.index,
                    y='positive percentage',
                    hue=hue,
                    data=combined_df,
                    ax=ax)
    if hue:
        unique_hue = combined_df[hue].unique()
        if kwargs.get('bar_annotate'):
            for idx, container in enumerate(g.containers):
                g.bar_label(container,
                            labels=[
                                f'{int(i)}' for i in combined_df.loc[
                                    combined_df[hue] == unique_hue[idx],
                                    'Positive tests']
                            ])
    ax.set_ylabel('Positive test (%)',fontsize=15)
    ax.set_title(kwargs.get('title'),fontsize=20)
    ax.tick_params(axis='x', rotation=45,labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.legend(loc='upper left',prop={'size':15})
    ax.set_xlabel('Date',fontsize=15)
    

class Square:
    """
    Perform square layout
    """
    @staticmethod
    def process_squarify_data(df:pd.DataFrame,
                              start_date:str,
                              end_date:str,
                              country_col:str,
                              total_col:str,
                              pos_col:str) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with daily information about travellers country of depature.
        start_date : str
            choose the date in form '%YYYY-%mm-%dd.
        end_date : str
            choose the date in form '%YYYY-%mm-%dd.
        country_col : str
            Name of the country column.
        total_col : str
            Name of the number of total tests column.
        pos_col : str
            Name of the number of positive tests column.

        Returns
        -------
        df_by_country : pd.DataFrame
            Preprocessed data for square layout.

        """
        df = df.loc[start_date:end_date]
        df_by_country = df.groupby(country_col).sum()
        df_by_country['positive percentage'] = calculate_percentage(df_by_country[pos_col], df_by_country[total_col])
        df_by_country = df_by_country.sort_values(by=total_col,ascending=False)
        df_by_country = df_by_country.reset_index()
        return df_by_country
    
    @staticmethod
    def squarify_country(ax,
                         df:pd.DataFrame,
                         country_col:str,
                         total_col:str,
                         percentage_col:str,
                         top:int=20):
        """
        

        Parameters
        ----------
        ax : matplotlib ax
            ax from matplotlib.
        df : pd.DataFrame
            preprocessed data for square layout. See Square.process_squarify_data
        country_col : str
            Name of the country column.
        total_col : str
            Name of the number of total tests column.
        percentage_col : str
            Name of the number of positive percentage column.
        top : int, optional
            Number of country to visualise. The default is 20.

        Returns
        -------
        im : image plot
            DESCRIPTION.
        sm : color range of the squares
            DESCRIPTION.

        """
        countries = df.loc[:top,country_col].tolist()
        sizes = df.loc[:top,total_col].tolist()
        percentages = df.loc[:top,percentage_col].tolist()
        cmap = matplotlib.cm.Blues
        mini=min(percentages)
        maxi=max(percentages)
        norm =  matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
        colors = [cmap(norm(value)) for value in percentages]
    
        pal = sns.color_palette('Blues', len(percentages))
        
        my_cmap = ListedColormap(pal)
        norm = plt.Normalize(min(percentages), max(percentages))
        sm = plt.cm.ScalarMappable(cmap=my_cmap, norm=norm)
        sm.set_array([])
    
        im = squarify.plot(label=countries,sizes=sizes, alpha=.8, color=colors, pad=True,ax=ax,text_kwargs=dict(fontsize=15))
        # cbar = plt.colorbar(sm)
        # cbar.set_label('Percentage of positive tests')
        return im,sm