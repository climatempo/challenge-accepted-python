# Instalação
Para poder executar o projeto é necessário já possuir a distribuição Anaconda instalada.
 Para instalar em uma distribuição Linux, as instruções se encontram aqui: https://docs.anaconda.com/anaconda/install/linux/
 
##
Com essa etapa já concluída, escolha um local para os arquivos e realize este comando:
`conda create -n <nome-do-ambiente> --file req.txt`

Com o ambiente do Anaconda já criado e com os arquivos do projeto já inseridos nele, ative-o com:
`conda activate <nome-do-ambiente>`

E verifique se a instalação foi bem sucedida com:
`conda env list`

# Execução

Com o ambiente já aberto no terminal, execute esse comando para iniciar o projeto:
`python main.py`

# Detalhes do projeto
O projeto tem como função ler dois arquivos NetCDF, 
 - `observation.nc` - Arquivo com dados de temperatura observados
 - `forecast.nc` - Arquivo com dados de temperatura previstos

Com esses arquivos lidos, a ideia é usar seus dados para calcular uma série de índices **RMSE** (Raiz quadrada do erro-médio).

Isso pode ser dividido em três tarefas:
 - Calcular o índice RMSE para cada intervalo de 6 horas em todos os pontos da matriz e, posteriormente, plotar mapas de duas dimensões do índice em cada período;
 - Calcular o índice RMSE para cada intervalo de 6 horas no ponto de Latitude **-23.5489** e Longitude **-46.6388** e, posteriormente, plotar um gráfico da série temporal do mesmo;
 - Escrever o resultado do cálculo do índice em um arquivo NetCDF.
 
Para isso foi usado, principalmente, a biblioteca **XArray** para leitura e manipulação dos dados dos arquivos NetCDF; a biblioteca **Numpy** para a realização dos cálculos do índice RMSE; e a biblioteca **Matplotlib** para plotar os dados em gráficos.

## Principais variáveis
- `obs` - Váriavel que armazena o DataSet do arquivo de observação
- `fc` -  Váriavel que armazena o DataSet do arquivo de previsão
- `generalRMSE`- DataArray com o índice RMSE de cada coordenada para cada intervalo
- `localRMSE` - DataArray com o índice RMSE da coordenada de SP para cada intervalo
- `dsRMSE` - Variável que armazena a conversão do DataArray com os Índices RMSE gerais para um DataSet, com a intenção de salvar os dados em um arquivo NetCDF

## Descrição do cálculo
O cálculo do Índice RMSE é feito com a seguinte lógica:  
 - É feito a conversão de Kelvin para °C no DataArray do arquivo de previsão.
 - O resultado é subtraído pelo DataArray do arquivo de observação.
 - A diferença é elevada ao quadrado.
 - É feito a média aritmética dos intervalos e depois é resolvido o índices que ficaram NaN.   
 - Por último é feito a raiz quadrada de cada índice.

