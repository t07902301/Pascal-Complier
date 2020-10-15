# from compile.basic import upper_to_lower
def s0(i):
    return 1
def s1(i):
    if i=='\\':
        return 2
    elif i=='"':
        return 6
    else:
        return 1
def s2(i):
    if i=='\\' or i=='"':
        return 3
    elif i=='t':
        return 4
    else:
        return 5
def s3(i):
    return 1
def s4(i):
    return 1
state_switch={
    0:s0,
    1:s1,
    2:s2,
    3:s3,
    4:s4,
}
def string_recognize(string,current_cursor,end):
    ''' Return is_string and current index of input string 
    '''
    index=0
    state=0
    previous_state=0
    buffer=''
    end-=current_cursor
    while state<5 and index<end:
        each=string[index]
        previous_state=state
        state=state_switch[state](each)
        if state==1:
            if previous_state==4:
                buffer+='\t'
            # elif previous_state==3:
            #     buffer+=each
            elif previous_state!=0:
                buffer+=each
        elif state==3 or state==4:
            continue
        index+=1
    if state==6:
        return buffer,current_cursor+index
    else:
        return 0,current_cursor+index
# if __name__ == "__main__":
#     txt=r'"a\t\\\""'
#     # print(txt)
#     buf,index=string_recognize(txt,0,len(txt))
#     print(buf,index)