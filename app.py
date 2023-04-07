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
from utils import get_columns

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

        trace_default=[]
        trace_brightest=[]
        trace_hdr=[]

        _x_default=[]
        _y_default=[]
        _ids_default=[]
        _screen_areas_default=[]

        _x_brightest=[]
        _y_brightest=[]
        _ids_brightest=[]
        _screen_areas_brightest=[]

        _x_hdr=[]
        _y_hdr=[]
        _ids_hdr=[]
        _screen_areas_hdr=[]
        
        for idx, item in enumerate(modified_df):
            for i in range(44,53):
                try:
                    float(modified_df[idx][i])
                except Exception as e:
                    modified_df[idx][i]=0

        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(get_columns())
            writer.writerows(modified_df)
        
        rows=[]
        with open('./output.csv','r') as f:
            lines = csv.reader(f,delimiter='\t')
            for line in lines:
                rows.append(line[0].split(','))

        for row in rows[1:]:
            #default
            if row[2]!= 'nan' and row[23]!= 'nan':
                try:
                    float(row[2])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[2]))
                    _y_default.append(float(row[23]))
                    _screen_areas_default.append(float(row[1]))
                    trace_default.append((float(row[2])*float(row[2])*float(row[44]))+(float(row[2])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e)

            if row[3]!= 'nan' and row[24]!= 'nan':
                try:
                    float(row[3])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[3]))
                    _y_default.append(float(row[24]))
                    _screen_areas_default.append(row[1])
                    trace_default.append((float(row[3])*float(row[3])*float(row[44]))+(float(row[3])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e)

            if row[4]!= 'nan' and row[25]!= 'nan':
                try:
                    float(row[4])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[4]))
                    _y_default.append(float(row[25]))
                    _screen_areas_default.append(float(row[1]))
                    trace_default.append((float(row[4])*float(row[4])*float(row[44]))+(float(row[4])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e)

            if row[5]!= 'nan' and row[26]!= 'nan':
                try:
                    float(row[5])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[5]))
                    _y_default.append(float(row[26]))
                    _screen_areas_default.append(float(row[1]))
                    trace_default.append((float(row[5])*float(row[5])*float(row[44]))+(float(row[5])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e)

            if row[6]!= 'nan' and row[27]!= 'nan':
                try:
                    float(row[6])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[6]))
                    _y_default.append(float(row[27]))
                    _screen_areas_default.append(float(row[1]))
                    trace_default.append((float(row[6])*float(row[6])*float(row[44]))+(float(row[6])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e)

            if row[7]!= 'nan' and row[28]!= 'nan':
                try:
                    float(row[7])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[7]))
                    _y_default.append(float(row[28]))
                    _screen_areas_default.append(float(row[1]))
                    trace_default.append((float(row[7])*float(row[7])*float(row[44]))+(float(row[7])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e) 

            if row[8]!= 'nan' and row[29]!= 'nan':
                try:
                    float(row[8])
                    _ids_default.append(float(row[0]))
                    _x_default.append(float(row[8]))
                    _y_default.append(float(row[29]))
                    _screen_areas_default.append(float(row[1]))
                    trace_default.append((float(row[8])*float(row[8])*float(row[44]))+(float(row[8])*float(row[45])) + float(row[46]))
                except Exception as e:
                    print(e)
            # brightest
            if row[9]!= 'nan' and row[30]!= 'nan':
                try:
                    float(row[9])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[9]))
                    _y_brightest.append(float(row[30]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[9])*float(row[9])*float(row[47]))+(float(row[9])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)

            if row[10]!= 'nan' and row[31]!= 'nan':
                try:
                    float(row[10])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[10]))
                    _y_brightest.append(float(row[31]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[10])*float(row[10])*float(row[47]))+(float(row[10])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)    

            if row[11]!= 'nan' and row[32]!= 'nan':
                try:
                    float(row[11])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[11]))
                    _y_brightest.append(float(row[32]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[11])*float(row[11])*float(row[47]))+(float(row[11])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)  

            if row[12]!= 'nan' and row[33]!= 'nan':
                try:
                    float(row[12])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[12]))
                    _y_brightest.append(float(row[33]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[12])*float(row[12])*float(row[47]))+(float(row[12])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)

            if row[13]!= 'nan' and row[34]!= 'nan':
                try:
                    float(row[13])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[13]))
                    _y_brightest.append(float(row[34]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[13])*float(row[13])*float(row[47]))+(float(row[13])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)

            if row[14]!= 'nan' and row[35]!= 'nan':
                try:
                    float(row[14])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[14]))
                    _y_brightest.append(float(row[35]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[14])*float(row[14])*float(row[47]))+(float(row[14])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)

            if row[15]!= 'nan' and row[36]!= 'nan':
                try:
                    float(row[15])
                    _ids_brightest.append(float(row[0]))
                    _x_brightest.append(float(row[15]))
                    _y_brightest.append(float(row[36]))
                    _screen_areas_brightest.append(float(row[1]))
                    trace_brightest.append((float(row[15])*float(row[15])*float(row[47]))+(float(row[15])*float(row[48])) + float(row[49]))
                except Exception as e:
                    print(e)
            #hdr
            if row[16]!= 'nan' and row[37]!= 'nan':
                try:
                    float(row[16])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[16]))
                    _y_hdr.append(float(row[37]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[16])*float(row[16])*float(row[50]))+(float(row[16])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)                

            if row[17]!= 'nan' and row[38]!= 'nan':
                try:
                    float(row[17])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[17]))
                    _y_hdr.append(float(row[38]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[17])*float(row[17])*float(row[50]))+(float(row[17])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)     

            if row[18]!= 'nan' and row[39]!= 'nan':
                try:
                    float(row[18])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[18]))
                    _y_hdr.append(float(row[39]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[18])*float(row[18])*float(row[50]))+(float(row[18])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)     

            if row[19]!= 'nan' and row[40]!= 'nan':
                try:
                    float(row[16])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[19]))
                    _y_hdr.append(float(row[40]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[19])*float(row[19])*float(row[50]))+(float(row[19])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)     

            if row[20]!= 'nan' and row[41]!= 'nan':
                try:
                    float(row[16])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[20]))
                    _y_hdr.append(float(row[41]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[20])*float(row[20])*float(row[50]))+(float(row[20])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)     

            if row[21]!= 'nan' and row[42]!= 'nan':
                try:
                    float(row[16])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[16]))
                    _y_hdr.append(float(row[37]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[16])*float(row[16])*float(row[50]))+(float(row[16])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)    

            if row[22]!= 'nan' and row[43]!= 'nan':
                try:
                    float(row[16])
                    _ids_hdr.append(float(row[0]))
                    _x_hdr.append(float(row[22]))
                    _y_hdr.append(float(row[43]))
                    _screen_areas_hdr.append(float(row[1]))
                    trace_hdr.append((float(row[22])*float(row[22])*float(row[50]))+(float(row[22])*float(row[51])) + float(row[52]))
                except Exception as e:
                    print(e)     

        if 'Default SDR' in checkedItems:
            fig.add_trace(go.Scatter3d(
                x=_screen_areas_default,
                y=_x_default,
                z=_y_default,
                text = ['TV ID: %s<br>PPS:Default SDR<br>A: %s in^2<br>DL: %s nits<br>P: %s W'%(i,j,k,l) for i,j,k,l in zip(_ids_default,_screen_areas_default,_x_default,_y_default)],
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
                x=_screen_areas_default,
                y = _x_default,
                z=trace_default,
                mode='lines',
                line=dict(
                    color="#A0CFEC"
                )
            ))
            
        if 'Brightest SDR' in checkedItems:
            fig.add_trace(go.Scatter3d(
                x=_screen_areas_brightest,
                y=_x_brightest,
                z=_y_brightest,
                text = ['TV ID: %s<br>PPS:Brightest SDR<br>A: %s in^2<br>DL: %s nits<br>P: %s W'%(i,j,k,l) for i,j,k,l in zip(_ids_brightest,_screen_areas_brightest,_x_brightest,_y_brightest)],
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
                x=_screen_areas_brightest,
                y=_x_brightest,
                z=trace_brightest,
                mode='lines',
                line=dict(
                    color="#E6BF83"
                )
            ))

        if 'Default HDR' in checkedItems:
            fig.add_trace(go.Scatter3d(
                x=_screen_areas_hdr,
                y=_x_hdr,
                z=_y_hdr,                
                text = ['TV ID: %s<br>PPS:Default HDR<br>A: %s in^2<br>DL: %s nits<br>P: %s W'%(i,j,k,l) for i,j,k,l in zip(_ids_hdr,_screen_areas_hdr,_x_hdr,_y_hdr)],
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
                x=_screen_areas_hdr,
                y = _x_hdr,
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