from compile.basic import upper_to_lower
# def upper_to_lower(char):
#     if char<='Z' and char>='A':
#         return chr(ord(char)+32)
#     else:
#         return char
def s0(i):
    if i=='0':
        return 1
    elif i>='1' and i<='9':
        return 8
def s1(i):
    if i=='0':
        return 2
    elif i>='1' and i<='7':
        return 7
    elif i=='x' or i=='X':
        return 6
    elif i=='8' or i=='9':
        return 20
    elif i>='a' and i<='z':
        return 20
    elif i=='.':
        return 9
    else:
        return 11
def s2(i):
    if i=='1' or i=='0':
        return 2
    elif i>='2' and i<='7':
        return 3
    elif i=='8' or i=='9':
        return 4
    elif i>='a' and i<='f':
        return 5
    elif i>='g' and i<='z':
        return 20
    elif i=='.':
        return 20
    else:
        return 11
def s3(i):
    if i>='0' and i<='7':
        return 3
    elif i=="8" or i=="9":
        return 4
    elif i>='a' and i<='f':
        return 5
    elif i>='g' and i<='z':
        return 20
    elif i=='.':
        return 20
    else:
        return 11
def s4(i):
    if i>='0' and i<='9':
        return 4
    elif i>='a' and i<='f':
        return 5
    elif i>='g' and i<='z':
        return 20
    elif i=='.':
        return 20
    else:
        return 11
def s5(i):
    if i>="0" and i<="9":
        return 5
    elif i>='a' and i<='f':
        return 5
    elif i>='g' and i<='z':
        return 20
    elif i=='.':
        return 20
    else:
        return 11
def s6(i):
    if i>="0" and i<="9":
        return 5
    elif i>='a' and i<='f':
        return 5
    elif i>='g' and i<='z':
        return 20
    elif i=='.':
        return 20
    else:
        return 11
def s7(i):
    if i>='0' and i<='7':
        return 7
    elif i=='8' or i=='9':
        return 20
    elif i>='a' and i<='z':
        return 20
    elif i=='.':
        return 20
    else:
        return 11
def s8(i):
    if i>='0' and i<='9':
        return 8
    elif i>='a' and i<='z':
        return 20
    elif i=='.':
        return 9
    else:
        return 11
def s9(i):
    return 10
def s10(i):
    if i>='0' and i<='9':
        return 10
    elif i>='a' and i<='z':
        return 20
    else:
        return 11
def binary(buf):
    val=0
    for current in buf:
        current=ord(current)-48
        val=2*val+current
    return val
def octonary(buf):
    val=0
    for current in buf:
        current=ord(current)-48
        val=8*val+current
    return val
def decimal(buf):
    val=0
    for current in buf:
        current=ord(current)-48
        val=10*val+current
    return val
def heximal(buf):
    val=0
    for current in buf[2:]:
        current=ord(current)
        if current>=97:
            current-=97
            current+=10
            val=16*val+current
        elif current>=65:
            current-=65
            current+=10
            val=16*val+current
        else:
            current-=48
            val=16*val+current
    return val  
def float_calculate(buf):
    val=0
    for current in buf[::-1]:
        current=ord(current)-48
        val=0.1*val+0.1*current
    return val
state_switch={
    0:s0,
    1:s1,
    2:s2,
    3:s3,
    4:s4,
    5:s5,
    6:s6,
    7:s7,
    8:s8,
    9:s9,
    10:s10
}
cal_state={
    1:decimal,
    2:binary,
    3:octonary,
    4:decimal,
    5:heximal,
    7:octonary,
    8:decimal,
    10:float_calculate,
}
# 2020-5-7 final state dealing with operator
#5-17 what follows digits return to main 
# op_list=['=','<','>',' ','\\']
# stand at current state-> take in last input-> move according to current input 
def scale(string,current_cursor,end):
    ''' 
    Scale recodnition: Return state and current index of input string\n
    wrong state=-1
     '''
    buffer=''   #记录扫描后的数字
    current=''  #当前字符
    val=0       #记录数值
    index=0     #当前字符在输入字符串中的位置
    state=0
    previous_state=0    #记录上一状态
    end-=current_cursor
    is_float=0  #是否为小数的标志
    while state<11 and index<end:   #当前状态合法而且输入字符串尚未遍历完毕
        if state==9:    
            val+=cal_state[8](buffer)
            #去除小数点，以免让其进入数值计算部分
            current=''
            buffer=''
            is_float=1
        buffer+=current
        current=string[index]
        current=upper_to_lower(current)
        previous_state=state
        state=state_switch[state](current)  #根据输入，进行状态跳转
        index+=1
    if state==20:   #若遇到报错状态，返回错误信号给LEX模块
        # illegal format
        current_cursor+=index
        return -1,current_cursor,is_float
    elif state==11:     #若遇到运算符，去除最后一个字符（运算符），即回退一个字符
    # retract index and state
        index-=1
        state=previous_state
    else:  
        buffer+=current     #接受最后一个合法字符  
    current_cursor+=index   #告知LEX模块，下一个要扫描字符的位置
    val+=cal_state[state](buffer)   #计算数值
    return val,current_cursor,is_float  
# if __name__ == "__main__":
#     # txt=r'008	"a\nc"  1.0002'
#     txt='0\n'
#     print(scale(txt,0,len(txt)))