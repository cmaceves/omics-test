#app.py 
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from ast import literal_eval as make_tuple
app = dash.Dash(__name__)
server = app.server

"""
df = pd.read_csv('overlap.csv')
elements = []

with open('supplementary_msv.json') as f:
    msv_data = json.load(f)


#creating the nodes
all_nodes = df['set'].tolist()
all_nodes = [make_tuple(item) for item in all_nodes]
flatten = []
for item in all_nodes:
    flatten.append(item[0])
    flatten.append(item[1])
all_nodes = np.unique(flatten).tolist()

for node in all_nodes:
    temp_dict = {'data': {'id': node, 'label': node, 'description': msv_data[node][0]}}
    elements.append(temp_dict)

#creating the edges
for index, row in df.iterrows():
    set_val = make_tuple(row['set']) 
    cosine_text = row['cosine-text']
    num_comp = row['num_compounds']
    if cosine_text < 0.20:
        if num_comp >  0.90:
            print(set_val)
            
        
        #if set_val[0] in all_nodes and set_val[1] in all_nodes:
        #    temp_dict = {"data": {'source': set_val[0], 'target':set_val[1], 'compounds':num_comp}}
        #    elements.append(temp_dict)

sys.exit(0)
json_dict = {'elements':elements}
with open('elements.json', 'w') as f:
    json.dump(json_dict, f)
"""

with open('elements.json', 'r') as f:
    data = json.load(f)
elements = data['elements']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
	 {
            'selector': 'edge',
            'style': {
                'label': 'data(compounds)'
            }
        }
]


app.layout = html.Div([
    html.P("Massive Datasets Networked by Text Relationship:"),
    #drop down menu for node labeling options
    dcc.Dropdown(
        id='dropdown-update-nodes',
        value='none',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['description', 'label', 'none']
        ]
    ),

    #dropdown menu for edge labeling options
    dcc.Dropdown(
        id='dropdown-update-edges',
        value='none',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['cosine score', 'none']
        ]
    ),

    cyto.Cytoscape(
        id='cytoscape-event-callbacks-2',
        elements=elements,
        layout={'name': 'cose'},
        stylesheet=default_stylesheet,
        style={'width': '2000px', 'height': '3000px'}
    )
])

@app.callback(Output('cytoscape-event-callbacks-2', 'stylesheet'),
              Input('dropdown-update-nodes', 'value'),
              Input('dropdown-update-edges', 'value'))
def update_stylesheet(node_label, edge_label):
    print(node_label)
    print(edge_label)
    if node_label is None:
        node_label = ''
    if node_label == 'none':
        node_label = ''
    if edge_label is None:
        edge_label = ''
    if edge_label == 'cosine score':
        edge_label = 'compounds'
    if edge_label == 'none':
        edge_label = ''
    
    new_style = [ 
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(%s)' %node_label
        }
    },
	 {
            'selector': 'edge',
            'style': {
                'label': 'data(%s)' %edge_label
            }
        }
    ]
    return default_stylesheet + new_style

if __name__ == '__main__':
    app.run_server(debug=True)
