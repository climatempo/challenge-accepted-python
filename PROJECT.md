# Resolução do desáfio CLIMATEMPO

Este documento descreve a solução proposta para o desáfio realizado como parte do processo seletivo da empresa CLIMATEMPO.

## Geral

A resolução foi implementada usando a linguagem de programação Python e o paradigma Programação Orientada a Objeto.

Esta proposta possui um ambiente virtual com as dependências necessárias para sua execução. **IMPORTANTE:** Os mapas gerados são exportados em .html, mas existe a opção para exportar o mapa também em .png. Neste caso, é necessário o driver *geckodriver*. Para instalar este driver no Ubuntu use: **sudo apt install firefox-geckodriver**.

Outra característica da solução proposta é a possibilidade de excluir possíveis valores *outliers* de RMSE para a geração dos mapas. Essa opção foi implementada porque os valores *outliers* podem atrapalhar a visualização das informações apresentadas nos mapas por serem valores muito altos e o comportamento padrão é de valores baixos.

Os dados contidos nos arquivos *forecast.nc* e *observation.nc* são exportados um banco de dados relacional (implementado com SQLite) organizados como *Time*, *Latitude*, *Longitude* e *Temperatura* para cada temperatura observada e prevista (em tabelas separadas). Durante o processo de ETL, as temperaturas são padronizadas na unidade *Celsius* e os valores faltantes "None" são convertidos para *0*.

Os valores de RMSE também são armazenados em uma tapela específica. Por outro lado, os mapas (.html e .png) e o gráfico da série temporal do RMSE de Sâo Paulo são salvos no diretório *MapasPeriodos*.



### Detalhes da implementação


**Nome da classe:** ClimaTempo

**Parâmetros de inicialização:**  

- *pathDB:* caminho e nome para criar a base de dados. 

- *precisionCoord:* A precisão (quantidade de casas decimais) para armazenar e consultar as coordenadas na base de dados.
                                  
- *ff:* Caminho e nome do arquivo com as coordenadas e temperaturas previstas.

- *fo:* Caminho e nome do arquivo com as coordenadas e temperaturas observadas.

**Principais Métodos para uso:**  

- *ETL:* **Não recebe** argumentos. Este método realiza a extração dos dados dos arquivos NetCDF, padronizados e inseridos no banco de dados.

- *RMSEregistros:* **Requer** como argumento o tamanho da janela temporal das temperaturas que serão consideradas para o calcular o RMSE em cada par de coordenadas.

- *MapsPeriodos:* **Permite** receber argumentos lógicos (*True* e *False*) para indicar de os mapas também serão exportados para .png e se os valores *outliers* deverão ser mantidos nos mapas. Ambos são *False* por padrão.

- *GrafSaoPaulo:* **Não recebe** argumentos. Este método gera um gráfico temporal de linha e pontos sobre a variação do RMSE para São Paulo.

- *ConsultaRMSE:* **Não recebe** argumentos. Exibe os dados armazenados na tabela RMSE (Janela de tempo, Lat, Lon, RMSE).


### Para executar o código

**Comandos:**

$ cd challenge-accepted-python

$ source env/bin/activate

$ python3 main.py

$ deactivate


**Observação**

O arquivo **main.py** é um script com a instânciação de um objeto da classe ClimaTempo e as devidas invocações dos métodos para execução completa da solução proposta.

É possível excluir as linhas *242 até 252* e importar o código para um novo projeto e utilizar este código.


### Tabelas no SQLite


**Tabelas de coordenas:**

CoordObservation  |id | lat | lon |


CoordObservation  |id | lat | lon |


**Tabelas de dados:**

dataObservation  | id | time | lat | lon | temperatura |
                    
dataForecast  | id | time | lat | lon | temperatura |


**Tabela de RMSE:**

RMSE   |id | janelaTempo | lat | lon | rmse |
                    
