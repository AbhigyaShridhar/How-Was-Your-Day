import requests
import time

auth_key = 'edcb2cf6f9aa4785bc314aa1db075716'



headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}

def read_file(filename):
   with open(filename, 'rb') as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data

def assembly_ai(file_address):
    upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(file_address))
    audio_url = upload_response.json()['upload_url']


    transcript_request = {'audio_url': audio_url}
    endpoint = "https://api.assemblyai.com/v2/transcript"
    transcript_response = requests.post(endpoint, json=transcript_request, headers=headers)
    _id = transcript_response.json()['id']



    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
      "audio_url": audio_url,
      "iab_categories": True

    }

    headers = {
        "authorization": auth_key,
        "content-type": "application/json"
    }

    response = requests.post(endpoint, json=json, headers=headers)

    var=response.json()



    endpoint = "https://api.assemblyai.com/v2/transcript/"+var['id']

    headers = {
        "authorization": auth_key,
    }
    time.sleep(20)
    response = requests.get(endpoint, headers=headers)

    dictionary=response.json()
    obj=dictionary['iab_categories_result']
    obj1=obj['summary']
    fin_max= max(obj1, key=obj1.get)
    return fin_max
