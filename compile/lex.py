from compile.scale import scale
from compile.string import string_recognize
from compile.operator import operator_scan
from compile.basic import *
max_num=0x80000000
number_type={
    0:('int',4),
    1:('float',8)
}
token_dict={
    'program': 0, 'id': 1, 'begin': 2, 'end': 3, ';': 4, '.': 5, ':=': 6, 'while': 7, 'do': 8, 'repeat': 9, 'until': 10, 'if': 11, 'then': 12, 'else': 13, '>': 14, '<': 15, '+': 16, '-': 17, '*': 18, '/': 19, '^': 20, '(': 21, ')': 22, 'num': 23, 'int': 24, 'float': 25, '[': 26, ']': 27, '$': 28, 'compound_stmt': 29, 'stmts': 30, 'stmt': 31, 'if_stmt': 32, 'expr': 33, 'M': 34, 'N': 35, 'factor': 36, 'bool': 37, 'L': 38, 'X': 39, 'Y': 40, 'T': 41}
def error(each,line,col):
    # print('Lexical error:{} in Line {},Col {}'.format(each,line,col))
    return 'Lexical error:{} in Line {},Col {}\n'.format(each,line,col)
def scan(string):
    # string=repr(stream)
    output=[]
    # raw_output=''
    row=1
    index=0
    end=len(string)
    error_state=0
    new_line_start=index
    # input is a char string/ string
    while index<end:
        #search for next line
        if error_state==1:
            if string[index]=='\n':
                row+=1
                error_state=0
            index+=1
        else:
            each=string[index]
            if each==' ' or each=='\t':
                index+=1
            elif each=='\n':
                row+=1
                index+=1
                new_line_start=index
            else:
                if is_digit(each):
                    dig_val=0
                    dig_val,dig_index,is_float=scale(string[index:],index,end)
                    col=dig_index-new_line_start
                    if dig_val!=-1:
                        if dig_val>=max_num:
                            # raw_output+=error("Exceed maximun limit of integer",row,col)
                            output.append((42,error(" Exceed maximun limit of integer",row,col)))
                        else:
                            # raw_output+='<{}:{}>\n'.format(number_type[is_float],dig_val)
                            output.append((token_dict['num'],'num',row,dig_val,number_type[is_float]))
                    else:
                        # raw_output+=error(" Neither a number nor an ID",row,col)
                        output.append((42,error(" Neither a number nor an ID",row,col)))
                        error_state=1
                    index=dig_index
                elif is_char(each):
                    buffer=''
                    char_index=index
                    while char_index<end and (is_char(string[char_index]) or is_digit(string[char_index])):
                        buffer+=upper_to_lower(string[char_index])
                        char_index+=1
                    if buffer not in token_dict:
                        output.append((token_dict['id'],'id',row,buffer))
                        # raw_output+='<id:{}>\n'.format(buffer)
                    else:
                        output.append((token_dict[buffer],buffer,row,buffer))
                        # raw_output+='<reservered word:{}>\n'.format(buffer)
                    # move foreward
                    index=char_index
                elif each=='"':
                    str_val,str_index=string_recognize(string[index:],index,end)
                    if str_val==0:
                        # raw_output+=error(" Illegal string",row,str_index-new_line_start)
                        error_state=1
                        output.append((42,error(" Illegal string",row,str_index-new_line_start)))
                    else:
                        # raw_output+=("<string:{}>\n".format(str_val))
                        output.append((43,'string',row))
                    index=str_index
                elif (each<='/' and each>='(') or each=='^':
                    # raw_output+='<operator:{}>\n'.format(each)
                    output.append((token_dict[each],each,row))
                    index+=1
                else:
                    relop,op_index=operator_scan(string[index:],index,end)
                    # raw_output+=('<relop: {} >\n'.format(relop))
                    output.append((token_dict[relop],relop,row))
                    index=op_index
    return output
# def print_table():
#     table_print=''
#     for key,value in string_table.items():
#         tmp=key+':<'+value[0]+','+value[1]+'>\n'
#         table_print+=tmp
#     return (table_print)