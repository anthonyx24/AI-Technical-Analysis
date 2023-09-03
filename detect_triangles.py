import numpy as np
import pandas as pd
import general_pkg.get_data as gd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import linregress


# Credit: https://www.youtube.com/watch?v=WVNB_6JRbl0


def findpivots(df, p, f):
    '''
    Finds the pivots of the triangles. If a point is lower than previous p points
    and following f points, mark as local minima. Same for maxima. 

    cd is the index of the current candle

    EDIT: There is apparently a lookahead bias (using future data). May not be an issue
    for labeling, but still should try to account for this.

    '''
    # Add new column to df with pivots
    df['Pivots'] = ''
    
    # Each candle i
    for i in range(len(df)):

        # For out of bounds cases
        if i - p < 0 or i + f >= len(df): 
            df.loc[i,'Pivots'] = 'none'
            continue
    
        is_max = 1
        is_min = 1

        # For all points within f to p range around i
        for j in range(i - p, i + f + 1): 
            if(df.loc[i,'Close'] < df.loc[j,'Close']):
                is_max = 0
            if(df.loc[i,'Close'] > df.loc[j,'Close']):
                is_min = 0

        if is_max and is_min: df.loc[i,'Pivots'] = 'both'
        
        elif is_min: df.loc[i,'Pivots'] = 'min'
        
        elif is_max: df.loc[i,'Pivots'] = 'max'
        
        else: df.loc[i,'Pivots'] = 'none'
    
    return df


def detect(df, back, min_points):
    '''
    Draws lines based on pivots:

    Find horizontal top lines by comparing y pos of maxes, if y pos is same between two points
    mark them and draw a line between them.

    Next, do bottom lines by finding min point in range of horizontal top line, then find the 
    largest slope from all previous points.

    Walk potential top line and bottom line along candles, 
    - if top line is broken check if bottom line is close enough; if not, it fails
    - if bottom line is broken automatically fails

    back represents the number of candles to look back to detect triangles

    min_points is the minimum number of pivots needed to detect a triangle

    '''

    # Loop through all candles, starting with candle back+1
    for i in range(back+1, len(df)):
        minima = np.array([])
        maxima = np.array([])

        # Loop through the candle window (defined with back)
        for j in range(i-back, i+1):
            # Append tuples with x,y coords of pivots
            if df.loc[j,'Pivots'] == 'min':
                minima = np.append(minima, (j,df.loc[j,'Low'])) # Close
            elif df.loc[j,'Pivots'] == 'max':
                maxima = np.append(maxima, (j,df.loc[j,'High'])) # Close
        
        
        
def plot(df):
    
    df['Points'] = ''

    for i in range(len(df)):
        if df.loc[i,'Pivots'] == 'min':
            df.loc[i,'Points'] = df.loc[i,'Low'] - 1e-3
        elif df.loc[i,'Pivots'] == 'max':
            df.loc[i,'Points'] = df.loc[i,'High'] + 1e-3
        else:
            df.loc[i,'Points'] = np.nan

    dfpl = df[:500]

    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                    open=df.loc[:,'Open'],
                    close=df.loc[:,'Close'],
                    low=dfpl.loc[:,'Low'],
                    high=dfpl.loc[:,'High'])])
    
    fig.add_scatter(x=dfpl.index, y=dfpl.loc[:,'Points'],
                    mode='markers', marker=dict(color='Blue'), name='pivots')
    
    fig.show()


if __name__ == '__main__':
    data = gd.get_data()[0]
    data = findpivots(data, 3, 3)
    plot(data)
    


