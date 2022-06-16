#token_required jwt token uyumunu sağlayrak işlemleri yapılmasına yardımcı 

#Postman Key-Value --> Authorization : Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJuYW1lIjoiYWxtaXIiLCJpZCI6IjViMmE5Mzg0LWMzNDYtNDJjMy1hMmZlLWJjOWQzZGYyM2UwOSJ9LCJleHAiOjE2NTUxODA5MjJ9.U5sQeEG-Y3LxCUJHG771aTGSi91pEQZp3XSZs6zP2GE

#Örnek URL->http://localhost:5000/user/5b2a9384-c346-42c3-a2fe-bc9d3df23e09 bu url ile kayıtların eşlenen idsini listeler. id UUID formatına göre oluşturulmuştur.

#TimeSeries dataseti de github a ekleyeceğim, farklı şehirlere göre bulamadım fakat bir çok condtionı bulunmakta.

#http://localhost:5000/weather?PrecipType=rain --> veri seti içinde Precip Type kolunun altında rain olan bütün kayıtları listelemekte.

#veri setini mail ile iletiyorum.


#docker-compose up -d komutu ile çalıştırıyorum, mongodb ye garip bir şekilde bağlanmıyor port bilgisi doğru olmasına rağmen 
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS         PORTS                      NAMES
36e59eed01f6   oauth_restapi_app   "python -u app.py"       10 seconds ago   Up 5 seconds   0.0.0.0:5000->5000/tcp     oauth_restapi-app-1
c4abc8ef0538   mongo               "docker-entrypoint.s…"   13 seconds ago   Up 6 seconds   0.0.0.0:27017->27017/tcp   mongodb

db bağlantısından dolayı aldığım hata : localhost:27017: [Errno 111] Connection refused, Timeout: 30s, Topology Description: <TopologyDescription id: 62aab885e1b2e1e28e5cc53b, topology_type: Unknown, servers: [<ServerDescription ('localhost', 27017) server_type: Unknown, rtt: None, error=AutoReconnect('localhost:27017: [Errno 111] Connection refused')