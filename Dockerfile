# Aqui será criado um container novo usando uma sintaxe específica do Docker
# Criar um container p/ rodar uma API a partir do container mais simples (o do Python 3)

# Configurando qual o container base (o mais simples)
FROM python:3.8
#especificando q daqui p/ frente tudo estará guardado dentro da app
WORKDIR /app
# apontar que todos os arquivos serao copiados
# Copy tem dois parametros (origem e destino) O primeiro posto diz q eh tudo. O segundo ponto diz q será salvo no arquivo principal.
COPY . .
# Running three commands apt get (managing linus programs) - Preparing the container so that the db can work
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y


# Installing the libraries
RUN pip install -r requirements.txt
# avisar o container o comando de entrada
ENTRYPOINT ["python"]
CMD ["server.py"]



