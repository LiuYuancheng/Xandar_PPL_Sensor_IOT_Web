# Flask_Sensor_Server
#### Introduction

This project will create a simple web server to provide the history chart to show the Xandar Kardian(

[XAKA]: 	"Xandar Kardian"

) People counting sensor data.  So when the engineer are install the sensor with the IOT gateway. They don't need to use the computer to connect to the sensor directly to check the sensor state. They can login in the web sever running in the  IOT gateway to finish the job.

###### Web Main UI View: 

![](https://github.com/LiuYuancheng/Flask_Sensor_Server/blob/master/doc/2019-09-19_103505.png)

------

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

------

#### Program usage

###### Program execution cmd: 

```
python testProute.py
```

###### Usage : 

Type in the URL [IPaddr:5000] in your browser then the page will shown as below: 

 ![](https://github.com/LiuYuancheng/Flask_Sensor_Server/blob/master/doc/2019-09-19_103258.png)

They click the Login link: 

![](https://github.com/LiuYuancheng/Flask_Sensor_Server/blob/master/doc/2019-09-19_103328.png)

After type in the correct user name and password, the people counting sensor main page will show. 