from flask import Flask, request, jsonify, send_file
import requests
import xml.etree.ElementTree as ET
import os

app = Flask(**name**)

API_KEY = os.getenv("API_KEY")

def parse_time(txt):
if txt and "분" in txt:
return int(txt.split("분")[0])
return None

def get_arrival(ars_id, route_id):
url = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid"
params = {"ServiceKey": API_KEY, "arsId": ars_id}

```
res = requests.get(url, params=params)
root = ET.fromstring(res.content)

for item in root.iter("itemList"):
    if item.findtext("busRouteId") == route_id:
        return parse_time(item.findtext("arrmsg1")), parse_time(item.findtext("arrmsg2"))

return None, None
```

def get_route_id(bus_no):
url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
res = requests.get(url, params={"ServiceKey": API_KEY, "strSrch": bus_no})
root = ET.fromstring(res.content)

```
for item in root.iter("itemList"):
    if item.findtext("busRouteNm") == bus_no:
        return item.findtext("busRouteId")
return None
```

def get_stations(route_id):
url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute"
res = requests.get(url, params={"ServiceKey": API_KEY, "busRouteId": route_id})
root = ET.fromstring(res.content)

```
return [{"arsId": i.findtext("arsId")} for i in root.iter("itemList")]
```

@app.route("/predict")
def predict():
bus = request.args.get("bus")
ars = request.args.get("ars")

```
route = get_route_id(bus)
stations = get_stations(route)

idx = next(i for i,v in enumerate(stations) if v["arsId"] == ars)
next_ars = stations[idx+1]["arsId"]

A1,A2 = get_arrival(ars, route)
B1,B2 = get_arrival(next_ars, route)

gap = B2 - B1

return jsonify({
    "1번": A1,
    "2번": A2,
    "3번": A2 + gap,
    "4번": A2 + gap*2
})
```

@app.route("/")
def home():
return send_file("index.html")

if **name** == "**main**":
app.run(host="0.0.0.0", port=10000)
