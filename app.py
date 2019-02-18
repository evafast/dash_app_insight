# -*- coding: utf-8 -*-
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pickle as pkl
import pandas as pd
import numpy as np


import dash_daq as daq
from myfunc import rescale


fname = 'rdg_final1.pkl'
with open(fname, 'rb') as InFile:
    model = pkl.load(InFile)

fname = 'colnames_rdg.pkl'
with open(fname, 'rb') as InFile:
    cols = pkl.load(InFile)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = True

server = app.server

colors = {
    'background': '#FFFFFF',
    'text':  '#17202A',
	'title': '#AF2C1F'
}

###
app.layout = html.Div(style={'backgroundColor': colors['background']},

    children=[
    	html.H1(children='Kidney Predict Me',
    	        style={
            		'textAlign': 'center',
            		'color': colors['title'],
            		'marginTop': 15,
            		'marginBottom': 5
        			}
                ),
        html.Label(['Personalized quality of life forecasts for living kidney donors'
        ],
             style = {
                 'font-size' : '16px',
                 'text-align' : 'center',
                 'marginBottom': 25
                    }
    	       ),


html.Div([		#first main block - will be divided into left and right
html.Div([		# start of the left block

#####################all this will be in left block



html.Div([		#top block will be left and right dropdowns
    html.Div([		# start of the left block

        html.Label('Age'),
        dcc.Input(id='age', value= 40, type='number'),

        html.Label('Weight (lbs)'),
        dcc.Input(id='weight', value= 150, type='number'),

],  style={'padding': 8, 'display': 'inline-block'}),

html.Div([
        html.Label('Height - feet'),
        dcc.Input(id='feet', value= 5, type='number'),

        html.Label('Height - inches'),
        dcc.Input(id='inch', value= 8, type='number'),

], style={'padding': 8, 'display': 'inline-block'}),

html.Div([
        html.Label('Blood pressure Systolic'),
        dcc.Input(id='sys', value= 120, type='number'),

        html.Label('Blood pressure Diastolic'),
        dcc.Input(id='dias', value= 80, type='number'),

], style={'padding': 8, 'display': 'inline-block'}),


], style={'float':'center', 'marginLeft':10,}),


html.Div([
        html.Label('Highest completed Education'),
        dcc.Dropdown(
            id='edu',
            options=[
                {'label': 'Grade School', 'value': 'KSOCDON_EDU_Grade_School'},
                {'label': u'High School', 'value': 'KSOCDON_EDU_High_School'},
                {'label': 'Associate degree', 'value': 0},
                {'label': 'Technical School', 'value': 'KSOCDON_EDU_AttendedCollege_TechnicalSchool	'},
                {'label': 'Bachelor degree', 'value': 'KSOCDON_EDU_Bachelordegree'},
                {'label': 'Graduate degree', 'value': 'KSOCDON_EDU_Graduatedegree'},
                    ],
                    value='KSOCDON_EDU_High_School'
                    ),
], style={'padding': 4}),

html.Div([
        html.Label('Marital Status'),
        dcc.Dropdown(
            id='mar',
            options=[
                {'label': 'Married or Live in Partner', 'value': 'KSOCDON_MARSTAT_Married'},
                {'label': u'Single', 'value': 'KSOCDON_MARSTAT_Single'},
                {'label': 'Divorced', 'value': 0},
                {'label': 'Widowed', 'value': 'KSOCDON_MARSTAT_Widowed'},
                    ],
                    value='KSOCDON_MARSTAT_Single'
                    ),
], style={'padding': 4}),

html.Div([
        html.Label('Tobacco use'),
        dcc.Dropdown(
            id='smk',
            options=[
                {'label': 'Currently smoking', 'value': 0}, #'value': ''
                {'label': 'Previously smoking', 'value': 'KHL_TOBACCO_HX_Tobacco_former'},
                {'label': u'Never smoked', 'value': 'KHL_TOBACCO_HX_Tobacco_never'},
                    ],
                    value='KHL_TOBACCO_HX_Tobacco_former'
                    ),
], style={'padding': 4}),

html.Div([		#this is to arrange the buttons next to each other

    html.Div([
        html.Label('Chronic Pain'),
        dcc.RadioItems(
            id='pain',
            options=[
                {'label': 'previous', 'value': 'KHL_COMO_CHRPAIN_chronicpain_previous'},
                {'label': u'never', 'value': 'KHL_COMO_CHRPAIN_chronicpain_never'},
                {'label': 'currently', 'value': 0}
                    ],
                    value='KHL_COMO_CHRPAIN_chronicpain_never'
                    ),
                ], style={'padding': 8,'display': 'inline-block'}),

    html.Div([
        html.Label('History of Surgery'),
        dcc.RadioItems(
            id='surg',
            options=[
                {'label': 'yes', 'value': 'KEVAL_SURGHX_sugicalhx_yes'},
                {'label': u'no', 'value': 0},
                    ],
                    value='KEVAL_SURGHX_sugicalhx_yes'
                    ),
                ], style={'padding': 8,'display': 'inline-block'}),

        html.Div([
        html.Label('Psychiatric Disease'),
        dcc.RadioItems(
            id='psy',
            options=[
                {'label': 'yes', 'value': 'KHL_COMO_PSYCH_psychiatricdiff_yes'},
                {'label': u'no', 'value': 0},
                    ],
                    value='KHL_COMO_PSYCH_psychiatricdiff_yes'
                    ),
                ], style={'padding': 8,'display': 'inline-block'}),

        html.Div([
        html.Label('History of UTI'),
        dcc.RadioItems(
            id='uti',
            options=[
                {'label': 'yes', 'value': 'KHL_COMO_UTI_UTI_yes'},
                {'label': u'no', 'value': 0},
                    ],
                    value='KHL_COMO_UTI_UTI_yes'
                    ),
                ], style={'padding': 8,'display': 'inline-block'}),
]),

html.Div([
        html.Label('Disease in Relative'),
        dcc.Dropdown(
            id='rel1',
            options=[
                {'label': 'Kidney disease', 'value': 'KHL_KDIS_kiddisrela_yesSTDEG_kiddisrela_yes'},
                {'label': u'Heart disease', 'value': 'KHL_HD_heartdrela_yesSTDEG_heartdrela_yes'},
                {'label': 'Hypertension', 'value': 'KHL_HYPTENS_hypertrela_yesSTDEG_hypertrela_yes'}
                    ],
                    multi=True
                    ),
], style={'padding': 8}),

html.Div([
        html.Button(id='submit-button', children='Submit')],
        style = {'text-align' : 'center'}
        ),

    ], className="six columns", style={'marginLeft':20, 'width': '45%'}), ###end of left block

    html.Div([ # start of the right block - where in this case an image will go
        html.Div([

        html.Label(['Fatigue levels'])
        ],
             style = {
                 'font-size' : '24px',
                 'text-align' : 'center',
                 'marginTop':10,
                 'marginBottom':5,
                    }
                    ),

        html.Div([
        daq.Gauge(
        id = 'output-b',
        color={"gradient":True,"ranges":{"red":[0,40],"white":[40,60],"blue":[60,100]}},
        value= 50,
        max=100,
        min=0,
        )
        ],
        style = {
        'text-align' : 'center',
           }
        ),

        html.Div([

        html.Label(['0 = no fatigue, 100 = maximum fatigue'])
        ],
             style = {
                 'font-size' : '14px',
                 'text-align' : 'center',
                    }
                    ),


        html.Div(
        id='output-a',
             style = {
                 'font-size' : '24px',
                 'text-align' : 'center',
                 'marginTop':20,
                 'marginBottom':10,
                    }
                ),

        html.Div([

        html.Label(['The average fatigue level for healthy adults is 47.9.'])
        ],
             style = {
                 'font-size' : '18px',
                 'text-align' : 'center',
                 'padding': 10
                    }
                    ),

        html.Div([

        html.Label(['Disclaimer: This app is not a replacement for a medical diagnosis. It provides personalized information on long term (>1 year after donation) medical outcomes based on a ', html.A('scientific study', href='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4333130/', target='_blank'), ' and should be used in combination with the advice of a qualified healthcare professional. More details about survey questions relating to Fatigue/Energy can be found ', html.A('here.', href='https://www.rand.org/health-care/surveys_tools/mos/36-item-short-form/scoring.html', target='_blank'), ' This project was done as part of Insight Data Science Fellowship, more background on the analysis is available ' , html.A('here.', href='https://docs.google.com/presentation/d/1N0MNjH5wjfrOClCZuA29AoP8MpJYHKPV32sFAvuKuKo/edit?usp=sharing', target='_blank'),])
        ],
             style = {
                 'font-size' : '12px',
                 'text-align' : 'center',
                 'padding': 20
                    }
                ),



        ], className="six columns"), #end of right block

          ]),

])

@app.callback(
   Output('output-a', 'children'),
    [Input('submit-button', 'n_clicks')],
     [State('age', 'value'),
     State('weight', 'value'),
     State('feet', 'value'),
     State('inch', 'value'),
     State('sys', 'value'),
     State('dias', 'value'),
     State('edu', 'value'),
     State('mar', 'value'),
     State('smk', 'value'),
     State('pain', 'value'),
     State('surg', 'value'),
     State('uti', 'value'),
     State('psy', 'value'),
     State('rel1', 'value'),]
)

def predict_energy_level(n_clicks, age, weight, feet, inch, sys, dias, edu, mar, smk, pain, surg, psy, uti, rel):

    bmi = (weight/(feet*12+inch)**2)*703

    imp = pd.DataFrame(columns=cols)
    imp.loc[1] = 0 # this fills everthing with zeros
    imp['AGE_TX'].loc[1] = age
    imp['BMI'].loc[1] = bmi
    imp['AVG_SYS'].loc[1] = sys
    imp['AVG_DIAST'].loc[1] = dias
    if edu != 0:
        imp[edu].loc[1] = 1
    if mar != 0:
        imp[mar].loc[1] = 1
    if smk != 0:
        imp[smk].loc[1] = 1
    if pain != 0:
        imp[pain].loc[1] = 1
    if surg != 0:
        imp[surg].loc[1] = 1
    if uti != 0:
        imp[uti ].loc[1] = 1
    if psy != 0:
        imp[psy].loc[1] = 1
    if rel is not None:
        for i in rel:
            imp[i].loc[1] = 1

    imp = rescale(imp)
    X = imp
    probs = model.predict(X)
    probs = np.squeeze(np.round(probs, decimals=1))

    if  age < 17 or age > 100 or bmi < 10 or bmi > 50 or sys > 200 or sys < 50 or dias > 120 or dias < 20:
        return 'Entered numbers are outside of possible range.'
    return 'Your predicted fatigue level after kidney donation will be {}.'.format(probs)


@app.callback(
   Output('output-b', 'value'),
    [Input('submit-button', 'n_clicks')],
     [State('age', 'value'),
     State('weight', 'value'),
     State('feet', 'value'),
     State('inch', 'value'),
     State('sys', 'value'),
     State('dias', 'value'),
     State('edu', 'value'),
     State('mar', 'value'),
     State('smk', 'value'),
     State('pain', 'value'),
     State('surg', 'value'),
     State('uti', 'value'),
     State('psy', 'value'),
     State('rel1', 'value'),]
)

def predict_energy_level2(n_clicks, age, weight, feet, inch, sys, dias, edu, mar, smk, pain, surg, psy, uti, rel):

    bmi = (weight/(feet*12+inch)**2)*703

    imp1 = pd.DataFrame(columns=cols)
    imp1.loc[1] = 0 # this fills everthing with zeros
    imp1['AGE_TX'].loc[1] = age
    imp1['BMI'].loc[1] = bmi
    imp1['AVG_SYS'].loc[1] = sys
    imp1['AVG_DIAST'].loc[1] = dias
    if edu != 0:
        imp1[edu].loc[1] = 1
    if mar != 0:
        imp1[mar].loc[1] = 1
    if smk != 0:
        imp1[smk].loc[1] = 1
    if pain != 0:
        imp1[pain].loc[1] = 1
    if surg != 0:
        imp1[surg].loc[1] = 1
    if uti != 0:
        imp1[uti ].loc[1] = 1
    if psy != 0:
        imp1[psy].loc[1] = 1
    if rel is not None:
        for i in rel:
            imp1[i].loc[1] = 1

    imp1 = rescale(imp1)
    X1 = imp1
    probs1 = model.predict(X1)
    probs1 = np.squeeze(np.round(probs1, decimals=1))

    if  age < 17 or age > 100 or bmi < 10 or bmi > 50 or sys > 200 or sys < 50 or dias > 120 or dias < 20:
        return 0
    return probs1



if __name__ == '__main__':
    app.run_server(debug=True)
