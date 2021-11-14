# Projeto para desenvolvedores Python-Processo Seletivo Climatempo 


## Descrição do projeto: 

Ler dados de temperatura prevista e observada a partir de arquivos netcdf, calcular o índice RMSE para 
intervalos de 6 horas para toda a série, e também plotar imagens 2D (distribuição espacial do RMSE) e um
gráfico com a evolução temporal do RMSE para a cidade de São Paulo. 

## Nome do arquivo .PY:

teste_climatempo.py

## Bibliotecas necessárias:

1. Numpy
2. Math
3. Cartopy
4. Matplotlib
5. netCDF4 
6. pandas

## Passo a Passo:

$ git clone https://github.com/douglima8/challenge-accepted-python.git

$ unzip challenge-accepted-python-master.zip

$ cd challenge-accepted-python-master

$ unzip shapefile.zip 

$ python teste_climatempo.py 

## Resultado:

- Criação de 12 figuras 2D para cada intervalo de 6 horas com os valores do índice de RMSE para o estado de São Paulo. 


  **Nome do arquivo: RMSE_T2m_(varição do intervalo dos dados).png**
  
  ![alt text](https://github.com/douglima8/challenge-accepted-python/blob/b7cc7955008823b93711ca73b4484bb29587c3a8/RMSE_T2m_0.png)

- Criação de uma figura x-y para a série temporal do índice RMSE para a cidade de São Paulo. 


   **Nome do arquivo: RMSE_serie.png**
   
   ![alt text](https://github.com/douglima8/challenge-accepted-python/blob/master/RMSE.png)

## Detalhes do processo:

Inicialmente se faz a leitura dos dados 

- forecast.nc
- observation.nc

[1] A partir da leitura, indica-se as variáveis de temperatura prevista (retirada do forecast) e temperatura observada (retirada do observation) as quais são 
registradas como t2m_F (prevista) e t2m_O (observada). Além disso, nós iremos setar os valores de longitude e latitude juntamente com o tempo, todos retirados
dos arquivos. Devido a falta de dois arquivos nos valores da temperatura observada, adicionou-se uma máscara para descarte destes valores para conseguirmos calcular
o RMSE.

[2] Com isso, foi aberto um looping para o cálculo do RMSE a partir do intervalo de 6 em 6 horas como foi pedido. 

[3] Com os valores de RMSE, indico o tamanho da plotagem e a projeção usada para a plotagem do mapa. Irei usar um shapefile (o qual está inserido na pasta do git) 
para as bouders do país e logo após seto  os limites prévios dos valores de RMSE e o intervalo para a escala de cores a qual será inserida após a plotagem. 
Como adicional, foi feita a inserção de um ponto indicando a localização da cidade de São Paulo a partir da lat/lon. Com isso, salvo os mapas 
com a indicação da variação do intervalo de tempo. 

[4] Foi feito um looping para o cálculo da série temporal do RMSE para a cidade de São Paulo durante todo o período. Criou-se um dataFrame e foi inserido os valores
encontrados no mesmo. 

[5] Como feito na plotagem dos mapas, foi aqui escolhida o tamanho da figura e algumas setagens de legenda, gradeamento do plot e estilo da linha.  


