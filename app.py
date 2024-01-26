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
stdLimit = 1.5  # highest standard deviation for which a badge is awarded
pointLimit = 80  # points awarded for achieving stdLimit

# program
exercisesCompleted = 0  # number of exercises completed
totalExercisePoints = 0  # total points earned during one exercise
totalPoints = 0  # total points earned for all completed exercises

accuracyPoints = 0  # points earned for accuracy
tiltPoints = 0  # points earned for tilt
pressurePoints = 0  # points earned for pressure

accuracyBadges = 0  # number of badges awarded for accuracy
tiltBadges = 0  # number of badges awarded for tilt
pressureBadges = 0  # number of badges awarded for pressure

x = "10 exercises"  # temporary

# Program
# Points, badges calculation
for exercise in data["exercises"]:
    exercisesCompleted += 1  # adds 1 to the number of exercises
    totalExercisePoints = 0  # sets total points earned during one exercise to 0

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

file.close()  # closes dummy.json
