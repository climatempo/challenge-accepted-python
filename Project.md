Passos de utilização do código desenvolvido para o Python Challenge do Climatempo

   O Objetivo era plotar uma série temporal do índice RMSE de uma determinada coordenada e plotar gráficos 2D com os valores dos índices RMSE em 4 períodos do dia (intervalos de 6 horas). Para isso, utilizamos algumas bibliotecas prontas do proprio Python com suporte de softwares secundários.
   
   Para rodar este script, primeiramente será necessário instalar alguns pacotes Python no seu environment. Neste caso foi utilizado o ambiente Ubuntu 20.04 do Windows 10 como base para desenvolvimento do código em um ambiente local, permitindo a instalação de softwares de maneira facilitada. 
   
   Os pacotes utilizados são:
   
   pandas: Um dos pacotes de gerenciamento de dataframes do Python. Muito utilizado para inteligência artificial e análise de dados
        
   xarray: Biblioteca para conversão de arquivos netCDF para diversos dataframes, no caso utilizado para a conversão para um dataframe do pandas
        
   netCDF4: Biblioteca para leitura dos arquivos *.nc fornecido pelos autores do desafio.
    
   math: Uma biblioteca matemática de Python, utilizada para calcular o menor inteiro de uma divisão
    
   numpy: Biblioteca de gerenciamento de vetores no Python. Utilizado para obter a raiz quadrada do mean_squared_error
   
   matplotlib: Biblioteca gráfica do Python, bastante utilizada em ciência e engenharia de dados.
   
   mpl_toolkits: Função basemap desta biblioteca, utilizado nos mapas 2D.
        
   Uma destas biblitotecas só funcionam com a instalação de softwares externas. Para a utilização do Basemap, foi instalado o PROJ4 e GEOS, seguindo o guia disponível em https://matplotlib.org/basemap/users/installing.html  
   
   Para utilizar o netCDF4 é necessário instalra alguns pacotes Python e softwares previamente, a saber: numpy, cython, hdf5 library, LibCurl, HDF4, biblioteca em C do netCDF-4 e cftime. Os requerimentos foram obtidos no site https://unidata.github.io/netcdf4-python/
   
   Neste desafio foi utilizado o Python 3.8 em sua última versão no repositório do Ubuntu 20.04. Como plataforma de programação foi instalado o Jupyter Notebook em um ambiente local criado na minha máquina pessoal. Todos as bibliotecas foram instaladas usando o comando pip presente no Python.
