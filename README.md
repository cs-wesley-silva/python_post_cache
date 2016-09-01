HTTP POST Cache
===============

Esta POC valida a possibilidade de executar um servidor de proxy reverso
no NGINX para cachear requests POST.

Para fazer o cache do request, o NGINX cria um hash do body e da URI.

Fiz uma API de teste que recebe um POST e aguarda 5 segundos antes
de dar a resposta.

Execução
--------

Clone o repositório e entre na pasta.

Para iniciar a API, execute:

```{shell}
virtualenv -p python2.7 env
source env/bin/activate
pip install flask
python app.py
```

Para iniciar o NGINX, execute:

```{shell}
docker run --rm -ti \
  --name proxy-nginx \
  -v $(pwd)/default.conf:/etc/nginx/conf.d/default.conf:ro \
  -p 8080:8080 \
  nginx
```

Pronto! O ambiente está no ar. Para executar os testes, você precisa saber
o seu IP local e o IP do container do proxy.
Após descobrí-los, execute o request contra a API. Você verá que todas as
chamadas demoram 5 segundos:

```{shell}
$ time curl -X POST --header "Content-Type:application/json" --data '{"msg":"hello, moto!"}' http://10.200.63.171:5000/
POST is working
{u'msg': u'hello, moto!'}

real    0m5.012s
user    0m0.004s
sys     0m0.000s
$ time curl -X POST --header "Content-Type:application/json" --data '{"msg":"hello, moto!"}' http://10.200.63.171:5000/
POST is working
{u'msg': u'hello, moto!'}

real    0m5.012s
user    0m0.000s
sys     0m0.004s
```

Em seguida, execute o request contra o proxy. Apenas o 1o request demora
5 segundos, o segundo é respondido imediatamente:

```{shell}
$ time curl -X POST --header "Content-Type:application/json" --data '{"msg":"hello, motoooo!"}' http://10.200.63.171:8080/
POST is working
{u'msg': u'hello, motoooo!'}

real    0m5.012s
user    0m0.004s
sys     0m0.000s
$ time curl -X POST --header "Content-Type:application/json" --data '{"msg":"hello, motoooo!"}' http://10.200.63.171:8080/
POST is working
{u'msg': u'hello, motoooo!'}

real    0m0.006s
user    0m0.004s
sys     0m0.000s
```

Ajustes devem ser feitos no `default.conf`.
