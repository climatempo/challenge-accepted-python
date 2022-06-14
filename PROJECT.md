# challenge-accepted-python

**Instalação**

Para executar este software é necessário instalar o `TKinter` e o `Virtualenv`. O `TKinter` é utilizado para plotar os gráficos da biblioteca `matplotlib`, e o `Virtualenv` é utilizado para baixar as bibliotecas do software. Este software utiliza as bibliotecas `netCDF4`, `matplotlib` e `geopandas`.

Para instalar o TKinter e o Virtualenv digite os seguintes comandos no terminal:

  ```
  $ sudo apt install python3-tk
  $ sudo apt install python3-venv
  ```

Após concluir estas instalações, clone este repositório e acesse o seu diretório no terminal. No diretório deste software, digite os seguintes comandos:

  ```
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ python3 -m pip install -r requirements.txt
  ```

Os comandos acima irão criar um ambiente virtual, ativar este ambiente e então instalar as bibliotecas. Após a instalação das bibliotecas, será possível executar este software da seguinte forma:

  ```
  $ python app.py
  ```

O software irá ler os arquivos NetCDF, calcular os índices RMSE, plotar o gráfico e mapas, e salvar os índices RMSE no arquivo `rmse.nc`.

**Funcionamento do Software**

O código fonte deste software está contido no arquivo `app.py`. Este por sua vez contém a classe `Challenge`, que é composta pelos métodos `__init__`, `calculate_rmse`, `plot` e `save_rmse_data`.

O método `__init__` é o construtor da classe `Challenge`. Ele recebe como parâmetro os conjuntos de dados previstos e observados, e a partir daí inicializa os atributos da classe. O método `calculate_rmse` calcula o índice RMSE para períodos de 6 horas. O método `plot` plota o gráfico da série temporal e os mapas através das bibliotecas `matplotlib` e `geopandas`. O método `save_rmse_data`, através da biblioteca `netCDF4`, salva os índices RMSE no arquivo `rmse.nc`.

Dentro do escopo da estrutura condicional `if __name__ == '__main__':` é feito a leitura dos conjuntos de dados, e então instancia-se o objeto `ch` da classe `Challenge` e executa-se os seus métodos.

**Observação**

Estas instruções foram feitas considerando a utilização de distribuições `Linux` derivadas do `Ubuntu`. Caso o leitor esteja utilizando outra distribuição, adapte a instalação do `TKinter` e do `Virtualenv` de acordo com a distribuição utilizada.

Caso o leitor não consiga executar este software, a pasta `img` contém as imagens do gráfico e dos mapas resultantes da execução deste software.

