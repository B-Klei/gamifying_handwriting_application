from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import json
from gamification import *

# Open file and convert to json
file = open("dummy.json", "r")
jsonContents = file.read()

data = json.loads(jsonContents)

# Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Variables
# limits
stdLimit = 1.5  #
pointLimit = 20  # 20 points = 20% deviation acceptable

# program
exercisesCompleted = 0
totalExercisePoints = 0
totalPoints = 0

accuracyPoints = 0
tiltPoints = 0
pressurePoints = 0

accuracyBadges = 0
tiltBadges = 0
pressureBadges = 0

x = "10 exercises"  # temporary

# Program
# Points, badges calculation
for exercise in data["exercises"]:
    exercisesCompleted += 1
    totalExercisePoints = 0

    for parameter in exercise["parameters"]:
        if parameter["name"] == "accuracy":
            accuracyPoints = assign_points(parameter["standard deviation"], stdLimit, pointLimit)
            accuracyBadges += assign_badges(accuracyPoints, pointLimit)
            totalExercisePoints += accuracyPoints

        elif parameter["name"] == "tilt":
            tiltPoints = assign_points(parameter["standard deviation"], stdLimit, pointLimit)
            tiltBadges += assign_badges(tiltPoints, pointLimit)
            totalExercisePoints += tiltPoints

        elif parameter["name"] == "pressure":
            pressurePoints = assign_points(parameter["standard deviation"], stdLimit, pointLimit)
            pressureBadges += assign_badges(pressurePoints, pointLimit)
            totalExercisePoints += pressurePoints

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

        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercises"),
                    html.P(("Next badge: ", x)),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted, 10),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width":"80%", "display":"inline-block"}),
                            "grey badge"
                        )
                    )
                ]
            ),
            style={"width": "50%", "display":"inline-block"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercises"),
                    html.P(("Next badge: ", x)),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted, 10),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width":"80%", "display":"inline-block"}),
                            "grey badge"
                        )
                    )
                ]
            ),
            style={"width": "50%", "display":"inline-block"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Exercises"),
                    html.P(("Next badge: ", x)),
                    html.P(
                        (
                            dbc.Progress(value=progress_bar(exercisesCompleted, 10),
                                         color="purple", label=exercisesCompleted,
                                         style={"height": "20px", "width":"80%", "display":"inline-block"}),
                            "grey badge"
                        )
                    )
                ]
            ),
            style={"width": "50%", "display":"inline-block"},
        )
        ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

file.close()
