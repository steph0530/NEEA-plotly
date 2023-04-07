from dash import Dash,html,dash_table,dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import datetime 
import io
import csv 
import math
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop your CSV file here',
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Checklist(
        ['Default SDR', 'Brightest SDR', 'Default HDR'],
        ['Default SDR', 'Brightest SDR', 'Default HDR'],
        id='checklist',
    ),
    #html.Div(id='output-data-upload'),
    dcc.Graph(id='data-graph'),
])

col_names = [
    'id',#0
    'screen_area(sq)',#1
    'default_ABC_off(nits)',#2
    'default_100/140(nits)',#3
    'default_35/50(nits)',#4
    'default_12/17(nits)',#5
    'defualt_3/4(nits)',#6
    'default_low_backlight(nits)',#7
    'default_mid_backlight(nits)',#8
    'brightest_ABC_off(nits)',#9
    'brightest_100/140(nits)',#10
    'brightest_35/50(nits)',#11
    'brightest_12/17(nits)',#12
    'brightest_3/4(nits)',#13
    'brightest_low_backlight(nits)',#14
    'brightest_mid_backlight(nits)',#15
    'hdr10_ABC_off(nits)',#16
    'hdr10_100/140(nits)',#17
    'hdr10_35/50(nits)',#18
    'hdr10_12/17(nits)',#19
    'hdr10_3/4(nits)',#20
    'hdr10_low_backlight(nits)',#21
    'hdr10_mid_backlight(nits)',#22
    'default_ABC_off(watts)',#23
    'default_100/140(watts)',#24
    'default_35/50(watts)',#25
    'default_12/17(watts)',#26
    'defualt_3/4(watts)',#27
    'default_low_backlight(watts)',#28
    'default_mid_backlight(watts)',#29
    'brightest_ABC_off(watts)',#30
    'brightest_100/140(watts)',#31
    'brightest_35/50(watts)',#32
    'brightest_12/17(watts)',#33
    'brightest_3/4(watts)',#34
    'brightest_low_backlight(watts)',#35
    'brightest_mid_backlight(watts)',#36
    'hdr10_ABC_off(watts)',#37
    'hdr10_100/140(watts)',#38
    'hdr10_35/50(watts)',#39
    'hdr10_12/17(watts)',#40
    'hdr10_3/4(watts)',#41
    'hdr10_low_backlight(watts)',#42
    'hdr10_mid_backlight(watts)',#43
    'default_a1',#44
    'default_a2',#45
    'default_b',#46
    'brightest_a1',#47
    'brightest_a2',#48
    'brightest_b',#49
    'hdr_a1',#50
    'hdr_a2',#51
    'hdr_b'#52
    ]

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
             df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), skiprows=2)
             modified_df = df.iloc[0:59,[0,14,114,115,116,117,118,119,120,123,124,125,126,127,128,129,132,133,134,135,136,137,138,141,142,143,144,145,146,147,150,151,152,153,154,155,156,159,160,161,162,163,164,165,30,31,32,53,54,55,75,76,77]]
    except Exception as e:
        print(e)
        return html.Div([
            'there was an error uploading file'
        ])
    return modified_df
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

      dash_table.DataTable(
            modified_df.to_dict('records'),
            [{'name': i, 'id': i} for i in modified_df.columns]
        ),
        
        html.Hr(),
    ])

@app.callback(Output('data-graph', 'figure'),
              Input('upload-data','contents'),
              Input('checklist', 'value'),
             State('upload-data','filename'),
             State('upload-data','last_modified'))
def update_graph(list_of_contents, checkedItems, list_of_names, list_of_dates):
    fig = go.Figure()
    if list_of_contents is not None:
        modified_df = parse_contents(list_of_contents[0],list_of_names[0],list_of_dates[0])
        modified_df = modified_df.values.tolist()
        #print(modified_df)
        trace_default=[]
        trace_brightest=[]
        trace_hdr=[]
        
        for idx, item in enumerate(modified_df):
            #print(modified_df[idx])
            for i in range(44,53):
                try:
                    float(modified_df[idx][i])
                except Exception as e:
                    modified_df[idx][i]=0

        for l in modified_df:
            for i in range(2,9):
                try:
                    float(l[i])
                    trace_default.append((float(l[i])*float(l[i])*float(l[44]))+(float(l[i])*float(l[45]))+float(l[46]))
                except Exception as e:
                    print('skip')
            for i in range(9,16):
                try:
                    float(l[i])
                    trace_brightest.append((float(l[i])*float(l[i])*float(l[47]))+(float(l[i])*float(l[48]))+float(l[49]))
                except Exception as e:
                    print('skip')
            for i in range(16,23):
                try:
                    float(l[i])
                    trace_hdr.append((float(l[i])*float(l[i])*float(l[50]))+(float(l[i])*float(l[51]))+float(l[52]))
                except Exception as e:
                    print('skip')

        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            writer.writerows(modified_df)
        
        df = pd.read_csv('./output.csv')
        #print('new csv:',df.head())
        if 'Default SDR' in checkedItems:
            x=[df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)']]
            y=[df['default_ABC_off(nits)'].dropna(), df['default_100/140(nits)'].dropna(),df['default_35/50(nits)'].dropna(),df['default_12/17(nits)'].dropna(),df['defualt_3/4(nits)'].dropna(),df['default_low_backlight(nits)'].dropna(),df['default_mid_backlight(nits)'].dropna()]
            z=[df['default_ABC_off(watts)'].dropna(), df['default_100/140(watts)'].dropna(),df['default_35/50(watts)'].dropna(),df['default_12/17(watts)'].dropna(),df['defualt_3/4(watts)'].dropna(),df['default_low_backlight(watts)'].dropna(),df['default_mid_backlight(watts)'].dropna()]
            ids=[df['id'],df['id'],df['id'],df['id'],df['id'],df['id'],df['id']]

            _x = [i for s in x for i in s]
            _y = [i for s in y for i in s]
            _z = [i for s in z for i in s]
            _ids = [int(i) for s in ids for i in s]
            _x = _x[:len(_y)]
            #print(len(_y) == len(_z)) #true

            fig.add_trace(go.Scatter3d(
                x=_x,
                y=_y,
                z=_z,
                text = ['TV ID: %d<br>PPS:Default SDR<br>A: %d in^2<br>DL: %d nits<br>P: %d W'%(i,j,k,l) for i,j,k,l in zip(_ids,_x,_y,_z)],
                hoverinfo = 'text',
                mode='markers',
                marker=dict(
                    size=[5,5,5],
                    sizemode='diameter',
                    color='#4682B4',
                )
            )

            )
            fig.add_trace(go.Scatter3d(
                x=_x,
                y = _y,
                z=trace_default,
                mode='lines',
                line=dict(
                    color="#A0CFEC"
                )
            ))
            
        if 'Brightest SDR' in checkedItems:
            x=(df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'])
            y=(df['brightest_ABC_off(nits)'].dropna(),df['brightest_100/140(nits)'].dropna(), df['brightest_35/50(nits)'].dropna(), df['brightest_12/17(nits)'].dropna(),df['brightest_3/4(nits)'].dropna(),df['brightest_low_backlight(nits)'].dropna(),df['brightest_mid_backlight(nits)'].dropna())
            z=(df['brightest_ABC_off(watts)'].dropna(),df['brightest_100/140(watts)'].dropna(), df['brightest_35/50(watts)'].dropna(), df['brightest_12/17(watts)'].dropna(),df['brightest_3/4(watts)'].dropna(),df['brightest_low_backlight(watts)'].dropna(),df['brightest_mid_backlight(watts)'].dropna())
            ids=[df['id'],df['id'],df['id'],df['id'],df['id'],df['id'],df['id']]

            _x = [i for s in x for i in s]
            _y = [i for s in y for i in s]
            _z = [i for s in z for i in s]
            _ids = [int(i) for s in ids for i in s]
            _x = _x[:len(_y)]
            #print(len(_y) == len(_z)) #true

            fig.add_trace(go.Scatter3d(
                x=_x,
                y=_y,
                z=_z,
                text = ['TV ID: %d<br>PPS:Brightest SDR<br>A: %d in^2<br>DL: %d nits<br>P: %d W'%(i,j,k,l) for i,j,k,l in zip(_ids,_x,_y,_z)],
                hoverinfo = 'text',
                mode='markers',
                marker=dict(
                    size=[5,5,5],
                    sizemode='diameter',
                    color='#AA6C39',
                )
        )
        )
            fig.add_trace(go.Scatter3d(
                x=_x,
                y = _y,
                z=trace_brightest,
                mode='lines',
                line=dict(
                    color="#E6BF83"
                )
            ))

        if 'Default HDR' in checkedItems:
            x=(df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'],df['screen_area(sq)'])
            y=(df['hdr10_ABC_off(nits)'].dropna(),df['hdr10_100/140(nits)'].dropna(),df['hdr10_35/50(nits)'].dropna(),df['hdr10_12/17(nits)'].dropna(),df['hdr10_3/4(nits)'].dropna(),df['hdr10_low_backlight(nits)'].dropna(),df['hdr10_mid_backlight(nits)'].dropna())
            z=(df['hdr10_ABC_off(watts)'].dropna(),df['hdr10_100/140(watts)'].dropna(),df['hdr10_35/50(watts)'].dropna(),df['hdr10_12/17(watts)'].dropna(),df['hdr10_3/4(watts)'].dropna(),df['hdr10_low_backlight(watts)'].dropna(),df['hdr10_mid_backlight(watts)'].dropna())
            ids=[df['id'],df['id'],df['id'],df['id'],df['id'],df['id'],df['id']]

            _x = [i for s in x for i in s]
            _y = [i for s in y for i in s]
            _z = [i for s in z for i in s]
            _ids = [int(i) for s in ids for i in s]
            _x = _x[:len(_y)]
            #print(len(_y) == len(_z))  #true

            fig.add_trace(go.Scatter3d(
                x=_x,
                y=_y,
                z=_z,                
                text = ['TV ID: %d<br>PPS:Default HDR<br>A: %d in^2<br>DL: %d nits<br>P: %d W'%(i,j,k,l) for i,j,k,l in zip(_ids,_x,_y,_z)],
                hoverinfo = 'text',
                mode='markers',
                marker=dict(
                    size=[5,5,5],
                    sizemode='diameter',
                    color='#7D0541',
                )
            )
            )
            fig.add_trace(go.Scatter3d(
                x=_x,
                y = _y,
                z=trace_hdr,
                mode='lines',
                line=dict(
                    color="#BC8F8F"
                )
            ))

        fig.update_layout(
            title='test data',
            width=1000,
            height=1000,
            scene=dict(
                xaxis_title='Screen Area(sq)',
                yaxis_title='Dynamic Luminance (nits)',
                zaxis_title='Power(watts)'
            )
        )
        #fig.show()
    return fig

    
if __name__ == '__main__':
    app.run_server(debug = True) 