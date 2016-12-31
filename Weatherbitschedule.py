import json
import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=10)
def timed_job():
    
  #! Grab snow forecast for CYYZ (Toronto Pearson Airport)
  r = requests.post('http://api.wunderground.com/api/0ce78aaeec5a1a53/forecast/q/CYYZ.json')

  resp = r.json()
  resp1=resp['forecast']['simpleforecast']['forecastday'][0]['snow_allday']['cm']

  print("Forecasted snowfall for all day:", resp1,"cm")

  #! Ajusta o servo do Cloudbits para a um maximo de 10 cm
  #! Escala minima = 0
  #! Escala maxima = 10

  escalaMinima = 0
  escalaMaxima = 10

  escalaPressao = int(80 * (resp1 - escalaMinima)/(escalaMaxima - escalaMinima))

  if escalaPressao <= 0:
      escalaPressao = 0

  if escalaPressao >= 80:
      escalaPressao = 80
    
  print('Valor da escala:',escalaPressao)

  headers = {'Authorization': 'Bearer ebd261f46574f3622a90d7474ff2c23c58f956209a6b59eb660b9c6233919c58','Content-type': 'application/json'}

  data = '{"percent":0, "duration_ms":0}'
  requests.post('https://api-http.littlebitscloud.cc/v2/devices/00e04c038e35/output', headers=headers, data=data)

  time.sleep(2)

  data = '{"percent":'+ str(escalaPressao) + ', "duration_ms":0}'
  requests.post('https://api-http.littlebitscloud.cc/v2/devices/00e04c038e35/output', headers=headers, data=data)

sched.start()
