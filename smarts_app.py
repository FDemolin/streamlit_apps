import streamlit as st
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd
import json

def update_prices(df):
  for row in df.iterrows():
    new_values = f'''
    {{
    "descricao":{row[1][1]}, 
    "precoCusto":{row[1][3]},
    "precoVenda":{row[1][4]}
    }}
    '''
    url_edit = f'https://api.egestor.com.br/api/v1/produtos/{row[1][0]}'
    r_edit = requests.put(url_edit, data=new_values, headers=headers)
    # st.write(r_edit.content)
    if r_edit.status_code != 200:
      st.write(f"Produto {row[1][1]}: Erro ao atualizar ❌")
    else:
      st.write(f"Produto {row[1][1]}: Atualizado com sucesso ✅")
        
  return None
        

data = {'grant_type': 'personal', 'personal_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiI4M2EyZWVkOGU1YzMyMjhlYzc2ODQyM2VhNDFkZjA0NyIsInN1YmRvbWluaW8iOiJzbWFydHNkaXN0cmlidWlkb3JhIiwiY2xpZW50IjoiNjc3ODg2YzE0N2RlZGI1Yjc5MjYzZmNhNTNkMzM1ZjUzZDVhNGY3MyIsImNyZWF0ZWQiOjE2MDAxOTUyMTF9.dPz1g2o1d7l4i0a3z5LHbkcVgP60W/WmsoDa3jRLHi4='}
headers = { 'Content-Type': 'application/json'}
token_req = requests.post('https://v4.egestor.com.br/api/oauth/access_token', json=data, headers=headers)
token_data = token_req.content
my_json_token = json.loads(token_data.decode('utf8'))
df_token = pd.json_normalize(my_json_token)
access_token = df_token['access_token'][0]

del df_token
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer '+ access_token
}

st.title('Atualização de Descrição e Preços')
st.markdown(':red[Atenção ao formato do arquivo, deve conter 5 colunas nessa ordem:] ')
st.text('Cod, Descricao, Categoria, Preço de Custo, Preço de Venda')
df = st.file_uploader("Upload arquivo de preços", type="xlsx")

if df:
  prices_df = pd.read_excel(df)
  st.write(prices_df)
    
bt = st.button("Iniciar Alterações")

if bt:
  update_prices(prices_df)
