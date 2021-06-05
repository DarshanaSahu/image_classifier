# Image Classification Server

## Pre-requisites
Install docker from https://www.docker.com/products/docker-desktop

## Steps to Run docker container

Build the image: *docker build -f "Dockerfile" -t classifier:1.0 "."* \
Run the image: *docker run -p 5000:5000 --name classifier-container classifier:1.0* \

## Steps to make API request:
*curl http://0.0.0.0:5000/upload?image={filename}* \
If filename is "panda.jpg", then it is pulled from local image folder \
If filename is a url, then image is pulled from the url

Sample Request 1: \
*curl http://0.0.0.0:5000/upload?image=panda.jpg* \
<br>
Sample Response 1 :
```json
{
    "0.8278709650039673":"GIANT PANDA",
    "0.14099308848381042":"INDRI",
    "0.021509533748030663":"LESSER PANDA",
    "0.0018896708497777581":"AMERICAN BLACK BEAR",
    "0.0013063416117802262":"GIBBON"
}
```
Sample Request 2: \
*curl http://0.0.0.0:5000/upload?image=http://r.ddmcdn.com/s_f/o_1/APL/uploads/2018/06/jabufromsandi.jpg* \
<br>
Sample Response 2 :
```json
{
    {
        "0.8441684246063232":"AFRICAN ELEPHANT",
        "0.14807699620723724":"TUSKER",
        "0.007744418922811747":"INDIAN ELEPHANT",
        "4.442084900802001e-06":"TRICERATOPS",
        "1.9905830868083285e-06":"RAM"
    }
}
```
Here, key(on the left) denotes the probablity
