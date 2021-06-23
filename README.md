Os passos usados para resolução dos exercícios
1 Questao: Ler dois arquivos NetCDF com dados de temperatura, sendo um com dados de previsão e o outro com dados observados
Para leitura dos arquivos em NetCDF dos dados observados e previsto, primeiro abriu-se o jupyter notebook, e em seguida foi importada a biblioteca Xarray. Atraves da Biblioteca Xarray foram visualizados os dados contidos em cada arquivo NetCDF. Cada arquivo tem as seguintes variaveis tempo, latitude, longitude e a temperatura. Variavel tempo é correspondente ao dia 14,15 e 16 de abril de 2018 com uma varição temporal de 1 hora.As dimensoes de tempo (72), latitude (25) e longitude (37). Essas dimensoes sao iguais em dois arquivos NetCDF. 

2 Questao: Calcular o índice RMSE para cada intervalo de 6 horas na série temporal em todos os pontos da matriz
para responder esta questao, primeiro foi criada uma matriz contendo 12 intervalos de tempo com valores iguais a zero. Esses 12 intervalos foram definidos considerando que um dia tem 4 periodos com intervalos de tempo de 6 horas(0-5,6-11,12-17,18-23). Para tres dias totalizaram-se 12 periodos.Para cada ponto da matriz (latitude e longitude) foi calculado o valor do indice RMSE, usando a equacao de RMSE. Alem disso, também foi feita a conversao da temperatura prevista de Kelvin para graus Celsius. Esses calculos foram feitos importando as bibliotecas numpy e sklearn.metrics Assim sendo, foi rodado o script calculando e salvando os valores do indice RMSE para cada ponto da matriz. Depois disso foram salvos as matrizes do indice RMSE em formato de NetCDF. Só para salientar que o arquivo rms salvo em NetCDF, os valores do erro quadratico médio estao salvos como temperatura e também dizer que tirando o nan que antecede o mean o script roda normalmente.


3 Questao: Plotar mapas de duas dimensões do índice de cada período
Para responder esta questao, os mapas foram plotados chamando rms calculado na questao 2. O plote foi feito em todos intervalos. Esse plote foi feito por intermedio da biblioteca matplotlib.pyplot. 


4 Questao: Plotar um gráfico da série temporal do índice RMSE para São Paulo (Latitude -23.5489 e Longitude -46.6388, correspondente ao ponto Y: 8 e X: 26 na grade da matriz dos dados)
Para responder essa questao, o plote foi feito atraves da biblioteca importada (matplotlib), onde foi chamada matriz rms no ponto Y: 8 e X: 26. Portanto, os resultados mostram o grafico do ponto mais proximo das latitudes e longitudes apresentadas na questao (Latitude -23.5489 e Longitude -46.6388. So para enfatizar que no eixo x sao apresentados os 12 intervalos.

Observacao: No arquivo rms salvo, nao foram definidos os intervalos, razao pela qual no mapa e no grafico plotado foram inseridas as designacoes referentes a cada periodo.



