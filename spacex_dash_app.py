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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=[
                                                                {'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                                                            ],
                                                                    value='ALL',
                                                                    placeholder="place holder here",
                                                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                 dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                                    marks={0: {'label': '0'},
                                                                        2500: {'label': '2500'},
                                                                        5000: {'label': '5000'},
                                                                        7500: {'label': '7500'},
                                                                        10000: {'label': '10000'}},
                                                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
            Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby('Launch Site')['class'].value_counts().to_frame()
    filtered_df.columns = ['Success']
    filtered_df = filtered_df.reset_index()
    filtered_df['class'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
    
    
    if entered_site == 'ALL':
        filtered_df = filtered_df[filtered_df['class'] == 'Success']
        fig = px.pie(filtered_df, 
                     values= 'Success',  
                    names='Launch Site', 
                    title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site

        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     values='Success', 
                    names='class', 
                    title= 'Total Success Launches by ' + entered_site)
        
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def Scatter_Plot(site_dropdown, payload_slider ):   
    if site_dropdown == 'ALL':
        payload_slider == [min_payload, max_payload]
        payload_mask = (spacex_df['Payload Mass (kg)'] >= payload_slider[0]) & (spacex_df['Payload Mass (kg)'] <= payload_slider [1])
        payload_data = spacex_df[payload_mask]
        fig = px.scatter(payload_data, x= 'Payload Mass (kg)', y = 'class', color= 'Booster Version Category')
        return fig
        
    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] ==  site_dropdown]
        payload_mask = (filtered_data['Payload Mass (kg)'] >= payload_slider[0]) & (filtered_data['Payload Mass (kg)'] <= payload_slider [1])
        payload_data = filtered_data[payload_mask]
        fig = px.scatter(payload_data, x= 'Payload Mass (kg)', y = 'class', color= 'Booster Version Category')
        return fig
 

# Run the app
if __name__ == '__main__':
    app.run_server()

#Which site has the largest successful launches?
#KSC-L39A with 41.7% success rate.

#Which site has the highest launch success rate?
#KSC-L39A with 76.9% success rate.

#Which payload range(s) has the highest launch success rate?
#Payload between 2000kg & 4500kg had the highest success rate

#Which payload range(s) has the lowest launch success rate?
#Payload between 0kg & 2000kg + payload 
#higher than 5500 kg had the lowest success rate

#Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
#launch success rate?
#F9 Booster version FT has the highest success rate
