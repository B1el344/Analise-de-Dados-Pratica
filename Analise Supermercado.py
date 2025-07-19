# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:45:38 2025

@author: gabri
"""
#%% Motivo da Analise
## Analise feita em Python com banco de dados público disponivel no Kaggle, usando o software Spyder, pois considero mais amigavel
## e com mais funcionalidades se comparado com o VS Code
## A Presente analise tem como base uma visualização descritiva dos dados
## Foi feita uma regressão para tentar ver se algum componente afeta a receita de vendas , contudo como será visualizado mais abaixo a mesma não foi significativa
## Esse pequeno projeto, foquei menos em explicar os dados, focando mais em maneiras de gerar tabelas e gráficos no Python, a fim de me habituar no mesmo.
#%% Baixando as bibliotecas caso não tenha instaladas

#%% Carregando as bibliotecas
import pandas as pd
import statsmodels.api as sm
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
#%% Carregando o Banco de Dados
vendas_supermercado=pd.read_csv('BalajiFastFoodSales.csv',delimiter=",")
#%% Analisando o Banco de Dados
print(vendas_supermercado)
print(vendas_supermercado.describe())
print(vendas_supermercado.info())
#%% Analises descritiva (Por Tipo de Item)
descritiva_vendas_tipo = vendas_supermercado[['item_type','transaction_amount']]
tabela_vendas_portipo= descritiva_vendas_tipo.groupby('item_type')['transaction_amount'].sum().reset_index()
tabela_vendas_portipo['transaction_amount']=tabela_vendas_portipo['transaction_amount'].map('U${:,.2f}'.format)
print(tabela_vendas_portipo)
#Média
descritiva_vendas_tipo_média = vendas_supermercado[['item_type','transaction_amount']]
descritiva_vendas_tipo_média= descritiva_vendas_tipo_média.groupby('item_type')['transaction_amount'].mean().reset_index()
descritiva_vendas_tipo_média['transaction_amount']=descritiva_vendas_tipo_média['transaction_amount'].map('U${:,.2f}'.format)
print(descritiva_vendas_tipo_média)


# Tabela Formatada (soma)
tabelaf_vendas_portipo = tabulate(
    tabela_vendas_portipo,
    headers=['Tipo de Item', 'Valor Total (U$)'],
    tablefmt='rounded_outline',
    floatfmt=".2f",
    showindex=False
)
print(tabelaf_vendas_portipo)
#%% Analises descritiva (Por Tempo)
#Soma
tabela_vendas_periodo=vendas_supermercado.groupby('time_of_sale')['transaction_amount'].sum().reset_index()
tabela_vendas_periodo['transaction_amount']=tabela_vendas_periodo['transaction_amount'].map('U${:,.2f}'.format)
tabela_vendas_periodo = tabela_vendas_periodo.sort_values('transaction_amount', ascending=False)
print(tabela_vendas_periodo)
#Média
tabelaf_vendas_periodo_média=vendas_supermercado.groupby('time_of_sale')['transaction_amount'].mean().reset_index()
tabelaf_vendas_periodo_média['transaction_amount']=tabelaf_vendas_periodo_média['transaction_amount'].map('U${:,.2f}'.format)
tabelaf_vendas_periodo_média = tabelaf_vendas_periodo_média.sort_values('transaction_amount', ascending=False)
print(tabelaf_vendas_periodo_média)
# Tabela Formatada (soma)
tabelaf_vendas_periodo = tabulate(
    tabela_vendas_periodo,
    headers=['Perido', 'Valor Total (U$)'],
    tablefmt='rounded_outline',  
    floatfmt=".2f",
    showindex=False
)
print(tabelaf_vendas_periodo)

#%% Analises descritiva (Por Item)
#Soma
tabela_vendas_por_item=vendas_supermercado.groupby('item_name')['transaction_amount'].sum().reset_index()
tabela_vendas_por_item['transaction_amount']=tabela_vendas_por_item['transaction_amount'].map('U${:,.2f}'.format)
tabela_vendas_por_item=tabela_vendas_por_item.sort_values('transaction_amount',ascending=False)
print(tabela_vendas_por_item)
#Média
tabela_vendas_por_item_média=vendas_supermercado.groupby('item_name')['transaction_amount'].mean().reset_index()
tabela_vendas_por_item_média['transaction_amount']=tabela_vendas_por_item_média['transaction_amount'].map('U${:,.2f}'.format)
tabela_vendas_por_item_média=tabela_vendas_por_item_média.sort_values('transaction_amount',ascending=False)
print(tabela_vendas_por_item_média)
# Tabela Formatada (soma)
tabelaf_vendas_por_item = tabulate(
    tabela_vendas_por_item,
    headers=['Item', 'Valor Total (U$)'],
    tablefmt='rounded_outline',
    floatfmt=".2f",
    showindex=False)
print(tabelaf_vendas_por_item)

#%% Formatando a data do banco de dados
# Lista de formatos a serem testados (priorizando MM/DD/AAAA e MM-DD-AAAA)
formats = ['%m/%d/%Y', '%m-%d-%Y']

# Função para tentar cada formato
def parse_date(date_str):
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    return pd.NaT  

# Aplicar a função à coluna de datas
vendas_supermercado['data_formatada'] = vendas_supermercado['date'].apply(parse_date)
print(vendas_supermercado[['date', 'data_formatada']])
#%% Analise Descritiva (Pos Mês)
vendas_supermercado['month'] = vendas_supermercado['data_formatada'].dt.month
vendas_supermercado['year'] = vendas_supermercado['data_formatada'].dt.year
vendas_supermercado['month_year'] = vendas_supermercado['data_formatada'].dt.strftime('%m/%Y')

tabela_vendas_mes_e_ano=vendas_supermercado.groupby(['month','year'])['transaction_amount'].sum().reset_index()
tabela_vendas_mes_e_ano['transaction_amount']=tabela_vendas_mes_e_ano['transaction_amount'].map('U${:,.2f}'.format)
print(tabela_vendas_mes_e_ano)

tabela_vendas_mes_e_ano2=vendas_supermercado.groupby('month_year')['transaction_amount'].sum().reset_index()
tabela_vendas_mes_e_ano2['transaction_amount']=tabela_vendas_mes_e_ano2['transaction_amount'].map('U${:,.2f}'.format)
print(tabela_vendas_mes_e_ano)

#%% Ordenando a tabela por Mês e ano
dados = {
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'year': [2023, 2023, 2023, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022, 2022],
    'transaction_amount': ['U$28,670.00', 'U$25,595.00', 'U$25,390.00', 'U$17,670.00', 
                          'U$26,570.00', 'U$17,335.00', 'U$19,490.00', 'U$22,305.00',
                          'U$18,640.00', 'U$27,205.00', 'U$22,900.00', 'U$23,460.00']
}

df = pd.DataFrame(dados)

# Criando uma coluna auxiliar para ordenação
df['ordenacao'] = df.apply(lambda x: (0, x['year'], x['month']) if x['year'] == 2022 else (1, x['year'], x['month']), axis=1)
# Ordenando os dados
df_ordenado = df.sort_values('ordenacao')

# Selecionando apenas as colunas desejadas
df_final = df_ordenado[['month', 'year', 'transaction_amount']]

print(df_final)
#Isso sera usado para gerar um gráfico de linha temporal, bem como agora já conseguimos analisar de forma mais intuitiva o crescimento da empresa ao longo do 
#tempo
#%% Analise Descritiva (Por sexo do Comprador)
tabela_vendas_sexo=vendas_supermercado.groupby('received_by')['transaction_amount'].sum().reset_index()
tabela_vendas_sexo['transaction_amount']=tabela_vendas_sexo['transaction_amount'].map('U${:,.2f}'.format)
tabela_vendas_sexo=tabela_vendas_sexo.sort_values('transaction_amount',ascending=False)
print(tabela_vendas_sexo)

# Tabela Formatada
tabelaf_vendas_sexo = tabulate(
    tabela_vendas_sexo,
    headers=['Sexo','Valor Total (U$)'],
    tablefmt='rounded_outline',
    floatfmt=".2f",
    showindex=False)
print(tabelaf_vendas_sexo)
#%% Tabelas Cruzadas
##### Por Tipo e Perido do Tempo ####

tabela_cruzada1= pd.crosstab(
    index=vendas_supermercado['item_type'], 
    columns=vendas_supermercado['time_of_sale'],
    values=vendas_supermercado['transaction_amount'],
    aggfunc='sum',
    margins=True,
    margins_name="Total").fillna(0)
tabela_formatada = tabela_cruzada1.map(lambda x: f"U${x:,.2f}")
print( tabela_formatada)
### Por Tipo e Sexo do Cliente
tabela_cruzada2= pd.crosstab(
    index=vendas_supermercado['item_type'], 
    columns=vendas_supermercado['received_by'],
    values=vendas_supermercado['transaction_amount'],
    aggfunc='sum',
    margins=True,
    margins_name='Total').fillna(0)
print(tabela_cruzada2)
#%% Tratamento dos dados para analise de Regressão
#A ideia é ver quanto cada variavel afeta na receita total
### Separando um DF com as variaveis x1 , x2 ,x3 e a variavel y 'dependente'
Vendas_supermercado_reg = vendas_supermercado[['transaction_amount','time_of_sale','received_by','item_type']].copy()

## Como são todas variaveis qualitativas podemos dummizar nosso data frame

Vendas_supermercado_reg = pd.get_dummies(
    Vendas_supermercado_reg,
    columns=['time_of_sale', 'item_type', 'received_by'],
    drop_first=True)
Vendas_supermercado_reg.rename(columns={'received_by_Mrs.': 'received_by_Mrs'}, inplace=True)
Vendas_supermercado_reg.info()
#%% Modelo de Regressão

modelo_vendas_supermercado = sm.OLS.from_formula("transaction_amount ~ time_of_sale_Evening +\
                                                   time_of_sale_Midnight +\
                                                   time_of_sale_Morning +\
                                                   time_of_sale_Night  +\
                                                   item_type_Fastfood +\
                                                   received_by_Mrs",Vendas_supermercado_reg).fit()
modelo_vendas_supermercado.summary()

### Nenhum dos coeficientes das variaveis foram significativos o que nos leva a acreditar que tais variaveis não são significativas para determinar e prever 
### a quantidade que cada cliente gasta no supermercado em questão. 

#%%
df_final['mes_ano'] = df_final['month'].astype(str) + '/' + df_final['year'].astype(str)
df_final = df_final.sort_values(['year', 'month'])
print(df_final)
#%% Gráfico evolução das vendas por mês e ano
#Transformando os valores para plotar o gráfico
df_final['valor_numerico'] = df_final['transaction_amount'].str.replace('U$', '').str.replace(',', '').astype(float)
plt.figure(figsize=(19, 8))
plt.plot(df_final['mes_ano'], df_final['valor_numerico'], marker='o', linestyle='-', color='blue')

# Adiciona os valores exatos em cada ponto
for x, y in zip(df_final['mes_ano'], df_final['valor_numerico']):
    plt.text(x, y, f'U${y:,.0f}', ha='center', va='bottom', fontsize=14)

# Formatação 
plt.title('Vendas Mensais (Abr/2022 - Mar/2023) - Variação Real', fontsize=18)
plt.xlabel('Mês/Ano', fontsize=14)
plt.ylabel('Valor das Vendas', fontsize=14)
plt.xticks(rotation=45)
plt.grid(False, axis=x)

# Formata o eixo Y como moeda
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'U${x:,.0f}'))

plt.tight_layout()
plt.show()

#%% Gráfico comparativo por Tipo de Item
tabela_vendas_portipo.info()
#Transformando o DF em float
tabela_vendas_portipo['valor_monetario']= tabela_vendas_portipo['transaction_amount'].str.replace('U$', '').str.replace(',', '').astype(float)
#Gráfico em questão
plt.figure(figsize=(19,8))
sns.barplot(data=tabela_vendas_portipo,
            x="valor_monetario",
            y="item_type",orient='h')

plt.title("Total por Tipo de Item", fontsize=16)
plt.xlabel("Tipo de Item",fontsize=14)
plt.ylabel("Valor Total", fontsize=14)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=13)
plt.show()

#%% Gráfico comparativo por Item
tabela_vendas_por_item.info()
#Transformando o DF em float
tabela_vendas_por_item['valor_monetario']= tabela_vendas_por_item['transaction_amount'].str.replace('U$', '').str.replace(',', "").astype(float)
#Criando um DF de cores para destacar as categorias mais vendidas
colours=['#289490','#289490','#289490','#585c5c','#585c5c','#585c5c','#585c5c']
#Gráfico em questão
plt.figure(figsize=(16,9))
sns.barplot(data=tabela_vendas_por_item,
            x="valor_monetario",
            y="item_name",orient='h',palette=colours)
plt.title("Total por Item", fontsize=16)
plt.xlabel("Item",fontsize=14)
plt.ylabel("Valor Total", fontsize=14)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=13)
plt.show()

#%% Gráfico comparativo por Périodo do Dia
tabela_vendas_periodo.info()
#Transformando o DF em float
tabela_vendas_periodo['valor_monetario']=tabela_vendas_periodo['transaction_amount'].str.replace('U$', '').str.replace(',', '').astype(float)
#Gráfico em questão
plt.figure(figsize=(19,8))
sns.barplot(data=tabela_vendas_periodo,
            x="valor_monetario",
            y="time_of_sale",orient='h')
plt.title("Total por Item", fontsize=16)
plt.xlabel("Item",fontsize=14)
plt.ylabel("Valor Total", fontsize=14)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=13)
plt.show()
#%% Gráfico de composição entre Tipo do Item e Perido do Dia
plot_data = tabela_cruzada1.drop('Total', axis=1).drop('Total', axis=0)

plot_data.plot(kind='barh', 
               stacked=True,
               figsize=(10, 8),  
               color=['#6E7F80', '#808080', '#4D5E5F'])

plt.title('Composição das Vendas por Turno', pad=20)
plt.ylabel('Tipo de Item')  
plt.xlabel('Valor Total (U$)')  
plt.yticks(rotation=0)  
plt.legend(title='Periodo do Dia', bbox_to_anchor=(1.05, 1))  
plt.grid(False,axis='x') 
plt.tight_layout()
plt.show()
#%% Gráfico Tipo de Item e Sexo do Consumidor
plot_data = tabela_cruzada2.drop('Total', axis=1).drop('Total', axis=0)

plot_data.plot(kind='barh', 
               stacked=True,
               figsize=(10, 8),  
               color=['#171f40', '#3d3f47'])

plt.title('Composição das Vendas por Turno', pad=20)
plt.ylabel('Tipo de Item')  
plt.xlabel('Valor Total (U$)')  
plt.yticks(rotation=0)  
plt.legend(title='Sexo do Consumidor', bbox_to_anchor=(1.05, 1))  
plt.grid(False,axis='x') 
plt.tight_layout()
plt.show()