# desafio-py
Descrição do projeto: Ler dados de temperatura prevista e observada a partir de arquivos netcdf, calcular o índice RMSE para intervalos de 6 
horas para toda a série, e posteriormente plotar imagens 2D (distribuição espacial do RMSE) e um gráfico com a evolução temporal do RMSE para a cidade de São Paulo. 

Dependências
------------
Bibliotecas necessárias:
- Numpy
- Glob
- Matplotlib
- netCDF4
- Cartopy
- Xarray

## Passo a passo
```bash
$ git clone https://github.com/WilliamCoelho/challenge-accepted-python.git

$ cd challenge-accepted-python/desafio-py

$ python main.py
```
## Resultado
Serão gerados:
- 12 figuras 2D, para cada intervalo de 6 horas, como a figura abaixo.

<img src="https://user-images.githubusercontent.com/28113714/122626069-b79e6580-d07e-11eb-8241-f5a23acd94aa.png" width="350" height="300">

- 1 gráfico de linha com a evolução temporal do índice RMSE para um ponto específico sobre São Paulo, como a figura abaixo.

<img src="https://user-images.githubusercontent.com/28113714/122626104-eddbe500-d07e-11eb-92a2-96005fe2d3f7.png" width="350" height="250">

- 1 arquivo netcdf com os valores do índice RMSE para todos os pontos de grade.
## Detalhes do processo
### Descrição das funções contidas no script aux.py
Esse script contém todas as funções necessárias para gerar os resultados solicidados no desafio.
#### aux.rmse()
Essa função calcula o índice RMSE com os dados observados e previstos de temperatura, lidos a partir dos arquivos observation.nc e forecast.nc. Os arquivos são calculados para intervalos de 6 em 6 horas, para todo o périodo de disponibilidade dos dados.
#### aux.save_netcdf()
Essa função cria um arquivo netcdf salvando os valores do índice RMSE para cada ponto de grade, de forma idêntica aos dados de temperatura originais.
#### aux.plot_2d()
Essa função gera uma imagem 2D com a distribuição do índice RMSE calculada para cada intervalo de 6 horas.
#### aux.plot_xy()
Essa função gera uma figura xy com a variação temporal do índice RMSE.
