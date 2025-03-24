from dash import Dash, dcc, html,Input, Output
import dash_bootstrap_components as dbc
import os
import pandas as pd

import Vizuals
from Vizuals import footer_card

##----Data Processing----##

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME],
)


##### Sourced from chatGPT #####
##prompt: Can you create a dash and pandas program that takes data from
# multiple csvs and combines it into a single dataframe?
# Folder containing CSV files
CSV_FOLDER = "csv_files"  # Change this to the correct folder path


# Function to load and merge CSV files
def load_csv_files(folder_path):
        all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        dataframes = [pd.read_csv(os.path.join(folder_path, file), parse_dates=['observation_date']) for file in
                      all_files]
        combined_df = pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

            ## I edit to get year average
        if not combined_df.empty:
                combined_df['year'] = combined_df['observation_date'].dt.year
                combined_df = combined_df.groupby('year', as_index=False).mean()
                combined_df = combined_df.drop(columns=['observation_date'], errors='ignore')
        return combined_df


# Load the data initially
data = load_csv_files(CSV_FOLDER)
####  ###


"""
===========================================================================
Main Layout
"""



app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                html.H2(

                    "Cost of Living and Eating in the US",
                    className="text-center bg-primary text-white p-2",
                ),
                html.H4(
                    "Elias Leon",
                    className="text-center"
                ),
                html.H4(
                    "CS-150 : Community Action Computing",
                    className="text-center"
                ),
            ])
        ),
        dbc.Row(
            [
                dbc.Col(Vizuals.tabs, width=12, lg=5, className="mt-4 border"),
                dbc.Col(
                    [
                        dcc.Graph(id="income-chart", className="mb-2"),
                        dcc.Graph(id="expense-chart", className="pb-4"),
                        Vizuals.food_cost_table,
                        html.Hr(),


                    ]
                ),
            ]
        ),
        dbc.Row(
        Vizuals.footer_card
        )
    ],
    fluid=True,
)

"""
==========================================================================
Callbacks
"""


@app.callback(
    Output("income-chart", "figure"),
    Input("year-slider", "value")
)
def update_income_chart(selected_year):
    filtered_df = data[data["year"] <= selected_year]
    return Vizuals.median_income_linegraph(filtered_df)

@app.callback(
    Output("expense-chart", "figure"),
    Input("expense-dropdown", "value")
)
def update_expense_chart(selected_category):
    if selected_category in ["breakfast", "lunch"]:
        return Vizuals.calculate_meal_cost(data, selected_category)
    return Vizuals.team_expense_linegraph(data, selected_category)

@app.callback(
    Output("food-cost-table", "data"),
    [Input("year-input", "value"),
     Input("family-size-input", "value"),
     Input("salary-input", "value")]
)
def update_food_cost_table(selected_year, family_size, salary):
    filtered_data = data[data["year"] == selected_year]

    return Vizuals.make_table(family_size, salary, filtered_data)

if __name__ == "__main__":
    app.run(debug=True)
