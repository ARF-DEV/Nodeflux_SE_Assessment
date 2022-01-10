# Nodeflux_SE_Assessment

this is a HTTP API server that could retrieve [GET] information about current status of covid cases and vaccination rates in Indonesia.

## Getting started
to get started clone this repository to your local machine using this command on your console
```
git clone https://github.com/ARF-DEV/Nodeflux_SE_Assessment.git
```

## How to Build
make sure that you had installed python 3.8 or higher (i use python 3.8.10)
if you haven't install it yet download the installer [here](https://www.python.org/downloads/)

copy this command to your console to install all the dependencies
```
pip install -r requirement.txt
```

to run the app make sure you're in the project folder
```
cd Nodeflux_SE_Assessment
```
and then run the command below
(windows)
```
python src/app.py
```
(linux)
```
python3 src/app.py
```
or if you want to built it using docker you can built the image using this command
```
docker built -t <docker-username>/<image-name>:<tag> .
```

and to run the image first you have to know the image ID you want to run using this command
```
docker images
```

once you know the command you can run this command to run the image
```
docker run -p 8080:8080 <image-id>
```
## Some screenshot of the API in action (Using Postman)

Index
![image](https://user-images.githubusercontent.com/33253103/148724048-e9329cf9-9ecc-4649-b0f1-f484faf94dcd.png)

Yearly
![image](https://user-images.githubusercontent.com/33253103/148724162-bfc193e9-0953-4e65-b623-c3a7bf887f48.png)

Monthly
![image](https://user-images.githubusercontent.com/33253103/148724181-3b883a0d-6953-449c-80c0-ff7ad2929ca0.png)

Daily
![image](https://user-images.githubusercontent.com/33253103/148724210-535d198d-6269-40ba-a532-5378c4438c57.png)
