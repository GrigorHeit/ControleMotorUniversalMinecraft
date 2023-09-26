from mcrcon import MCRcon as r
import serial
import msvcrt

ser = serial.Serial("COM7", baudrate=115200, timeout=1)
data = ''
valmotor = ''
valcorrente = ''
valmotorant = ''
valcorrenteant = ''
valsobrecorrente = ''
valsobrecorrenteant = '0'
enviaant = ''
ativaDescida = ''


#CONECTANDO NO SERVIDOR DO MINECRAFT COM A CONEXÃO RCON#
with r('localhost', '4002') as mcr:
    while True:
        if ser.in_waiting > 0:
            recebe = ser.readline()
            data = str(recebe, 'utf-8')
            
        for i in range(len(data)):
            if data[i] == '\\n' or data[i] == '\\r' or data[i] == ' ':
                data[i] = ''
        valmotorant = valmotor
        valcorrenteant = valcorrente
        valsobrecorrenteant = valsobrecorrente
        valcorrente = data[3:7]
        valmotor = data[0:3]
        valsobrecorrente = data[7:8]
        
        if ativaDescida == '1' and valmotor == '180':
            mcr.command('/execute as @a run function comandos:setemergencia')

        if valcorrente != valcorrenteant:
            mcr.command(f'/scoreboard players set Corrente(mA) MOTOR {valcorrente.strip()}')
        if valmotor != valmotorant:
            mcr.command(f'/scoreboard players set Graus MOTOR {valmotor.strip()}')
        
        if valsobrecorrente == '1' and valsobrecorrenteant == '0':
            mcr.command('/execute as @a run function comandos:setdescida')
            mcr.command('/execute as @a run function comandos:sobrecorrente')
        if valsobrecorrente == '2' and valsobrecorrenteant == '1':
            mcr.command('/execute as @a run function comandos:setemergencia')
            mcr.command('/execute as @a run function comandos:sobrecorrented')
            
        respSubida = mcr.command('/scoreboard players get Subida MOTOR')
        ativaSubida = respSubida[len(respSubida)-9]
        respDescida = mcr.command('/scoreboard players get Descida MOTOR')
        ativaDescida = respDescida[len(respDescida)-9]
        respEmergencia = mcr.command('/scoreboard players get Emergencia MOTOR')
        ativaEmergencia = respEmergencia[len(respEmergencia)-9]
        
        #ENVIANDO UM COMANDO PARA O SERVIDOR PARA OBTER A RESPOSTA COM O VALOR DO TEMPO DE SUBIDA#
        resptemposubida = mcr.command('/scoreboard players get Tempo_de_Subida MOTOR')
        TSub = ''
        #FILTRANDO O VALOR DO TEMPO DE SUBIDA EM RELAÇÃO À RESPOSTA DO SERVIDOR(PEGANDO O QUE ME INTERESSA BASICAMENTE, QUE É O VALOR DO TEMPO)#
        for i in range(5):
            subida = resptemposubida[len(resptemposubida)-9-i]
            if subida == ' ':
                break
            else:
                TSub = subida + TSub
            continue
        #ENVIANDO UM COMANDO PARA O SERVIDOR PARA OBTER A RESPOSTA COM O VALOR DO TEMPO DE DESCIDA#
        resptempodescida = mcr.command('/scoreboard players get Tempo_de_Descida MOTOR')
        TDes = ''
        #FILTRANDO O VALOR DO TEMPO DE DESCIDA EM RELAÇÃO À RESPOSTA DO SERVIDOR(PEGANDO O QUE ME INTERESSA BASICAMENTE, QUE É O VALOR DO TEMPO)#
        for i in range(5):
            descida = resptempodescida[len(resptempodescida)-9-i]
            if descida == ' ':
                break
            else:
                TDes = descida + TDes  
            continue
        #CASO O VALOR DOS TEMPOS SEJA MENOR QUE 9(OCUPE SÓ UMA CASA DECIMAL) EU ADICIONO O VALOR 0 ANTES DELE PARA PADRONIZAR O ENVIO DE DADOS PELA SERIAL#           
        if len(TSub) < 2:
            TSub = '0' + TSub
        if len(TDes) < 2:
            TDes = '0' + TDes
        envia = TSub+TDes+ativaSubida+ativaDescida+ativaEmergencia
        if envia != enviaant:
            #MANDANDO INFORMAÇÃO PARA O ARM PELA SERIAL# 
            ser.write((envia).encode('utf-8'))
        enviaant = envia
        #print(('Recebendo do Minecraft: '+TSub+TDes+ativaSubida+ativaDescida+ativaEmergencia))
        #print(('Recebendo do ARM: '+valmotor+' '+valcorrente+' '+valsobrecorrente))
        #PEGANDO TECLA PARA FECHAR O PROGRAMA#
        if msvcrt.kbhit(): 
            key = msvcrt.getch().decode("utf-8")
            if key == "p":
                break
#FINALIZAÇÃO DO PROGRAMA#
ser.close()
print("Programa encerrado.")