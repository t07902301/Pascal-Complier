def s0(i):
    if i=='<':
        return 1
    elif i=='=':
        return 5
    elif i=='>':
        return 6
    elif i==':':
        return 9
    else:
        return 11
def s1(i):
    if i=='=':
        return 2
    elif i=='>':
        return 3
    else:
        return 4
def s6(i):
    if i=='=':
        return 7
    else:
        return 8
def s9(i):
    return 10
op_state={
    0:s0,
    1:s1,
    6:s6,
    9:s9
}
# token={':=': 7, '<': 15, '>': 16}
def operator_scan(string,current_cursor,end):
    ''' Return operator and current index'''
    index=0
    state=0
    relop=''
    not_exit=[0,1,6,9]
    previous=''
    end-=current_cursor
    while index<end and (state in not_exit):
        # each refers to the previous one 
        relop+=previous
        #each moves to the new char
        each=string[index]
        state=op_state[state](each)
        previous=each
        index+=1
    if state==4 or state==8:
        # retract to record other chars
        index-=1
    else:
        #previous = string[index-1]
        relop+=previous
    return relop,current_cursor+index
# if __name__ == "__main__":
#     txt='<1'
#     print(operator_scan(txt,0,2))