
import pandas as pd
import lasio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from io import StringIO
st.title("LWD Log Quality Control Algorithm")
uploaded_file=st.file_uploader("Suba su .las aca para empezar el proceso")
#if uploaded_file:
    #bytes_data= uploaded_file.read()
    #str_io=StringIO(bytes_data.decode('Windows-1252'))
    #las= lasio.read(str_io)
las = lasio.read("https://github.com/josedanielbg/LWD-QC/blob/main/ALD%20PALOGRANDE.las")
# In[ ]:
df = las.df()
# In[ ]:
df.reset_index(inplace=True)
# In[ ]:
#PASAR DE EPOCH A FECHA 
df["DATE"]=pd.to_datetime(las["TIME"],unit='s')
# In[ ]:
df.head()
dftamaño=len(df.axes[0])
# In[ ]:
#ELIMINAR VALORES ERRONEOS DE TIEMPO Y ELIMINAR 0 PARA EVITAR INFINITOS
df=df.loc[df['TIME']> 800000000]
df.set_index("DATE", inplace=True)
df.replace(to_replace = 0, value =0.001, inplace=True)
df.head()
# In[ ]:
#TRACK NO 1 AVERAGE FAR AND NEAR DENSITY
st.subheader("TRACK1")
df1=df[['ALNDA', 'ALFDA']]
# In[ ]:
#CALCULAR DIF ABSOLUTA PARA VER DISTANCIA ENTRE CURVAS
df1["dif_abs"]=100*np.abs((df1["ALNDA"]-df1["ALFDA"])/df1["ALNDA"])
# In[ ]:
#FILTRAR DISTANCIA ENTRE CURVAS
#df1[df1["dif_abs"]>=300]
# In[ ]:
#FLAG DE DATOS DISCORDANTES EN DISTANCIA
df1["flg_CompAD"]=0
df1.loc[df1["dif_abs"]>= 300, "flg_CompAD"] = 1
flag_CompADshow= df1["flg_CompAD"] == 1
flag_CompAD=df1[flag_CompADshow]
flag_CompADtamaño=len(flag_CompAD.axes[0])
# In[ ]:
#FIGURA DE LOGPLOT DE LOS TRACKS
fig1, ax1 = plt.subplots(nrows=1, ncols=3, figsize=(10,10), sharey=True)
fig1.suptitle("TRACK AVERAGE FAR & NEAR DENSITY", fontsize=20,va="top")
fig1.subplots_adjust(top=0.8,wspace=0.25)
#1st track: AVERAGE FAR & NEAR DENSITY
ax01=ax1[0].twiny()
ax01.invert_xaxis()
ax01.invert_yaxis()
ax01.set_xlim(1.95,2.95)
ax01.set_ylim([np.min(df1.index), np.max(df1.index)])
ax01.spines['top'].set_position(('outward',10))
ax01.set_xlabel("ALNDA")
ax01.plot(df1["ALNDA"], df1.index,"--", label='ALNDA', color='red')
ax01.set_xlabel('ALNDA',color='red')    
ax01.tick_params(axis='x', colors='red')
ax11=ax1[0].twiny()
ax11.invert_xaxis()
ax11.invert_yaxis()
ax11.set_xlim(1.95,2.95)
ax11.plot(df1["ALFDA"], df1.index, label='ALFDA', color='blue') 
ax11.spines['top'].set_position(('outward',40))
ax11.set_xlabel('ALFDA',color='blue')    
ax11.tick_params(axis='x', colors='blue')
ax11.grid(True)
#2nd track: DIFERENCIA ABSOLUTA ENTRE CURVAS 
ax02=ax1[1].twiny()
ax02.invert_xaxis()
ax02.invert_yaxis()
ax02.set_xlim(0,400)
ax01.set_ylim([np.max(df1.index), np.min(df1.index)])
ax02.spines['top'].set_position(('outward',30))
ax02.set_xlabel('Dif_Abs[%]')
ax02.plot(df1.dif_abs, df1.index,"--", label='Dif_Abs[%]', color='lime')
ax02.set_xlabel('Dif_Abs[%]', color='lime')
ax02.tick_params(axis='x', colors='lime')    
ax02.grid(True)
#3rd track: FLAG DE DATOS DISCORDANTES EN DISTANCIA
ax04=ax1[2].twiny()
ax04.invert_xaxis()
ax04.invert_yaxis()
ax04.set_xlim(0,1)
ax04.spines['top'].set_position(('outward',5))
ax04.set_xlabel('Flag_Comportamiento AD')
ax04.fill_between(df1.flg_CompAD, df1.index, label="Flag Diferencia entre curvas", color='g') 
ax04.set_xlabel('Curvas Cerca [0] - Curvas Separadas [1]', color='g')
ax04.tick_params(axis='x', colors='g')
ax04.grid(True)

# In[ ]:
#HISTOGRAMA DISTANCIA ENTRE CURVAS AVERAGE FAR & NEAR DENSITY
hist1 = go.Figure(go.Histogram(x=df1["dif_abs"], xbins=dict(start=0,end=600,size=10),autobinx=False,marker_color='#CC0001'))
hist1.add_vline(x=300, line_dash = 'dash', line_color = 'firebrick',annotation_text="Max", 
              annotation_position="top right")
hist1.update_layout(
    title={
        'text': "Histograma Diferencia Absoluta entre curvas Average Density",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Diferencia Absoluta %",
    yaxis_title="Frecuencia De Dato",
    bargap = 0.1)
st.write("**Valores fuera de rango**")     
st.write("Tienes",flag_CompADtamaño,"Datos fuera de rango")   
c_1,c_2= st.columns(2,gap="medium")
st.plotly_chart(hist1)
c_1,c_2= st.columns(2,gap="medium")
c_1.pyplot(fig1)
c_2.write(flag_CompAD)
# In[ ]:
st.subheader("TRACK2")
#ALD PEAK RESOLUTION & PEAK LOCATION
df3_1=df[["ALFPR","ALNPR","ALFPL","ALNPL"]]
#Sacar índices con nan
list_nanPR = df3_1.index[((df3_1['ALFPR'].isna())|(df3_1['ALNPR'].isna()))].tolist()
tamañoPR=len(list_nanPR)
#Macar nan con true y false
nan_ALNPR = df3_1['ALNPR'].isna()
nan_ALFPR = df3_1['ALFPR'].isna()
df3_1["nan_ALNPR"]=nan_ALNPR
df3_1["nan_ALFPR"]=nan_ALFPR
#Flag Nan´s
def flag_2(row):
    gap = True
    no_gap = False
    if (row.nan_ALFPR == gap) and (row.nan_ALNPR == gap) :
        return 1
    else:
        return 0
df3_1.loc[:, 'flag_2'] = df3_1.apply(flag_2, axis = 1)
# In[ ]:
#FLAG DE RANGOS PARA RES Y LOCATION
df3_1.loc[df3_1['ALFPR']<= 6,"mayor"] = 1
df3_1.loc[df3_1['ALNPR']<= 6,"mayor"] = 1
df3_1.loc[df3_1['ALFPR']>= 16,"menor"] = 1
df3_1.loc[df3_1['ALNPR']>= 16,"menor"] = 1
df3_1['mayor'] = df3_1['mayor'].fillna(0)
df3_1['menor'] = df3_1['menor'].fillna(0)
flg_rngALDRes=df3_1["menor"]+df3_1["mayor"]
df3_1["flg_rngALDRes"]=flg_rngALDRes
flg_rngALDReshow= df3_1["flg_rngALDRes"] >= 1
flg_rngALDRes=df3_1[flg_rngALDReshow]
flg_rngALDRestamaño=len(flg_rngALDRes.axes[0])
# In[ ]:
#FIGURA DE LOGPLOT DE LOS TRACKS
fig2, ax2 = plt.subplots(nrows=1, ncols=3, figsize=(10,10), sharey=True)
fig2.suptitle("Peak Resolution", fontsize=20,va="top")
fig2.subplots_adjust(top=0.8,wspace=0.25)
df3_1["flg_rngALDRes"].replace(to_replace = 2, value =1, inplace=True)
#1st track: ALD PEAK RESOLUTION & PEAK LOCATION
ax01=ax2[0].twiny()
ax01.invert_xaxis()
ax01.invert_yaxis()
ax01.set_xlim(0,50)
ax01.set_ylim([np.max(df3_1.index), np.min(df3_1.index)])
ax01.spines['top'].set_position(('outward',10))
ax01.set_xlabel("ALFPR")
ax01.plot(df3_1["ALFPR"], df3_1.index,"--", label='ALNPR', color='red')
ax01.set_xlabel('ALFPR',color='red')    
ax01.tick_params(axis='x', colors='red')
ax11=ax2[0].twiny()
ax11.invert_xaxis()
ax11.invert_yaxis()
ax11.set_xlim(0,50)
ax11.plot(df3_1["ALNPR"], df3_1.index,"--" ,label='ALNPR', color='blue') 
ax11.spines['top'].set_position(('outward',40))
ax11.set_xlabel('ALNPR',color='blue')    
ax11.tick_params(axis='x', colors='blue')
ax11.grid(True)
   #2rd track: FLAG DATOS EN RANGO ACEPTABLE
ax02=ax2[1].twiny()
ax02.invert_xaxis()
ax02.invert_yaxis()
ax02.set_xlim(0,1)
ax02.spines['top'].set_position(('outward',10))
#ax02.plot(df3_1["flg_rngALDRes"], df3_1.index,"--", label='ALNPR', color='red')
ax02.fill_between(df3_1.flg_rngALDRes, df3_1.index, label="Flag Rango Aceptable", color='blue') 
ax02.set_xlabel('En rango [0] - Fuera de rango [1]', color='blue')
ax02.tick_params(axis='x', colors='blue')
ax02.grid(True)
ax03=ax2[2].twiny()
ax03.invert_xaxis()
ax03.invert_yaxis()
ax03.set_xlim(0,1)
ax03.spines['top'].set_position(('outward',40))
ax03.set_xlabel('Flag Valores Nulos')
ax03.fill_between(df3_1.flag_2,0, label='Valores nulos', color='r')
ax03.set_xlabel('Hay valores [0] - No exsiten Valores [1]', color='r')
ax03.tick_params(axis='x', colors='red')
# In[ ]:
#HISTOGRAMA CS PEAK RESOLUTION
x0=df3_1["ALFPR"]
x1=df3_1["ALNPR"]
hist2 = go.Figure()
hist2.add_trace(go.Histogram(x=x0,xbins=dict(start=0,end=40,size=2),autobinx=False,marker_color='#CC0001',name="ALFPR"))
hist2.add_trace(go.Histogram(x=x1,xbins=dict(start=0,end=40,size=2),autobinx=False,marker_color='#000000',name="ALNPR"))
hist2.add_vline(x=6, line_dash = 'dash', line_color = 'firebrick',annotation_text="Min", 
              annotation_position="top right")
hist2.add_vline(x=16, line_dash = 'dash', line_color = 'firebrick',annotation_text="Max", 
              annotation_position="top right")
hist2.update_layout(
    title={
        'text': "Histograma Cs Peak Resolution",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    
    xaxis_title="CS peak resolution %",
    yaxis_title="Frecuencia De Dato",
    bargap = 0.05,
    barmode="stack")
st.write("**Valores Nulos**")  
list_nanPR
st.write("Tiene",tamañoPR,"Datos Nulos")
st.write("**Valores fuera de rango**")    
st.write("Tienes",flg_rngALDRestamaño,"Datos fuera de rango")
st.plotly_chart(hist2)   
c_1,c_2= st.columns(2,gap="medium")
c_1.pyplot(fig2)
c_2.write(flg_rngALDRes)    
# In[ ]:
st.subheader("TRACK2.1")
#FLAG RANGO ACEPTABLE PEAK LOCATION
df3_1.loc[df3_1['ALFPL']<= 195,"c_mayor"] = 1
df3_1.loc[df3_1['ALNPL']<= 195,"c_mayor"] = 1
df3_1.loc[df3_1['ALFPL']>= 205,"c_menor"] = 1
df3_1.loc[df3_1['ALNPL']>= 205,"c_menor"] = 1
df3_1['c_mayor'] = df3_1['c_mayor'].fillna(0)
df3_1['c_menor'] = df3_1['c_menor'].fillna(0)
flg_rngALDCuentas=df3_1["c_menor"]+df3_1["c_mayor"]
df3_1["flg_rngALDCuentas"]=flg_rngALDCuentas
flg_rngALDCshow= df3_1["flg_rngALDCuentas"] >= 1
flg_rngALDCuentas=df3_1[flg_rngALDCshow]
flg_rngALDCtamaño=len(flg_rngALDCuentas.axes[0])
# In[ ]:
#FIGURA DE LOGPLOT DE LOS TRACKS
fig3, ax3 = plt.subplots(nrows=1, ncols=3, figsize=(10,10), sharey=True)
fig3.suptitle("Peak Location", fontsize=20,va="top")
fig3.subplots_adjust(top=0.8,wspace=0.25)
df3_1["flg_rngALDCuentas"].replace(to_replace = 2, value =1, inplace=True)
#1st track: NEAR Y FAR PEAK LOCATION
ax01=ax3[0].twiny()
ax01.invert_xaxis()
ax01.invert_yaxis()
ax01.set_xlim(190,210)
ax01.set_ylim([np.max(df3_1.index), np.min(df3_1.index)])
ax01.spines['top'].set_position(('outward',10))
ax01.set_xlabel("ALFPL")
ax01.plot(df3_1["ALFPL"], df3_1.index,"--", label='ALFPL', color='red')
ax01.set_xlabel('ALFPL',color='red')    
ax01.tick_params(axis='x', colors='red')
ax11=ax3[0].twiny()
ax11.invert_xaxis()
ax11.invert_yaxis()
ax11.set_xlim(190,210)
ax11.plot(df3_1["ALNPL"], df3_1.index,"--", label='ALNPL', color='blue') 
ax11.spines['top'].set_position(('outward',40))
ax11.set_xlabel('ALNPL',color='blue')    
ax11.tick_params(axis='x', colors='blue')
ax11.grid(True)
   #2nd track:FLAG RANGO ACEPTABLE PEAK LOCATION
ax02=ax3[1].twiny()
ax02.invert_xaxis()
ax02.invert_yaxis()
ax02.set_xlim(-1,2)
ax02.spines['top'].set_position(('outward',10))
ax02.set_ylim([np.max(df3_1.index), np.min(df3_1.index)])
ax02.fill_between(df3_1.flg_rngALDCuentas, df3_1.index, label="Flag Rango Aceptable", color='blue') 
ax02.set_xlabel('En rango [0] - Fuera de rango [1]', color='blue')
ax02.tick_params(axis='x', colors='blue')
ax02.grid(True)
ax03=ax3[2].twiny()
ax03.invert_xaxis()
ax03.invert_yaxis()
ax03.set_xlim(0,1)
ax03.spines['top'].set_position(('outward',40))
ax03.set_xlabel('Flag Valores Nulos')
ax03.set_ylim([np.max(df3_1.index), np.min(df3_1.index)])
ax03.fill_between(df3_1.flag_2,0, label='Valores nulos', color='r')
ax03.set_xlabel('Hay valores [0] - No exsiten Valores [1]', color='r')
ax03.tick_params(axis='x', colors='red')

# In[ ]:
#HISTOGRAMA CS PEAK LOCATION
x0=df3_1["ALFPL"]
x1=df3_1["ALNPL"]
hist3 = go.Figure()
hist3.add_trace(go.Histogram(x=x0,xbins=dict(start=180,end=260,size=5),autobinx=False,marker_color='#CC0001',name="ALFPR"))
hist3.add_trace(go.Histogram(x=x1,xbins=dict(start=180,end=260,size=5),autobinx=False,marker_color='#000000',name="ALNPR"))
hist3.add_vline(x=195, line_dash = 'dash', line_color = 'firebrick',annotation_text="Min", 
              annotation_position="top right")
hist3.add_vline(x=205, line_dash = 'dash', line_color = 'firebrick',annotation_text="Max", 
              annotation_position="top right")
hist3.update_layout(
    title={
        'text': "Histograma Cs Peak Location",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    
    xaxis_title="Cs Peak Location",
    yaxis_title="Frecuencia De Dato",
    bargap = 0.05,
    barmode="stack")
st.write("**Valores Nulos**")  
list_nanPR
st.write("Tiene",tamañoPR,"Datos Nulos")
st.write("**Valores fuera de rango**")    
st.write("Tienes",flg_rngALDCtamaño,"Datos fuera de rango")
st.plotly_chart(hist3)   
c_1,c_2= st.columns(2,gap="medium")
c_1.pyplot(fig3)
c_2.write(flg_rngALDCuentas)    
# In[ ]:
#CUENTAS PER SEC
st.subheader("Track 3")
df4=df[["ALFPC","ALNPC"]]
# In[ ]:
#Sacar índices con nan
list_nanPC = df4.index[((df4['ALFPC'].isna())|(df4['ALNPC'].isna()))].tolist()
tamañoPC=len(list_nanPC)
#Macar nan con true y false
nan_ALNPC = df4['ALNPC'].isna()
nan_ALFPC = df4['ALFPC'].isna()
df4["nan_ALNPC"]=nan_ALNPC
df4["nan_ALFPC"]=nan_ALFPC
#Flag Nan´s
def flag_2(row):
    gap = True
    no_gap = False
    if (row.nan_ALFPC == gap) and (row.nan_ALNPC == gap) :
        return 1
    else:
        return 0
df4.loc[:, 'flag_2'] = df4.apply(flag_2, axis = 1)
# In[ ]:


#CALCULAR DIF ABSOLUTA PARA VER DISTANCIA ENTRE CURVAS
df4["dif_abs"]=100*np.abs((df4["ALFPC"]-df4["ALNPC"])/df4["ALFPC"])
# In[ ]:
#FILTRAR DISTANCIA ENTRE CURVAS 
#df4[df4["dif_abs"]>=300]
# In[ ]:
#FLAG DE DATOS DISCORDANTES EN DISTANCIA
df4["flg_CompPC"]=0
df4.loc[df4["dif_abs"]>= 300, "flg_CompPC"] = 1
flag_CompPCshow= df4["flg_CompPC"] == 1
flag_CompPC=df4[flag_CompPCshow]
flag_CompPCtamaño=len(flag_CompPC.axes[0])
# In[ ]:
#FIGURA DE LOGPLOT DE LOS TRACKS
fig4, ax4 = plt.subplots(nrows=1, ncols=4, figsize=(10,10), sharey=True)
fig4.suptitle("PEAK COUNT cps", fontsize=20,va="top")
fig4.subplots_adjust(top=0.8,wspace=0.25)
 
#1st track: NEAR Y FAR PEAK COUNT
ax01=ax4[0].twiny()
ax01.invert_xaxis()
ax01.invert_yaxis()
ax01.set_xlim(0,200)
ax01.set_ylim([np.max(df4.index), np.min(df4.index)])
ax01.spines['top'].set_position(('outward',10))
ax01.set_xlabel("ALNPC")
ax01.plot(df4["ALNPC"], df4.index,"--", label='ALNPC', color='red')
ax01.set_xlabel('ALNPC',color='red')    
ax01.tick_params(axis='x', colors='red')

ax11=ax4[0].twiny()
ax11.invert_xaxis()
ax11.invert_yaxis()
ax11.set_xlim(0,200)
ax11.plot(df4["ALFPC"], df4.index, label='ALFPC', color='blue') 
ax11.spines['top'].set_position(('outward',40))
ax11.set_xlabel('ALFPC',color='blue')    
ax11.tick_params(axis='x', colors='blue')
ax11.grid(True)

   #2nd track: DIFERENCIA ABSOLUTA ENTRE CURVAS
ax02=ax4[1].twiny()
ax02.invert_xaxis()
ax02.invert_yaxis()
ax02.set_xlim(0,500)
ax01.set_ylim([np.max(df4.index), np.min(df4.index)])
ax02.spines['top'].set_position(('outward',40))
ax02.set_xlabel('Dif_Abs[%]')
ax02.plot(df4.dif_abs, df4.index,"--", label='Dif_Abs[%]', color='lime')
ax02.set_xlabel('Dif_Abs[%]', color='lime')
ax02.tick_params(axis='x', colors='lime')    
ax02.grid(True)

   #3nd track:FLAG DATOS DISCORDANTES EN DISTANCIA

ax04=ax4[2].twiny()
ax04.invert_xaxis()
ax04.invert_yaxis()
ax04.set_xlim(0,1)
ax04.spines['top'].set_position(('outward',5))
ax04.set_xlabel('Flag_Comportamiento PC')
ax04.fill_between(df4.flg_CompPC, df4.index, label="Flag Diferencia entre curvas", color='g') 
ax04.set_xlabel('Curvas Cerca [0] - Curvas Separadas [1]', color='g')
ax04.tick_params(axis='x', colors='g')
ax04.grid(True)

ax03=ax4[3].twiny()
ax03.invert_xaxis()
ax03.invert_yaxis()
ax03.set_xlim(0,1)
ax03.spines['top'].set_position(('outward',40))
ax03.set_xlabel('Flag Valores Nulos')
ax03.fill_between(df4.flag_2,0, label='Valores nulos', color='r')
ax03.set_xlabel('Hay valores [0] - No exsiten Valores [1]', color='r')
ax03.tick_params(axis='x', colors='red')



# In[ ]:
#HISTOGRAMA COUNT RATE DISTANCIA ENTRE NEAR Y FAR
hist4 = go.Figure(go.Histogram(x=df4["dif_abs"], xbins=dict(start=0,end=600,size=10),autobinx=False,marker_color='#CC0001'))
hist4.add_vline(x=300, line_dash = 'dash', line_color = 'firebrick',annotation_text="Max", 
              annotation_position="top right")
hist4.update_layout(
    title={
        'text': "Histograma Diferencia Absoluta entre curvas",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Diferencia Absoluta %",
    yaxis_title="Frecuencia De Dato",
    bargap = 0.1)

st.write("**Valores Nulos**")  
list_nanPC
st.write("Tiene",tamañoPC,"Datos Nulos")
st.write("**Valores fuera de rango**")    
st.write("Tienes",flag_CompPCtamaño,"Datos fuera de rango")
st.plotly_chart(hist4)   
c_1,c_2= st.columns(2,gap="medium")
c_1.pyplot(fig4)
c_2.write(flag_CompPC)   

# In[ ]:


#VOLTAJE NEAR Y FAR
st.subheader("TRACK3.1")
df4_1=df[["ALNHV","ALFHV"]]
# In[ ]:
#Sacar índices con nan
list_nanHV = df4_1.index[((df4_1['ALFHV'].isna())|(df4_1['ALNHV'].isna()))].tolist()
tamañoHV=len(list_nanHV)
#Macar nan con true y false
nan_ALNHV = df4_1['ALNHV'].isna()
nan_ALFHV = df4_1['ALFHV'].isna()
df4_1["nan_ALNHV"]=nan_ALNHV
df4_1["nan_ALFHV"]=nan_ALFHV
#Flag Nan´s
def flag_2(row):
    gap = True
    no_gap = False
    if (row.nan_ALFHV == gap) or (row.nan_ALNHV == gap) :
        return 1
    else:
        return 0
df4_1.loc[:, 'flag_2'] = df4_1.apply(flag_2, axis = 1)
# In[ ]:
#FLAG RANGO ACEPTABLE VOLTAJE
df4_1.loc[df4_1['ALNHV']<= 900,"mayor"] = 1
df4_1.loc[df4_1['ALFHV']<= 900,"mayor"] = 1
df4_1.loc[df4_1['ALNHV']>= 1300,"menor"] = 1
df4_1.loc[df4_1['ALFHV']>= 1300,"menor"] = 1
df4_1['mayor'] = df4_1['mayor'].fillna(0)
df4_1['menor'] = df4_1['menor'].fillna(0)
flg_rngHVS=df4_1["menor"]+df4_1["mayor"]
df4_1["flg_rngHVS"]=flg_rngHVS
#df4_1.reset_index(inplace=True)

# In[ ]:
#FILTRAR DATOS FLAGEADOS
flg_rngHVshow= df4_1["flg_rngHVS"] >= 1
flg_rngHV=df4_1[flg_rngHVshow]
flag_rngHVtamaño=len(flg_rngHV.axes[0])
# In[ ]:
#FIGURA DE LOGPLOT DE LOS TRACKS
fig5, ax5 = plt.subplots(nrows=1, ncols=3, figsize=(10,11.5), sharey=True)
fig5.suptitle("Voltage", fontsize=20,va="top")
fig5.subplots_adjust(top=0.8,wspace=0.25)
df4_1["flg_rngHVS"].replace(to_replace = 2, value =1, inplace=True)
#1st track: NEAR Y FAR VOLTAGE 
ax01=ax5[0].twiny()
ax01.invert_xaxis()
ax01.invert_yaxis()
ax01.set_xlim(500,1500)
ax01.set_ylim([np.max(df4_1.index), np.min(df4_1.index)])
ax01.spines['top'].set_position(('outward',10))
ax01.set_xlabel("ALNHV")
ax01.plot(df4_1["ALNHV"], df4_1.index,"--", label='ALNHV', color='red')
ax01.set_xlabel('ALNHV',color='red')    
ax01.tick_params(axis='x', colors='red')

ax11=ax5[0].twiny()
ax11.invert_xaxis()
ax11.invert_yaxis()
ax11.set_xlim(500,1500)
ax11.plot(df4_1["ALFHV"], df4_1.index,"--", label='ALFHV', color='blue') 
ax11.spines['top'].set_position(('outward',40))
ax11.set_xlabel('ALFHV',color='blue')    
ax11.tick_params(axis='x', colors='blue')
ax11.grid(True)


   #2rd track: FLAG DISTANCIA ACEPTABLE ENTRE CURVAS
ax02=ax5[1].twiny()
ax02.invert_xaxis()
ax02.invert_yaxis()
ax02.set_xlim(0,1)
ax02.spines['top'].set_position(('outward',0))
ax02.set_xlabel('Stuck Pipe')
ax02.fill_between(df4_1.flg_rngHVS, df4_1.index, label="Flag Rango Aceptable", color='blue') 
ax02.set_xlabel('En rango [0] - Fuera de rango [1]', color='blue')
ax02.tick_params(axis='x', colors='blue')
ax02.grid(True)

ax03=ax5[2].twiny()
ax03.invert_xaxis()
ax03.invert_yaxis()
ax03.set_xlim(0,1)
ax03.spines['top'].set_position(('outward',40))
ax03.set_xlabel('Flag Valores Nulos')
#ax03.plot(df4_1["flag_2"], df4_1.index,"--", label='ALFHV', color='blue')
ax03.fill_between(df4_1.flag_2,df4_1.index, label='Valores nulos', color='r')
ax03.set_xlabel('Hay valores [0] - No exsiten Valores [1]', color='r')
ax03.tick_params(axis='x', colors='red')



# In[ ]:

#HISTOGRAMA PEAK VOLTAGE
x0=df4_1["ALNHV"]
x1=df4_1["ALFHV"]
hist5 = go.Figure()
hist5.add_trace(go.Histogram(x=x0,xbins=dict(start=600,end=1500,size=10),autobinx=False,marker_color='#CC0001',name="ALNHV"))
hist5.add_trace(go.Histogram(x=x1,xbins=dict(start=600,end=1500,size=10),autobinx=False,marker_color='#000000',name="ALFHV"))
hist5.add_vline(x=900, line_dash = 'dash', line_color = 'firebrick',annotation_text="Min", 
              annotation_position="top right")
hist5.add_vline(x=1300, line_dash = 'dash', line_color = 'firebrick',annotation_text="Max", 
              annotation_position="top right")
hist5.update_layout(
    title={
        'text': "Histograma Peak Voltage",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    
    xaxis_title=" Peak Voltage",
    yaxis_title="Frecuencia De Dato",
    bargap = 0.05,
    barmode="stack")
  
st.write("**Valores Nulos**")  
list_nanHV
st.write("Tiene",tamañoHV,"Datos Nulos")
st.write("**Valores fuera de rango**")    
st.write("Tienes",flag_rngHVtamaño,"Datos fuera de rango")
st.plotly_chart(hist5)   
c_1,c_2= st.columns(2,gap="medium")
c_1.pyplot(fig5)
c_2.write(flg_rngHV)  

# In[ ]
#FACTOR FOTOELTRICO
df5=df[["ALPEA"]]
# In[ ]:
# In[ ]:
#DENSIDAD EN COUNT RATE
st.subheader("TRACK4")
df5_1=df[["ALNCA","ALFCA"]]
# In[ ]:
#Sacar índices con nan
list_nanAD = df5_1.index[((df5_1['ALFCA'].isna())|(df5_1['ALNCA'].isna()))].tolist()
tamañoAD= len(list_nanAD)
#Macar nan con true y false
nan_ALNCA = df5_1['ALNCA'].isna()
nan_ALFCA = df5_1['ALFCA'].isna()
df5_1["nan_ALNCA"]=nan_ALNCA
df5_1["nan_ALFCA"]=nan_ALFCA
#Flag Nan´s
def flag_2(row):
    gap = True
    no_gap = False
    if (row.nan_ALNCA == gap) and (row.nan_ALFCA == gap) :
        return 1
    else:
        return 0
df5_1.loc[:, 'flag_2'] = df5_1.apply(flag_2, axis = 1)
# In[ ]:
#CALCULAR Y FILTRAR DIF ABSOLUTA PARA VER DISTANCIA ENTRE CURVAS
df5_1["dif_abs"]=100*np.abs((df5_1["ALFCA"]-df5_1["ALNCA"])/df5_1["ALFCA"])
#df5_1[df5_1["dif_abs"]>=300]

# In[ ]:
#FLAG DATOS DISCORDANTES EN DISTANCIA
df5_1["flg_CompCA"]=0
df5_1.loc[df5_1["dif_abs"]>= 300, "flg_CompCA"] = 1
flag_CompCAshow= df5_1["flg_CompCA"] == 1
flag_CompCA=df5_1[flag_CompCAshow]
flag_CompCAtamaño=len(flag_CompCA.axes[0])
# In[ ]:
#FIGURA LOGPLOT DE LOS TRACKS
fig6, ax6 = plt.subplots(nrows=1, ncols=4, figsize=(10,10), sharey=True)
fig6.suptitle("CR Density", fontsize=20,va="top")
fig6.subplots_adjust(top=0.8,wspace=0.25)
 
#1st track: NEAR Y FAR CS DENSITY 
ax01=ax6[0].twiny()
ax01.invert_xaxis()
ax01.invert_yaxis()
ax01.set_xlim(0,3000)
ax01.set_ylim([np.min(df5_1.index), np.max(df5_1.index)])
ax01.spines['top'].set_position(('outward',10))
ax01.set_xlabel("ALNCA")
ax01.plot(df5_1["ALNCA"], df5_1.index,"--", label='ALNCA', color='red')
ax01.set_xlabel('ALNCA',color='red')    
ax01.tick_params(axis='x', colors='red')

ax11=ax6[0].twiny()
ax11.invert_xaxis()
ax11.invert_yaxis()
ax11.set_xlim(0,3000)
ax11.plot(df5_1["ALFCA"], df5_1.index, label='ALFCA', color='blue') 
ax11.spines['top'].set_position(('outward',40))
ax11.set_xlabel('ALFCA',color='blue')    
ax11.tick_params(axis='x', colors='blue')
ax11.grid(True)

#2nd track: DIFERENCIA ABSOLUTA ENTRE CURVAS
ax02=ax6[1].twiny()
ax02.invert_xaxis()
ax02.invert_yaxis()
ax02.set_xlim(0,500)
ax02.spines['top'].set_position(('outward',30))
ax02.set_xlabel('Dif_Abs[%]')
ax02.plot(df5_1.dif_abs, df5_1.index,"--", label='Dif_Abs[%]', color='lime')
ax02.set_xlabel('Dif_Abs[%]', color='lime')
ax02.tick_params(axis='x', colors='lime')    
ax02.grid(True)

 
#3nd track:FLAG DATOS DISCORDANTES EN DISTANCIA
ax04=ax6[2].twiny()
ax04.invert_xaxis()
ax04.invert_yaxis()
ax04.set_xlim(0,1)
ax04.spines['top'].set_position(('outward',10))
ax04.set_xlabel('flg_CompCA')
ax04.fill_between(df5_1.flg_CompCA, df5_1.index, label="Flag Diferencia entre curvas", color='g') 
ax04.set_xlabel('Curvas Cerca [0] - Curvas Separadas [1]', color='g')
ax04.tick_params(axis='x', colors='g')
ax04.grid(True)

ax03=ax6[3].twiny()
ax03.invert_xaxis()
ax03.invert_yaxis()
ax03.set_xlim(0,1)
ax03.spines['top'].set_position(('outward',40))
ax03.set_xlabel('Flag Valores Nulos')
ax03.fill_between(df5_1.flag_2,0, label='Valores nulos', color='r')
ax03.set_xlabel('Hay valores [0] - No exsiten Valores [1]', color='r')
ax03.tick_params(axis='x', colors='red')


#HISTOGRAMA DISTANCIA ENTRE CURVAS CS DENSITY
hist6 = go.Figure(go.Histogram(x=df5_1["dif_abs"], xbins=dict(start=0,end=600,size=10),autobinx=False,marker_color='#CC0001'))
hist6.add_vline(x=300, line_dash = 'dash', line_color = 'firebrick',annotation_text="Max", 
              annotation_position="top right")
hist6.update_layout(
    title={
        'text': "Histograma Diferencia Absoluta entre curvas",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Diferencia Absoluta %",
    yaxis_title="Frecuencia De Dato",
    bargap = 0.1)
st.write("**Valores Nulos**")  
list_nanAD
st.write("Tiene",tamañoAD,"Datos Nulos")
st.write("**Valores fuera de rango**")    
st.write("Tienes",flag_CompCAtamaño,"Datos fuera de rango")
st.plotly_chart(hist6)   
c_1,c_2= st.columns(2,gap="medium")
c_1.pyplot(fig6)
c_2.write(flag_CompCA)  
