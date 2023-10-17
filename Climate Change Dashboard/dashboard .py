import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# read in data
data = pd.read_csv('Annual_Surface_Temperature_Change.csv')
df = pd.DataFrame(data)

# selecting columns to drop
cleaning_df = df.drop(['ObjectId', 'ISO2', 'ISO3', 'Indicator', 'Unit', 'Source',
       'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor'], axis=1)

# stripping f from column
for column in cleaning_df.columns:
    cleaning_df.columns = cleaning_df.columns.str.lstrip('F')

# dropping null rows
cleaning_df = cleaning_df.dropna()

# adding sum column to df
df_no_country = cleaning_df.drop("Country", axis=1)
clor_cleaning_df = cleaning_df.copy()
clor_cleaning_df["Total Change"] = df_no_country.sum(axis=1)

# creating yearly average column
yearly_averages = cleaning_df.iloc[:, 1:].mean()

# adding new column to dataframe
new_row = pd.DataFrame({'Country': ['Yearly Average'], **yearly_averages.to_dict()})
cleaned_df = pd.concat([cleaning_df, new_row], ignore_index=True)

# global yearly average temperature changes
yearly_averages = cleaned_df.iloc[:, 1:].mean()
yearly_averages = yearly_averages.reset_index()
yearly_averages.columns = ['Year', 'Average Temperature Change']

# Create the main Dash application
app = dash.Dash(__name__)

# define layout for yearly temp differences
layout1 = html.Div([
    html.H1("Temperature Differences by Year"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in cleaning_df.columns if year != 'Country'],
        value='2022',  # Set a default year
    ),
    dcc.Graph(id='temperature-graph'),
])

# Define the callback for the first dashboard
@app.callback(
    Output('temperature-graph', 'figure'),
    Input('year-dropdown', 'value')
)

def update_temperature_graph(selected_year):
    '''
    Updates the output of the choropleth  map

    :param selected_year: year chosen by user
    :return: temperature_fig
    '''
    # Filter the data for the selected year
    year_data = clor_cleaning_df[['Country', selected_year]]

    # Create the temperature graph
    temperature_fig = px.choropleth(
        year_data,
        locations="Country",
        locationmode="country names",
        color=selected_year,
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"Temperature Differences in {selected_year}",
    )

    return temperature_fig


# Define the layout for the Choropleth Map
layout2 = html.Div([
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(
            clor_cleaning_df,
            locations="Country",
            locationmode="country names",
            color="Total Change",
            scope="world",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="Click on Country to Explore Further:"
        )
    ),
    dcc.Graph(id='scatter-plot')
])


# Define the callback for the second dashboard
combined_country_options = [{'label': country, 'value': country} for country in cleaned_df['Country'].unique()]
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('choropleth-map', 'clickData')
)

def update_scatter_plot(clickData):
    '''
    Updates the output of the scatter plot

    :param clickData: country that user selected
    :return: scatter_fig
    '''

    # clickData formatting assistance by chatgpt
    if clickData is None:
        return px.scatter()  # Return an empty scatter plot if no country is selected

    selected_country = clickData['points'][0]['location']

    # Filter data for the selected country
    country_data = clor_cleaning_df[clor_cleaning_df['Country'] == selected_country]

    # Transpose the data so that years become the x-axis and temperature change the y-axis
    transposed_data = country_data.iloc[:, 1:-1].T
    transposed_data.columns = ["Temperature Change"]

    scatter_fig = px.scatter(
        transposed_data,
        x=transposed_data.index,  # Years on the x-axis
        y="Temperature Change",
        title=f"Temperature Change Over Time for {selected_country}",
    )

    return scatter_fig

# Define the layout for the third dashboard ("Surface Temperature Change by Country")
layout3 = html.Div([
    html.H1("Surface Temperature Change by Country"),
    dcc.Dropdown(options=combined_country_options, value='Canada', id='combined-country-dropdown'),
    dcc.Graph(id='temperature-plot'),
    dcc.Graph(id='line-chart'),
])

# Define the callback for the third dashboard
@app.callback(
    Output('temperature-plot', 'figure'),
    Output('line-chart', 'figure'),
    [Input('combined-country-dropdown', 'value')]
)
def update_graphs(selected_country):
    # DataFrame for the selected country
    country_data = cleaned_df[cleaned_df['Country'] == selected_country]

    # reshape the data for plotting
    country_data = country_data.T.reset_index()
    country_data.columns = ['Year', 'Temperature Change']
    country_data = country_data[1:]  # Skip the 'Country' row

    # line plot for the selected country for temperature data
    temperature_fig = px.bar(country_data, x='Year', y='Temperature Change',
                             title=f'Yearly Surface Temperature Change for {selected_country} Compared to Global Average')
    temperature_fig.update_traces(marker_color='blue', opacity=0.5)

    # overlay the global yearly average temperature change on the same temperature figure
    global_fig = px.bar(yearly_averages, x='Year', y='Average Temperature Change',
                        title='Yearly Average Temperature Change Globally')
    global_fig.update_traces(marker_color='pink', opacity=0.5)
    temperature_fig.add_trace(global_fig.data[0])

    # DataFrame for the selected country for line chart data
    filtered_df = cleaned_df[cleaned_df['Country'] == selected_country]

    # flatten the data to have all years in one list for line chart data
    x_values = [year for year in filtered_df.columns if year != 'Country']
    y_values = [filtered_df[year].values[0] for year in x_values]

    # line chart using Plotly Express for line chart data
    line_chart_fig = go.Figure()
    line_chart_fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name=selected_country))
    line_chart_fig.update_layout(title=f'{selected_country} Data Over Time', xaxis_title='Year', yaxis_title='Value')

    return temperature_fig, line_chart_fig



@app.callback(
    Output('indicator-chart', 'figure'),
    [Input('combined-country-dropdown', 'value')]
)
def update_indicator(selected_country):
    '''

    :param selected_country: country defined by user
    :return: fig
    '''
    # Filter the DataFrame based on the selected country
    filtered_df = clor_cleaning_df[clor_cleaning_df['Country'] == selected_country]

    # Get the average value for the "Sum" column for the selected country
    avg_value = filtered_df['Total Change'].mean()

    # Create the Indicator with the average value and mode 'number'
    fig = go.Figure(go.Indicator(
        mode="number",
        value=avg_value,
        number={'valueformat': '.2f'},  # Add the dollar sign and set value format
        delta={'position': "top", 'reference': 320},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(paper_bgcolor="lightgray")

    return fig

# Create an empty Indicator chart as the initial figure
initial_fig = go.Figure(go.Indicator(
        mode="number",
        value=0,
        number={'valueformat': '.2f'},
        delta={'position': "top", 'reference': 0},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

# Create a Plotly Graph Object figure
indicator_chart = dcc.Graph(id='indicator-chart', figure=initial_fig)

# defines layout for 4th element in dashboard (bottom right)
layout4 = html.Div([
    html.H1('Total Change in Percent Temperature Change'),
    indicator_chart
], style={'float': 'right', 'width': '100%', 'display': 'inline-block'})



# Combine the layouts of all three dashboards within the main layout with CSS styling
app.layout = html.Div([
    html.H1("Surface Temperature Dashboard"),
    html.Div(
        [layout1, layout2],  # Left side: Temperature by Year and Choropleth Map
        style={'display': 'inline-block', 'width': '50%'}
    ),
    html.Div(
            [layout3, layout4],  # Right side: surface
            style={'display': 'inline-block', 'width': '50%'}
    ), # Right side: Surface Temperature Change
])

# creating the final layout
app.layout = html.Div([
    html.H1("Surface Temperature Dashboard"),
    html.Div([
        # Left side: Temperature by Year and Choropleth Map
        html.Div([layout1, layout2], style={'display': 'inline-block', 'width': '50%'}),

        # Right side: Surface Temperature Change and Indicator
        html.Div([layout3, layout4], style={'display': 'inline-block', 'width': '50%'})
    ])
])


if __name__ == '__main__':
    app.run_server(port = 8060, debug=True)