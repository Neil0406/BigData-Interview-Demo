## Big Data Interview Demo
## 使用方式 :

#### 1. 下載專案
```
git clone https://github.com/Neil0406/BigData-Interview-Demo.git
```
#### 2. 移動至專案資料夾內
```
cd BigData-Interview-Demo
```
#### 3. 執行docker-compose （請確保本機端80 port未被使用）
```
docker-compose up -d
```

#### 4. 開啟瀏覽器
```
http://127.0.0.1/swagger/
```
#### 5. 登入，輸入測試帳號 + 密碼
```
email : demo@gmail.com
passwoed : 123456
```
## 透過Swagger操作API:
```
1. 透過Swagger可直接對API進行操作，並且測試。
2. Swagger內使用帳號登入權限，無需另外取得Token。
```

## 透過程式操作API:
### 1. 取得 Access Token

```
[Request]

Method : Post

Url : http://127.0.0.1/get_token/token/

body : {"email": "demo@gmail.com","password": "123456"}
```

```
[Response]

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0Mzk3OTg4MywiaWF0IjoxNjQzODkzNDgzLCJqdGkiOiIzODkwNzQyODA4Njc0MDdiOTgxNzRlMTdhODNiNjZjYyIsInVzZXJfaWQiOjF9.c8sfoB5tkJ8-EGEYptLEkQz-lMzAx84dUqJVK46fQQ8",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQzODkzNzgzLCJpYXQiOjE2NDM4OTM0ODMsImp0aSI6IjBhYTllNTdiZjE0OTQ0YmU5MzcyYzNjNjA5OTMyNGZhIiwidXNlcl9pZCI6MX0.19FTzpAjellqyqdbk69HMFphkpJeYYinzm5Htd3rXds"
}
```
### 2. 操作API

```
將以上所取得之access放入headers即可

headers :{"Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}
```
