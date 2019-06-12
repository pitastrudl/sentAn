#!/usr/bin/env python3
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd


df = pd.read_csv('kadunc_scored.csv',delimiter='^')

sample_data_table = FF.create_table(df.head())
plotly.iplot(sample_data_table, filename='sample-data-table')

