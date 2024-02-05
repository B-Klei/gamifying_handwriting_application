from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import csv
from gamification import *
from attribute import *
from dash.dependencies import Input, Output

# Open file and convert to json
with open("dummy.csv", mode='r') as file:
    csv_reader = csv.DictReader(file)
    data = []

    for row in csv_reader:
        data.append(row)

# Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Variables
# misc
pointLimit = 80  #
allGoals = [1, 5, 10, 25, 50, 100]

# exercises
exercisesCompleted = 0
totalExercisePoints = 0
totalPoints = 0

# objects
accuracy = Attribute(1.5, "#ff0055")
tilt = Attribute(1.5, "#070091")
pressure = Attribute(1.5, "#02c42f")

# Program
# Points, badges calculation
for attempt in data:
    exercisesCompleted += 1
    totalExercisePoints = 0

    # Accuracy
    stdAccuracy = attempt['accuracy_std']
    accuracy.points = assign_points(float(stdAccuracy), accuracy.std_limit, 100-pointLimit)
    accuracy.point_list.append(accuracy.points)
    accuracy.badges += assign_badges(accuracy.points, 100-pointLimit)
    totalExercisePoints += accuracy.points

    # Tilt
    stdTilt = attempt['tilt_std']
    tilt.points = assign_points(float(stdTilt), tilt.std_limit, 100-pointLimit)
    tilt.point_list.append(tilt.points)
    tilt.badges += assign_badges(tilt.points, 100-pointLimit)
    totalExercisePoints += tilt.points

    # Pressure
    stdPressure = attempt['pressure_std']
    pressure.points = assign_points(float(stdPressure), pressure.std_limit, 100-pointLimit)
    pressure.point_list.append(pressure.points)
    pressure.badges += assign_badges(pressure.points, 100-pointLimit)
    totalExercisePoints += pressure.points

    totalPoints += totalExercisePoints

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
                                figure=(),
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


if __name__ == "__main__":
    app.run_server(debug=True)
