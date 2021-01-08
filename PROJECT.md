
### Produto desenvolvido para calcular a Raiz quadrada do erro-médio (RMSE) entre dados de previsão e dados  observados

Caro usuário, para utilizar esse código é necessário a instalação do Python e algumas bibliotecas dessa linguagem em seu computador.

As bibliotecas utilizadas são:
- xarray
- pandas
- numpy
- matplotlib

OBSERVAÇÃO:

- Esse produto foi desenvolvido para calcular o RMSE entre dados de temperatura para um intervalo de 6 em 6 hrs


Abaixo é descrito a funcionalidade de cada célula desse código.


###                                                           Parte 1 do projeto - Cálculo do RMSE

#### Célula 1

Nessa primeira célula é realizado a importação das bibliotecas que serão utilizadas.

#### Célula 2

Neste projeto o RMSE é calculado considerando dados de temperatura.

-Linha 1 e 2:leitura dos dados
-Linha 3:aqui é realizado a alteração da unidade de temperatura do dado de previsão. Neste caso iremos trabalhar com a unidade de **graus celsius**

#### Célula 3

Aqui estou deixando os dois conjuntos de dados na mesma grade.

#### Célula 4

Linha 1: nessa linha do código é criado uma lista vazia para receber os dataArrays com o resultado do cáluclo do RMSE.

Linha 2: aqui é criada uma lista de datas para variar em um determinado passo de tempo (6horas)

Linhas 3: utilização de um loop para realizar o cáluclo do RMSE a cada passo de tempo.
No código há uma descrição mais detalhada do que é feito nessa etapa do código.



#Criando uma lista para receber os dataArrays com rmse 
**lista_rmse=[]** - criando uma lista para receber os dataArrays com rmse


**tempo=pd.date_range(prev.time[0].values, prev.time[-1].values, freq='6H')** - criando datas para variar de 6 em 6 hrs


**for t in tempo:** - fazendo um loop para percorrer a lista de datas
    
**t1=pd.Timestamp(str(t))** - #Data inicial (Data1)
 
**t2=pd.Timestamp(str(t))** -Data2=(Data2=Data1+6h)
    
**prev_6h=prev.sel(time=slice(t1,t2))** - fazendo a seleção dos intervalos de tempos para a prev
   
**obs_6h=obs.sel(time=slice(t1,t2))** - fazendo a seleção dos intervalos de tempos para a obs
    
**rmse_6h=(((prev_6h - obs_6h)**2).mean(dim='time')**0.5).assign_coords(time=t).expand_dims('time')** - criando um novo Datarray que vai ser o cálculo do RMSE. Aqui também é inserido a coordenada de tempo para fazer a concatenação entre o RMSE e os tempos correspondentes

**lista_rmse.append(rmse_6h)** -para cada etapa do loop é calculado o RMSE
    

#### Célula 5

**rmse_ds=xr.concat(lista_rmse, dim='time')** - fazendo a concatenação do tempo com o resultado do RMSE obtido

**rmse_ds.to_netcdf('result_rmse.nc')** -  criação de um dado netcdf com o resultado do cálculo do RMSE (result_rmse.nc)

    
#### Célula 6    
Como foi gerado um novo dado netcdf com os resultados calculados anteriormente. Nessa célula do código é feito a abertura desse novo dado.

**result = xr.open_dataset('result_rmse.nc')** - abrindo o novo netcdf com os resultados


  
  ###                                                        Parte 2 do projeto - Plot de mapas espaciais


Neste projeto os dados que foram utlizados (observation.nc e forecast.nc) possuíam uma resolução temporal horária de 1 hora (72 tempos)

Como o objetivo desse projeto é calcular o RMSE a cada 6 horas, o arquivo de saída gerado ('result_rmse.nc') possui apenas 12 tempos.


#RMSE do primeiro intervalo de Python
**clevs=np.arange(-8,8,0.5)** - definindo o *range* em que os valores de RMSE vão variar na figura juntamente com o intervalo

**rmse_ds.sel(time='2018-04-14T00:00:00.000000000').plot.contourf(levels=clevs,cmap='jet')** - nessa linha é realizado o plot espacial do RMSE calculado para o primeiro intervalo de tempo de interesse. Nessa linha é selecionado o tempo de interesse e realizado o plot considerando o range de **clves**. Aqui a tonalidade de cores utilizado é o **jet**. O *contourf* é utilizado para desenhar linhas de contornos preenchidos mais suavizadas.


**OBSERVAÇÃO:**
As próximas células dessa parte do código são utilizadas para realizar o plot dos demais intervalos de tempo de interesse.



###                                                             Plot de série temporal 

Linha 1: nessa linha é selcionado um ponto de grade de interesse para ser realizado o plot da série temporal do RMSE (12 tempos)

A utilização do **method='nearest'** é feita para informar ao código que caso não exista o ponto de grade que foi informado pelo o usuário, o código deve fazer uma extrapolção para o ponto mais próximo. 

**plot.line(color="red", marker="o",linewidth=2.5)** - aqui estamos informando ao código que o plot deve ser na forma de um gráfico de linhas, sendo que a cor dessa linha deve ser *vermelha*. Além disso também é informado que para cada ponto do gráfico, deve ser utilziado um marcador do tipo **o** e a espessura da linha de 2.5. 

**plt.xlabel('Time', fontsize=14, weight='bold')** - aqui é dado o nome para o eixo x, tamanho da fonte e forma da fonte (nesse caso negrito). 

**plt.xlabel('Time', fontsize=14, weight='bold')** - similar ao comando acima, só que para o eixo y
                                                                   
**plt.xticks(fontsize=12)** - informando o tamanho dos rótulos do eixo x 

**plt.yticks(np.arange(0,3,0.3),fontsize=12)** - informando o tamanho dos rótulos do eixo y e também definindo o range dos valores deste eixo


___


Projeto desenvolvido por Thales Teodoro