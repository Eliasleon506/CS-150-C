from dash import dcc, html, dash_table
## This page has any Text used

about_page = html.Div(
    dcc.Markdown(
        """
        This app allows users to explore the relationship between household income, house prices, and food costs over time. 
        This is to get an idea and understand how the cost of living has changed over the years.

         What are we Seeing?:
        - **Median Household Income**: Shows the average income of households over the years.
        - **Median House Prices**: Displays the trend of house prices over the years.
        - **Food Costs**: Provides data on the cost of meals, including breakfast and lunch, adjusted for family size.
        
        Use the Slider to see different year ranges that show median income has changed.  Try different item on the dropdown to see how prices have changed through the years.  Input you data, or your future families data to see what you basic food costs will be. 
        
         **Breakfast Cost Breakdown**
        A typical breakfast consists of:
        - **Eggs**: 2 eggs (calculated from the price per dozen)
        - **Bread**: 3 slices of white bread (each slices weighs abot 1oz from the price per pound) Note 
        - **Bacon**: 5 slices (each slice weighs about 0.6 oz, calculated from the price per pound)
        - **Orange Juice**: 16 ounces (full serving from the price per 16oz bottle)

        This is a pretty basic breakfast. Serving sizes are not standard.  

         **Lunch Cost Breakdown**
        A typical lunch consists of:
        - **Rice**: 8 ounces (half a pound, calculated from the price per pound)
        - **Chicken**: 8 ounces (half a pound, using the price per pound of whole chicken)

        This bare minimum lunch. These are the standard serving sizes 
        
        The data was sources from FRED(FEDERAL RESERVE BANK oF ST. LOUIS) and is the average or median prices taken from the US.   
        """


    )
)
play_text = html.Div(dcc.Markdown(
    """
> **Living Cost** When brought to their very basic needs are shelter and food.   Play with the app and see if you could afford it!

> See how housing and different food items have been priced over time. Enter your information to see what your basic food cost are.  
"""
))

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only and is not a substitute for professional advice and
        services from qualified financial services providers familiar with your financial
        situation.    
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)