#######################################################
## Carregando as bibliotecas a serem utilizadas########
#######################################################


from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
from numpy.core.fromnumeric import size
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#######################################################
#####Carregando a base de dados a ser utilizada########
#######################################################
'''
Essa é a base de consumo de diferentes bebidas alcoolicas na Russia de 1998 até 2016.
**Context**

This is Alcohol Consumption in Russia (1998-2016) Dataset. It contains values of consumption for wine, beer, vodka, brandy and champagne.

**Content**

Dataset has 1615 rows and 7 columns. Keys for columns:

"year" - year (1998-2016)

"region" - name of a federal subject of Russia. It could be oblast, republic, 
krai, autonomous okrug, federal city and a single autonomous oblast

"wine" - sale of wine in litres by year per capita

"beer" - sale of beer in litres by year per capita

"vodka" - sale of vodka in litres by year per capita

"champagne" - sale of champagne in litres by year per capita

"brandy" - sale of brandy in litres by year per capita

**Acknowledgements**

ЕМИСС (UIISS) - Unified interdepartmental information and statistical system

**Inspiration**

You can analyze the relationships between various years, find best regions by each feature and compare them.

**LINK**:
https://www.kaggle.com/dwdkills/alcohol-consumption-in-russia
'''
df = pd.read_csv('russia_alcohol.csv')

#Sempre fazer uma cópia para evitar modificar o original
global_df = df.copy()

#######################################################
#####Preparação da base de dados ######################
#######################################################


#Criação de uma nova coluna com a soma dos valores de todas as bebidas
global_df['total']=global_df['wine']+global_df['beer']+ global_df['vodka']+global_df['champagne']+global_df['brandy']

#Criação de uma lista contendo as regiões da Russia contida no dataset
regioes=global_df['region'].unique()

#criação de uma lista contendo os tipos de bebidas do dataset
bebidas=['wine','beer','vodka','champagne','brandy','total']

#Criação de uma lista contendo os anos descritos no dataframe

anos=global_df['year'].unique()
#######################################################
#Definição das cores de fundo de gráfico e de texto
# https://colorswall.com/
#######################################################
colors = {
    'background': '#E5E8E8',#fcecd4',
    'text': '#000000'
}

#######################################################
#Para escolher o melhor tema para o dash é só utilizar o site abaixo
#https://www.bootstrapcdn.com/bootswatch/
#######################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SUPERHERO],
                                        # Para responsivilidade para mobile layout
                                        meta_tags=[ {'name': 'viewport',
                                                    'content': 'width=device-width, initial-scale=1.0'}  ] )

#INICIO DA CRIAÇÃO DO LAYOUT DO DASHBOARD

#Para facilitar imagina o Container como uma matriz                                                    
app.layout = dbc.Container([

    dbc.Row([
        #Mais informações dessas mudanças
        #https://hackerthemes.com/bootstrap-cheatsheet/
        ##
        dbc.Col( html.H1('Vendas de bebidas alcoólicas na Russia',                     # text-primary add cor azul no texto
                    className = 'text-center text-primary, display-2 shadow' , ),  # mb-4 cria espaço entre a row do titulo e a row abaixo,
                        width = 10 ) , #Isso é o tamanho do elemento, Imaginar que inicialmente o Dash tem tamanho 12
                                                     # representa o numero de colunas  que posso usar no texto               
        dbc.Col([
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                            html.P("Vinicius Mattoso ",
                                className="card text-white bg-primary text-center"),
                            html.P("Dashboard para auxiliar a tomada de decisão "
                                    "sobre o consumo de alcool nas regiões da Russia nos anos  de 1998-2016.",
                                className="card-text"),    
                            dbc.CardLink(
                                'Linkedin Profile', href='https://www.linkedin.com/in/vinicius-mattoso/',
                            className='text-left text-info'),
                            dbc.CardLink(
                                'Github Profile', href='https://github.com/vinicius-mattoso',
                             className='text-right text-info'),    
                            
                            ]
                        ),

                    ],
                    style={"width": "17rem"},
                                
                    )

            ], width = {'size':2, 'order':2 }) #Estamos colocando a ordem para evitar que ele utilize a ordem dos códigos para criar o dash
       
        ]),
#Criação da segunda linha do dashboard:
#
#CRIAÇÃO DA PRIMEIRA LINHA COM OS COMPONENTES PARA COMANDO DOS PRIMEIROS GRÁFICOS
    dbc.Row([
        
        dbc.Col([
            #Action para escolher qual vai ser a reigão filtrada
                html.H2('Região Selecionada'),
                html.Br(children=[]),
                dcc.Dropdown(id = 'Lineplot-1-dropdown',
                                multi = False,
                                value = 'Republic of Adygea',#Valor Default
                                options = [
                                    {'label': x , 'value': x} for x in global_df['region'].unique() #Aqui estamos passando todas as regiões como opção
                                   ] ),

        ], width = {'size':6, 'order':1 }),

        dbc.Col([
             #Action para escolher qual vai ser a bebida filtrada   
                html.H2('Bebida Selecionada'),
                html.Br(children=[]),
                dcc.RadioItems(id='drink-type',
                                options=[{'label': i, 'value': i} for i in bebidas],
                                value='wine',
                                labelStyle={'display': 'inline-block'}
                            ), 
        ], width = {'size':6, 'order':2 }),
    ], align="center"),
#Criação da terceira linha do dashboard:
#Nessa linha vamos ter dois gráficos, o primeiro vai ocupar 2/3 da linha contendo o line plot para uma determinada região ao longo de todo tempo
# Para o segundo gráfico vai ser mais específico, onde iremos filtrar apenas uma única bebida de uma única região a fim de identificar qualquer ano que possa ser um outlier 
    dbc.Row([
        ################################
        # PRIMEIRO GRÁFICO A SER CRIADO
        ################################
        dbc.Col([
                html.Br(children=[]), 
                dcc.Graph(id = 'line-1-fig-1', figure = {})
                ], width = {'size':6, 'order':1 }), 
        ################################
        # SEGUNDO GRÁFICO A SER CRIADO
        ################################
        dbc.Col([
                html.Br(children=[]),
                dcc.Graph(id = 'line-1-fig-2', figure = {})    
                ], width = {'size':6, 'order':2 }),
        ], align="center"),  # Vertical: start, center, end),

#CRIAÇÃO DE MAIS UMA LINHA NO DASHBOARD
    html.Br(children=[]),
#Essa linha vai conter apenas os actions para os gráficos seguintes
    dbc.Row([
        #Primeira coluna com opção de localização
            dbc.Col([
                    html.H3('Região Selecionada'),
                    dcc.Dropdown(id = 'Regiao_selecionada',
                                # multi = False,
                                value = 'Republic of Adygea',#Valor Default
                                style={'width': "50%"},
                                options = [
                                    {'label': x , 'value': x} for x in global_df['region'].unique() #Aqui estamos passando todas as regiões como opção
                                   ] ),
                    ], width = {'size':6, 'order':1 }),
        #Segunda Coluna coluna com opção de localização
            dbc.Col([
                    html.H3('Ano Base '),
                    dcc.Dropdown(id = 'Anos-opcao1',
                                # multi = False,
                                value = 1998,#Valor Default
                                style={'width': "50%"},
                                options = [
                                    {'label': x , 'value': x} for x in anos #Aqui estamos passando todas as regiões como opção
                                   ] ),
                    ], width = {'size':3, 'order':2 }),
        #Terceira Coluna coluna com opção de localização
            dbc.Col([
                    html.H3('Ano Comparação'),
                    dcc.Dropdown(id = 'Anos-opcao2',
                                # multi = False,
                                value = 2000,#Valor Default
                                style={'width': "50%"},
                                options = [
                                    {'label': x , 'value': x} for x in anos #Aqui estamos passando todas as regiões como opção
                                   ] ),
                    ], width = {'size':3, 'order':3 }),         
        ], justify="center"),
#CRIAÇÃO DE MAIS UMA LINHA NO DASHBOARD
    html.Br(children=[]),
    dbc.Row([
            # PRIMEIRO GRÁFICO A SER CRIADO
        dbc.Col([
                html.Br(children=[]),
                dcc.Graph(id = 'line-2-fig-1', figure = {})
            ], width = {'size':6, 'order':1 }), #Já sabemos que vamos ter 3 gráficos logo cada um vai ocupar 4 unidades
        ################################
        # SEGUNDO GRÁFICO A SER CRIADO
        ################################
            dbc.Col([
                html.Br(children=[]),
                dcc.Graph(id = 'line-2-fig-2', figure = {})
            ], width = {'size':6, 'order':2 }),
    ], align="center"),  # Vertical: start, center, end),

    dbc.Row([
        dbc.Col([
            html.Br(children=[]),
            html.H3('Ano Selecionado'),
            dcc.Dropdown(id = 'Anos-opcao3',
                                # multi = False,
                        value = 1998,#Valor Default
                        style={'width': "50%"},
                        options = [
                                   {'label': x , 'value': x} for x in anos #Aqui estamos passando todas as regiões como opção
                                   ] ),
        ], width = {'size':3, 'order':1 }),
    ], align="center"),

    dbc.Row([
        dbc.Col([
            html.H3(id = 'output_title', children = [], style={'text-align': 'center'} ),
            html.Br(children=[]),
            dcc.Graph(id = 'line-3-fig-1', figure = {})
        ], width = {"size": 10, "offset": 1}),
        
    ], align="center"),

],fluid = True) # para dar um respiro entre as bordas

#Callback para o primeiro gráfico
# Line Plot - Single
@app.callback(
    Output('line-1-fig-1', 'figure'),#(Aonde vamos mudar, o que vamos mudar)
    Input('Lineplot-1-dropdown', 'value')#(daonde vamos receber a info, qual vai ser a info)
)
def update_line_chart_1(regiao_selecionada):
    df_aval_1 = global_df[global_df['region']==regiao_selecionada]#Passando o dataframe já com o filtro da regiao selecionada
    #Criação do primeiro gráfico de linhas
    fig_01 = go.Figure()
    fig_01.add_trace(go.Scatter(x=df_aval_1['year'], y=df_aval_1['wine'],
                    mode='lines+markers',name='Wine'))

    fig_01.add_trace(go.Scatter(x=df_aval_1['year'], y=df_aval_1['beer'],
                    mode='lines+markers',name='Beer'))

    fig_01.add_trace(go.Scatter(x=df_aval_1['year'], y=df_aval_1['vodka'],
                    mode='lines+markers', name='Vodka'))

    fig_01.add_trace(go.Scatter(x=df_aval_1['year'], y=df_aval_1['champagne'],
                    mode='lines+markers', name='Champagne'))

    fig_01.add_trace(go.Scatter(x=df_aval_1['year'], y=df_aval_1['brandy'],
                    mode='lines+markers', name='Brandy'))
    fig_01.add_trace(go.Scatter(x=df_aval_1['year'], y=df_aval_1['total'],
                    mode='lines+markers', name='TOTAL'))
    # #Ciração de um gráfico em barras horizontal
    # figln = px.bar(dff, x='SALES', y='COUNTRY', 
    #                 orientation = 'h',
    #                 color_discrete_sequence = ['#33a5ee'])
    #Atualização do Layout do gráfico, aqui utilizamos as mesmas cores já definidas anteriormente
    fig_01.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )  
    fig_01.update_xaxes(
        title_font_size=15,
        title_text='Ano',
        showgrid=False,
        gridcolor='#7c7c84'
    ) 
    fig_01.update_yaxes(
        title_font_size=15,
        title_text='Venda em litros per capita',
        showgrid=False,
        gridcolor='#7c7c84'
    ) 
    return fig_01

#Callback para o segundo gráfico da primeira linha 

# Line Plot - Single
@app.callback(
    Output('line-1-fig-2', 'figure'),#(Aonde vamos mudar, o que vamos mudar)
    [Input('Lineplot-1-dropdown', 'value'),Input('drink-type', 'value')]#(daonde vamos receber a info, qual vai ser a info)
)
def update_line_chart_2(regiao_selecionada,bebida_selecionada):
    df_aval_2 = global_df[global_df['region']==regiao_selecionada]#Passando o dataframe já com o filtro da regiao selecionada
    df_aval_2=df_aval_2.loc[:, ['year', bebida_selecionada]]#Passando o dataframe já com o filtro da bebida selecionada
    fig_02 = px.scatter(df_aval_2, x="year", y=bebida_selecionada,trendline="ols",size=bebida_selecionada)
    fig_02.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    fig_02.update_xaxes(
        title_font_size=15,
        title_text='Ano',
        showgrid=False,
        gridcolor='#B3B3BD'
        
    ) 
    fig_02.update_yaxes(
        title_font_size=15,
        title_text='Venda em litros per capita',
        gridcolor='#7c7c84'
    )
    
    return fig_02


#Callback para o primeiro gráfico da segunda linha
# Histogram plot
@app.callback(
    Output('line-2-fig-1', 'figure'),#(Aonde vamos mudar, o que vamos mudar)
    [Input('Regiao_selecionada', 'value'),Input('Anos-opcao1', 'value'),Input('Anos-opcao2', 'value')]#(daonde vamos receber a info, qual vai ser a info)
)
def update_histogram_chart_1(regiao_selecionada,Ano_base,Ano_comparacao):
    ##########################
    #preparação do dataframe
    #########################
    #Filtrando por regiao
    df_aval_2 = global_df[global_df['region']==regiao_selecionada]#Passando o dataframe já com o filtro da regiao selecionada
    #Fazendo o filtro dos anos
    df_aval_ano1=df_aval_2.loc[df_aval_2['year']==Ano_base]
    df_aval_ano2=df_aval_2.loc[df_aval_2['year']==Ano_comparacao]
    #Calculadno os valores
    aux_wine=(df_aval_ano2.iloc[0]['wine']-df_aval_ano1.iloc[0]['wine'])/df_aval_ano1.iloc[0]['wine']
    aux_beer=(df_aval_ano2.iloc[0]['beer']-df_aval_ano1.iloc[0]['beer'])/df_aval_ano1.iloc[0]['beer']
    aux_vodka=(df_aval_ano2.iloc[0]['vodka']-df_aval_ano1.iloc[0]['vodka'])/df_aval_ano1.iloc[0]['vodka']
    aux_champagne=(df_aval_ano2.iloc[0]['champagne']-df_aval_ano1.iloc[0]['champagne'])/df_aval_ano1.iloc[0]['champagne']
    aux_brandy=(df_aval_ano2.iloc[0]['brandy']-df_aval_ano1.iloc[0]['brandy'])/df_aval_ano1.iloc[0]['brandy']
    #Criar um dataframe contendo as variações de cada bebida nesse intervalo de ano
    df_graphic=pd.DataFrame({"bebidas":['wine','beer','vodka','champagne','brandy'],"Variacao":[aux_wine,aux_beer,aux_vodka,aux_champagne,aux_brandy]})
    ##################################################
    #Codigo para a criação do Gráfico
    ##################################################

    fig_03 =px.bar(df_graphic, x='bebidas', y='Variacao')
    fig_03.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
                        )
    fig_03.update_xaxes(
        title_font_size=15,
        title_text='Tipo de bebida',
        showgrid=False,
        gridcolor='#7c7c84'
    ) 
    fig_03.update_yaxes(
        tickformat= ".1%",
        title_font_size=15,
        title_text='Variação percentual',
        showgrid=False,
        gridcolor='#7c7c84'
    )
    
    return fig_03

#Callback para o segundo gráfico da segunda linha
# Histogram plot
@app.callback(
    Output('line-2-fig-2', 'figure'),#(Aonde vamos mudar, o que vamos mudar)
    [Input('Regiao_selecionada', 'value'),Input('Anos-opcao1', 'value'),Input('Anos-opcao2', 'value')]#(daonde vamos receber a info, qual vai ser a info)
)
def update_pie_chart_1(regiao_selecionada,Ano_base,Ano_comparacao):
    ##########################
    #preparação do dataframe
    #########################
    #Filtrando por regiao
    df_aval_2 = global_df[global_df['region']==regiao_selecionada]#Passando o dataframe já com o filtro da regiao selecionada
    #Fazendo o filtro dos anos
    df_aval_ano1=df_aval_2.loc[df_aval_2['year']==Ano_base]
    df_aval_ano2=df_aval_2.loc[df_aval_2['year']==Ano_comparacao]
    #Lista contendo as bebidas 
    list_drink=['wine','beer','vodka','champagne','brandy']
    #vetores percentuais de composição
    composicao1=[df_aval_ano1.iloc[0]['wine']/df_aval_ano1.iloc[0]['total']*100,df_aval_ano1.iloc[0]['beer']/df_aval_ano1.iloc[0]['total']*100,df_aval_ano1.iloc[0]['vodka']/df_aval_ano1.iloc[0]['total']*100,df_aval_ano1.iloc[0]['champagne']/df_aval_ano1.iloc[0]['total']*100,df_aval_ano1.iloc[0]['brandy']/df_aval_ano1.iloc[0]['total']*100]
    composicao2=[df_aval_ano2.iloc[0]['wine']/df_aval_ano2.iloc[0]['total']*100,df_aval_ano2.iloc[0]['beer']/df_aval_ano2.iloc[0]['total']*100,df_aval_ano2.iloc[0]['vodka']/df_aval_ano2.iloc[0]['total']*100,df_aval_ano2.iloc[0]['champagne']/df_aval_ano2.iloc[0]['total']*100,df_aval_ano2.iloc[0]['brandy']/df_aval_ano2.iloc[0]['total']*100]
    #criação do gráfico
    # Create subplots: use 'domain' type for Pie subplot
    fig_04 = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=["Composição das vendas do ano de {}".format(Ano_base), "Composição das vendas do ano de {}".format(Ano_comparacao)])
    fig_04.add_trace(go.Pie(labels=list_drink, values=composicao1, name=Ano_base),
              1, 1)
    fig_04.add_trace(go.Pie(labels=list_drink, values=composicao2, name=Ano_comparacao),
              1, 2)
    # Use `hole` to create a donut-like pie chart
    fig_04.update_traces(hole=.4, hoverinfo="label+percent+name")

    return fig_04


#Callback para o primeiro gráfico da terceira linha
# Histogram plot
@app.callback(
    [Output(component_id='output_title', component_property='children'),Output(component_id='line-3-fig-1', component_property='figure')],#(Aonde vamos mudar, o que vamos mudar)
    Input(component_id='Anos-opcao3', component_property='value')#(daonde vamos receber a info, qual vai ser a info)
)
def update_scatter_chart_3(Ano_selecionado):
    ##########################
    #preparação do dataframe
    #########################
    #Filtrando pelo ano
    df_graph= global_df[global_df['year']==Ano_selecionado]#Passando o dataframe já com o filtro da regiao selecionada
    ##################################################
    #Codigo para a criação do Gráfico
    ##################################################
    fig_06 = go.Figure(data=go.Scatter(
                                    x=df_graph['region'],
                                    y=df_graph['total'],
                                    mode='markers',
                                    marker_color=df_graph['total']))
                                #text=df_graph['region'])) # hover text goes here
    title="Total de Vendas por região da Russia no ano de {}".format(Ano_selecionado)
    fig_06.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        font_size=15
                        )
    fig_06.update_xaxes(
        title_font_size=15,
        # title_text='Região da Russia',
        showgrid=False,
        gridcolor='#7c7c84',
        tickangle=45
    ) 
    fig_06.update_yaxes(
        # tickformat= ".1%",
        title_font_size=15,
        title_text='Total de Vendas per capita',
        showgrid=True,
        gridcolor='#7c7c84'
    )
    
    return title, fig_06

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)