# People Detection Radar [IoT]

### Raspberry PI Xandar Kardian IoT People Count Radar

![](doc/img/Logo.png)

**Program Design Purpose**: 

People detection sensors and radars are utilized in various applications across multiple fields such as security and surveillance, healthcare, building automation, smart cities, transportation, and autonomous systems. This project aims to develop a prototype for an indoor people counting IoT device using the Xandar Kardian People Detection Radar and a Raspberry Pi. The device will be network-ready and easily integrated with other systems. The Python-based IoT firmware will run on the Raspberry Pi and provide the following functionalities:

1. Read raw data from the people detection radar to determine the number of people in an area.

2. Offer a web interface for users to view the data and adjust radar parameters.

3. Provide IoT data access authorization and interfaces for integration with other systems.

The system workflow is shown below : 

![](doc/img/sysworkflow.png)

The project Python IoT firmware code is also modularized and flexible for user to plug their own sensors on Raspberry PI to build different kinds of customized IoT device. 

```
# Created:     2019/09/11 [ rebuilt from v1.5 on 22/06/2024 ]
# version:     v2.3 
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction

This project will create a prototype people count(detection) radar IoT with a website server to provide the live history chart to show the Xandar Kardian People counting sensor data. It is build by using one/two Xandar CT-100 people detection radar and one Raspberry PI. The firmware will run on Raspberry PI and contents five modules: 

- **IoT Radar Communication Module** : Module used to connect to the Raspberry PI serial(COM) or GPIO port to fetch the radar raw data and convert to list of parameter value. 
- **IoT Data Management Module** : Module used to do radar data normalization and manage all the data update on the web UI. 
- **IoT User Authorization Module** : Provide a user authorization function with a data base for IoT admin to create, update and remove users and manage the data assessment for different users. 
- **IoT web host Module** : Webhost module provide a website for user to view radar data, manage users and change radar setting, it also provide http(s) data GET API for other program to fetch data from the IoT
- **IoT Hub report module**: Module used to report the IoT data to IoT hub server regularly and fetch the IoT control commands.  

When the engineer are installing the  people count radar with its IOT device in the network. They don't need to use the computer to connect to the sensor directly to check the sensor state. They can use the login in the web sever running in the  IOT gateway to finish the job. The web side view is shown below:

![](doc/img/radarIoT.gif)



#### Background Information Introduction

People detection sensors use various technologies, including infrared, ultrasonic, microwave, and video analytics, to detect and monitor human presence and movement. The choice of technology and application depends on the specific requirements and environment. In this project we use the microwave people detection radar which can be used in the dark area as an assist of the surveillance cameras. 

- Introduction of Xandar People Detection Radar : https://xkcorp.com/
- Introduction of Raspberry IoT:  https://www.raspberrypi.com/

#### Possible Usage Cases

In this project, we only use the people counting function (1 of the 30 parameters ) of the CT100 people detection radar. User can use the other data of the radar sensor to pivotal in enhancing security, improving energy efficiency, and providing valuable data for business and operational insights. We think there may be 10 fields where IoT people detection sensors can be used:

| Idx  | Use case type                           | Use case detail description                                  |
| ---- | --------------------------------------- | ------------------------------------------------------------ |
| 1    | Security and Surveillance               | Intruder detection and perimeter security especially in the dark area. |
| 2    | Building Automation and Smart Buildings | Optimize lighting control, AC Systems and access Control.    |
| 3    | Retail and Marketing                    | Customer counting, foot traffic analysis and queue management |
| 4    | Healthcare                              | Patient Monitoring, Staff Utilization and room occupancy     |
| 5    | Transportation                          | Passenger Counting, Crowd Management and Safety Systems      |
| 6    | Smart Cities                            | Public Space Management, Traffic Management, Emergency Response |
| 7    | Office Environments                     | Space Utilization and Energy Savings.                        |
| 8    | Hospitality                             | Guest Services, Security and Resource Management             |
| 9    | Industrial and Manufacturing            | worker Safety, Efficiency Monitoring and Asset Protection    |
| 10   | Residential                             | Home Automation, Elderly Care and Energy Management          |



------

### Program Design

The IoT firmware program is a multi-threading program. The IoT Radar Communication Module and IoT Hub report module will run in two parallel thread to automated fetch data from the radar senor and report the information to IoT hub.









The web host program contents three main section

##### Sensor data collection module 

This module will normalized the reading data from the sensor and get the final people count. 

##### Web host module 

This module will provide a web host program to do the use authorization, result visualization.   



------

### Program Setup

###### Development env: Python 3.7

###### Additional Lib need: 

1. Flask 1.1.1 (buil Web-Server lib need to be installed)

   [Flask]: https://pypi.org/project/Flask/:	"Flask"

   ```
   pip install -U Flask
   ```

###### Hardware Need:

1. Raspberry PI 3 B+ (used as IOT gateway)

   [Raspberry PI]: https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/	"IOT gateway"

2. Xandar Kardian People counting sensor.

   [Xandar Kardian]: http://xandar.com/people-counting/	"People counting sensor"
   
   ![](doc/img/sensor.png)

###### Program Files List 

| Program File            | Execution Env | Description                                                  |
| ----------------------- | ------------- | ------------------------------------------------------------ |
| src/ConfigLoader.py     | python 3      | Loader module to read the user name and password information. |
| src/ConfigUser.txt      |               | Save user and password.                                      |
| src/XAKAsensorComm.py   | python 3      | Sensor communication interface module.                       |
| src/XAKAsensorGlobal.py | python 3      | Global parameters module.                                    |
| src/XandaWebHost.py     | python 3      | Web host program.                                            |
| src/templates/*.html    |               | All the html web pages.                                      |
| src/static              |               | static files storage folder such as css, image file.         |
|                         |               |                                                              |

------

### Program Usage/Execution

###### Program execution cmd: 

```
python XandaWebHost.py
```

###### Usage : 

Type in the URL [IPaddr:5000] (http://127.0.0.1:5000/) in your browser then the page will shown as below: 

 ![](doc/img/home.png)

Then click the Login link and type in the username/password for authorization: 

![](doc/img/authorization.png)

After type in the correct user name and password, the people counting sensor main page will show. 

![](doc/img/2019-09-19_103505.png)



### Problem and Solution

N.A

------

### Reference

Xandar Kardian people counting sensors : https://www.xkcorp.com/

------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 31/01/2022

