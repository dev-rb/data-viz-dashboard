import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from _datetime import date
import flask

data = pd.read_csv("uspollution_pollution_us_2000_2016 1.csv")
data["Date Local"] = pd.to_datetime(data["Date Local"], format="%m/%d/%Y")

scatterFig = px.scatter(data, x="Date Local", y="CO Mean",
                        color="County", render_mode="webgl")
scatterFig.update_yaxes(title_text="CO Mean (Parts per Million)")
fig = px.line(data, x="Date Local", y="CO Mean", color="County",
              render_mode="webgl")

newData = data[data["County"] == "Queens"].groupby(
    (data["Date Local"].dt.year))["CO Mean"].agg(['sum', 'mean', 'max']).reset_index()

server = flask.Flask(__name__)
app = dash.Dash(server=server, title="Data Viz")

app.layout = html.Div(id="spam", className="allContainer", children=[
    html.Div(className="background"),

    html.Div(
        className="appContainer",
        children=[

            html.Div(className='dashboardContainer', children=[
                html.Div(className='graphContainer', children=[
                    html.Div(id='graphOne', className='graph activeGraph', children=[
                        html.Div(id="expandOne",
                                 title="Maximize Graph",
                                 className="expandButton", children="X"),
                        html.Div(id='inactiveScreenOne', className='inactiveScreen', children=[
                            html.H1(className='modifyText',
                                    children='Click to Modify')
                        ]),
                        dcc.Graph(id="figOne", figure=scatterFig, style={
                                  "height": "98%", "width": "98%"}, responsive=True)
                    ]),
                    html.Div(id='graphTwo', className='graph', children=[
                        html.Div(id="expandTwo",
                                 title="Maximize Graph",
                                 className="expandButton", children="X"),
                        html.Div(id='inactiveScreenTwo', className='inactiveScreen', children=[
                            html.H1(className='modifyText',
                                    children='Click to Modify')
                        ]),
                        dcc.Graph(id="figTwo", figure=fig, style={
                                  "height": "98%", "width": "98%"}, responsive=True)
                    ]),

                ]),
                html.Div(id="aggregateContainer", className='aggregateContainer', children=[
                    html.Div(className='aggregateOne', children=[
                        html.H1(id="tableTitleOne",
                                className=" tableTitle", children=""),
                        DataTable(
                            id="aggTableOne",
                            data=newData.to_dict('records'),
                            columns=[{"name": i, "id": i}
                                     for i in newData.columns],
                            style_cell={"textAlign": "left",
                                        "background": "#202020", "color": "white"},
                            style_header={
                                "background": "#202020", "color": "white"}
                        )
                    ]),
                    html.Div(className='seperatorLine', children=[

                    ]),
                    html.Div(className='aggregateTwo', children=[
                        html.H1(id="tableTitleTwo",
                                className=" tableTitle", children=""),
                        DataTable(
                            id="aggTableTwo",
                            data=newData.to_dict('records'),
                            columns=[{"name": i, "id": i}
                                     for i in newData.columns],
                            style_cell={"textAlign": "left",
                                        "background": "#202020", "color": "white"},
                            style_header={
                                "background": "#202020", "color": "white"}
                        )
                    ])
                ])
            ]),

            html.Div(className='settingsContainer', children=[
                html.Div(id="settingsOne", className="settingsOne", children=[
                    # dcc.Slider(id="sliderOne", className="slider",
                    #            min=0, max=20, step=1, value=0),
                     html.H1(className="settingsTitle",
                             children="Visualization 1"),
                     html.H1(className="dateRange label",
                             children="Change Date Range"),
                     dcc.DatePickerRange(id="dateRangeOne", className="dateRangePicker", display_format="YYYY-MM-DD", month_format="MMM YYYY", min_date_allowed=min(
                         data["Date Local"]), max_date_allowed=max(data["Date Local"]), start_date=min(data["Date Local"]), end_date=max(data["Date Local"])),
                     html.H1(className="radioLabel label",
                             children="Choose County"),
                     dcc.RadioItems(id="countyOptionsOne", className="radioChoices", inputClassName="radioInput",
                                    options=[
                                       {"label": "All", "value": "All"},
                                       {"label": "Queens", "value": "Queens"},
                                       {"label": "Bronx", "value": "Bronx"},
                                       {"label": "Suffolk", "value": "Suffolk"},
                                       {"label": "Steuben", "value": "Steuben"},
                                    ], value="All"),
                     html.H1(className="radioLabel label",
                             children="Choose Chemical"),
                     dcc.RadioItems(id="chemicalOptionsOne", className="radioChoices", inputClassName="radioInput",
                                    options=[
                                       {"label": "CO", "value": "CO Mean"},
                                       {"label": "NO2", "value": "NO2 Mean"},
                                       {"label": "O3", "value": "O3 Mean"},
                                       {"label": "SO2", "value": "SO2 Mean"},
                                    ], value="CO Mean"),
                     html.H1(className="textInput label",
                             children="Change X-Axis Label"),
                     dcc.Input(id="xAxisInputOne", type="text",
                               placeholder="X-Axis Label", value="Date Local", debounce=True),
                     html.H1(className="textInput label",
                             children="Change Y-Axis Label"),
                     dcc.Input(id="yAxisInputOne", type="text",
                               placeholder="CO Mean", debounce=True),
                     html.H1(className="textInput label",
                             children="Change Title"),
                     dcc.Input(id="titleInputOne", type="text",
                               placeholder="Title", value="Title", debounce=True),

                     ]),

                html.Div(id="settingsTwo", className="settingsTwo", children=[
                    # dcc.Slider(id="sliderTwo", className="slider",
                    #            min=0, max=20, step=1, value=0),
                    html.H1(className="settingsTitle",
                                      children="Visualization 2"),
                    html.H1(className="dateRange label",
                                      children="Change Date Range"),
                    dcc.DatePickerRange(id="dateRangeTwo", className="dateRangePicker", display_format="YYYY-MM-DD", month_format="MMM YYYY", min_date_allowed=min(
                        data["Date Local"]), max_date_allowed=max(data["Date Local"]), start_date=min(data["Date Local"]), end_date=max(data["Date Local"])),
                    html.H1(className="radioLabel label",
                            children="Choose County"),
                    dcc.RadioItems(id="countyOptionsTwo", className="radioChoices", inputClassName="radioInput",
                                   options=[
                                       {"label": "All", "value": "All"},
                                       {"label": "Queens", "value": "Queens"},
                                       {"label": "Bronx", "value": "Bronx"},
                                       {"label": "Suffolk", "value": "Suffolk"},
                                       {"label": "Steuben", "value": "Steuben"},
                                   ], value="All"),
                    html.H1(className="radioLabel label",
                            children="Choose Chemical"),
                    dcc.RadioItems(id="chemicalOptionsTwo", className="radioChoices", inputClassName="radioInput",
                                   options=[
                                       {"label": "CO", "value": "CO Mean"},
                                       {"label": "NO2", "value": "NO2 Mean"},
                                       {"label": "O3", "value": "O3 Mean"},
                                       {"label": "SO2", "value": "SO2 Mean"},
                                   ], value="CO Mean"),
                    html.H1(className="textInput label",
                            children="Change X-Axis Label"),
                    dcc.Input(id="xAxisInputTwo", type="text",
                              placeholder="X-Axis Label", value="Date Local", debounce=True),
                    html.H1(className="textInput label",
                                      children="Change Y-Axis Label"),
                    dcc.Input(id="yAxisInputTwo", type="text",
                              placeholder="CO Mean", debounce=True),
                    html.H1(className="textInput label",
                                      children="Change Title"),
                    dcc.Input(id="titleInputTwo", type="text",
                              placeholder="Title", value="Title", debounce=True),

                ])
            ]),
        ]),
    html.A(className='footer', href="https://github.com/dev-rb/data-viz-dashboard", target="_blank", children=[
        html.H1(className='name', children='Dev-RB'),
        html.Span(children=""),
        html.Span(children=""),
        html.H1(children='CSCI-39579')
    ])
])

# UI Callbacks


@app.callback(
    Output("graphOne", "className"),
    Output("graphTwo", "className"),
    Output("inactiveScreenOne", "style"),
    Output("inactiveScreenTwo", "style"),
    Output("settingsOne", "style"),
    Output("settingsTwo", "style"),
    [Input("graphTwo", "n_clicks"), Input("graphOne", "n_clicks")]
)
def activeGraph(graphTwo, graphOne):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'graphOne' in changed_id:
        return "graph activeGraph", "graph", {"display": "none"}, {"display": "flex"}, {"display": "flex"}, {"display": "none"}
    elif 'graphTwo' in changed_id:
        return "graph", "graph activeGraph", {"display": "flex"}, {"display": "none"}, {"display": "none"}, {"display": "flex"}
    else:
        return "graph activeGraph", "graph", {"display": "none"}, {"display": "flex"}, {"display": "flex"}, {"display": "none"}


@app.callback(
    Output("graphTwo", "style"),
    Output("aggregateContainer", "style"),
    Output("graphOne", "style"),
    [Input("expandOne", "n_clicks"), Input("expandTwo", "n_clicks")],
    prevent_initial_call=True
)
def expand(expandOne, expandTwo):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if expandOne is not None and expandOne % 2 != 0:
        return {"width": "0", "flex": "0", "display": "none"}, {"height": "0", "flex": "0"}, {"display": "flex"}
    elif expandTwo is not None and expandTwo % 2 != 0:
        return {"flex": "1", "display": "flex"}, {"height": "0", "flex": "0"}, {"width": "0", "flex": "0", "display": "none"}
    return {"flex": "1", "display": "flex"}, {"height": "15rem", "flex": "1"}, {"display": "flex"}
# Functional Callbacks


@app.callback(
    Output("figOne", "figure"),
    [
        Input("countyOptionsOne", "value"), Input("chemicalOptionsOne", "value"), Input("xAxisInputOne", "value"), Input(
            "yAxisInputOne", "value"), Input("titleInputOne", "value"),
        Input("dateRangeOne", "start_date"), Input("dateRangeOne", "end_date")],
    prevent_initial_call=True
)
def changeGraphOne(countyRadio, chemRadio, xTextInput, yTextInput, titleTextInput, startDate, endDate):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    newData = data
    if countyRadio != "All":
        newData = newData.query("County == '{0}'".format(countyRadio))

    start_date = pd.to_datetime(startDate)
    end_date = pd.to_datetime(endDate)
    newData = newData[(newData["Date Local"] >= pd.Timestamp(start_date)) &
                      (newData["Date Local"] <= pd.Timestamp(end_date))]
    scatterFig = px.scatter(newData, x="Date Local", y=chemRadio,
                            color="County", render_mode="webgl")
    scatterFig.update_xaxes(title_text=xTextInput)
    scatterFig.update_yaxes(
        title_text=yTextInput if yTextInput is not None else chemRadio)
    scatterFig.update_layout(title_text=titleTextInput)
    return scatterFig


@app.callback(
    Output("figTwo", "figure"),
    [
        Input("countyOptionsTwo", "value"), Input("chemicalOptionsTwo", "value"), Input(
            "xAxisInputTwo", "value"), Input("yAxisInputTwo", "value"), Input("titleInputTwo", "value"),
        Input("dateRangeTwo", "start_date"), Input("dateRangeTwo", "end_date")],
    prevent_initial_call=True
)
def changeGraphTwo(countyRadio, chemRadio, xTextInput, yTextInput, titleTextInput, startDate, endDate):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    newData = data
    if countyRadio != "All":
        newData = newData.query("County == '{0}'".format(countyRadio))
    start_date = pd.to_datetime(startDate)
    end_date = pd.to_datetime(endDate)
    newData = newData[(newData["Date Local"] >= pd.Timestamp(start_date)) &
                      (newData["Date Local"] <= pd.Timestamp(end_date))]
    fig = px.line(newData, x="Date Local", y=chemRadio, color="County",
                  render_mode="webgl")
    fig.update_xaxes(title_text=xTextInput)
    fig.update_yaxes(
        title_text=yTextInput if yTextInput is not None else chemRadio)
    fig.update_layout(title_text=titleTextInput)
    return fig


@app.callback(
    Output("tableTitleOne", "children"),
    Output("tableTitleTwo", "children"),
    Output("aggTableOne", "data"),
    Output("aggTableTwo", "data"),
    [Input("chemicalOptionsOne", "value"),
     Input("chemicalOptionsTwo", "value")],
)
def updateAggTables(radioOne, radioTwo):
    newData = data[data["County"] == "Queens"].groupby(
        (data["Date Local"].dt.year))[radioOne].agg(['sum', 'mean', 'max']).reset_index()
    newDataTwo = data[data["County"] == "Queens"].groupby(
        (data["Date Local"].dt.year))[radioTwo].agg(['sum', 'mean', 'max']).reset_index()
    return ("{0} Yearly Data".format(radioOne.replace(" Mean", ""))), ("{0} Yearly Data".format(radioTwo.replace(" Mean", ""))), newData.to_dict('records'), newDataTwo.to_dict('records')


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True, dev_tools_hot_reload=True)
