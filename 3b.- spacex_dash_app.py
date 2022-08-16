# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#create list of dictionaries for dropdown options
sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()[['Launch Site']]
sites_list = []
sites_list.append({'label':'All sites','value':'ALL'})
for index, row in sites_df.iterrows():
    sites_list.append({'label':row['Launch Site'],'value':row['Launch Site']})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=sites_list, value='ALL', placeholder='Choose a launch site', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, marks={0: '0', 2500: '2.500', 5000:'5.000', 7500:'7.500', 10000:'10.000'},value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_pie_chart(entered_site, entered_payload):
    filtered_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Succesful launches for all sites', hole=.3, color='Launch Site', color_discrete_map={'KSC LC-39A':'orange','VAFB SLC-4E':'red', 'CCAFS SLC-40':'blue','CCAFS LC-40':'pink'})
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df['Launch Site']== entered_site]
        fig = px.pie(filtered_df, names='class', title="Successful launches (green) in '" + str(entered_site) + "' site", hole=.3, color = 'class', color_discrete_map={0:'black',1:'green'})
        fig.layout.update(showlegend=False)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site,entered_payload):
    filtered_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for all sites")
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df['Launch Site']== entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success in '" + str(entered_site) + "' site")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
