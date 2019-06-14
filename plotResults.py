#!/usr/bin/env python3
import plotly
import plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import sys
from operator import itemgetter
import plotly.io as pio
range = list(sys.argv[2].split(','))

plotly.io.orca.config.executable = '/usr/local/lib/python3.5/dist-packages/plotly/io/'

def get_all_data():
    with open(sys.argv[1], "r", encoding='UTF-8') as text_file:
        # with open("output.csv", "r") as text_file:
        data = text_file.read().split('\n')
        # remove the csv header
        data.pop(0)
    return data


def preprocessing_data(data):
    processing_data = []
    for single_data in data:
        splitData = single_data.split("^")
        if len(splitData) > 10:
            processing_data.append(splitData)

    return processing_data


podatki = get_all_data()
parsed = preprocessing_data(podatki)

dates = []
scores = []
parsed = sorted(parsed, key=itemgetter(0))
for key in parsed:
    if key[13] != '' and key[13] != 0:  # discard 0
        dates.append(key[0])
        scores.append(float(key[13]))

print(parsed)


def printGraph(dates,scores):
    trace = go.Scatter(

        x=dates,
        y=scores,
        marker={'color': 'red',
                'symbol': 104,
                'size': 5},
        mode='markers')
    trace1 = go.Scatter(
        x=[1.5, 4.5],
        y=[0.75, 0.75],
        text=['Unfilled Rectangle', 'Filled Rectangle'],
        mode='text',
    )
    data = go.Data([trace, trace1])
    layout = go.Layout(title="First Plot",
                       xaxis={'title': 'Time',
                              'showticklabels': True,
                              'tickfont' : {
                                    'size': 16
                              }
                           , },
                       yaxis={'title': 'Sentiment value',
                              'range': range,
                              'showticklabels': True,
                              'tickfont' : {
                                    'size': 16
                              }

                              },
                       shapes=[{
                           'type': 'rect',
                           'xref': 'x',
                           'yref': 'paper',
                           'x0': '2019-03-21 00:00:00',
                           'y0': 0,
                           'x1': '2019-03-24 23:59:59',
                           'y1': 1,
                           'fillcolor': '#d3d3d3',
                           'opacity': 0.2,
                           'line': {
                               'width': 1,
                               'color': 'rgba(0, 0, 0, 1)'
                           }
                       }]

                       )

    figure = go.Figure(data=[trace], layout=layout)

    plot(figure)
    pio.write_image(figure, 'fig1.png')
    figure.savefig("output.png")

printGraph(dates,scores)




# highlighting


# -----------my data







# print(data)
# layout=go.Layout(title="First Plot", xaxis={'title':'x1'}, yaxis={'title':'x2'})
# figure=go.Figure(data=data,layout=layout)

# trace1 = go.Scatter(x=[1, 2, 3], y=[4, 5, 6], marker={'color': 'red', 'symbol': 104, 'size': 10},
#                     mode="markers+lines", text=["one", "two", "three"], name='1st Trace')
#
# data = go.Data([trace1])
# print(type(trace1))
# print(type(data))

# plot([go.Scatter(x=[1, 2, 3], y=[3, 1, 6])])
