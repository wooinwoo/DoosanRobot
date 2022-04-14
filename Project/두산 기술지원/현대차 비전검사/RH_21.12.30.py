#ip : 192.168.0.121
drl_report_line(1)

########## 초기 세팅 값 ##########

#전역 조인트 스피드를 설정합니다.
set_velj(80)
set_accj(20)
#전역 태스크 스피드를 설정합니다.
set_velx(30,20)
set_accx(60,30)



#툴을 등록합니다.
set_tool("weight_RH")


#모든 신호를 초기화합니다.
def signal_reset(): 
    drl_report_line(0)
    set_output_register_bit(0,OFF)
    set_output_register_bit(1,OFF)
    set_output_register_bit(2,OFF)
    set_output_register_bit(3,OFF)
    set_output_register_bit(4,OFF)
    set_output_register_bit(5,OFF)
    set_output_register_bit(6,OFF)
    set_output_register_bit(7,OFF)
    set_output_register_bit(8,OFF)
    set_output_register_bit(9,OFF)
    set_output_register_bit(10,OFF)
    set_output_register_bit(11,OFF)
    set_output_register_int(0,0)
    set_output_register_int(1,0)
    set_digital_outputs(bit_start=1, bit_end=16, val=0b0000 0000 0000 000)
    drl_report_line(1)
    
def vision():
    wait(1)#로봇 떨림 대기 시간
    set_output_register_bit(1,ON) #비전 요청
    while(1):
        if get_input_register_bit(1)==1: break #비전 완료
    #wait(0.1)
    set_output_register_bit(1,OFF)
#def Emergency_Stop():
    #if get_input_register_bit(0)==1:
        #exit()
    #


#th_id = thread_run(Emergency_Stop, loop=True)


home_P=posj(-90.01, 42.41, -109.24, -1.38, -48.82, 91.01)
signal_reset()
while(1):

    #B=get_input_register_int(2) 차종 정보 획득

    while(1):
        #if get_input_register_bit(4)==1:#홈위치 요청
        ##
        ##서브마다 회피 추가
        #if
        #elif
        #elif
        #move_home(DR_HOME_TARGET_USER)
        #signal_reset() #신호 초기화
        set_output_register_bit(0,ON)#홈위치 완료
        set_output_register_bit(5,ON)#작업 준비 완료
        set_output_register_bit(2,ON)#불간섭 신호 전달
        break
        
    
    while(1):
        if get_input_register_bit(5)==1: break
        wait(0.1)
    set_output_register_bit(8,OFF)
    
    
    ######## main program #########
    
    
    for step in range(1,15):
        tp_log("step : {}".format(step))
    

        """ 로봇 상호 인터록
        if step==1: value=19 #LH 뒷판넬 작업 중
        if step==8: value=17 #LH 본넷 작업 중
        if 8<step<14: value=18 #LH 루프 작업 중
        while(True):
            if get_intput_register_bit(value)==0: break
        """
        
        
        
        
        
        
        
        set_output_register_int(1,step)#서보 위치 요청 정보
        set_output_register_bit(3,ON)#서보 이동 요청
        

        list0=[]
        while(1):
            #if  get_input_register_bit(2)==0 and 1 not in list : list.append(1)  #불간섭 신호
            if  get_input_register_bit(3)==1 and 1 not in list0 :  list0.append(1) # 서보 완료
            if  get_input_register_int(1)==step and 2 not in list0 :  list0.append(2) #현재 서보 위치 
            wait(0.1)
            if 1 in list0 and 2 in list0 : break
        tp_log("return: {}".format(step))
        
        signal_reset() #신호 초기화
        
        
        # step 1 = 뒷판넬
        # step 2~7 = 사이드
        # step 8 = 본넷
        # step 9~13 = 루프
        # step 14 = 사이드(반대)
        
        """ 로봇 상호 인터록
        if step==1: 
            set_output_register_bit(19,ON) # RH 뒷판넬 작업 중
            set_output_register_bit(17,OFF)
            set_output_register_bit(18,OFF)
        if step==8: 
            set_output_register_bit(17,ON) # RH 본넷 작업 중
            set_output_register_bit(18,OFF)
            set_output_register_bit(19,OFF)
        if 8<step<14: 
            set_output_register_bit(18,ON) # RH 루프 작업 중
            set_output_register_bit(17,OFF)
            set_output_register_bit(19,OFF)
        """
        
        set_output_register_bit(6,ON)#로봇 작업 중 전달
        if step==1: #rear_0_0
            movej(Global_sub7_app)
            movej(Global_sub7_p1)
            vision()
            movej(Global_sub7_p2)
            vision()
            movej(Global_sub7_app)
            movej(home_P)
            
        elif step==2: #side_0_0
            movej(Global_side_app)
            movej(Global_sub8_p1)
            vision()
            movej(Global_sub8_p2)
            vision()
            movej(Global_sub8_p3)
            vision()
            #movej(Global_sub8_app)
            #movej(home_P)
            
        elif step==3: #side_350_0
            #movej(Global_side_app)
            movej(Global_sub9_p1)
            vision()
            movej(Global_sub9_p2)
            vision()
            movej(Global_sub9_p3)
            vision()
            movej(Global_sub9_p4)
            vision()
            movej(Global_sub9_p5)
            vision()
            movej(Global_sub9_p6)
            vision()
            #movej(Global_side_app)
            #movej(home_P)
            
        elif step==4: #side_900_0
            #movej(Global_side_app)
            movej(Global_sub10_p1)
            vision()
            movej(Global_sub10_p2)
            vision()
            movej(Global_sub10_p3)
            vision()
            movej(Global_sub10_p4)
            vision()
            movej(Global_sub10_p5)
            vision()
            movej(Global_sub10_p6)
            vision()
            #movej(Global_side_app)
            #movej(home_P)
            
        elif step==5: #_side_1399_0
            #movej(Global_side_app)
            movej(Global_sub11_p1)
            vision()
            movej(Global_sub11_p2)
            vision()
            movej(Global_sub11_p3)
            vision()
            #movej(Global_side_app)
            #movej(home_P)
            
        elif step==6: #_side_2300_0
            #movej(Global_side_app)
            movej(Global_sub12_p1)
            vision()
            movej(Global_sub12_p2)
            vision()
            movej(Global_sub12_p3)
            vision()
            movej(Global_sub12_p4)
            vision()
            movej(Global_sub12_p5)
            vision()
            movej(Global_sub12_p6)
            vision()
            movej(Global_sub12_p7)
            vision()
            #movej(Global_side_app)
            #movej(home_P)
            movej(Global_sub13_app)
            
        elif step==7: #_side_3204_0
            #movej(Global_side_app)
            movej(Global_sub13_p1)
            vision()
            movej(Global_sub13_p2)
            vision()
            #movej(Global_side_app)
            movej(home_P)
            
        elif step==8: #front_4400_0
            movej(Global_sub1_p1)
            vision()
            movej(Global_sub1_p2)
            vision()
            movej(Global_sub1_p3)
            vision()
            movej(Global_sub1_p4)
            vision()
            movej(Global_sub1_p5)
            vision()
            movej(Global_sub1_p6)
            vision()
            movej(Global_sub1_p7)
            vision()
            movej(Global_sub1_p8)
            vision()
            movej(Global_sub1_p9)
            vision()
            movej(Global_sub1_p10)
            vision()
            movej(Global_sub1_p11)
            vision()
            movej(Global_sub1_p12)
            vision()
            movej(Global_sub1_p13)
            vision()
            movej(home_P)
        elif step==9: #top_2823_300
            movej(Global_sub2_p1)
            vision()
            movej(Global_sub2_p2)
            vision()
            movej(Global_sub2_p3)
            vision()
            movej(Global_sub2_p4)
            vision()
            movej(Global_sub2_p5)
            vision()
            movej(Global_sub2_p6)
            vision()
            #movej(home_P)
            
        elif step==10: #top_2586_300
            movej(Global_sub3_p1)
            vision()
            #movej(home_P)
            
        elif step==11: #top_1928_300
            movej(Global_sub4_p1)
            vision()
            movej(Global_sub4_p2)
            vision()
            movej(Global_sub4_p3)
            vision()
            movej(Global_sub4_p4)
            vision()
            movej(Global_sub4_p5)
            vision()
            #movej(home_P)
        elif step==12: #top_1560_300
            movej(Global_sub5_p1)
            vision()
            movej(Global_sub5_p2)
            vision()
            movej(Global_sub5_p3)
            vision()
            movej(Global_sub5_p4)
            vision()
            movej(Global_sub5_p5)
            vision()
            movej(Global_sub5_p6)
            vision()
            #movej(home_P)
        elif step==13: #top_1360_300
            movej(Global_sub6_p1)
            vision()
            movej(Global_sub6_p2)
            vision()
            movej(Global_sub6_p3)
            vision()
            movej(Global_sub6_p4)
            vision()
            movej(home_P)
        elif step==14: #opposite side_1210_0
            movej(Global_sub14_app)
            movej(Global_sub14_p1)
            vision()
            movej(Global_sub14_p2)
            vision()
            movej(Global_sub14_app)
            movej(home_P)
        
        
        
        
        
        set_output_register_bit(2,ON)#불간섭 신호 전달
        set_output_register_int(0,step)
        set_output_register_bit(7,ON) # 작업완료신호 전달
        wait(0.5)
        set_output_register_bit(7,OFF)
        set_output_register_bit(6,OFF)
        tp_log("작업완료 : {}".format(step))
        
    signal_reset()
    set_output_register_bit(8,ON)
