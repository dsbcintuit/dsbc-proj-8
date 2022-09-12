######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Cheese!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/datasets/ericsims/world-cheese-awards-worlds-cheesiest-dataset'
githublink = 'https://github.com/dsbcintuit/dsbc-proj-8'


###### Import a dataframe #######
df = pd.read_csv("apps/world_cheese_awards_2021.csv")

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Rating', 'Number of Countries'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Rating'].index,
        y=results.loc['Number of Countries'][continuous_var],
        name='Number of Countries',
        marker=dict(color=color1)
    )
#     mydata2 = go.Bar(
#         x=results.loc['Cherbourg'].index,
#         y=results.loc['Cherbourg'][continuous_var],
#         name='Cherbourg',
#         marker=dict(color=color2)
#     )
#     mydata3 = go.Bar(
#         x=results.loc['Queenstown'].index,
#         y=results.loc['Queenstown'][continuous_var],
#         name='Queenstown',
#         marker=dict(color=color3)
#     )

#     mylayout = go.Layout(
#         title='Grouped bar chart',
#         xaxis = dict(title = 'Port of Embarkation'), # x-axis label
#         yaxis = dict(title = str(continuous_var)), # y-axis label

#     )
    fig = go.Figure(data=[mydata1
                          # , mydata2, mydata3
                         ], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
