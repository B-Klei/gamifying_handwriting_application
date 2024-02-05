from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import csv
from gamification import *  # functions file
from attribute import *  # attribute class
from dash.dependencies import Input, Output

# Opening file, converting into a list of dictionaries
with open("dummy.csv", mode='r') as file:
    csv_reader = csv.DictReader(file)
    data = []

    for row in csv_reader:
        data.append(row)

# Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Variables
# misc
pointLimit = 80  # number of points awarded for achieving std_limit
allGoals = [1, 5, 10, 25, 50, 100]  # list of all goals

# exercises
exercisesCompleted = 0  # number of completed exercises
totalExercisePoints = 0  # total points earned per exercise
totalPoints = 0  # total points earned

# objects
accuracy = Attribute(1.5, "#ff0055")  # accuracy object
tilt = Attribute(1.5, "#070091")  # tilt object
pressure = Attribute(1.5, "#02c42f")  # pressure object

# Program
# Points, badges calculation
for attempt in data:  # going through data
    exercisesCompleted += 1  # completed exercises counter
    totalExercisePoints = 0  # number of total points earned per exercise set to 0

    # Accuracy
    stdAccuracy = attempt['accuracy_std']  # getting the standard deviation value
    accuracy.points = assign_points(float(stdAccuracy), accuracy.std_limit, pointLimit)  # assigning points
    accuracy.point_list.append(accuracy.points)  # append points to list of points
    accuracy.badges += assign_badges(accuracy.points, pointLimit)  # badges counter
    totalExercisePoints += accuracy.points  # total exercise points counter

    # Tilt
    stdTilt = attempt['tilt_std']  # getting the standard deviation value
    tilt.points = assign_points(float(stdTilt), tilt.std_limit, pointLimit)  # assigning points
    tilt.point_list.append(tilt.points)  # append points to list of points
    tilt.badges += assign_badges(tilt.points, pointLimit)  # badges counter
    totalExercisePoints += tilt.points  # total exercise points counter

    # Pressure
    stdPressure = attempt['pressure_std']  # getting the standard deviation value
    pressure.points = assign_points(float(stdPressure), pressure.std_limit, pointLimit)  # assigning points
    pressure.point_list.append(pressure.points)  # append points to list of points
    pressure.badges += assign_badges(pressure.points, pointLimit)  # badges counter
    totalExercisePoints += pressure.points  # total exercise points counter

    totalPoints += totalExercisePoints  # total points counter

# Layout
"""app.layout = html.Div(

    children=[

        html.H1(children="Avocado Analytics"),

        html.P(

            children=(

                "Analyze the behavior of avocado prices and the number"

                " of avocados sold in the US between 2015 and 2018"

            ),

        ),

        dcc.Graph(

            figure={

                "data": [

                    {

                        "x": data["Date"],

                        "y": data["AveragePrice"],

                        "type": "lines",

                    },

                ],

                "layout": {"title": "Average Price of Avocados"},

            },

        ),

        dcc.Graph(

            figure={

                "data": [

                    {

                        "x": data["Date"],

                        "y": data["Total Volume"],

                        "type": "lines",

                    },

                ],

                "layout": {"title": "Avocados Sold"},

            },

        ),

    ]

)"""

app.layout = html.Div(

    children=[
        dbc.Row(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Exercise results"),
                            html.Div(
                                children=
                                [
                                    html.P("Accuracy:"),
                                    html.P("Tilt:"),
                                    html.P("Pressure:")
                                ],
                                style={"display": "inline-block"}
                            ),
                            html.Div(
                                children=
                                [
                                    html.P(accuracy.points),
                                    html.P(tilt.points),
                                    html.P(pressure.points)
                                ],
                                style={"display": "inline-block"}
                            ),
                            html.Div(
                                children=
                                [
                                    html.P(dbc.Progress(value=progress_bar(accuracy.points, pointLimit),
                                                        color=accuracy.colour,
                                                        style={"height": "20px", "width": "300px"})),
                                    html.P(dbc.Progress(value=progress_bar(tilt.points, pointLimit),
                                                        color=tilt.colour,
                                                        style={"height": "20px", "width": "300px"})),
                                    html.P(dbc.Progress(value=progress_bar(pressure.points, pointLimit),
                                                        color=pressure.colour,
                                                        style={"height": "20px", "width": "300px"}))
                                ],
                                style={"display": "inline-block"}
                            ),
                            html.Div(
                                children=
                                [
                                    html.P("badge" if (accuracy.points >= pointLimit) else "grey badge"),
                                    html.P("badge" if (tilt.points >= pointLimit) else "grey badge"),
                                    html.P("badge" if (pressure.points >= pointLimit) else "grey badge")
                                ],
                                style={"display": "inline-block"}
                            ),

                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Exercises"),
                            html.P(("Next badge: ", next_goal(exercisesCompleted, allGoals), " exercises")),
                            html.P(
                                (
                                    dbc.Progress(value=progress_bar(exercisesCompleted,
                                                                    next_goal(exercisesCompleted, allGoals)),
                                                 color="purple", label=exercisesCompleted,
                                                 style={"height": "20px", "width": "80%", "display": "inline-block"}),
                                    html.P("grey badge", style={"display": "inline-block"})
                                )
                            )
                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.RadioItems(
                                options=[
                                    {"label": "accuracy", "value": "accuracy_graph"},
                                    {"label": "tilt", "value": "tilt_graph"},
                                    {"label": "pressure", "value": "pressure_graph"}
                                ],
                                value="accuracy_graph", inline=True, id="radio", labelStyle={"margin": "10px"}
                            ),
                            dcc.Graph(
                                #figure=(),
                                id="attribute_graph"
                            ),
                        ]
                    ),
                    style={"width": "50%", "display": "inline-block"},
                )
            ]
        )
    ]
)


@app.callback(
    Output('attribute_graph', 'figure'),
    [Input(component_id='radio', component_property='value')]
)
def build_graph(value):
    #figure.update_layout(yaxis_range=[0,100])
    if value == "accuracy_graph":
        return {
                "data": [
                    {
                        "x": [x for x in range(1, exercisesCompleted+1)],
                        "y": accuracy.point_list,
                        "type": "lines",
                        "name": "accuracy",
                        "line": dict(color=accuracy.colour),
                    }
                ],
                #layout={'yaxis': {'range': [0, 100]}}

        }
    elif value == "tilt_graph":
        return {
            "data": [
                {
                    "x": [x for x in range(1, exercisesCompleted+1)],
                    "y": tilt.point_list,
                    "type": "lines",
                    "name": "tilt",
                    "line": dict(color=tilt.colour),
                }
            ]
        }
    elif value == "pressure_graph":
        return {
            "data": [
                {
                    "x": [x for x in range(1, exercisesCompleted+1)],
                    "y": pressure.point_list,
                    "type": "lines",
                    "name": "pressure",
                    "line": dict(color=pressure.colour),
                }
            ]
        }


# Layout description
# first row:
#   Exercise result: heading; points, progress bar, badge for each attribute
#   Completed exercises: heading; next goal; progress bar and badge
# second row:
#   Attribute graph(s): radio items; graph

# Display in browser
if __name__ == "__main__":
    app.run_server(debug=True)  # "debug=True": being able to edit while program is running
