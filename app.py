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

countries = ['Afghanistan', 'Algeria', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bangladesh', 'Barbados', 'Belgium', 'Belize', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Canada', 'Cayman Islands', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guatemala', 'Guernsey', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea', 'Kosovo', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Montenegro', 'Morocco', 'Myanmar', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Nigeria', 'Norway', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Romania', 'Russia', 'Rwanda', 'Saint Lucia', 'Saudi Arabia', 'Senegal', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'St Vincent &amp; the Grenadines', 'Sudan', 'Swaziland', 'Sweden', 'Switzerland', 'Taiwan', 'Tanzania', 'Thailand', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'USA', 'Venezuela', 'Vietnam', 'Yemen', 'Zimbabwe']
counties = ['Aberdeen City', 'Aberdeenshire', 'Angus', 'Antrim', 'Argyll and Bute', 'Armagh', 'Bedfordshire', 'Berkshire', 'Buckinghamshire', 'Cambridgeshire', 'Carlow', 'Carmarthenshire', 'Cavan', 'Ceredigion', 'Cheshire', 'Clackmannanshire', 'Clare', 'Clwyd', 'Cork', 'Cornwall', 'County Durham', 'Cumbria', 'Denbighshire', 'Derbyshire', 'Derry', 'Devon', 'Donegal', 'Dorset', 'Down', 'Down', 'Dublin', 'Dumfries and Galloway', 'Dundee City', 'East Ayrshire', 'East Dunbartonshire', 'East Lothian', 'East Renfrewshire', 'East Riding of Yorkshire', 'East Sussex', 'East Yorkshire', 'Edinburgh', 'Essex', 'Falkirk', 'Fermanagh', 'Fife', 'Flintshire', 'Galway', 'Glamorgan', 'Glasgow', 'Gloucestershire', 'Greater London', 'Greater Manchester', 'Gwent', 'Gwynedd', 'Hampshire', 'Herefordshire', 'Hertfordshire', 'Highland', 'Inverclyde', 'Isle of Anglesey', 'Isle of Man', 'Isle of Wight', 'Kent', 'Kerry', 'Kildare', 'Kilkenny', 'Kingston upon Hull', 'Lancashire', 'Laois', 'Leicestershire', 'Leitrim', 'Limerick', 'Lincolnshire', 'Londonderry', 'Longford', 'Louth', 'Mayo', 'Meath', 'Merseyside', 'Mid Glamorgan', 'Middlesex', 'Midlothian', 'Monaghan', 'Monmouthshire', 'Moray', 'Norfolk', 'North Ayrshire', 'North Humberside', 'North Lanarkshire', 'North Yorkshire', 'Northamptonshire', 'Northumberland', 'Nottinghamshire', 'Offaly', 'Orkney Islands', 'Oxfordshire', 'Pembrokeshire', 'Perth and Kinross', 'Powys', 'Renfrewshire', 'Rhondda Cynon Taf', 'Roscommon', 'Rutland', 'Scottish Borders', 'Shetland Islands', 'Shropshire', 'Sligo', 'Somerset', 'South Ayrshire', 'South Glamorgan', 'South Lanarkshire', 'South Yorkshire', 'Staffordshire', 'Stirling', 'Suffolk', 'Surrey', 'Tipperary', 'Tyne and Wear', 'Tyrone', 'Warwickshire', 'Waterford', 'West Dunbartonshire', 'West Glamorgan', 'West Lothian', 'West Midlands', 'West Sussex', 'West Yorkshire', 'Western Isles', 'Westmeath', 'Wexford', 'Wicklow', 'Wiltshire', 'Worcestershire']

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
    grouped_mean=df.groupby(['Embarked', 'Cabin Class'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Southampton'].index,
        y=results.loc['Southampton'][continuous_var],
        name='Southampton',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Cherbourg'].index,
        y=results.loc['Cherbourg'][continuous_var],
        name='Cherbourg',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['Queenstown'].index,
        y=results.loc['Queenstown'][continuous_var],
        name='Queenstown',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Port of Embarkation'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
