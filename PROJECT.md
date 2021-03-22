## Resolução do Desafio Clima Tempo

As funções criadas para a resolução deste problema estão no arquivo `source.py` com a devida documentação. Escolhi desenvolver desta maneira pois facilita a manutenção, expansão e generalização das funções do software, de maneira que seja possível criar os arquivos pedido para diferentes conjuntos de dados além dos determinados.

Script `resolução.py`
---

Neste arquivo está a execução do que foi pedido. O arquivo deve ser executado pelo prompt de comando da seguinte maneira:

```
python resolução.py 
```

Resultados
---

Para gerar os resultados unifiquei os dados dos arquivos .nc em um dicionário. Fiz isso pois foi a primeira vez trabalhando com este tipo de arquivo, assim, me sinto mais confortável sobre os resultados. A seguir, estão os códigos do arquivo `resolução.py`:

```python
forecast = nc.Dataset('forecast.nc')
observation = nc.Dataset('observation.nc')
source.teste(forecast, observation)

infos = source.nc_to_dict(forecast, observation)

source.plot_time_series(dados=infos, lat=8, lon=26, r=6)
```

Análise dos Resultados e do Processo
---

Infelizmente, não consegui instalar a biblioteca Basemap a tempo da entrega do exercício no meu computador. Mas a idéia principal permanece. Poucas linhas gerando grandes resultados.

De todo o modo, foi uma excelente oportunidade de aprender sobre um novo tipo de problema.