#Desafio_climatempo

Neste projeto criamos um programa para gerar a partir de arquivos NetCDF contornos de duas dimensões e series temporais da Raiz do erro quadrático médio (RMSE).
Além, dos gráficos, o programa também permite que um novo arquivo NetCDF seja criado e salvo pelo usuário.

A RMSE é obtida a partir de duas variáveis, uma observada (o) e outra modelada ou prevista (f) utilizando a equação:

<img src="https://i.imgur.com/MlK4w0X.png" alt="RMSE - Root Mean Square Error" />

Esse índice é relevante para quantificar a acurácia de um modelo em prever uma dada variável.
E sua vantagem reside no fato de ter a mesma dimensão da variável estudada.

Para ilustrar o funcionamento do programa, utilizamos dois arquivos com dados previstos e observados para temperatura do ar em 2 metros.
Esses arquivos estão no repositório e possuem o nome forecast.nc e observation.nc respectivamente.

Nas Tabelas abaixo temos os detalhes de cada arquivo.

| Propriedade                        | Descrição   |
| :--------------------------------- |:------------|
| Arquivo                            | forecast.nc |
| Número de tempos                   | 72          |
| Data de referência                 | 2018/04/14  |
| Frequência do tempo                | Horária     |
| Nome da variável de temperatura    | t2m         |
| Unidade da variável de temperatura | Kelvin      |

Dados Observados

| Propriedade                        | Descrição      |
| :--------------------------------- |:---------------|
| Arquivo                            | observation.nc |
| Número de tempos                   | 72             |
| Data de referência                 | 2018/04/14     |
| Frequência do tempo                | Horária        |
| Nome da variável de temperatura    | temperatura    |
| Unidade da variável de temperatura | Grau Celsius   |

Para utilização do programa é possível baixar manualmente o arquivo de nome RMSE_CALC.py 
Clonar o repositório e instalar via pip:

```
git clone https://github.com/RubensFPereira/Desafio_climatempo.git
pip install .
```
Ou instalar diretamente desse repositório: 

```
pip install+https://github.com/RubensFPereira/Desafio_climatempo.git
```

Foram utilizados os seguintes pacotes na aplicação:

```
- Cartopy
- Numpy
- Pandas
- NetCDF4 
- Glob
- Matplotlib
- Seaborn 
```
A obtenção de cada pacote segue os seguintes métodos:
* `conda install -nome do pacote`
ou
* `pip install -nome do pacote`

Nossa aplicação tem ao todo 4 principais funções:


Função que calculo o RMSE entre as Variáveis
```
calc_rmse(intervalo,observado,previsto,escala)
intervalo: Qual intervalo de tempo desejado (no caso utilizamos 6)
observado: Dados observados
previsto: Dados de modelagem
escala: A mesma escala de tempo do intervalo mas no formato 'intervaloH' (nesse exemplo '6H')
```


Função que Gera e salva os contornos bidimensionais da RMSE
```
plot_contour(lon_obs, lat_obs, rmse_cal,time_range,lv_min,lv_max)
lon_obs: Longitudes do arquivo dos dados observados/modelados
lat_obs: Latitudes do arquivo dos dados observados/modelados
time_range: Array com TimeStamps que corresponde a data de cada contorno
lv_min: Valor minimo encontrado entre os dados para definir o limite inferior da escala de cor
lv_max=Valor maximo encontrado entre os dados para definir o limite superior da escala de cor
```

Função que Gera e salva o arquivo NetCDF com os valores de RMSE para grade
```
netcdf_creator(data,lats,lons,path_save)
lons: Longitudes do arquivo dos dados observados/modelados
lats: Latitudes do arquivo dos dados observados/modelados
data: Dados de RMSE
path_save: Caminho do diretório onde será salvo o arquivo NetCDF (caso não seja especificado, o arquivo será salvo na mesma pasta do arquivo .py)
```

Função que plota e salva a serie temporal da RMSE para um dado ponto de grade.
```
plot_timeserie (data,indice_x,indice_y,time_range,lat_ref,lon_ref)
data: Dados de RMSE
indice_x: ponto de grade indice x
indice_y: ponto de grade indice y
time_range: Array com TimeStamps que corresponde a data de cada ponto
lat_ref: informação da latitude do ponto de grade (variável meramente gráfica para criação do título do plot)
Lat_ref: informação da longitude do ponto de grade (variável meramente gráfica para criação do título do plot)
```

Para execução do programa, poucas modificações são necessárias.


Basicamente precisamos/podemos determinar os caminhos dos arquivos .nc de entrada...
```Python
path_entrada = r'' # caminho da pasta onde os arquivos estão salvos
try:
    all_files = glob.glob(path_entrada  + "/*.nc") 
except:
    all_files = glob.glob(os.getcwd() + "/*.nc")
 ```  
...do caminho de saída do arquivo .nc criado e dos gráficos 2D e temporal:

```Python
path_save = 'C:/temp/test.nc'  
if os.path.exists(path_save):
  os.remove(path_save)
 ``` 
 E das coordenadas para as quais queremos calcular a serie temporal:
 
```Python
coord_x=26
coord_y=8
lat_ref=-23.5489
lon_ref=-46.6388
``` 
Obs. Pode ser interessante determinar caminhos diferentes para os diretórios de saída e entrada dos arquivos .nc,
Assim evitamos que em caso de rodar múltiplas vezes o programa, ele não colete um arquivo de saída como entrada.

Caso tudo corra bem, você deve obter contornos de RMSE em função das latitudes e longitudes como o ilustrado abaixo.

<img src="https://github.com/RubensFPereira/Desafio_climatempo/blob/b2f3e24fcbe26b99ee7c3c993acdbbbe7d39d172/Contorno%20do%20RMSE%20da%20temperatura%20para%20o%20dia%2016%2004%202018%2018.jpeg" width="350" height="300">


E um gráfico da série temporal variação do RMSE:

 <img src=https://github.com/RubensFPereira/Desafio_climatempo/blob/b2f3e24fcbe26b99ee7c3c993acdbbbe7d39d172/Varia%C3%A7%C3%A3o%20Da%20RMSE%20Temperatura%20a%20cada%206H%20.png  width="350" height="300">
 
 
