## Desafio resolvido:
# Cicero Santos

### Prepara ambiente
* Primeira coisa é baixar o projeto, para ter acesso ao código e ao arquivo de dependências
* Download gerenciador de dependências [miniconda](https://docs.conda.io/en/latest/miniconda.html)
  * Com ele posso instalar dependências do OS e da linguagem!
* Apos instalar o conda, criar um ambiente novo
  * Criando um ambiente, terei o python na versão selecionada e também o GDAL(dependências OS e python wrapper lib)
```
conda create --name env3 python=3.7.6 gdal
pip install -r requirements.txt
```
### Execução local
Para executar precisa ativar o ambiente criado acima

```
conda activate env3
python climatempo_teste.py
```

### Execução online
* Criei um notebook que pode ser acessado para leitura e execução
  * [Link Google Colab](https://colab.research.google.com/drive/1J4Mh1birxGqTSrGE6d1rH7L0_J3EHbrl?usp=sharing)
  * Para executar necessário fazer login com uma conta Google

