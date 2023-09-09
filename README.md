# Technical Analysis Project using Tensorflow

## Introduction
This is an attempt to build an AI model that can recognize price patterns and indicators used in technical analysis to inform day traders when to buy and sell. A relative of mine runs a hedge fund, so he asked me to help him build an algorithm that could help him detect exactly when patterns/indicators occur.

I will use TensorFlow to build a Long Short-Term Memory neural network, since it seems to be the most successful for stock analysis/prediction tasks. 

I am far from knowledgeable in AI nor finance, but I am learning every day. This project is also still in its early stages.

Price data obtained from [Polygon REST API](https://polygon.io/docs/stocks/getting-started).  

For the data formatting, I followed along [this tutorial](https://wire.insiderfinance.io/how-to-develop-a-pattern-recognition-neural-network-for-trading-d0398eeb56f5) from Danny Groves. 

Installed Libraries: pandas, numpy, requests, tensorflow, backtesting

## Current Status
I am now trying to label the data to train the AI on, using ascending triangles as my first example. This [research paper](https://ui.adsabs.harvard.edu/abs/2018arXiv180800418V/abstract) is the closest thing I could find to what I am doing. They mentioned that they could not find existing datasets to train their networks on, so they had to create their own datasets algorithmically. 

Thus, I am also trying to write an algorithm to label ascending triangles. I followed [this tutorial](https://www.youtube.com/watch?v=WVNB_6JRbl0) to label the pivot points, but after discussing with my relative I need to draw the lines different to how they did, which I'm currently implementing.

![image](https://github.com/anthonyx24/AI-Technical-Analysis/assets/79112832/7012819c-73d5-4849-a53a-28bf581e789d)

## Running the Program
To see the current status of detecting the triangles, run
```
python3 detect_triangles.py
```
To see an example of formatting data for the NN (using EMA as an indicator), run
```
python3 format_data.py
```
