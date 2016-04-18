import json
import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    
  #! Le as condicoes do tempo em SBSP do Weather Underground usando meu token
  #r = requests.post('http://api.wunderground.com/api/0ce78aaeec5a1a53/conditions/q/SBMT.json')

  r = requests.post('http://api.wunderground.com/api/0ce78aaeec5a1a53/conditions/q/SBSP.json')

  resp = r.json()
  resp1 = resp['current_observation']
  resp2 = eval(resp1['pressure_mb'])

  print("Pressao atmosferica em Congonhas:", resp2,"hPa")

  #! Ajusta o servo do Cloudbits para a pressao atual, com as seguintes premissas
  #! Escala minima = 1000
  #! Escala maxima = 1030

  escalaMinima = 1000
  escalaMaxima = 1030
  desvio = 3 #! Devido ao servo nao ter ajuste fino na rosca


  escalaPressao = int(100 * (resp2 -desvio - 1000)/(escalaMaxima - escalaMinima))

  if escalaPressao <= 0:
      escalaPressao = 0

  if escalaPressao >= 100:
      escalaPressao = 100
    
  print('Valor da escala:',escalaPressao)

  duracao = 0

  r = requests.post('https://api-http.littlebitscloud.cc/v2/devices/00e04c038e35/output',\
  headers = {'Authorization':'Bearer ebd261f46574f3622a90d7474ff2c23c58f956209a6b59eb660b9c6233919c58'},\
  data = {'percent': 0, 'duration_ms': duracao})

  time.sleep(1)

  r = requests.post('https://api-http.littlebitscloud.cc/v2/devices/00e04c038e35/output',\
  headers = {'Authorization':'Bearer ebd261f46574f3622a90d7474ff2c23c58f956209a6b59eb660b9c6233919c58'},\
  data = {'percent': escalaPressao, 'duration_ms': duracao})

sched.start()
