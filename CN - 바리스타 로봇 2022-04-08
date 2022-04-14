import copy
#plc ip 192.168.0.95
#kiosk ip 192.168.0.7
#robot ip 192.168.0.100
for i in range(100):
    if get_modbus_slave(209)==1: break
    wait(0.5)
else:
    tp_popup("PLC-ROBOT Communication Error")
    
################함수 모음#######################
def coffee_status():
    Get_Serial=[0x01, 0x10, 0x40, 0x6C, 0x10, 0x41, 0x42, 0x41, 0x1F, 0x10, 0x40, 0x10, 0x40, 0x10, 0x40, 0x10, 0x40, 0xB4, 0x1E, 0x04]    
    get_status=[0x01, 0x10, 0x40, 0x6C, 0x10, 0x40, 0x42, 0x41, 0x10, 0x41, 0x10, 0x40, 0x10, 0x40, 0x10, 0x40, 0x10, 0x40, 0xDD, 0xD0, 0x04]
    ser1=serial_open(port[0],115200)#
    serial_write(ser1,bytes(Get_Serial))
    res=serial_read(ser1,timeout=3)
    #tp_log("{}".format(res))
    serial_write(ser1,bytes(get_status))
    res=serial_read(ser1,timeout=3)
    #tp_log("{}".format(res))
    serial_close(ser1)
    a=0
    res=str(res)
    if "10P" in res: a+=1 #커피 작업 중
    elif res.count("ff")==3 and "10B" in res: a=1 
    elif res.count("ff")==4 and "10B" not in res: a=1 
    if "10B" in res: a+=2 #워터 작업 중
    
    return a
    
def coffee_order():
    global menu_n
    ##########주문 명령 모음##########
    Get_Serial=[0x01, 0x10, 0x40, 0x6C, 0x10, 0x41, 0x42, 0x41, 0x1F, 0x10, 0x40, 0x10, 0x40, 0x10, 0x40, 0x10, 0x40, 0xB4, 0x1E, 0x04]
    #product dump
    do_left=[0 for i in range(50)]
    #left 1
    do_left[1]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x41, 0xC2, 0xFE, 0x04, ]
    #left 2
    do_left[2]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x42, 0x82, 0xFF, 0x04, ]
    #left 3
    do_left[3]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x43, 0x43, 0x3F, 0x04, ]
    #left 4
    do_left[4]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x44, 0x10, 0x42, 0xFD, 0x04, ]
    #left 5
    do_left[5]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x05, 0xC3, 0x3D, 0x04, ]
    #left 6
    do_left[6]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x06, 0x83, 0x3C, 0x04, ]
    #left 7
    do_left[7]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x07, 0x42, 0xFC, 0x04, ]
    #left 8
    do_left[8]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x08, 0x10, 0x42, 0xF8, 0x04, ]
    #left 9
    do_left[9]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x09, 0xC3, 0x38, 0x04, ]
    #left 10
    do_left[10]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x4A, 0x83, 0x39, 0x04, ]
    #left 11
    do_left[11]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x0B, 0x42, 0xF9, 0x04, ]
    #left 12
    do_left[12]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x0C, 0x10, 0x43, 0x3B, 0x04, ]
    #left 31
    do_left[13]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x4D, 0xC2, 0xFB, 0x04, ]
    #left 14
    do_left[14]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x0E, 0x82, 0xFA, 0x04, ]
    #left 15
    do_left[15]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x0F, 0x43, 0x3A, 0x04, ]
    #left 16
    do_left[16]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x50, 0x10, 0x42, 0xF2, 0x04, ]
    #left 17
    do_left[17]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x11, 0xC3, 0x32, 0x04, ]
    #left 18
    do_left[18]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x12, 0x83, 0x33, 0x04, ]
    #left 19
    do_left[19]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x13, 0x42, 0xF3, 0x04, ]
    #left 20
    do_left[20]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x14, 0x10, 0x43, 0x31, 0x04, ]
    #left 21
    do_left[21]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x15, 0xC2, 0xF1, 0x04, ]
    #left 22
    do_left[22]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x16, 0x82, 0xF0, 0x04, ]
    #left 23
    do_left[23]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x10, 0x57, 0x43, 0x30, 0x04, ]
    #left 24
    do_left[24]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x18, 0x10, 0x43, 0x34, 0x04, ]
    #left 25
    do_left[25]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x19, 0xC2, 0xF4, 0x04, ]
    #left 26
    do_left[26]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x1A, 0x82, 0xF5, 0x04, ]
    #left 27
    do_left[27]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x1B, 0x43, 0x35, 0x04, ]
    #left 28
    do_left[28]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x1C, 0x10, 0x42, 0xF7, 0x04, ]
    #left 29
    do_left[29]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x1D, 0xC3, 0x37, 0x04, ]
    #left 30
    do_left[30]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x1E, 0x83, 0x36, 0x04, ]
    #left 31
    do_left[31]=[0x01, 0x10, 0x40, 0x68, 0x10, 0x40, 0x42, 0x41, 0x13, 0x10, 0x40, 0x10, 0x40, 0x10, 0x41, 0x10, 0x40, 0x1F, 0x42, 0xF6, 0x04,]
    global port
    n=0
    if menu_n==1: n=2 # hot 아메
    elif menu_n==2:n=12 #hot 카푸치노
    elif menu_n==3:n=7 #hot 카페라떼 
    elif menu_n==4:n=3 # ice 아메
    elif menu_n==5:n=13 # ice 카푸치노
    elif menu_n==6:n=8 # ice 카페라떼
    
    elif menu_n==7:n=17 # hot 아메2
    elif menu_n==8:n=27 # hot 카푸치노2
    elif menu_n==9:n=22 # hot 카페라떼2 
    elif menu_n==10:n=18 #ice 아메2
    elif menu_n==11:n=28 #ice 카푸치노2
    elif menu_n==12:n=23 #ice 카페라떼2
    elif menu_n==13:n=31 #핫워터
    
    ser1=serial_open(port[0],115200)#
    serial_write(ser1,bytes(Get_Serial))
    res=serial_read(ser1,timeout=1)
    #tp_log("{}".format(res))
    serial_write(ser1,bytes(do_left[n]))
    res=serial_read(ser1,timeout=1)
    #tp_log("{}".format(res))
    serial_close(ser1)
    #################menu num########################
    #1~6 원두A ,  7~12 원두B
    #1,7 Hot 아메리카노   #2,8 Hot 카푸치노    #3,9 Hot 카페라떼
    #4,10 Ice 아메리카노  #5,11 Ice 카푸치노  #6,12 Ice 카페라떼
    
    #13 TEA   #14 sparkling_water 
    
    #15~17 시럽 보통(N 푸쉬), 18~20 시럽 + (N+n 푸쉬) 
    #15 ade1  #16 ade2  #17 ade3
    #18 ade1  #19 ade2  #20 ade3
    
def ice_machine_status():
    global port
    ser2=serial_open(port[0],9600) #제빙기 연결
    sales_order=[0x7A,0x10 , 0x00 , 0x00 , 0x7B]
    serial_write(ser2,bytes(sales_order))
    res=serial_read(ser2,timeout=1)
    tp_log("{}".format(res))
    
def ice_machine_order(n):
    #제빙기 명령
    global port
    ser2=serial_open(port[1],9600) #제빙기 연결
    if n==0:
        sales_order=[0x7A,0x11,0x0a,0x00,0x7B]
        serial_write(ser2,bytes(sales_order))
        res=serial_read(ser2,timeout=1)
        #tp_log("{}".format(res))
        set_modbus_slave(146,1);wait(0.8)
        set_modbus_slave(146,0)
        wait(1.5)
    if n==1:#커피 아이스
        sales_order=[0x7A,0x11,0x0c,0x00,0x7B]
        serial_write(ser2,bytes(sales_order))
        res=serial_read(ser2,timeout=1)
        #tp_log("{}".format(res))
        set_modbus_slave(146,1);wait(0.8)
        set_modbus_slave(146,0)
        wait(1.7)
    if n==2:# 커피 물
        sales_order=[0x7A,0x11,0x00,0x46,0x7B]
        serial_write(ser2,bytes(sales_order))
        res=serial_read(ser2,timeout=1)
        #tp_log("{}".format(res))
        set_modbus_slave(146,1);wait(0.8)
        set_modbus_slave(146,0)
        wait(7.5)
    serial_close(ser2)


def rodless_out():
    begin_blend(radius=5)
    set_modbus_slave(147,1);wait(1)
    set_modbus_slave(147,0)
    wait(2)
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#app
    movej(posj(-13.19, 8.08, -110.1, 68.3, -49.19, -60.85))#app2
    movel(posx(-349.11, -41.24, 94.8, 108.91, -87.33, 92.47))#app3
    movel(posx(-309.96, -156.48, 100.67, 109.08, -91.32, 92.4),r=0)#pick
    set_tool_digital_outputs([1,-2]);wait(0.5)
    movel(posx(-309.86, -156.47, 241.33, 109.08, -91.32, 92.4))#base z+
    movej(posj(44.81, -12.51, -120.97, 69.28, -109.74, -48.74))#app
    movej(posj(65.38, 17.24, -105.39, 87.94, -50.63, 2.79))#app2
    movej(posj(117.24, 3.72, -99.66, 79.36, 29.4, 12.17))#app3
    movel(posx(148.89, -431.39, 410.32, 88.41, -89.99, 90))#place
    set_tool_digital_outputs([-1,2]);wait(0.5)
    wait(10.5)
    set_tool_digital_outputs([1,-2]);wait(0.5)
    movel(posx(148.9, -431.34, 529.29, 88.42, -89.99, 90.01))
    movej(posj(65.38, 17.24, -105.39, 87.94, -50.63, 2.79))#app2
    movej(posj(44.81, -12.51, -120.97, 69.28, -109.74, -48.74))#app
    movel(posx(-309.86, -156.47, 241.33, 109.08, -91.32, 92.4))#app
    
    movej(posj(-79.41, -19.59, -124.33, 78.54, -96.63, -52.33))#turn(j1-)
    set_modbus_slave(137,1)#로드레스 컵 OUT
    
    
    
    global menu1,menu2,menu3,menu4
    global Rodless
    if menu1==Rodless: 
        movej(posj(-64.25, -25.49, -116.11, 150.03, -50.68, -71.13))#app
        movej(posj(-55.91, -74.75, -18.32, 272.55, -62.19, -175.88))# app
        movel(posx(-229.54, 780.83, 196.02, 47.77, 95.52, -87.17))#place
        movel(posx(-229.54, 780.83, 136.02, 47.77, 95.52, -87.17),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(-355.93, 641.49, 150.19, 47.77, 95.52, -87.17),50,50)#tool z-
        menu1=0
    elif menu2==Rodless:
        movej(posj(-143.94, -43.54, -89.03, 90.45, -83.25, -42.21))#2 app
        movej(posj(-111.41, -71.97, -31.48, 90.55, -67.13, -11.41))#2 app2
        movel(posx(173.67, 778.19, 124.15, 135.56, 95.18, -91.79),r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(216.74, 735.95, 129.62, 135.56, 95.18, -91.79),30,30)#tool z-
        movel(posx(395.74, 668.2, 139.77, 118.59, 95.98, -93.37))#app
        movej(posj(-143.94, -43.54, -89.03, 90.45, -83.25, -42.21))#2 app
        menu2=0
    elif menu3==Rodless:
        movej(posj(-93.05, -40.24, -88.19, 121.19, -45.75, -52.35))#3 app
        movel(posx(-39.56, 608.33, 145.23, 103.95, 98.59, -88.16),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(-7.11, 477.59, 161.58, 103.95, 98.59, -88.16),50,50)#tool z-
        menu3=0
    elif menu4==Rodless:
        movej(posj(-118.32, -43.54, -89.03, 90.45, -83.25, -42.21))#app
        movej(posj(-112.37, -45.53, -80.27, 98.6, -62.48, -37.33))#4app
        movel(posx(118.26, 640.45, 137.86, 125.99, 98.18, -92.12),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(267.05, 435.28, 170.29, 125.99, 98.18, -92.11),50,50)#tool z-
        menu4=0
    
    
    
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 



def coffee_out():
    begin_blend(radius=5)
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#app
    movej(posj(-165.76, -25.58, -115.93, 243.08, -60.28, -119.43))#app2
    movel(posx(479.31, -86.21, 207.9, 130.18, -93.17, 91.13))#근접
    movel(posx(568.97, -192.51, 200.21, 130.13, -90.77, 91.13),r=0)#pick
    set_tool_digital_outputs([1,-2]);wait(0.5)
    movel(posx(445.88, -24.34, 215.46, 130.08, -88.63, 91.14))#app
    global Coffee
    global ice_Coffee
    if Coffee in ice_Coffee[0] : #실링기 무브
        movej(posj(-156.92, -38.89, -103.21, 302.82, -114.46, -119.97))#app2
        movej(posj(-179.58, 22.45, -130.19, 271.67, -89.38, -160.15))#app3
        movej(posj(-244.67, 3.61, -96.82, 262.56, -25.61, -170.35))#app4
        movel(posx(145.62, -435.11, 406.62, 89.89, -89.7, 91.55),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        wait(10.5)
        set_tool_digital_outputs([1,-2]);wait(0.5)
        movel(posx(145.62, -435.09, 523.14, 89.9, -89.7, 91.55))#app z+
        movej(posj(-179.58, 22.45, -130.19, 271.67, -89.38, -160.15))#app2
        movej(posj(-153.91, -35.38, -110.74, 287.4, -102.68, -121.03))#app3

    
    global menu1,menu2,menu3,menu4
    
    if menu1==Coffee: 
        movej(posj(-21.13, -35.04, -110.74, 287.4, -102.68, -121.03))#app
        movej(posj(-55.91, -74.75, -18.32, 272.55, -62.19, -175.88))#app2
        movel(posx(-229.54, 780.83, 196.02, 47.77, 95.52, -87.17),30,30)#place
        movel(posx(-229.54, 780.83, 135.02, 47.77, 95.52, -87.17),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(-355.93, 641.49, 150.19, 47.77, 95.52, -87.17),50,50)#tool z-
        menu1=0
    elif menu2==Coffee: 
        movej(posj(-151.09, -32.94, -101.76, 182.2, -43.8, -93.52))#APP
        movej(posj(-143.94, -43.54, -89.03, 90.45, -83.25, -42.21))#2 app
        movej(posj(-111.41, -71.97, -31.48, 90.55, -67.13, -11.41))#2 app2
        movel(posx(173.67, 778.19, 127.15, 135.56, 95.18, -91.79),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(216.74, 735.95, 129.62, 135.56, 95.18, -91.79),30,30)#tool z-
        movel(posx(395.74, 668.2, 135.77, 118.59, 95.98, -93.37))#app
        movej(posj(-143.94, -43.54, -89.03, 90.45, -83.25, -42.21))#2 app
        menu2=0
    elif menu3==Coffee:
        movej(posj(-151.09, -32.94, -101.76, 182.2, -43.8, -93.52))#APP
        movej(posj(-94.89, -19.28, -126.09, 130.37, -56.77, -69.03))#app
        movej(posj(-93.05, -40.24, -88.19, 121.19, -45.75, -52.35))#3 app
        movel(posx(-39.56, 608.33, 144.23, 103.95, 98.59, -88.16),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(-7.11, 477.59, 161.58, 103.95, 98.59, -88.16),50,50)#tool z-
        menu3=0
    elif menu4==Coffee:
        movej(posj(-151.09, -32.94, -101.76, 182.2, -43.8, -93.52))#APP
        movej(posj(-129.05, -41.04, -89.37, 97.54, -79.12, -39.97))
        movej(posj(-112.37, -45.53, -80.27, 98.6, -62.48, -37.33))#4app
        movel(posx(118.26, 640.45, 137.86, 125.99, 98.18, -92.12),30,30,r=0)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(267.05, 435.28, 170.29, 125.99, 98.18, -92.11),50,50)#tool z-
        menu4=0
        
    Coffee=0
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 
    
    
    
    
    #커피머신 -> 퇴출구 move
def H_W_out():
    begin_blend(radius=5)
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#app
    movej(posj(-167.73, -44.31, -90.19, 260.37, -78.05, -131.88))#app2
    movel(posx(719.21, -155.59, 215.69, 120.84, -92.16, 92.45))#진입
    set_tool_digital_outputs([1,-2]);wait(0.5)
    movel(posx(719.21, -155.59, 220.69, 120.84, -92.16, 92.45))#진입
    movel(posx(590.48, 59.78, 220.82, 120.84, -92.16, 92.45))#tool_z-
    
    global menu1,menu2,menu3,menu4
    global H_W
    if menu1==H_W: 
        movej(posj(-21.13, -35.04, -110.74, 287.4, -102.68, -121.03))#app
        movej(posj(-55.91, -74.75, -18.32, 272.55, -62.19, -175.88))#app2
        movel(posx(-229.54, 780.83, 196.02, 47.77, 95.52, -87.17),30,30)#place
        movel(posx(-229.54, 780.83, 136.02, 47.77, 95.52, -87.17),30,30)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(-355.93, 641.49, 150.19, 47.77, 95.52, -87.17),50,50)#tool z-
        menu1=0
    elif menu2==H_W: 
        movej(posj(-151.09, -32.94, -101.76, 182.2, -43.8, -93.52))#APP
        movej(posj(-143.94, -43.54, -89.03, 90.45, -83.25, -42.21))#2 app
        movej(posj(-111.41, -71.97, -31.48, 90.55, -67.13, -11.41))#2 app2
        movel(posx(173.67, 778.19, 127.15, 135.56, 95.18, -91.79))#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(216.74, 735.95, 129.62, 135.56, 95.18, -91.79),30,30)#tool z-
        movel(posx(395.74, 668.2, 135.77, 118.59, 95.98, -93.37))#app
        movej(posj(-143.94, -43.54, -89.03, 90.45, -83.25, -42.21))#2 app
        menu2=0
    elif menu3==H_W:
        movej(posj(-151.09, -32.94, -101.76, 182.2, -43.8, -93.52))#APP
        movej(posj(-94.89, -19.28, -126.09, 130.37, -56.77, -69.03))#app
        movej(posj(-93.05, -40.24, -88.19, 121.19, -45.75, -52.35))#3 app
        movel(posx(-39.56, 608.33, 145.23, 103.95, 98.59, -88.16),30,30)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(-7.11, 477.59, 161.58, 103.95, 98.59, -88.16),50,50)#tool z-
        menu3=0
    elif menu4==H_W:
        movej(posj(-151.09, -32.94, -101.76, 182.2, -43.8, -93.52))#APP
        movej(posj(-129.05, -41.04, -89.37, 97.54, -79.12, -39.97))
        movej(posj(-112.37, -45.53, -80.27, 98.6, -62.48, -37.33))#4app
        movel(posx(118.26, 640.45, 137.86, 125.99, 98.18, -92.12),30,30)#place
        set_tool_digital_outputs([-1,2]);wait(0.5)
        movel(posx(267.05, 435.28, 170.29, 125.99, 98.18, -92.11),50,50)#tool z-
        menu4=0
        
    H_W=0
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 
    
def cup_out():
    begin_blend(radius=5)
    global cup_num
    count=0; offset=0
    for i in range(4):
        if cup_num==1:
            movej(posj(96.91, -11.57, -82.87, 179.99, 85.58, -81.31))#CUP_APP
            movel(posx(58.87, -469.46-offset, 258.26, 131.53, 179.98, 133.31),r=0)#PICK
            set_tool_digital_outputs([1,-2]); wait(0.2)
            movel(posx(53.8, -289.85, 258.08, 130.55, 179.98, 132.33))#y+
            movel(posx(8.87, -290.03, 281.73, 156.87, 179.69, 156.75))#z+
            movel(posx(-255.36, -292.27, 281.73, 131.85, 179.98, 133.63))#컵 센싱
        elif cup_num==2:
            movej(posj(120.01, -13.28, -70.1, 179.99, 96.59, -61.7))#cup_app
            movel(posx(229.34, -466.97-offset, 256.14, 89.56, -179.98, 87.85),r=0)#pick
            set_tool_digital_outputs([1,-2]); wait(0.2)
            movel(posx(229.71, -325.49, 256.21, 90.25, -179.98, 88.54))#y+
            movel(posx(8.87, -290.03, 281.73, 156.87, 179.69, 156.75))#z+
            movel(posx(-255.36, -292.27, 281.73, 131.85, 179.98, 133.63))#컵 센싱
        if get_modbus_slave(208)==0: #포토 센서 inposx(229.76, -480.21, 256.73, 90.4, -179.98, 88.69)
            set_tool_digital_outputs([-1,2]); wait(0.2)
            count+=1; offset=5
            if count==2:
                count==0; offset=0
                if cup_num==1: cup_num=2
                elif cup_num==2: cup_num=1
        else: break
    else:
        tp_popup("컵이 없습니다. 컵을 넣고 계속을 눌러주세요.")
        wait(10)
        cup_out()
    end_blend() 

def ice_in(n):
    begin_blend(radius=5)
    movej(posj(44.41, 28.27, -130.66, 180.07, 21.31, -129.35))#app
    movej(posj(16.56, -7.96, -126.49, 140.81, -47.41, -64.51))#app2
    movej(posj(15.33, -14.72, -113.97, 137.81, -46.4, -62.25))#app3
    if n==2: #ice coffe:
        ice_machine_order(1)#얼음
        ice_machine_order(2)#물
    else:
        ice_machine_order(0)#얼음
    movej(posj(16.56, -7.96, -126.49, 140.81, -47.41, -64.51))#app2
    end_blend() 
    
def rodless_in():
    begin_blend(radius=5)
    movej(posj(-1.79, -18.6, -118.63, 91.67, -90.25, -61))#app
    
    movel(posx(-310.87, -96.32, 239.18, 108.8, -89.69, 89.99))#app
    movel(posx(-310.78, -96.32, 172.21, 108.81, -89.69, 89.99))#app
    movel(posx(-310.99, -96.32, 143.84, 108.8, -89.69, 90),30,30,r=0)#place
    set_tool_digital_outputs([-1,2]);wait(1.5)
    set_tool_digital_outputs([1,-2]);wait(0.5)
    
    movel(posx(-312.96, -156.48, 160.67, 108.91, -87.32, 92.4))#app
    movel(posx(-312.96, -156.48, 100.67, 108.91, -87.32, 92.4),r=0)#place
    set_tool_digital_outputs([-1,2]);wait(0.5)
    movel(posx(-349.11, -41.24, 94.8, 108.91, -87.33, 92.47))#tool_z-
    
    
    movej(posj(-13.19, 8.08, -110.1, 68.3, -49.19, -60.85))#homing_app
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 
    
def ice_coffee_in():
    begin_blend(radius=5)
    movej(posj(-165.76, -25.58, -115.93, 243.08, -60.28, -119.43))#app
    movel(posx(565.13, -188.02, 206.45, 130.08, -88.63, 91.14))#진입
    movel(posx(565.13, -188.02, 180.4, 130.08, -88.63, 91.14),30,30,r=0)#place
    set_tool_digital_outputs([-1,2]);wait(0.5)
    movel(posx(408.31, -1.88, 174.59, 130.08, -88.62, 91.13))#tool_z-
    coffee_order()
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 
    
    
def hot_coffee_in():
    begin_blend(radius=5)
    movej(posj(-31.54, 10.22, -112.13, 58.05, -94.95, -44.73))#app
    movej(posj(-165.76, -25.58, -115.93, 243.08, -60.28, -119.43))#app2
    movel(posx(565.13, -188.02, 206.45, 130.08, -88.63, 91.14))#진입
    movel(posx(565.13, -188.02, 180.4, 130.08, -88.63, 91.14),30,30,r=0)#place
    set_tool_digital_outputs([-1,2]);wait(0.5)
    movel(posx(408.31, -1.88, 174.59, 130.08, -88.62, 91.13))#tool_z-
    coffee_order()
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 

def H_W_in():
    begin_blend(radius=5)
    movej(posj(-31.54, 10.22, -112.13, 58.05, -94.95, -44.73))#app
    movej(posj(-168.52, -37.8, -97.56, 238, -63.18, -123.81))#app2
    movel(posx(719.21, -155.59, 215.69, 120.84, -92.16, 92.45))#진입
    movel(posx(719.21, -155.59, 183.37, 120.84, -92.16, 92.45),30,30,r=0)#place
    set_tool_digital_outputs([-1,2]);wait(1)
    coffee_order()
    movel(posx(590.48, 59.78, 192.82, 120.84, -92.16, 92.45))#tool_z-
    movej(posj(-2.8, 19.93, -108.87, 130.83, 65.19, -65.34))#homing_app2
    movej(posj(80.82, 15.28, -89.09, 179.99, 106.21, -100.92))#homing
    end_blend() 
    
def menu_navigation(a,b,c):
    #제조 우선 메뉴 탐색 
    global m_list
    value = [ len(m_list[0][1]), len(m_list[1][1]),len(m_list[2][1]),len(m_list[3][1]), len(m_list[4][1]) ] 
    
    if a!=0: #제조 중이기에 시작 X
        value[0]=0; value[2]=0
    if b!=0:
        value[1]=0; value[3]=0
    if c!=0: value[4]=0
        
    max_n = max(value) 
    if max_n==0: return 0
    index_n = value.index(max_n)   
    return m_list[index_n][1].pop(0)

def menu_navigation2():
    # 퇴출 우선 메뉴 탐색
    global m_list
    v_list=copy.deepcopy(m_list)
    value = [ len(v_list[0][1]), len(v_list[1][1]),len(v_list[2][1]),len(v_list[3][1]), len(v_list[4][1]) ] 
    max_n = max(value)
    if max_n==0: return 0
    index_n = value.index(max_n)
    n=v_list[index_n][1].pop(0)
    return n,v_list


def signal_reset():
    drl_report_line(0)
    set_modbus_slave(130,0)
    set_modbus_slave(131,0)
    set_modbus_slave(132,0)
    set_modbus_slave(133,0)
    set_modbus_slave(134,0)
    set_modbus_slave(135,0)
    set_modbus_slave(136,0)
    set_modbus_slave(137,0)
    set_modbus_slave(138,0)
    set_modbus_slave(139,0)
    set_modbus_slave(140,0)
    set_modbus_slave(141,0)
    set_modbus_slave(142,0)
    set_modbus_slave(143,0)
    set_modbus_slave(144,0)
    set_modbus_slave(145,0)
    set_modbus_slave(146,0)
    set_modbus_slave(147,0)
    set_modbus_slave(148,0)
    set_modbus_slave(149,0)
    set_modbus_slave(150,0)
    set_modbus_slave(151,0)
    set_modbus_slave(152,0)
    set_modbus_slave(153,0)
    set_modbus_slave(154,0)
    set_modbus_slave(155,0)
    set_modbus_slave(156,0)
    set_modbus_slave(157,0)
    set_modbus_slave(158,0)
    set_modbus_slave(159,0)
    set_modbus_slave(160,0)
    drl_report_line(1)
    
############################초기 세팅#####################################
n=1
q = get_current_posj() #관절각 리턴받아 홈위치로 되어있는 지 확인
if 82 >q[0]> 78 and  17 >q[1]> 13 and -87 >q[2]> -91 and 181 >q[3]> 178 and 108 >q[4]> 104 and -98 >q[5]> -102:
    a=1
else:
    tp_popup("Not a Home Posithon")
    exit()
    
signal_reset() # 신호 리셋
set_tool_digital_outputs([-1,2])#그리퍼 열기
set_velx(500) # 전역 태스크 속도
set_accx(500) # 전역 태스크 가속도
set_velj(70) # 전역 조인트 속도
set_accj(45) # 전역 조인트 가속도
set_tool("Tool Weight") # 툴 무게 설정
#set_tcp("!@#12") #그리퍼 설정


set_modbus_slave(130,1)#로봇 대기 상태 ON 송신



################get 포트 #######################
port=[]
for i in range(1,3):
    port_info, device_name = serial_get_info(i)
    port.append(port_info)   
    tp_log("포트 넘버{}".format(i))
    tp_log("{}".format(port_info))
    tp_log("{}".format(device_name))


   
################프로그램 시작 #####################3
cup_num=1
while True:
    signal_reset() # 신호 리셋
    set_modbus_slave(130,1)#로봇 대기 상태 ON 송신
    ###############PLC-ROBOT 송수신값 매칭########################
    while True:
        if get_modbus_slave(204)==1: break# 메뉴 수신
    
    menu1=get_modbus_slave(200) #메뉴 1
    menu2=get_modbus_slave(201) #메뉴 2
    menu3=get_modbus_slave(202) #메뉴 3
    menu4=get_modbus_slave(203) #메뉴 4
    set_modbus_slave(131,menu1) #메뉴 1 값 송신
    set_modbus_slave(132,menu2) #메뉴 2 값 송신
    set_modbus_slave(133,menu3) #메뉴 3 값 송신
    set_modbus_slave(134,menu4) #메뉴 4 값 송신
    set_modbus_slave(135,1) # 메뉴 송신
    
    while True:
        if get_modbus_slave(205)==1: break# 제조 시작 수신
    
    set_modbus_slave(130,0)#로봇 대기 상태 off 송신
    set_modbus_slave(141,0)# 제조 완료 off 송신
    set_modbus_slave(131,0) #메뉴 1 값 송신
    set_modbus_slave(132,0) #메뉴 2 값 송신
    set_modbus_slave(133,0) #메뉴 3 값 송신
    set_modbus_slave(134,0) #메뉴 4 값 송신
    set_modbus_slave(135,0) # 메뉴 송신
    
    
    tp_log("{},{},{},{}".format(menu1,menu2,menu3,menu4))
    
    ##################제조 순서#######################
    # 제조 시간 높은 순 : hot water → 탄산수 → hot coffee → ade → ice coffee  (시간측정 필요)
    
    #1         ice coffee        : 로봇(컵) → 제빙기 → 커피머신 → ToGo
    #2             ade             : 로봇(컵) → 제빙기 → 로드레스 →  제빙기 → ToGo
    #3         hot coffee        : 로봇(컵) → 커피머신 → ToGo
    #4    sparkling_water     : 로봇(컵) → 로드레스 → ToGo
    #5         hot water         : 로봇(컵) → 커피머신 → ToGo
    # ade >< ice coffee - ??
    # * 우선순위가 낮아도 주문 수량이 많으면 우선 체크
    # ex : hot water 2 , hot coffee 1
    # hot water -> hot coffee -> hot water
    
    
    #################menu num########################
    #1~6 원두A ,  7~12 원두B
    #1,7 Hot 아메리카노   #2,8 Hot 카푸치노    #3,9 Hot 카페라떼
    #4,10 Ice 아메리카노  #5,11 Ice 카푸치노  #6,12 Ice 카페라떼
    
    #13 TEA   #14 sparkling_water 
    
    #15~17 시럽 보통(N 푸쉬), 18~20 시럽 + (N+n 푸쉬) 
    #15 ade1  #16 ade2  #17 ade3
    #18 ade1  #19 ade2  #20 ade3
    
    
    ##################Variable########################
    ice_Coffee         =[ [4,10], [] ]
    Ade                  =[ [15,16,17,18,19,20] , [] ]
    Hot_Coffee         =[ [1,2,3,5,6,7,8,9,11,12] , [] ]
    Sparkling_Water =[ [14], [] ]
    Hot_Water          =[ [13], [] ]
    
    m_list=[ice_Coffee, Ade, Hot_Coffee, Sparkling_Water, Hot_Water]
    for M in menu1,menu2,menu3,menu4:
        for i in range(5):
            if M in m_list[i][0]: m_list[i][1].append(M)
            
    #0 사용 가능 , (menu num) 제조 중
    # ex : Coffee=12 : ice 카페라떼 제조 중
    Coffee=0#커피머신 사용 가능
    Rodless=0#로드레스 사용 가능
    H_W=0#핫워터 사용 가능
    
        
    ################제조 시작########################
    while sum([menu1,menu2,menu3,menu4]):
        V=0
        menu_n=menu_navigation(Coffee,Rodless,H_W)
        
        if menu_n!=0: #제조 시작 우선
            if menu_n in m_list[0][0] or menu_n in m_list[2][0]: #커피머신을 사용하는 가?
                
                cup_out()
                if menu_n in ice_Coffee[0]: #제빙기 후 커피
                    ice_in(2)
                    ice_coffee_in()
                else:
                    hot_coffee_in()
                
                Coffee=menu_n
            elif menu_n in m_list[1][0] or menu_n in m_list[3][0]: #로드레스를 사용하는 가?
                set_modbus_slave(147,1);wait(1)
                set_modbus_slave(147,0)
                cup_out()
                ice_in(1)
                
                rodless_in()
                if menu_n==14:
                    num1=4; num2=0
                if menu_n==15:
                    num1=1; num2=11
                if menu_n==16:
                    num1=2; num2=11
                if menu_n==17:
                    num1=3; num2=11
                if menu_n==18:
                    num1=1; num2=20
                if menu_n==19:
                    num1=2; num2=20
                if menu_n==20:
                    num1=3; num2=20
                
                set_modbus_slave(136,1)#로드레스 컵 IN 송신
                set_modbus_slave(138,num1)#실린더 넘버 or 탄산 송신
                set_modbus_slave(139,num2)#시럽 양 or 0 송신
                set_modbus_slave(140,1)#로드레스 동작 송신
                wait(0.3)
                set_modbus_slave(140,0)#로드레스 동작 송신 offf
                Rodless=menu_n
            elif menu_n in m_list[4][0]: # 핫 워터인가?
                cup_out()
                H_W_in()
                H_W=menu_n
        elif menu_n==0: #제조 시작 불가 or 모든 메뉴 제조 중
            # 다음 메뉴 우선 퇴출
            for i in range(3):
                menu_n=menu_navigation2()
  
                if menu_n in m_list[0][0] or menu_n in m_list[2][0]: #커피머신을 사용하는 가?
                    a=coffee_status()
                    if a==0 or a==2 : #커피 작업 종료
                        coffee_out() #퇴출 무브
                        V,Coffee=Coffee,V
                        tp_log("{}".format(Coffee))
                        break
                elif menu_n in m_list[1][0] or menu_n in m_list[3][0]: #로드레스를 사용하는 가?
                    if get_modbus_slave(207)==1: #로드레스 작업 완료 수신
                        rodless_out() #퇴출 무브
                        V,Rodless=Rodless,V
                        break
                elif menu_n in m_list[4][0]: # 핫 워터인가?
                    a=coffee_status()
                    if a==0 or a==1: #핫워터 작업 종료
                        H_W_out() #퇴출 무브
                        V,H_W=H_W,V
                        break
                
            else: #제조 X 퇴출만 하면 종료
                if get_modbus_slave(207)==1and Rodless!=0:#: #로드레스 작업 완료 수신
                    rodless_out() #퇴출 무브
                    set_modbus_slave(136,0)#로드레스 컵 홀더 in off
                    set_modbus_slave(137,1)#로드레스 컵 홀더 out
                    wait(0.3)
                    set_modbus_slave(137,0)
                    V,Rodless=Rodless,V

                elif coffee_status()==0 and Coffee!=0: #커피 작업 종료
                    coffee_out() #퇴출 무브
                    V,Coffee=Coffee,V

                elif coffee_status()==0 and H_W!=0: #핫워터 작업 종료
                    H_W_out() #퇴출 무브
                    V,H_W=H_W,V

        if menu1==V: menu1=0
        if menu2==V: menu2=0
        if menu3==V: menu3=0
        if menu4==V: menu4=0
    set_modbus_slave(141,1)#제조 완료 송신
    wait(5)
    
    
    
