from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

from text import about_page, footer, play_text

income_df = pd.read_csv("csv_files/Median_household_income.csv")


houseprice_df = pd.read_csv("csv_files/Median_Sales_Price_of_Houses.csv")


# ===========

year_input= dbc.InputGroupText(
    [
        dbc.InputGroupText("Select Year"),
        dbc.Input(
            id="year-input",
            type="number",
            min=1984,
            max=2025,
            value=2025,
            step=1,
            placeholder=f"min {1984}   max {2025}"
        ),
    ],
    className="mb-3",
)

family_size_input= dbc.InputGroup(
    [
        dbc.InputGroupText("Family Size "),
        dbc.Input(
            id="family-size-input",
            type="number",
            min=1,
            value=1,
            step=1,
            placeholder="Family Size",
        ),
    ],
    className="mb-3",
)
salary_input = dbc.InputGroup(
    [
        dbc.InputGroupText("Yearly Salary $"),
        dbc.Input(id="salary-input",
            type="number",
            min=0,
            value=50000,
            step=1000,
            placeholder="Enter Salary",
        ),
    ],
    className="mb-3",
    )

input_groups = html.Div(
    [year_input,salary_input,family_size_input  ],
    className="mt-4 p-4",
)

# ============ Slider
slider_card = dbc.Card(
    [
    html.H4("Year Slider",className="card-title"),
    dcc.Slider(
        id="year-slider",
        min=1984,
        max=2025,
        value=2025,
        marks={year: str(year) for year in range(1984, 2026, 5)},
        step=1,
    ),
    ],
    body=True,
    className="mt-4",
)

# ============= dropdown
dropdown_card = dbc.Card(
    [
        html.H4(
            "Select a to see price history ",
            className="card-title",
        ),
        dcc.Dropdown(
            id="expense-dropdown",
            options=[
                {"label": "Housing", "value": "Median_Sales_price_house"},
                {"label": "Breakfast", "value": "breakfast"},
                {"label": "Lunch", "value": "lunch"},
                {"label": "Bacon (per Pound)", "value": "bacon_perPound"},
                {"label": "Chicken (per Pound)", "value": "whole_chicken"},
                {"label": "Eggs (per Dozen)", "value": "Eggs_per_dozen"},
                {"label": "Milk (per Gallon)", "value": "milk_per_gallon"},
                {"label": "Orange Juice (16oz)", "value": "orange_juice_16oz"},
                {"label": "Rice (per Pound)", "value": "Rice_perPound"},
                {"label": "White Bread (per Pound)", "value": "white_bread_per_pound"},
            ],
            value="Median_Sales_price_house",
            clearable=False,
        )
    ],
    body=True,
    className="mt-4",
)
# ============= dropdown
food_cost_table = dash_table.DataTable(
    id="food-cost-table",
    columns=[
        {"name": "Category", "id": "category"},
        {"name": "Cost ($)", "id": "cost"},
    ],
    style_table={"margin": "20px", "width": "50%"},
    style_header={"fontWeight": "bold"},
)


# ========= Tables
# Create the Household Income Table
income_table_data = [
    {"observation_date": row["observation_date"], "median_income": round(row["Median_house_income"], 2)}
    for _, row in income_df.iterrows()
]

# Create the House Price Table
house_price_table_data = [
    {"observation_date": row["observation_date"], "house_price": round(row["Median_Sales_price_house"], 2)}
    for _, row in houseprice_df.iterrows()
]

# Create the tables for each dataset
income_table = dash_table.DataTable(
    id="income-table",
    columns=[
        {"name": "Date", "id": "observation_date"},
        {"name": "Median Household Income ($)", "id": "median_income"}
    ],
    data=income_table_data,
    style_table={"margin": "20px", "width": "50%"},
    style_header={"fontWeight": "bold"},
)

house_price_table = dash_table.DataTable(
    id="house-price-table",
    columns=[
        {"name": "Date", "id": "observation_date"},
        {"name": "Median House Price ($)", "id": "house_price"}
    ],
    data=house_price_table_data,
    style_table={"margin": "20px", "width": "50%"},
    style_header={"fontWeight": "bold"},
)

# =====  Results Tab components

income_card = dbc.Card(
    [
        dbc.CardHeader("Source data: Median Household Income "),
        html.Div(income_table),
    ],
    className="mt-4",
)


house_price_card = dbc.Card(
    [
        dbc.CardHeader("Source data: Median House Sales Price"),
        html.Div(house_price_table),
    ],
    className="mt-4",
)
# ========= Learn Tab  Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("An Introduction to the Cost of Shelter and Food"),
        dbc.CardBody(about_page),
    ],
    className="mt-4",
)

# ========== Play Tab
play_card = dbc.Card(play_text, className="mt-2")

# =========== Footer Card
footer_card = dbc.Card(
    dbc.CardBody(footer),
 className="mt-4",
)

# ========== Layout Components
tabs = dbc.Tabs(
    [
        dbc.Tab(learn_card, tab_id="tab1", label="Learn"),
        dbc.Tab([play_card,slider_card, dropdown_card,input_groups], tab_id="tab-2", label="Play", className="pb-4"),
        dbc.Tab([html.Div("Income and House price data"),income_card,house_price_card], tab_id="tab-3", label="Results"),
    ],
    id="tabs",
    active_tab="tab-2",
    className="mt-2",
)



# ========== Graph Functions
def median_income_linegraph(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["year"],
        y=data["Median_house_income"],
        mode="lines",
        line=dict(color="blue"),
        name="Median Income"
    ))
    fig.update_layout(title="Median Household Income Over Time", xaxis_title="Year", yaxis_title="Income ($)")
    return fig


def team_expense_linegraph(data, category):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["year"],
        y=data[category],
        mode="lines",
        line=dict(color="green"),
        name=category.capitalize()
    ))
    fig.update_layout(title=f"{category.capitalize()} Over Time", xaxis_title="Year", yaxis_title="Cost ($)")
    return fig


# ========== Meal Cost Calculation
def calculate_meal_cost(data, meal_type):


    data["meal_cost"] = get_meal_cost(data, meal_type)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["year"],
        y=data["meal_cost"],
        mode="lines",
        line=dict(color="orange"),
        name=f"{meal_type.capitalize()} Cost"
    ))

    fig.update_layout(title=f"{meal_type.capitalize()} Cost Over Time", xaxis_title="Year", yaxis_title="Cost ($)")

    return fig


def make_table(family_size, salary, filtered_data, ):
    if filtered_data.empty:
        return []

    # Get meal costs
    breakfast_cost = get_meal_cost(filtered_data, "breakfast", family_size)
    lunch_cost = get_meal_cost(filtered_data, "lunch", family_size)

    # Compute total costs
    daily_food_cost = breakfast_cost + lunch_cost
    yearly_food_cost = daily_food_cost * 365
    food_salary_percentage = (yearly_food_cost / salary) * 100 if salary > 0 else 0
    remaining_salary = salary - yearly_food_cost

    # Create table data
    table_data = [
        {"category": "Daily Cost of Breakfast", "cost": round(float(breakfast_cost), 2)},
        {"category": "Daily Cost of Lunch", "cost": round(float(lunch_cost), 2)},
        {"category": "Total Cost of Food per Day", "cost": round(float(daily_food_cost), 2)},
        {"category": "Total Cost of Food per Year", "cost": round(float(yearly_food_cost), 2)},
        {"category": "Percentage of Salary Spent on Food", "cost": f"{round(food_salary_percentage, 2)}%"},
        {"category": "Remaining Salary After Food", "cost": round(float(remaining_salary), 2)},
    ]

    return table_data


def get_meal_cost(data, meal_type, family_size=1, ):
    if family_size is None:
        family_size =1
    if meal_type == "breakfast":
        meal_cost = (
                (2 / 12) * data["Eggs_per_dozen"] +  # 2 eggs from a dozen
                (3 / 16) * data["white_bread_per_pound"] +  # 3 oz of bread
                (5 * 0.6 / 16) * data["bacon_perPound"]+  # 5 slices of bacon (each 0.6 oz)
                data["orange_juice_16oz"] # 16 oz of orange juice
        )

    elif meal_type == "lunch":
        meal_cost = (
                (8 / 16) * data["Rice_perPound"] +  # 8 oz of rice
                (8 / 16) * data["whole_chicken"]
         # 8 oz of chicken
        )

    return meal_cost * family_size

# Function to generate the tables for household income and house prices
def make_income_and_price_tables(filtered_data):
    if filtered_data.empty:
        return [], []  # return empty lists if there's no data

    # Create the Household Income Table
    income_table_data = [
        {"year": row["year"], "median_income": round(row["Median_house_income"], 2)}
        for _, row in filtered_data.iterrows()
    ]

    # Create the House Price Table
    house_price_table_data = [
        {"year": row["year"], "house_price": round(row["Median_Sales_price_house"], 2)}
        for _, row in filtered_data.iterrows()
    ]

    # Generate the tables for each dataset
    income_table = dash_table.DataTable(
        id="income-table",
        columns=[
            {"name": "Year", "id": "year"},
            {"name": "Median Household Income ($)", "id": "median_income"}
        ],
        data=income_table_data,
        style_table={"margin": "20px", "width": "50%"},
        style_header={"fontWeight": "bold"},
    )

    house_price_table = dash_table.DataTable(
        id="house-price-table",
        columns=[
            {"name": "Year", "id": "year"},
            {"name": "Median House Price ($)", "id": "house_price"}
        ],
        data=house_price_table_data,
        style_table={"margin": "20px", "width": "50%"},
        style_header={"fontWeight": "bold"},
    )

    return income_table, house_price_table