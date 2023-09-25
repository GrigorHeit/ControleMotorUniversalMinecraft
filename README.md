# ControleMotorUniversalMinecraft
Controle de um motor universal de dentro do Minecraft

O arquivo server.properties seriam as configurações do servidor que eu criei. Para a comunicação RCON eu utilizei a porta padrão 25575.

O mundo criado e utilizado no projeto é esse arquivo \world e no mapa podem ser encontrados command blocks responsáveis pela criação de cada placa, independente da função, e também para a criação do scoreboard.

As funções de controle dentro do minecraft podem ser encontradas em: \world\datapacks\functions\data\comandos\functions
Lá estão as funções para fazer a a adição de mais tempo de subida ou descida por exemplo e também outras funções que setam o estado de emergência, subida ou descida.

E o pack.mcmeta é encontrado em: \world\datapacks\functions
Ele é basicamente usado para setar o bambiente das funções .mcfunction.

O programinha criado em python ConSerialMC.py utiliza duas bibliotecas que podem ser baixadas após instalar o compilador da linguagem com os seguintes comandos no prompt de comando:
pip install mcrcon
pip install pyserial

A biblioteca mcrcon é basicamente utilizada para se comunicar com o console do servidor. Com essa comunicação, eu mando um comando para o console e ele retorna alguma coisa, como por exemplo o valor de algo, e então eu filtro o valor que eu quero e transformo em um valor inteiro para que seja interpretado e enviado, utilizando a biblioteca pyserial para enviar uma série de caracteres para o ARM.
