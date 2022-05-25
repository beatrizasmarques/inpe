#!/usr/bin/env python
# coding: utf-8

# ### TAREFA 1: DADOS DE TSM DE ALTA RESOLUÇÃO (750 m) - VIIRS (NOAA-20)

# #### Processando o Dado
# 
# Requisitos
# 
# 1. A região de plot deverá ser:
# 
# Longitude mínima: -55.0
# 
# Latitude mínima: -35.0
# 
# Longitude máxima: -49.5
# 
# Latitude máxima: -29.5
# 
# 2. Características das linhas de latitude e longitude:
# 
# Espaçamento: a cada 0.5°, tanto em latitude como longitude
# 
# Cor: a sua escolha
# 
# 3. Paleta de Cores:
# 
# Deverá ser utilizada a paleta de cores do Worldview, vista no pré-curso
# 
# Valor mínimo da paleta: deverá ser o valor mínimo do próprio dado (data.min())
# 
# Valor máximo da paleta: deverá ser o valor máximo do próprio dado (data.max())
# 
# 4. Máscaras de Oceano e Continente:
# 
# A máscara de oceano deverá ser na cor preta ('#000000' ou 'black')
# 
# A máscara de continente deverá ser na cor cinza ('#a9a9a9' ou 'gray')
# 
# 5. Shapefiles:
# 
# O shapefile de municípios ('BR_Municipios_2019.shp') deverá ter espessura 0.3 (cor a sua escolha)
# 
# O shapefile de estados ('BR_UF_2019.shp') deverá ter espessura 2.0 (cor a sua escolha)
# 
# 6. Anotações:
# 
# Deverão ser adicionadas ao plot 4 anotações:
# 
# Anotação 1: Texto: "Porto Alegre" Posição: lat: -30.0277° / lon = -51.2287°
# 
# Anotação 2: Texto: "Lagoa dos Patos" Posição: lat: -30.5° / lon = -50.8°
# 
# Anotação 3: Texto: "Lagoa Mirim" Posição: lat: -32.5° / lon = -52.8°
# 
# Para os três textos acima, offset sugerido entre círculo e texto: 0.1°
# 
# Anotação 4: Texto: "Tarefa 1: Curso de Produtos de Oceanografia por Satélite" Posição: Texto ancorado do lado inferior direito
# 
# 7. Título:
# 
# Lado esquerdo: Texto: "NOAA-20 - Temperatura da Superfície do Mar - 750 m"
# 
# Lado direito: Texto: Data formatada ('YYYY-MM-DD')
# 
# ______________________________________________________________
# 
# 
# Dado TSM de Alta Resolução (750 m)
# 
# Considerações Importantes:
# 
# 1. Quais os NOMES DOS DATASETS de TSM, Coordenadas e Data?
# 
# 2. Qual a DIMENSÃO do Dado?
# 
# 3. Qual a ORIGEM do Dado?
# 
# 4. Qual a UNIDADE do Pixel?
# 
# 5. Qual a DATA de Referêcia?

# ### Tarefa 1

# In[9]:


# Importando as Bibliotecas

import os
from os import walk
import requests
import numpy as np
import wget
import zipfile
from zipfile import ZipFile
from tqdm import tqdm #progress bar
import matplotlib.pyplot as plt


# In[2]:


# Definindo uma função para fazer o download de URLs em uma pasta determinada

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

# How to call the function:
# download("http://website.com/Motivation-Letter.docx", dest_folder="mydir")


# In[3]:


# Baixando os shapefiles dentro da pasta shapefiles usando a função <download>

url = ['https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2019/Brasil/BR/br_unidades_da_federacao.zip',
       'https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2019/Brasil/BR/br_municipios_20200807.zip'
       ]

dest_folder = 'C:\\Users\\beatr\\Documents\\Cursos\\INPE\\oceanografiaporsatelite\\shapefiles\\'

for i in np.arange(0, len(url)):
    download(url[i], dest_folder)
    print(url[i] + ' - download complete\n')


# In[4]:


# Descomprimindo os shapefiles dentro da pasta shapefiles

origin_folder = 'C:\\Users\\beatr\\Documents\\Cursos\\INPE\\oceanografiaporsatelite\\shapefiles\\'
dest_folder = 'C:\\Users\\beatr\\Documents\\Cursos\\INPE\\oceanografiaporsatelite\\shapefiles\\'

for i in os.listdir(origin_folder): 
    if i.endswith('.zip'):
        file_path = origin_folder + i
        with ZipFile(file_path) as zip_file:
            for file in tqdm(iterable=zip_file.namelist(), total=len(zip_file.namelist())):
                # Extract each file to another directory. If you want to extract to current working directory, don't specify path
                zip_file.extract(member = file, path = dest_folder)

print('unzip complete')


# In[5]:


# Baixando um Dado de Amostra (TSM de 07/05/2022)

# Download do arquivo NetCDF de amostra:
# O arquivo a seguir foi retirado do seguinte catálogo:
# https://coastwatch.noaa.gov/thredds/catalog/sst_acspo/nightVIIRSn20SectorDailyWX00/catalog.html

# Cria o diretório de amostras, caso não exista
dir = "Samples"; os.makedirs(dir, exist_ok=True)

# Change working directory
dir_name = 'C:\\Users\\beatr\\Documents\\Cursos\\INPE\\oceanografiaporsatelite\\Samples\\'
os.chdir(dir_name) 

# Se o arquivo já existe, deleta (necessário para evitar possíveis erros de leitura)
files = ['VSSTNCW_C2022127_C14_003000-005000_021001_022001_023000_035000_040000_041001_054000_055000_144000_162001_180000_WX00_mixed_seasurfacetemperature.nc',
         'amostra_tsm.nc']

for i in files:
    try:
        os.remove(i)
    except OSError:
        pass

# Download do arquivo usando a função <download>
url = 'https://coastwatch.noaa.gov/thredds/fileServer/sst_acspo/nightVIIRSn20SectorDailyWX00/VSSTNCW_C2022127_C14_003000-005000_021001_022001_023000_035000_040000_041001_054000_055000_144000_162001_180000_WX00_mixed_seasurfacetemperature.nc'
download(url, dest_folder='C:\\Users\\beatr\\Documents\\Cursos\\INPE\\oceanografiaporsatelite\\Samples\\')
print('download complete!\n')

# Renomeia o arquivo para um nome mais fácil de usar
os.rename('VSSTNCW_C2022127_C14_003000-005000_021001_022001_023000_035000_040000_041001_054000_055000_144000_162001_180000_WX00_mixed_seasurfacetemperature.nc',
          'amostra_tsm.nc')
print ('file renamed to: amostra_tsm.nc')

# Change back the working directory
dir_name = 'C:\\Users\\beatr\\Documents\\Cursos\\INPE\\oceanografiaporsatelite\\'
os.chdir(dir_name)

# Check working directory
print('\nCurrent working directory: ' + os. getcwd())


# In[12]:


# Biblioteccas
from netCDF4 import Dataset               # Read / Write NetCDF4 files
import matplotlib.pyplot as plt           # Plotting library
from datetime import datetime, timedelta  # Basic date and time types
import cartopy, cartopy.crs as ccrs       # Plot maps
import cartopy.feature as cfeature        # Common drawing and filtering operations
import numpy as np                        # Import the Numpy package
import matplotlib.colors                  # Matplotlib colors  
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset('Samples\\amostra_tsm.nc')

Show all columns names to first check how is the file

s = pd.Series(df.index)
print (s)



#---------------------------------------------------------------------------------------------------------------------------
# # Select the extent [min. lon, min. lat, max. lon, max. lat]
# extent = [-55.0, -35.00, -49.50, -29.50] 

# # Reading lats and lons 
# lats = file.variables['lat'][:]
# lons = file.variables['lon'][:]

# # Latitude lower and upper index
# latli = np.argmin( np.abs( lats - extent[1] ) ) # latitude lower index (latitude mínima)
# latui = np.argmin( np.abs( lats - extent[3] ) ) # latitude upper index (latitude máxima)
 
# # Longitude lower and upper index
# lonli = np.argmin( np.abs( lons - extent[0] ) )
# lonui = np.argmin( np.abs( lons - extent[2] ) )
 
# # Extract the Sea Surface Temperature
# data = file.variables['analysed_sst'][ 0 , latli:latui , lonli:lonui ]
# #---------------------------------------------------------------------------------------------------------------------------
# # Choose the plot size (width x height, in inches)
# plt.figure(figsize=(15,15))

# # Use the Cilindrical Equidistant projection in cartopy
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# # Define the image extent
# img_extent = [extent[0], extent[2], extent[1], extent[3]]

# # Add coastlines, borders and gridlines
# ax.coastlines(resolution='50m', color='black', linewidth=0.8)
# ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
# gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-90, 90, 10), draw_labels=True)
# gl.top_labels = False
# gl.right_labels = False

# # Create a custom color scale:
# colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", 
#           "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", 
#           "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", 
#           "#ab1900", "#6b0200", '#3c0000']
# cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
# cmap.set_over('#3c0000')
# cmap.set_under('#28000a')
# vmin = -2.0
# vmax = 35.0

# # Add a land mask
# ax.add_feature(cfeature.LAND)

# # Plot the image
# img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', extent=img_extent, cmap=cmap)

# # Add a colorbar
# plt.colorbar(img, label='Sea Surface Temperature (°C)', extend='both', orientation='vertical', pad=0.02, fraction=0.05)

# # Getting the file time and date
# add_seconds = int(file.variables['time'][0])
# date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
# date_formatted = date.strftime('%Y-%m-%d')
	
# # Add a title
# plt.title(f'NOAA Coral Reef Watch Daily 5 km SST - {date_formatted}', fontweight='bold', fontsize=13, loc='left')
# plt.title('Region: ' + str(extent), fontsize=13, loc='right')
# #--------------------------------------------------------------------------------------------------------------------------- 
# # Save the image
# plt.savefig('Output/image_06.png')

# # Show the image
# plt.show()


# In[ ]:




