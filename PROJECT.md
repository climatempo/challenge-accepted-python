
# Challenge Python Climatempo 
Autora Brenda Almeida Santos

## Instalação
### Software Python:

Alguns sistemas operacionais já possuem como padrão a versão *2.x* da linguagem **Python**. No entanto, caso a linguagem não venha instalada por padrão é possível baixar os executáveis, e seguir com o processo de instalação padrão para cada sistema operacional.

Exemplo utilizando o o sistema Linux **Ubuntu 20.04.2 LTS**:
1. Verificar as versões do Python instaladas, digite no terminal:
	* `python -V`
	 

1. Caso a versão do Python de interesse não esteja disponível, a mesma pode ser instalada pelos gerenciadores de pacotes de distribuição. O gerenciador de pacotes utilizado será o `apt-get`. Antes, instale a versão mais recentes do gerenciador:
	* `sudo apt - get update`
Após o update, instale o **python** com o seguinte comando:
    * `sudo apt - get install python`
	
Assim, o Python já estará devidamente instalado. Uma forma alternativa de instalar o Python é através de distribuições para finalidades especificas. Uma distribuição muito popular é a **Anaconda** (não será abordado aqui).


### Pacotes/bibliotecas utilizadas:

### PIP
Primeiro, instale o `pip` que é um sistema de gerenciamento de pacotes usado para instalar e gerenciar pacotes de software escritos na linguagem de programação Python. Instalando via `apt-get`:
* `apt-get install python-pip`

### Cartopy
O CartoPy é um pacote criado pelo UK Met Office com o objetivo de permitir projeções cartográficas e plotagem de diversos tipos de dados geoespaciais em Python. Atualmente é o pacote dominante de projeções e mapas.
Primeiramente é necessário verificar se o Cartopy está instalado, isso pode ser feito usando os comandos abaixo:
* `conda list cartopy` ou
* `pip list cartopy`
	
Caso ele não esteja instalado, o mesmo pode ser adquirido com um dos seguintes comandos:
* `conda install -c conda-forge cartopy`
Outra forma é usando o comando do pip, mas para isso você precisa instalar primeiro as dependências necessárias, listadas abaixo: 
* `pip install cartopy`

Dependências necessárias: para instalar o Cartopy ou para acessar sua funcionalidade básica, será necessário primeiro instalar GEOS, Shapely e pyshp.

### Pandas
É uma biblioteca para manipulação e análise de dados. Em particular, oferece estruturas e operações para manipular tabelas numéricas e séries temporais. 
Primeiramente é necessário verificar se o Pandas está instalado, isso pode ser feito usando os comandos abaixo:
* `conda list pandas` ou
* `pip list pandas`
	
Caso ele não esteja instalado, o mesmo pode ser adquirido com um dos seguintes comandos:
* `python -m pip install pandas`
Outra forma é usando o comando do pip diretamente:
* `pip install pandas`

### Proplot

O pacote Proplot é um invólucro mais leve do matplotlib (pacote primordial de plotagem em Python) , uma ótima alternativa a esses pacotes mais convencionais. O Proplot foi criado recentemente por Luke Davis, doutorando do Departamento de Ciências Atmosféricas da Colorado University. Por conta disso, possui diversas funções e facilidades para quem trabalha não apenas com programação científica em geral, mas para meteorologistas e outros profissionais que estão ligados a área. O Proplot fornece uma série de funcionalidades e facilidades para plotagem de mapas baseadas em CartoPy.

Primeiramente é necessário verificar se o Proplot está instalado, isso pode ser feito usando os comandos abaixo:
* `conda list proplot` ou
* `pip list proplot`
	
Caso ele não esteja instalado, o mesmo pode ser adquirido usando pip ou conda:
* `pip install proplot` ou
* `conda install -c conda-forge proplot`

O Proplot possui algumas dependências como o matplotlib, cartopy, basemap, xarray e pandas. Verifique se possui essas bibliotecas. Veja a documentação para detalhes (https://proplot.readthedocs.io/en/latest/index.html).

### Xarray
É um pacote focado em manipulação de dados n-dimensionais em pontos de grade com formatos do tipo netcdf, grib e até mesmo geotiff. O Xarray incorpora muitas funcionalidades do NumPy e Pandas para dados descritos em pontos de grade.

Primeiramente é necessário verificar se o Xarray está instalado, isso pode ser feito usando os comandos abaixo:
* `conda list xarray` ou
* `pip list xarray`
	
Caso ele não esteja instalado, o mesmo pode ser adquirido com um dos seguintes comandos:
* `conda install -c conda-forge xarray dask netCDF4 bottleneck`

Caso você não use o conda, certifique-se de ter as dependências necessárias (numpy e pandas) instaladas primeiro. Em seguida, instale o xarray com pip:
*	`python -m pip install xarray`

# O Projeto

## Como executar o projeto:

Com o terminal aberto na pasta do arquivo `.py`, digite o executável  `python3`  e o nome do arquivo com extensão `.py`. Neste caso:
*	`python3 desafio.py`

Os dados de entrada (forecast.nc, observation.nc e o conjunto de arquivos relacionados ao shapefile) devem estar nessa mesma pasta.

### Sobre o projeto:

Primeiramente foi feita as importações das bibliotecas a serem utilizadas, respeitando a convenção da comunidade sobre as nomenclaturas:
```Python
import xarray as xr
import pandas as pd
import proplot as plot
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader
```

Depois foram feitas as declarações das principais constantes do código. Caso, posteriormente, formos usar o código com outras variações podemos trocar os valores somente aqui.

```Python
FREQUENCIA_TEMPO = '6H'
DIMENSAO = 'time'
CIDADE_REFERENCIA = 'São Paulo'
LATITUDE_REFERENCIA = -23.5489
LONGITUDE_REFERENCIA = -46.6388
RESOLUCAO_IMG = 300
```

A seguir foi efetuado a leitura dos arquivos **NetCDF** utilizando a biblioteca **Xarray**, extraindo a variável a ser utilizada e deixando as variáveis de temperatura com a mesma unidade **(°C)**:
```Python
	prev = xr.open_dataset('forecast.nc')['t2m']-273.15
	obser = xr.open_dataset('observation.nc')['temperatura']
```

Foi carregado também o arquivo shapefile com a divisão dos estados brasileiros:
```Python
arq_shp = 'UFEBRASIL'
```

Posteriormente, igualou-se as coordenadas de latitude e longitude dos arquivos de entrada, pois algumas tinham uma diferença na 3ª casa decimal em diante:
```Python
prev.coords['lat'] = obser.lat
prev.coords['lon'] = obser.lon
```

Criou-se uma lista vazia para colocar o resultado do **RMSE**:
```Python
lista_result = []
```

Criou-se uma frequência fixa de **6 horas**, utilizando o comando `data_range` da biblioteca **Pandas**, para cálculo do índice **RMSE**. Para isso, pegamos o primeiro e o último valor da dimensão **time** do arquivo **prev** e variamos numa frequência de 6 horas:
```Python
intervalo_tempo = pd.date_range(prev.time[0].values, prev.time[-1].values, freq= FREQUENCIA_TEMPO)
```

Com isso, foi criado um looping de 6 em 6 horas:

```Python
for tempo in intervalo_tempo:
	prev_6h = prev.sel(time = slice(pd.Timestamp(str(tempo)), pd.Timestamp(str(tempo)) + pd.Timedelta(FREQUENCIA_TEMPO)))
	obser_6h = obser.sel(time = slice(pd.Timestamp(str(tempo)), pd.Timestamp(str(tempo)) + pd.Timedelta(FREQUENCIA_TEMPO)))
	rmse_6h = ((((prev_6h - obser_6h) ** 2).mean(dim = DIMENSAO) ** 0.5).assign_coords(time = tempo).expand_dims(DIMENSAO))
	lista_result.append(rmse_6h)
```
Dentro do loop o comando `sel()` do **Xarray** seleciona essas 6 horas para todos os pontos de grade de cada arquivo (prev e obser) e retorna uma matriz. Em maiores detalhes, o comando `sel()`, do **Xarray**, utiliza a dimensão **time** da grade e realiza um recorte  do arquivo no intervalo especificado  pela `FREQUENCIA_TEMPO`.  Porém é necessário transformar o dado a ser recortado em um formato que o **Xarray** compreende, então é utilizado o `Timestamp` e o `Timedelta` está somando mais 6H ao tempo oferecido pelo looping.

Após o recorte, é realizado o cálculo do índice **RMSE**, onde o valor é armazenado na variável `rmse_6h`. Utilizamos a função `.mean()` para fazer a média na dimensão tempo, para cada ponto da grade. O `.assingn_coords` cria uma coordenada de tempo e o `expand_dims` define essa coordenada de tempo como uma dimensão do arquivo.
Depois, acrescentamos o resultado de cada iteração na lista vazia criada anteriormente, utilizando a função `.append` que adiciona o item ao final da lista.


Com o **RMSE** calculado, concatenamos o resultado do índice gerado pra cada tempo, criado anteriormente, armazenando na variável `rmse_ds` e então criamos um arquivo **netCDF** com os resultados:
```Python
rmse_ds = xr.concat(lista_result, dim = DIMENSAO)
rmse_ds.to_netcdf('RMSE_6H.nc')
```

Em seguida, foi realizado um looping para geração de cada mapa:
```Python
for tempo in intervalo_tempo:
	rmse_result = rmse_ds.sel(time = str(tempo))
	
	fig, axs = plot.subplots(axheight = 5, tight = True, proj = 'pcarree')
	axs.format(coast = True, borders = True, latlim = (min(rmse_ds.lat), max(rmse_ds.lat)), 
	lonlim = (min(rmse_ds.lon), max(rmse_ds.lon)), labels=True, title='Índice RMSE ' + str(tempo))
	mapa = axs.contourf(rmse_result, cmap = 'Blues', vmin = 0, vmax = 5)
	fig.colorbar(mapa,label = 'RMSE da temperatura')
	
	# Adicionando divisao estados
	shape_feature = ShapelyFeature(shpreader.Reader(arq_shp).geometries(),\
	ccrs.PlateCarree(), facecolor='none', edgecolor='k', linewidth=0.5)
	axs.add_feature(shape_feature)

	fig.save(str(tempo) + '_RMSE.png', dpi = RESOLUCAO_IMG)
```

No looping, o arquivo foi recortado para cada tempo, com o comando `.sel()`, e armazenado na variável `rmse_result`. Utilizando a biblioteca **Proplot**, armazenando no índice `axs`, plotou-se a projeção cartográfica, definindo uma altura para o gráfico com o comando `axheight` e adequando o gráfico ao tamanho da moldura da figura `Tight`.

Na formatação, foi adicionado as bordas e linhas de costas (o que será ainda mais útil caso ampliemos a área para outros dados). Neste  caso, a projeção foi selecionada para a área de interesse, utilizando-se o comando `.min()` e `.max()` para selecionar as latitudes e longitudes limites do arquivo.

Ainda na formatação da figura, `.format()`, foi  configurado as linhas de contorno do mapa e adicionado um título que varia conforme o **tempo** .

Em seguida, foi feito a plotagem dos dados `rmse_result` usando a função `.contourf()`, onde foi selecionado o mapa de cores (`cmap`) e os valores máximos(`vmax`) e mínimos(`vmin`) para a escala de cores. Depois, foi adicionado a barra de cores `.colorbar()` e a legenda. 

Acrescentou-se também um shapefile com a difisão dos estados do Brasil, utilizando a biblioteca cartopy. A leitura do arquivo foi feita através da função `shpreader.Reader` e foi feita algumas formatações como a cor `edgecolor` e a espessura `linewidth` do vetor. Por fim,  é salvo a figura com o nome que varia no tempo mais a string `_RMSE.png` com resolução de 300 dpi.

Para a série temporal do índice **RMSE** calculado para São Paulo, foi selecionado (novamente com o comando `.sel()`) os dados dos pontos de referência e armazenados na variável `rmse_sp`, utilizando o método `nearest`, que seleciona o ponto de grade mais próximo aos parâmetros passados.
```Python
rmse_sp = rmse_ds.sel(lon = LONGITUDE_REFERENCIA, lat = LATITUDE_REFERENCIA, method='nearest')
```

Para plotar a série foi utilizado o comando `.subplot()` da biblioteca **Proplot**. A seguir, foi plotado no eixo x a dimensão `time` dos dados `rmse_sp`, no eixo y os dados de RMSE, `rmse_sp`, com marcadores de círculos. Por fim, foi utilizado o `.format()` para adicionar título aos eixos e a figura e, por fim, a figura é salva com o nome da cidade referência mais a string 'RMSE_' no formato png.

```Python
graf, ax = plot.subplots(figsize = (7, 3), tight = True)
ax.plot(rmse_sp['time'], rmse_sp, marker = 'o')
ax.format(xlabel = 'Tempo', ylabel = 'Índice RMSE',
title = 'Índice RMSE da temperatura para ' + CIDADE_REFERENCIA)
graf.save('RMSE_' + CIDADE_REFERENCIA + '.png')
```

# Observações

Afim de evitar uma extensa documentação, não foram explicados todos os parâmetros das funções utilizados.
Para mais informações das bibliotecas e parâmetros, abaixo segue o link oficial das documentações:

Cartopy: https://scitools.org.uk/cartopy/docs/latest/

Pandas: https://pandas.pydata.org/pandas-docs/stable/index.html

Proplot: https://proplot.readthedocs.io/en/latest/index.html

Xarray: http://xarray.pydata.org/en/stable/index.html


