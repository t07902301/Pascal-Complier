def upper_to_lower(char):
    if char>='A' and char<='Z':
        return chr(ord(char)+32)
    else:
        return char
# def new_line(string,row,index):
#     """
#     Return is_new_line symbol, current row and index
#     """
#     if string==r'\n':
#         row+=1
#         index+=2
#         symbol=True
#     else:
#         index+=1
#         symbol=False
#     return symbol,row,index
def is_digit(each):
    if each<='9' and each>='0':
        return True
    else:
        return False
def is_char(each):
    if each<='Z' and each>='A':
        return True
    elif each<='z' and each>='a':
        return True
    else:
        return False
operator_dict={
    '(':1,
    ')':2,
    '+':3,
    '-':4,
    '*':5,
    '/':6,
    '^':7
}
def operator(each):
    '''
    tokenize operators
    '''
    return (operator_dict[each],each)