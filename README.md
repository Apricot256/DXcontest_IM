# Item Manage Too for DXcontest

## Discription
This is a repository of programs to estimate the quantity of materials at edge devices.

## Developing Environment
- Nvidia Jetson AGX Xavire (JetPack 4.6.0)
- Docker Engine ver.xx.xx
- Docker-compose version xx.xx

## How to Use

- build image
    ```
    docker build -t IMAGE_NAME DOCKERFILE_PATH
    ```
- run container
    ```
    docker run -d --rm --runtime nvidia -v MNT:/root --network host IMAGE_NAME
    ```
- If you want to run regularly, please register with crontab or other.

## Using Technologys

<p align="left"> 
    <a href="https://www.nvidia.com/en-us/autonomous-machines/embedded-systems//">
    <img alt="selenium" height="64px" src="https://www.openrtm.org/openrtm/sites/default/files/6341/NV_JETSON_TX1_LOGO4.png" /></a>
    <a href="https://www.docker.com/">
    <img alt="selenium" height="64px" src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" /></a>
    <a href="https://www.python.org/">
    <img alt="Python" height="64px" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/165px-Python-logo-notext.svg.png" /></a>　
    <a href="https://www.tensorflow.org/">
    <img alt="selenium" height="64px" src="https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg" /></a>
  
</p>
