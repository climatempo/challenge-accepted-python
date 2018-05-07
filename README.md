<p align="center">
  <a href="http://www.climatempo.com.br">
      <img src="http://i.imgur.com/Q9lCAMF.png" alt="Climatempo" width="300px"/>
  </a>
</p>

___


## Processo de recrutamento

Olá desenvolvedor Python, pronto para participar do nosso processo de recrutamento?

### Sobre a Vaga

- Empresa: Climatempo;
- Cargo: Desenvolvedor Python (CLT);
- VR e VT;
- Home Office após período de experiência;
- Flexibilidade no horário de trabalho para acompanhar eventos de tecnologia;
- Local: Parque Tecnológico - São José dos Campos (www.pqtec.org.br).


### Requisitos

Bons conhecimentos em:

- Python
- Programação Orientada a Objetos
- Design Patterns
- Testes automatizados
- Automação de tarefas
- Web scraping
- SQL
- NoSQL

IMPORTANTE:

- Residir no Vale do Paraíba ou nas proximidades.


### O Desafio

- Ler dois arquivos NetCDF com dados de temperatura, sendo um com *dados de previsão* e o outro com *dados observados*;
- Calcular o índice RMSE para cada intervalo de 6 horas na série temporal em todos os pontos da matriz;

<img src="https://i.imgur.com/MlK4w0X.png" alt="RMSE - Root Mean Square Error" />

- Plotar mapas de duas dimensões do índice de cada período e um gráfico da série temporal do mesmo índice para São Paulo (Latitude **-23.5489** e Longitude **-46.6388**, correspondente ao ponto Y: **8** e X: **26** na grade da matriz dos dados);
- Crie um arquivo PROJECT.md com descrições de todos os passos para instalação e utilização do seu software;
- Escrever o resultado do cálculo do índice em um arquivo NetCDF (**Opcional**).

**Descrição dos arquivos:**

Dados de Previsão

| Propriedade                        | Descrição   |
| :--------------------------------- |:------------|
| Arquivo                            | forecast.nc |
| Número de tempos                   | 72          |
| Data de referência                 | 2018/04/14  |
| Frequência do tempo                | Horária     |
| Nome da variável de temperatura    | t2m         |
| Unidade da variável de temperatura | Kelvin      |

Dados Observados

| Propriedade                        | Descrição      |
| :--------------------------------- |:---------------|
| Arquivo                            | observation.nc |
| Número de tempos                   | 72             |
| Data de referência                 | 2018/04/14     |
| Frequência do tempo                | Horária        |
| Nome da variável de temperatura    | temperatura    |
| Unidade da variável de temperatura | Grau Celsius   |


### Avaliação

O que vamos avaliar:

- Desempenho;
- Manutenabilidade;
- Organização;
- Boas práticas;


### Comece

O processo do desafio deve ser:

1. Faça o fork do desafio.

2. Crie um **PROJECT.md** com a explicação de como devemos executar o projeto e com o máximo de detalhes possível do que foi feito.

3. Após concluir faça um pull request.

5. Envie um e-mail para python@climatempo.com.br com seu **curriculo, pretensão salarial e o link do seu pull request**.


___


Qualquer dúvida entre em contato com nossa equipe.
