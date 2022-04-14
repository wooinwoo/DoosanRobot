# plc ip   : 192.168.###.###
#robot ip : 192.168.###.###
def signal_reset():
    set_digital_outputs([-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16])
######################################################################

def sig_send(num):
    range=[-1,-2,-3,-4,-5,-6,-7,-8]
    num=bin(num); c=0
    for i in reversed(num):
        if i=="1": range[c]*=-1
        c+=1
    set_tool_digital_outputs(range)
    set_tool_digital_outputs(9); wait(0.5)
    set_tool_digital_outputs(-9)
    
######################################################################

def sig_conversion(n):
    value=0
    range=[1,2,4,8,16,32,64,128]
    for i in range(len(n)):
        if n[i]==1: value+=range[i]
    return value

######################################################################

def Grip():
    sig_send(num)
    set_tool_digital_outputs([-1,-2])
    set_tool_digital_outputs([1,-2]);wait(0.5)
    for i in range(10):
        wait(0.5)
        if get_tool_digital_input(n)==1: break
    else:
        sig_send(n)#실린더 알람 보내기
        while True:
            if get_tool_digital_input(n)==1: #알람 해제
                if sig_conversion(get_digital_inputs([1,2,3,4,5,6,7,8]))==1: break
                
######################################################################

def Release():
    sig_send(num)
    set_tool_digital_outputs([-1,-2])
    set_tool_digital_outputs([-1,2]);wait(0.5)
    
######################################################################
    
    




q = get_current_posj() #관절각 리턴받아 홈위치로 되어있는 지 확인
if 82 >q[0]> 78 and  17 >q[1]> 13 and -87 >q[2]> -91 and 181 >q[3]> 178 and 108 >q[4]> 104 and -98 >q[5]> -102:
    a=1
else:
    tp_popup("Not a Home Posithon")
    exit()

    
    
#############초기 세팅##################
signal_reset() # 신호 리셋
Release()#그리퍼 열기
set_velx(500) # 전역 태스크 속도
set_accx(500) # 전역 태스크 가속도
set_velj(70) # 전역 조인트 속도
set_accj(45) # 전역 조인트 가속도
set_tool("Tool Weight") # 툴 무게 설정
#set_tcp("!@#12") #그리퍼 설정





while True:
    wait_digital_input(9)
    value=sig_conversion(get_digital_inputs([1,2,3,4,5,6,7,8]))
    #robot -> plc send
    if value<40: # 튀김기 넘버
        fryer=0
        wait_digital_input(9)
        fryer=sig_conversion(get_digital_inputs([1,2,3,4,5,6,7,8]))
        #robot -> plc send
        
        
    if value<40: #치킨 투입 배출
        if fryer<20: #투입
            sig_send(num) #비지 신호
            
            if value==1: mastr_pick=posx(0, 0, 0, 0, 0, 0)
            elif value==2: mastr_pick=
        
            if fryer==11: master_place=posx(0, 0, 0, 0, 0, 0)
            elif fryer==12: master_place=
            elif fryer==13: master_place=
            elif fryer==14: master_place=
            elif fryer==15: master_place=
            elif fryer==16: master_place=
            movej()#via
            movel(trans(master_pick,[0,0,200,0,0,0]))#app
            movel(trans(master_pick,[0,0,0,0,0,0]))#pick
            Grip()
            movel(trans(master_pick,[0,0,200,0,0,0]))#app
            
            movej()#app
            movel(trans(master_place,[0,0,200,0,0,0]))#app
            movel(trans(master_place,[0,0,0,0,0,0]))#place
            Release()
            movel(trans(master_place,[0,0,200,0,0,0]))#app
            movej()#대기위치
            
            sig_send(num)
        else: #배출
            sig_send(num) #비지 신호
        
            if value==21: mastr_place=posx(0, 0, 0, 0, 0, 0)
            elif value==22: mastr_place=
        
            if fryer==31: master_pick=posx(0, 0, 0, 0, 0, 0)
            elif fryer==32: master_pick=
            elif fryer==33: master_pick=
            elif fryer==34: master_pick=
            elif fryer==35: master_pick=
            elif fryer==36: master_pick=
            movej()#via
            movel(trans(master_pick,[0,0,200,0,0,0]))#app
            movel(trans(master_pick,[0,0,0,0,0,0]))#pick
            Grip()
            movel(trans(master_pick,[0,0,200,0,0,0]))#app
            
            movej()#app
            movel(trans(master_place,[0,0,200,0,0,0]))#app
            movel(trans(master_place,[0,0,0,0,0,0]))#place
            Release()
            movel(trans(master_place,[0,0,200,0,0,0]))#app
            movej()#대기위치
            
            sig_send(num)
        
    elif value==n: Grip() #그리퍼 열림
    elif value==n: Release() #그리퍼 닫힘
    elif value==n:#대기위치 
        sig_send(num) #비지 신호
        move_home(DR_HOME_TARGET_USER)
        sig_send(num)
