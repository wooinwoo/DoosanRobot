drl_report_line(1)
########## 초기 세팅 값 ##########

#전역 조인트 스피드를 설정합니다.
set_velj(30)
set_accj(60)
#전역 태스크 스피드를 설정합니다.
set_velx(30,20)
set_accx(60,40)
#TCP를 등록합니다.
set_tcp("공압그리퍼")
#툴을 등록합니다.
set_tool("Tool Weight_grip")
set_tool("Tool Weight_Driver")


########## 쓰레드 ########
def Check_Position(): 
    x,sol=get_current_posx()
    p=get_current_posj()
    
    if x[0]>0 or p[0]>0: 
        set_output_register_bit(22,OFF)
        set_output_register_bit(21,ON) #현재 로봇 위치 정면
    elif x[0]<0 and p[0]<0:
        set_output_register_bit(21,OFF)
        set_output_register_bit(22,ON) #현재 로봇 위치 후면
        
def Robot_Speed():
    value=get_input_register_int(0)
    velj=value*1.5
    accj=value*3
    velx_1=value*1.5
    velx_2=value*1
    accx_1=value*3
    accx_2=value*2
    #전역 조인트 스피드를 설정합니다.
    set_velj(velj)
    set_accj(accj)
    #전역 태스크 스피드를 설정합니다.
    set_velx(velx_1,velx_2)
    set_accx(accx_1,accx_2)
    wait(1)

########## 함수 ##########

#모든 신호를 초기화합니다.
def signal_reset(): 
    drl_report_line(0)
    set_output_register_bit(14,OFF)
    set_output_register_bit(15,OFF)
    set_output_register_bit(16,OFF)
    set_output_register_bit(32,OFF)
    set_output_register_bit(33,OFF)
    set_output_register_bit(34,OFF)
    set_output_register_bit(35,OFF)
    set_output_register_bit(36,OFF)
    set_output_register_bit(37,OFF)
    set_output_register_bit(38,OFF)
    set_output_register_bit(39,OFF)
    set_output_register_bit(40,OFF)
    set_output_register_bit(41,OFF)
    set_output_register_bit(42,OFF)
    set_output_register_bit(43,OFF)
    set_output_register_bit(44,OFF)
    set_output_register_bit(45,OFF)
    set_output_register_bit(46,OFF)
    set_output_register_bit(63,OFF)
    set_digital_outputs(bit_start=1, bit_end=15, val=0b000000000000000)
    drl_report_line(1)
    
def Grip():
    set_digital_outputs([-1,-2]) #신호 초기화
    set_digital_output(1)#그립 신호 ON
    wait(1.5)
    wait_digital_input(1,OFF)#그립완료신호 대기
    set_digital_output(1)#그립 신호 OFF
    
def Release():
    set_digital_outputs([-1,-2]) #신호 초기화
    set_digital_output(2)#그립해제 신호 ON
    wait_digital_input(2,ON)#그립해제 완료신호 대기
    set_digital_output(-2)#그립해제 신호 OFF
    
    
    
    



th_id_1 = thread_run(Check_Position, loop=True)

th_id_2 = thread_run(Robot_Speed, loop=True)

while(1):





    ###로봇 초기화 시작###
    # 1) plc → 초기화 ON
    # 2) robot → 초기화 ON
    # 3) plc → 초기화 OFF
    # 4) robot → 초기화 OFF
    while(1):
        if get_input_register_bit(16) == 1: # plc → 초기화 ON
            break
        wait(0.1)
        
    Release() #그립 해제
    Task_space_point,sol = get_current_posx()
    if Task_space_point[2]<50:
        Height=100-Task_space_point[2]
        movel([0,0,Height,0,0,0],mod=DR_MV_MOD_REL)
    signal_reset()#모든 신호를 초기화합니다.
    set_output_register_bit(19,ON) #현재 툴 상태 Grip (시작 그리퍼)
    set_output_register_bit(16,ON) # robot → 초기화 ON
    
    while(1):
        if get_input_register_bit(16) == 0: # plc → 초기화 OFF
            set_output_register_bit(16,OFF) # robot → 초기화 OFF
            break
        wait(0.1)
        
   
    
    
    
    
    
    
    
    
    ######## main program #########
    while(1):
    
        for step in range(32,64):
            if get_input_register_bit(step)==1: break
        else:
            if get_input_register_bit(16)==1: break
            continue #신호가 없을 시 신호를 재탐색 합니다.
            
        tp_log("step : {}".format(step))
        
        
        signal_reset()#모든 신호를 초기화합니다.
        
        
        if step==16: #프로그램 초기화
            break
        elif step==32: #정면 안전위치 이동
            movej(posj(-180.05, -0.06, -90.16, 0.04, -90.11, 159.73))# 정면 안전 위치
            
        elif step==33 : #후면 안전위치 이동
            movej(posj(0, -0.06, -90.16, 0.04, -90.11, 159.73))# 후면 안전위치
            
        elif step==34 : #툴 체인지 준비위치 이동
            movej(posj(-256.53, 24.98, -93.8, 0, -111.18, 79.96)) # 툴 체인지 준비위치 이동
            
        elif step==35 : #Tool 미부착 상태에서 Grip Tool Pick
            movel(posx(156.35, -447.39, 275.61, 20.73, 180, -0.21))#via
            movel(posx(156.49, -536.04, 275.78, 109.52, -180, 88.58)) #app            
            movel(posx(156.49, -536.04, 265.7, 25.43, 180, 4.49)) # grip pick
            set_tool("Tool Weight_grip")
            set_digital_output(10)
            movel(posx(156.49, -536.04, 275.78, 109.52, -180, 88.58)) #UP  
            movel(posx(156.35, -447.39, 275.61, 20.73, 180, -0.21))#via
            movej(posj(-256.53, 24.98, -93.8, 0, -111.18, 79.96)) # 툴 체인지 준비위치 이동
            
        elif step==36 : #Tool 미부착 상태에서 Driver Tool Pick
            movel(posx(-72.58, -396.14, 299.14, 84.65, 180, 63.56))#via
            movel(posx(-72.63, -503.27, 299.26, 81.42, 180, 60.33))#app
            movel(posx(-72.63, -503.29, 275.44, 81.42, 180, 60.33))#Driver pick
            set_tool("Tool Weight_Driver")
            set_digital_output(16)
            set_digital_output(10)
            movel(posx(-72.63, -503.27, 299.26, 81.42, 180, 60.33))#UP
            set_digital_output(-10)
            movel(posx(-72.58, -396.14, 299.14, 84.65, 180, 63.56))#via
            movej(posj(-256.53, 24.98, -93.8, 0, -111.18, 79.96)) # 툴 체인지 준비위치 이동
            
        elif step==37 : #그립 툴 체인지 동작시작
            movel(posx(-72.58, -396.14, 299.14, 84.65, 180, 63.56))#via
            movel(posx(-72.63, -503.27, 299.26, 81.42, 180, 60.33))#app
            movel(posx(-72.63, -503.29, 275.44, 81.42, 180, 60.33))#Driver place
            set_tool("Tool Weight")
            set_digital_output(-16)
            set_digital_output(10)
            movel(posx(-72.63, -503.27, 299.26, 81.42, 180, 60.33))#UP
            set_digital_output(-10)
            movel(posx(156.35, -503.27, 299.26, 81.42, 180, 60.33))#app1
            movel(posx(156.49, -536.04, 299.26, 109.52, -180, 88.58)) #app2
            movel(posx(156.49, -536.04, 265.7, 25.43, 180, 4.49)) # grip pick
            set_tool("Tool Weight_grip")
            set_digital_output(9)
            movel(posx(156.49, -536.04, 275.78, 109.52, -180, 88.58)) #UP
            set_digital_output(-9)
            movel(posx(156.35, -447.39, 275.61, 20.73, 180, -0.21))#app
            movej(posj(-256.53, 24.98, -93.8, 0, -111.18, 79.96)) # 툴 체인지 준비위치 이동

            set_output_register_bit(20,OFF) #현재 툴 상태 Grip
            set_output_register_bit(19,ON) #현재 툴 상태 Grip
            
        elif step==38 : #드라이버 툴 체인지 동작시작
            movel(posx(156.35, -447.39, 275.61, 20.73, 180, -0.21))#via
            movel(posx(156.49, -536.04, 275.78, 109.52, -180, 88.58)) #app            
            movel(posx(156.49, -536.04, 265.7, 25.43, 180, 4.49)) # grip place
            set_tool("Tool Weight")
            set_digital_output(10)
            movel(posx(156.49, -536.04, 275.78, 109.52, -180, 88.58)) #UP
            set_digital_output(-10)
            movel(posx(156.35, -503.27, 299.26, 81.42, 180, 60.33))#app1
            movel(posx(-72.63, -503.27, 299.26, 81.42, 180, 60.33))#app2
            movel(posx(-72.63, -503.29, 275.44, 81.42, 180, 60.33))#Driver pick
            set_tool("Tool Weight_Driver")
            set_digital_output(9)
            set_digital_output(16)
            movel(posx(-72.63, -503.27, 299.26, 81.42, 180, 60.33))#UP
            set_digital_output(-9)
            movel(posx(-72.58, -396.14, 299.14, 84.65, 180, 63.56))#via
            movej(posj(-256.53, 24.98, -93.8, 0, -111.18, 79.96)) # 툴 체인지 준비위치 이동



        
            set_output_register_bit(19,OFF)
            set_output_register_bit(20,ON) #현재 툴 상태 Driver
            
        elif step==39 : #메인 유닛 상부위치로 이동
            movej(posj(-37.04, -16.36, -87.28, -0.01, -76.41, 122.42))
            
        elif step==40 : #메인 유닛 공급 시작
        
            value=get_input_register_int(2)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            
            
            
            if i==0: master_pick=posx(-409.08, 259.65, -38.47, 150, -179.94, -50.54)#1번 메인유닛
            elif i==1: master_pick=posx(-408.08, 339.65, -38.48, 150.06, -179.94, -50.48)#2번 메인유닛
            elif i==2: master_pick=posx(-407.08, 419.65, -38.49, 150.1, -179.94, -50.44)#3번 메인유닛
            elif i==3: master_pick=posx(-406.08, 499.34, -38.49, 150.15, -179.94, -50.39)#4번 메인유닛
            elif i==4: master_pick=posx(-349.07, 258.72, -38.47, 149.99, -179.94, -50.54)#5번 메인유닛
            elif i==5: master_pick=posx(-348.07, 338.72, -38.47, 149.99, -179.94, -50.54)#6번 메인유닛
            elif i==6: master_pick=posx(-347.07, 418.72, -38.47, 149.99, -179.94, -50.54)#7번 메인유닛
            elif i==7: master_pick=posx(-346.07, 498.72, -38.47, 149.99, -179.94, -50.54)#8번 메인유닛
           
            movel(trans(master_pick,[0,0,50,0,0,0]))
            movel(master_pick)
            Grip()
            movel(trans(master_pick,[0,0,200,0,0,0]))
            
            movel(posx(-82.05, 513.07, 162.01, 150.44, -179.93, -50.1))#메인유닛 공급app
            movel(posx(-82.05, 513.07, 72.01, 150.44, -179.93, -50.1))#메인유닛 공급place
            Release()
            movel(posx(-82.05, 513.07, 162.01, 150.44, -179.93, -50.1))#UP
            set_output_register_bit(14,ON)
            while(1):
                if get_input_register_bit(14)==1:
                    set_output_register_bit(14,OFF)
                    break
                wait(0.1)
            set_output_register_bit(14,OFF)
            movel(posx(-82.05, 343.07, 162.01, 150.44, -179.93, -50.1))#app
        
        
        
        elif step==41 : #M2 볼트 상부위치로 이동
            movej(posj(-189.86, -8.5, -87.28, 0.05, -83.84, 149.47))
            
        elif step==42 : #M2 볼트 체결 시작(핸드 커버 체결)
        
            for loop in range(3):
                value=get_input_register_int(6)
                value=bin(value)#2진수로 변환
                value=value[::-1]#문자열 거꾸로 뒤집기
                if "1" in value:
                    i=value.index("1")
                else:
                    value=get_input_register_int(7)
                    value=bin(value)#2진수로 변환
                    value=value[::-1]#문자열 거꾸로 뒤집기
                    i=value.index("1")
                    i+=31
                    
                if i==0: master_pick=posx(384.17, -206.47, 5.8, 161.64, -180, 140.98)
                elif i==1: master_pick=posx(384.58, -190.47, 5.8, 163.8, 180, 143.14)
                elif i==2: master_pick=posx(384.58, -174.47, 5.8, 163.8, 180, 143.14)
                elif i==3: master_pick=posx(385.12, -158.53, 5.77, 168.27, 180, 147.61)
                elif i==4: master_pick=posx(385.12, -142.53, 5.77, 168.27, 180, 147.61)
                elif i==5: master_pick=posx(385.12, -126.53, 5.77, 168.27, 180, 147.61)
                
                elif i==6: master_pick=posx(399.12, -206.53, 5.77, 168.27, 180, 147.61)
                elif i==7: master_pick=posx(399.32, -190.53, 5.77, 168.27, 180, 147.61)
                elif i==8: master_pick=posx(399.52, -174.53, 5.77, 168.27, 180, 147.61)
                elif i==9: master_pick=posx(399.72, -158.53, 5.77, 168.27, 180, 147.61)
                elif i==10: master_pick=posx(399.92, -142.53, 5.77, 168.27, 180, 147.61)
                elif i==11: master_pick=posx(400.12, -126.53, 5.77, 168.27, 180, 147.61)
                
                elif i==12: master_pick=posx(414.2, -207.12, 5.77, 162.8, 180, 142.14)
                elif i==13: master_pick=posx(414.4, -191.12, 5.77, 162.8, 180, 142.14)
                elif i==14: master_pick=posx(414.6, -175.12, 5.77, 162.8, 180, 142.14)
                elif i==15: master_pick=posx(414.8, -159.12, 5.77, 162.8, 180, 142.14)
                elif i==16: master_pick=posx(415.0, -143.12, 5.77, 162.8, 180, 142.14)
                elif i==17: master_pick=posx(415.2, -127.12, 5.77, 162.8, 180, 142.14)
                
                elif i==18: master_pick=posx(429.2, -207.3, 5.77, 163.34, -180, 142.68)
                elif i==19: master_pick=posx(429.4, -191.3, 5.77, 163.34, -180, 142.68)
                elif i==20: master_pick=posx(429.6, -175.3, 5.77, 163.34, -180, 142.68)
                elif i==21: master_pick=posx(429.8, -159.3, 5.77, 163.34, -180, 142.68)
                elif i==22: master_pick=posx(430.0, -143.3, 5.77, 163.34, -180, 142.68)
                elif i==23: master_pick=posx(430.2, -127.3, 5.77, 163.34, -180, 142.68)
                
                elif i==24: master_pick=posx(444.2, -207.49, 5.77, 163.85, 180, 143.19)
                elif i==25: master_pick=posx(444.4, -191.49, 5.77, 163.85, 180, 143.19)
                elif i==26: master_pick=posx(444.6, -175.49, 5.77, 163.85, 180, 143.19)
                elif i==27: master_pick=posx(444.8, -159.49, 5.77, 163.85, 180, 143.19)
                elif i==28: master_pick=posx(445.0, -143.49, 5.77, 163.85, 180, 143.19)
                elif i==29: master_pick=posx(445.2, -127.49, 5.77, 163.85, 180, 143.19)
                
                elif i==30: master_pick=posx(459.2, -207.59, 6, 164.34, 180, 143.68)
                elif i==31: master_pick=posx(459.4, -191.59, 6, 164.34, 180, 143.68)
                elif i==32: master_pick=posx(459.6, -175.59, 6, 164.34, 180, 143.68)
                elif i==33: master_pick=posx(459.8, -159.59, 6, 164.34, 180, 143.68)
                elif i==34: master_pick=posx(460.0, -143.59, 6, 164.34, 180, 143.68)
                elif i==35: master_pick=posx(460.2, -127.59, 6, 164.34, 180, 143.68)
                
                elif i==36: master_pick=posx(474.2, -207.84, 6, 164.78, 180, 144.12)
                elif i==37: master_pick=posx(474.4, -191.84, 6, 164.78, 180, 144.12)
                elif i==38: master_pick=posx(474.6, -175.84, 6, 164.78, 180, 144.12)
                elif i==39: master_pick=posx(474.8, -159.84, 6, 164.78, 180, 144.12)
                elif i==40: master_pick=posx(475.0, -143.84, 6, 164.78, 180, 144.12)
                elif i==41: master_pick=posx(475.2, -127.84, 6, 164.78, 180, 144.12)
                
                
                movej(posj(-189.86, -8.5, -87.28, 0.05, -83.84, 149.47))#M2 볼트 상부위치로 이동
                movel(trans(master_pick,[0,0,100,0,0,0]))#app
                movel(master_pick)#pick
                set_digital_output(12)
                #wait_digital_input(12,ON)
                set_digital_output(-12)
                movel(trans(master_pick,[0,0,100,0,0,0]))#UP
                
                movej(posj(-69.22, -11.8, -79.85, 0, -88.35, 167.49))#app
                
                if loop==0: Bolting_point=posx(-89.09, 451.61, 137.42, 100.22, -179.95, -23.07)#bloting_1point
                elif loop==1: Bolting_point=posx(-70.81, 457.06, 136.67, 100.5, -179.95, -22.78)#bloting_2point
                elif loop==2: Bolting_point=posx(-65.31, 451.64, 136.52, 100.57, -179.95, -22.71)#bloting_3point
                
                movel(trans(Bolting_point,[0,0,30,0,0,0]))#app
                movel(trans(Bolting_point,[0,0,10,0,0,0]))#Down(감속구간)
                wait_digital_input(7,ON)
                set_digital_output(6)
                wait_digital_input(7,OFF)
                amovel(Bolting_point,2,2)
                #wait_digital_input(6,ON)
                stop(DR_SSTOP)
                set_digital_output(13)
                wait(0.3)
                set_digital_output(-13)
                set_digital_output(-6)
                movel(trans(Bolting_point,[0,0,30,0,0,0]))#UP
                movej(posj(-69.22, -11.8, -79.85, 0, -88.35, 167.49))#app
                
                set_output_register_bit(43,ON)
                wait(0.3)
                set_output_register_bit(43,OFF)
                
            
            
            
        elif step==44 : #메인 유닛 케이스 이동작업 시작
        
            set_output_register_bit(15,ON)
            while(1):
                if get_input_register_bit(15)==1:
                    set_output_register_bit(15,OFF)
                    break
        
            movej(posj(-78.39, -11.54, -82.31, -0.05, -86.2, 81.08))#app
            movel(posx(-82.05, 513.07, 72.01, 150.44, -179.93, -50.1))#메인유닛 pick
            Grip()
            movel(posx(-82.05, 513.07, 162.01, 150.44, -179.93, -50.1))#UP
            
            value=get_input_register_int(8)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            if i==0:master_place=posx(314.85, 366.32, -28.7, 140.51, -179.93, 28.88)#1번
            elif i==1:master_place=posx(316.19, 448.67, -28.7, 140.51, -179.93, 29.42)#2번
            elif i==2:master_place=posx(316.9, 532.4, -28.7, 140.63, -179.93, 29.54)#3번
            elif i==3:master_place=posx(317.68, 615.33, -28.71, 140.57, -179.93, 30.12)#4번
            elif i==4:master_place=posx(404.75, 364.85, -28.7, 140.6, -179.93, 29.25)#5번
            elif i==5:master_place=posx(405.75, 448.55, -28.7, 140.6, -179.93, 29.25)#6번
            elif i==6:master_place=posx(406.45, 532, -28.7, 140.6, -179.93, 29.25)#7번
            elif i==7:master_place=posx(407, 615.0, -28.7, 140.35, -179.93, 29)#8번
            
            
            
            movel(trans(master_place,[0,0,80,0,0,0]))#app
            movel(trans(master_place,[0,0,10,0,0,0]))#Down(감속 구간)
            movel(master_place,3,3)#place
            Release()
            movel(trans(master_place,[0,0,80,0,0,0]))#UP
            movej(posj(-131.24, 0.51, -92.43, -0.07, -88.08, 118.31))
            
            
            
        elif step==45 : #탑 커버 상부위치로 이동
            movej(posj(33.76, -24.4, -75.1, 0.13, -80.64, 193.39))
            
        elif step==46 : #탑 커버 공급 시작
            value=get_input_register_int(1)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            if i==0: master_pick=posx(-533.29, -382.87, -41, 38.35, 179.99, 160.06)#1번
            elif i==1: master_pick=posx(-532, -282.79, -41.2, 39.31, 179.99, 161.02)#2번
            elif i==2: master_pick=posx(-530.7, -182.74, -41, 28.92, 179.97, 150.64)#3번
            elif i==3: master_pick=posx(-529.42, -82.73, -41.5, 28.84, 179.97, 150.56)#4번
            elif i==4: master_pick=posx(-434, -384.5, -41.5, 38.16, 179.99, 159.87)#5번
            elif i==5: master_pick=posx(-432.6, -284.5, -41.5, 38.25, 179.99, 159.96)#6번
            elif i==6: master_pick=posx(-431, -184.5, -41.5, 38.34, 179.99, 160.05)#7번
            elif i==7: master_pick=posx(-429, -84.5, -41.5, 38.5, 179.99, 160.21)#8번
            
            movel(trans(master_pick,[0,0,100,0,0,0]))#app
            
            set_digital_outputs([-1,-2])
            set_digital_output(1)
            set_digital_output(-1)
            
            movel(master_pick)#pick
            set_digital_output(12)
            wait_digital_input(12,ON)
            set_digital_output(-12)
            movel(trans(master_pick,[0,0,160,0,0,0]))#UP
            
            movej(posj(0, 0, -90, 0, -90, 159.84))#app
            
            
            
            movej(posj(-124.94, -15.82, -71.58, 0, -92.6, 173.45))#탑커버 공급 대기위치 
            
            value=get_input_register_int(8)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            if i==0: master_place=posx(281.17, 312.18, -1.68, 53.45, -179.98, -5.73)#1번
            elif i==1: master_place=posx(281.15, 396.1, 1.37, 54.28, -179.98, -4.9)#2번 
            elif i==2: master_place=posx(283.22, 480.27, 4.13, 56.7, -179.97, -2.48)#3번
            elif i==3: master_place=posx(286.77, 564.88, 1.55, 56.39, -179.97, -2.79)#4번
            elif i==4: master_place=posx(368.62, 311.71, 1.5, 51.5, -179.97, -7.68)#5번
            elif i==5: master_place=posx(370.76, 395.38, 1.49, 51.41, -179.97, -7.77)#6번
            elif i==6: master_place=posx(371.98, 478.89, 1.47, 51.82, -179.97, -7.36)#7번
            elif i==7: master_place=posx(371.94, 562.61, 1.45, 51.85, -179.97, -7.33)#8번
            
            movel(trans(master_place,[0,0,50,0,0,0]))#app
            movel(master_place)#place
            set_digital_output(13)
            wait(0.3)
            set_digital_output(-13)
            movel(trans(master_place,[0,0,100,0,0,0]))#UP
            Release()
            movej(posj(-124.94, -15.82, -71.58, 0, -92.6, 173.45))#탑커버 공급 대기위치 
            
        elif step==63: #Homing
            move_home(DR_HOME_TARGET_USER)
            
            
            
            
        set_output_register_bit(step,ON) #작업 완료 신호[전달]
        
        while(True):
            if get_input_register_bit(step) == 0:
                set_output_register_bit(step,OFF)
                break
           
            wait(0.1)
            
    
