
drl_report_line(1)




########## 초기 세팅 값 ##########

#전역 조인트 스피드를 설정합니다.
set_velj(10)
set_accj(20)
#전역 태스크 스피드를 설정합니다.
set_velx(30,20)
set_accx(60,30)


#TCP를 등록합니다.
set_tcp("공압그리퍼")
#툴을 등록합니다.
set_tool("Tool Weight_grip")
#set_tool("Tool Weight_Driver")



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

########## 함수 ##########
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
    set_digital_outputs(bit_start=1, bit_end=15, val=0b000000000000000)

    drl_report_line(1)
    
def Handle_Grip():
    set_digital_outputs([-1,-2]) #신호 초기화
    set_digital_output(1)#그립 신호 ON
    wait(1.5)
    wait_digital_input(1,ON)#그립완료신호 대기
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
    if Task_space_point[2]<180:
        Height=180-Task_space_point[2]
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
            movej(posj(-90, 0, 90, 0, 90, 160))# 정면 안전 위치
            
        elif step==33 : #후면 안전위치 이동
            movej(posj(-270, 0, 90, 0, 90, -20))# 후면 안전위치
            
        elif step==34 : #툴 체인지 준비위치 이동
            movej(posj(-13.74, -21.83, 94.86, 0, 106.98, 236.45))
            
        elif step==35 : #Tool 미부착 상태에서 Grip Tool Pick
            a=1
            
        elif step==36 : #Tool 미부착 상태에서 Driver Tool Pick
            a=1
            
        elif step==37 : #그립 툴 체인지 동작시작
            movel(posx(297.66, -168.65, 357.59, 175.33, 180, 64.65))#via
            movel(posx(431.67, -169.21, 357.59, 165.95, 179.99, 55.27))#app
            movel(posx(431.67, -169.21, 332.08, 165.95, 179.99, 55.27))#Driver place
            set_tool("Tool Weight")
            set_digital_output(-16)
            set_digital_output(10)
            movel(posx(432.44, -168.71, 350, 177.47, 180, 66.78))#UP
            set_digital_output(-10)
            movel(posx(432.44, 60.78, 350, 11.27, -179.99, -98.53))#app1
            movel(posx(465.04, 60.78, 350, 11.27, -179.99, -98.53))#app2
            movel(posx(465.04, 60.81, 322.05, 6.69, -180, -103.12))#grip pick
            set_tool("Tool Weight_grip")
            set_digital_output(9)
            movel(posx(465.04, 60.78, 328.01, 11.27, -179.99, -98.53))#UP
            set_digital_output(-9)
            movel(posx(367.64, 60.76, 327.91, 10.4, -179.99, -99.4))#via
            movej(posj(-11.26, -15.98, 91.2, 0, 104.78, 238.93))# 준비위치이동
            set_output_register_bit(20,OFF) #현재 툴 상태 Grip
            set_output_register_bit(19,ON) #현재 툴 상태 Grip
            
        elif step==38 : #드라이버 툴 체인지 동작시작
        
            
            movel(posx(367.64, 60.76, 327.91, 10.4, -179.99, -99.4))#via
            movel(posx(465.04, 60.78, 328.01, 11.27, -179.99, -98.53))#app
            movel(posx(465.04, 60.81, 322.05, 6.69, -180, -103.12))#grip place
            set_tool("Tool Weight")
            set_digital_output(10)
            movel(posx(465.04, 60.78, 350, 11.27, -179.99, -98.53))#UP
            set_digital_output(-10)
            movel(posx(432.44, 60.78, 350, 11.27, -179.99, -98.53))#app1
            movel(posx(431.67, -169.21, 350, 165.95, 179.99, 55.27))#app2
            movel(posx(431.67, -169.21, 332.08, 165.95, 179.99, 55.27))#Driver pick
            set_tool("Tool Weight_Driver")
            set_digital_output(16)
            set_digital_output(9)
            movel(posx(432.44, -168.71, 357.65, 177.47, 180, 66.78))#UP
            set_digital_output(-9)
            movel(posx(297.66, -168.65, 357.59, 175.33, 180, 64.65))#app
            movej(posj(-11.26, -15.98, 91.2, 0, 104.78, 238.93))# 준비위치이동
            
            set_output_register_bit(19,OFF)
            set_output_register_bit(20,ON) #현재 툴 상태 Driver
            
        elif step==47 : #Handle 상부위치로 이동
            movej(posj(-258.05, 1.55, 93.97, 0, 84.49, -8.05))
        elif step==48 : #Handle 공급 시작            
            value=get_input_register_int(3)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            if i==0: master_pick=posx(-199.82, 440.6, 15.15, 103.93, -179.98, -6.07)#1번
            elif i==1: master_pick=posx(-169.82, 440.3, 15.15, 103.99, -179.98, -6.01)#2번
            elif i==2: master_pick=posx(-139.83, 440, 15.15, 95.48, -179.99, -14.52)#3번
            elif i==3: master_pick=posx(-109.83, 439.7, 15.15, 95.38, -179.99, -14.62)#4번
            elif i==4: master_pick=posx(-79.83, 439.4, 15.15, 95.26, -179.99, -14.74)#5번
            elif i==5: master_pick=posx(-49.83, 439.1, 15.15, 94.85, -179.99, -15.15)#6번
            elif i==6: master_pick=posx(-19.67, 438.8, 15.15, 95.24, -179.99, -14.76)#7번
            elif i==7: master_pick=posx(10.63, 438.5, 15.15, 95.65, -179.99, -14.35)#8번
            
            movel(trans(master_pick,[0,0,150,0,0,0]))#app
            movel(master_pick)#pick
            Handle_Grip() #그립
            movel(trans(master_pick,[0,0,150,0,0,0]))#UP
            
            movej(posj(-193.81, 2.73, 92.93, 5.18, 85.62, -127.89))#app
                        
            movel(posx(-546.41, 49.18, 200, 90.07, -174.68, 156.44))#app
            movel(posx(-546.41, 49.18, 146.5, 90.07, -174.68, 156.44))#place
            Release() #그립 해제
            movel(posx(-546.41, 49.18, 200, 90.07, -174.68, 156.44))#UP
            movej(posj(-193.81, 2.73, 92.93, 5.18, 85.62, -127.89))#app
            
        elif step==49 : #Handle Cover 상부위치로 이동
            movej(posj(-308.54, 11.07, 82.89, 0, 86.06, -59.35))
            
        elif step==50 : #Handle Cover 공급 시작 
            value=get_input_register_int(4)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            if i==0: master_pick= posx(273.16, 402.65, 18.47, 58.98, -179.98, -51.83)#1번
            elif i==1: master_pick=posx(343.45, 402.15, 18.47, 58.89, -179.98, -51.92)#2번
            elif i==2: master_pick=posx(273.16, 377.65, 18.47, 59.02, -179.98, -51.79)#2번
            elif i==3: master_pick=posx(343.05, 377.05, 18.46, 58.83, -179.98, -51.98)#2번
            elif i==4: master_pick=posx(272.96, 352.65, 18.47, 58.82, -179.98, -51.99)#2번
            elif i==5: master_pick=posx(342.86, 351.95, 18.47, 58.88, -179.98, -51.93)#2번
            elif i==6: master_pick=posx(272.76, 327.65, 18.47, 59.1, -179.98, -51.71)#2번
            elif i==7: master_pick=posx(342.56, 326.95, 18.47, 58.89, -179.98, -51.92)#2번
                
            movel(trans(master_pick,[0,0,150,0,0,0]))#app
            movel(master_pick)#pick
            set_digital_output(12)
            wait_digital_input(12,ON)
            set_digital_output(-12)
            movel(trans(master_pick,[0,0,150,0,0,0]))#UP
            
            movej(posj(-189.81, 2, 93.49, 0, 84.51, -29.08))#app
            
            
            movel(posx(-533.53, 79.09, 200, 175.97, -179.99, -23.3))#app
            movel(posx(-533.53, 79.09, 161, 175.97, -179.99, -23.3))#Down(감속구간)
            movel(posx(-533.53, 79.09, 151, 175.97, -179.99, -23.3),3,3)#place
            set_digital_output(13)
            wait(0.3)
            set_digital_output(-13)
            movel(posx(-533.53, 79.09, 200, 175.97, -179.99, -23.3))#UP
            
            movej(posj(-189.81, 2, 93.49, 0, 84.51, -29.08))#app

            
        elif step==51 : #Note 상부위치로 이동
            movej(posj(-315.69, 18.1, 73.88, 0, 88.04, -66.5))
            
        elif step==52 : #Note 공급 시작            
            value=get_input_register_int(4)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            #if i==0: master_pick=
            #elif i==1: master_pick=
            #elif i==2: master_pick=
            #elif i==3: master_pick=
            #elif i==4: master_pick=
            #elif i==5: master_pick=
            #elif i==6: master_pick=
            #elif i==7: master_pick=
            
            #movel(trans(master_pick,[0,0,150,0,0,0]))#app
            #movel(master_pick)#pick
            #Grip()
            #movel(trans(master_pick,[0,0,150,0,0,0]))#UP
            
            movej(posj(-189.81, 2, 93.49, 0, 84.51, 57.77))#app
            
            #movel()#app
            #movel()#place
            #Release()
            #movel()#UP
            
            
        elif step==53 : #M3 Feeder 상부위치로 이동
            movej(posj(-66.55, 13.57, 74.67, 0, 91.77, 183.45))#상부위치 이동
        
        elif step==54 : #M3 Bolt 체결 시작(Note 체결)
            set_tcp("공압그리퍼_Driver")
            
            Bolting_Point_1=posx(-569.73, 117.57, 136.37, 166.49, -179.99, -122.19)#1번 체결
            Bolting_Point_2=posx(-560.84, 120.85, 136.37, 165.89, -179.99, -122.79)#2번 체결
            for loop in range(2):
                
                
                movej(posj(-66.55, 13.57, 74.67, 0, 91.77, 183.45),r=0)#상부위치 이동 #r=0 블랜딩 방지
                movel(posx(314, -421.66, 182.79, 118.46, 179.99, 8.46))#app
                wait_digital_input(9,ON)
                movel(posx(314, -421.66, 101.79, 118.46, 179.99, 8.46))#M3 Bolt pick
                set_digital_output(12)
                wait_digital_input(12,ON)
                set_digital_output(-12)
                movel(posx(314, -421.66, 182.79, 118.46, 179.99, 8.46))#UP
                movej(posj(-192.42, 16.4, 72.4, 0, 91.21, 238.9))#app1
                
                
                if loop==0: Bolting_Point=Bolting_Point_1
                if loop==1: Bolting_Point=Bolting_Point_2
                
                
                movel(trans(Bolting_Point,[0,0,50,0,0,0,]))#app
                movel(trans(Bolting_Point,[0,0,8,0,0,0,]))#Down(감속)
                wait_digital_input(7,ON)
                set_digital_output(6)
                wait_digital_input(7,OFF)
                amovel(Bolting_Point,1,1)#볼트 체결
                wait_digital_input(6,ON)
                stop(DR_SSTOP)
                movel(trans(Bolting_Point,[0,0,50,0,0,0,]))#UP
                set_digital_output(13)
                wait(0.3)
                set_digital_output(-13)
                set_digital_output(-6)
                

            movej(posj(-194.33, 7.32, 83.58, 0, 89.11, 236.99))#app1
            set_tcp("공압그리퍼")
            
                    
        elif step==55 : #M3 Bolt 체결 시작(Case 체결)
            set_tcp("공압그리퍼_Driver")
            
            value=get_input_register_int(9)
            value=bin(value)#2진수로 변환
            value=value[::-1]#문자열 거꾸로 뒤집기
            i=value.index("1")
            
            if i==0:
                Bolting_Point_1=posx(-623.22, -216.7, 24, 27.98, 179.96, 32.37) #1번 case
                Bolting_Point_2=posx(-650.69, -233.64, 24, 1.79, -179.95, 6.18)
            elif i==1:
                Bolting_Point_1=posx(-539.15, -217.52, 24, 16.11, 180, 20.19) #2번 case
                Bolting_Point_2=posx(-566.53, -234.23, 24, 16.97, 180, 21.05)
            elif i==2:
                Bolting_Point_1=posx(-455.76, -218.31, 24, 99.98, 180, 104.06) #3번 case
                Bolting_Point_2=posx(-483.05, -235.44, 24, 133.5, 180, 137.58)
            elif i==3:
                Bolting_Point_1=posx(-371.69, -219.21, 24, 119.44, 180, 123.52) #4번 case
                Bolting_Point_2=posx(-399.35, -236.43, 24, 110.59, 180, 114.67)
            elif i==4:
                Bolting_Point_1=posx(-624.22, -306.35, 24, 118.93, 180, 123.01) #5번 case
                Bolting_Point_2=posx(-651.46, -323.6, 24, 118.07, 180, 122.15)
            elif i==5:
                Bolting_Point_1=posx(-540.1, -307.35, 24, 24.9, -180, 28.98) #6번 case
                Bolting_Point_2=posx(-567.66, -324.77, 24, 25.31, -180, 29.38)
            elif i==6:
                Bolting_Point_1=posx(-456.16, -308.32, 24, 29.15, -180, 33.22) #7번 case
                Bolting_Point_2=posx(-483.6, -325.16, 24, 29.3, -180, 33.37)
            elif i==7:
                Bolting_Point_1=posx(-372.37, -308.85, 24, 34.8, -180, 38.88) #8번 case
                Bolting_Point_2=posx(-400.15, -326.28, 24, 34.61, -180, 38.68)
        
            for loop in range(2):
            
            
                movel(posx(314, -421.66, 182.79, 118.46, 179.99, 8.46))#app
                wait_digital_input(9,ON)
                movel(posx(314, -421.66, 101.79, 118.46, 179.99, 8.46))#M3 Bolt pick
                set_digital_output(12)
                set_digital_output(-12)
                movel(posx(314, -421.66, 182.79, 118.46, 179.99, 8.46))#UP
                movej(posj(-139.56, -5.06, 94.07, 0, 90.99, 224.51))#app1
                
                #1
                if loop==0: Bolting_Point=Bolting_Point_2
                if loop==1: Bolting_Point=Bolting_Point_1
                
                movel(trans(Bolting_Point,[0,0,100,0,0,0,]))#app
                movel(trans(Bolting_Point,[0,0,8,0,0,0,]))#Down(감속)
                wait_digital_input(7,ON)
                set_digital_output(6)
                wait_digital_input(7,OFF)
                amovel(Bolting_Point,1,1)#볼트 체결
                wait_digital_input(6,ON)
                stop(DR_SSTOP)
                movel(trans(Bolting_Point,[0,0,100,0,0,0,]))#UP
                set_digital_output(13)
                wait(0.3)
                set_digital_output(-13)
                set_digital_output(-6)
                movej(posj(-139.56, -5.06, 94.07, 0, 90.99, 224.51))#app
                
                
    
            set_tcp("공압그리퍼")
                   

        elif step==56 : #오르골 TEST 시작
            movej(posj(-181.71, 0, 90, 0, 90, 160))#app
            M_Box=posx(-549.27, 40.39, 140.15, 2.87, 179.99, 71.48)
            
            movel(trans(M_Box,[0,0,60,0,0,0]))
            Release()#그립 해제
            movel(M_Box)    
            Handle_Grip()#그립
            
            p1=trans(M_Box,[10,0,-10,0,0,0])
            p2=trans(M_Box,[0,0,-20,0,0,0])
            p3=trans(M_Box,[-10,0,-10,0,0,0])
            p4=trans(M_Box,[0,0,0,0,0,0])
            for loop in range(5): # 5회 반복
                movec(p1, p2, vel=20, acc=60)
                movec(p3, p4, vel=20, acc=60)
            
            Release()#그립 해제
            movel(trans(M_Box,[0,0,60,0,0,0]))#UP
            movej(posj(-181.71, 0, 90, 0, 90, 160))#app
            
        elif step==63: #Homing
            move_home(DR_HOME_TARGET_USER)
                


        
        
        set_output_register_bit(step,ON) #작업 완료 신호[전달]
        
        while(True):
            if get_input_register_bit(step) == 0:
                set_output_register_bit(step,OFF)
                break
           
            wait(0.1)
            
    
