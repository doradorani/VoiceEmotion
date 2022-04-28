import urllib3
import json
import base64
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = "ea967964-351d-4fa5-9d49-f1ebbc649f34"
audioFilePath = "backend\tmp"
languageCode = "korea"
 
file = open(audioFilePath, "rb")
audioContents = base64.b64encode(file.read()).decode("utf8")
file.close()
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "language_code": languageCode,
        "audio": audioContents
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))