from threading import Timer
import numpy as np
import requests

count = 0
#url_con = 'http://106.15.230.111/api/machine/controler/'
#url_pro = 'http://106.15.230.111/api/machine/processor/'
url_con = 'http://localhost:8000/api/machine/controler/'
url_pro = 'http://localhost:8000/api/machine/processor/'

def dataGenerator(x):
    water_in = y = 9.6*(7.9*np.sin(0.075*x) + 8.9*np.cos(0.068*x + np.pi/4) + 9.5*np.sin(0.3*x)- 7.3*np.cos(0.053*x))+700
    #进水流量函数
    water_out = 0.94*(9.6*(7.9*np.sin(0.075*(x+2880)) + 8.9*np.cos(0.068*(x+2880) + np.pi/4) + 9.5*np.sin(0.3*(x+2880))- 7.3*np.cos(0.053*(x+2880)))+700)
    #出水流量，和wate_in比较延迟4小时，大概14400秒，相位差为14400/5=2880
    lift_pump_level = (1-water_in/1000)*4
    #提升泵液位，示数范围为0-4，和进水流量成反比
    #下面的参数都和水量无关，和水质有关，非连续变化的数值
    cod = abs(np.random.normal(37,12))  
    #出水的生化需氧量，正态分布 (mu,sigma)。
    bod = abs(np.random.normal(19,5.8))
    #出水的化学需氧量
    temp = abs(np.random.normal(28,2))
    #曝气池温度
    ph = abs(np.random.normal(8,0.36))
    #曝气池PH
    ss = abs(np.random.normal(760,69))
    #污泥浓度
    data_controller = {'water_in':round(water_in,2),
                       'water_out':round(water_out,2),
                       'COD':round(cod,2),
                       'BOD':round(bod,2)}
    data_processor = {'level':round(lift_pump_level,2),
                      'temperature':round(temp,2),
                      'PH':round(ph,2),
                      'density':round(ss,2)}
    #获得的某一个检测时刻的八个数据，保留两位小数
    return data_controller,data_processor


    
def datafunc(n):
    global count
    data_con,data_pro = dataGenerator(n)  #不断重新获取数据，不保存历史数据
    r_con = requests.post(url_con,auth=('chen','adminpwd'),json=data_con)
    r_pro = requests.post(url_pro,auth=('chen','adminpwd'),json=data_pro)
    print (r_con,r_pro)
    count += 1
    Timer(5, datafunc,[count]).start()  #计时器，5秒后调用函数,相当于每5秒采样一次

Timer(1,datafunc,[count]).start() #计时器，1后首次启动