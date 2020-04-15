# Instruções para execução do *notebook*

Toda implementação do desafio se encontra em arquivo do Jupyter Notebook na pasta raiz do projeto, chamado Calculo_RMSE.ipynb. Não é necessário executá-lo para ver os resultados, basta abrí-lo no próprio Github e será possível ver os mapas e gráficos de maneira estática. Porém, caso seja necessário executar o *script*, basta instalar as bibliotecas listadas na seção 1. Carregamento das bibliotecas, presente dentro do *notebook* ou nesse documento.

## 1. Carregamento das bibliotecas

As seguintes bibliotecas foram utilizadas para o desenvolvimento desse *script*:

* [XArray](https://pypi.org/project/xarray/)
* [Pandas](https://pypi.org/project/pandas/)
* [GeoPandas](https://pypi.org/project/geopandas/)
* [PyGeoHash](https://pypi.org/project/pygeohash/)
* [GeoPlot](https://pypi.org/project/geoplot/)
* [MapClassify](https://pypi.org/project/mapclassify/)
* [Shapely](https://pypi.org/project/Shapely/)
* [Scikit-learn](https://pypi.org/project/scikit-learn/)
* [Seaborn](https://pypi.org/project/seaborn/)
* [Matplotlib](https://pypi.org/project/matplotlib/)

Todas estão disponíveis para instalação via PIP, conforme é possível notar nos *links*.

## 2. Execução

É recomendada a execução utilizando o Jupyter Notebook. A distribuição [Anaconda](https://www.anaconda.com/distribution/) conta com o Jupyter Notebook, bem como algumas bibliotecas pré-instaladas, como o Pandas.

O *script* leva aproximadamente dois minutos para executar, esse tempo pode ser diferente dependendo do poder de processamento da máquina utilizada. Esse tempo de execução decorre especialmente do processamento feito para separar os dados nos períodos de seis horas para cada ponto.

No *notebook* há explicações linha a linha do que está sendo executado.