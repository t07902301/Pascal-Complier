symbol_table={}
code_addr=0
next_instruction=100    # number of the next avaiable instruction
t=0
w=0
patch_goto={}
patch_dict={}
error_output=[]
semantic_error=0
class number(object):
    def __init__(self,left):
        self.addr=left[3]
        self.type=basic_type(1,left[4][0],left[4][1],0)
        self.token=left[:2]
class identify(object):
    def __init__(self,left):
        self.addr=left[3]
        self.token=left
class operator(object):
    def __init__(object,left):
        self.token=left[:2]
class non_terminal(object):
    def __init__(self,left):
        '''
        left=(token_id,name,line,addr--lexme or value) --> a Token
        number_token——>(token_id,name,line,addr,int/float)
        '''
        self.true=[]
        self.false=[]
        self.next=[]
        # self.addr=''
        self.addr=''
        self.token=left[:2]
        self.error=0
        self.type=''
class marker(object):
    def __init__(self,left):
        self.ins=0
        self.token=left
class basic_type(object):
    '''
    (number of type elements,type element):
    e.g. (10,int)
    (2,(10,int)) composite of basic types, which is also seen as array(2,array(10,int))
    '''
    def __init__(self,num,typ,wid,array_flag):
        self.number=num #count of elements
        self.element=typ
        self.width=wid
        self.array=array_flag
class array(object):
    '''
    bas=base,ofs=offset,typ=type
    \n used in array operation
    '''
    def __init__(self,bas,ofs,typ,error_flag):
        self.base=bas
        self.offset=ofs     
        self.type=typ
        self.error=error_flag
        self.token=(38,'L')
class declaration(object):
    '''
    non-terminal in declaration
    '''
    def __init__(self,typ,wid,left):
        self.type=typ     #basic type:(count of type,type)
        self.width=wid
        self.token=left
        self.addr=0
# SDT function
def backpatch(patch_list,instruction):
    if len(patch_list)==0:
        patch_list.append(instruction)
    else:
        for patch in patch_list:
            patch_dict[patch]+=str(instruction)
def error(id_lexme,row):
    '''
    default type of undefined id is integer
    '''
    global semantic_error
    semantic_error=1
    error_type=basic_type(1,'int',4,0)
    symbol_table[id_lexme]=declaration(error_type,4,id_lexme)
    print('\t Semantic Error: Undefined identifier in Line '+str(row))
    error_output.append('Semantic Error: undefined identifier in Line '+str(row)+'\n')
def change_stack(left,body_len,stack,symbol,stack_rear,symbol_rear):
    try:
        for i in range(0,body_len):
            sym_tmp=symbol.pop()
            symbol_rear-=1
            tmp=stack.pop()
            stack_rear-=1
    except IndexError:
        print('In Reduce')
        print(redcution)
        exit(1)
    symbol.append(left)
    symbol_rear+=1
    return stack_rear,symbol_rear
    # for i in range(body_len):
    #     stack.pop()
    # rear-=body_len
    # stack.append(left)
    # rear+=1
    # return rear
def new_tmp_addr():
    global code_addr
    code_addr+=1
    tmp_addr='t{}'.format(code_addr)
    return tmp_addr
def widen(address,type_t,type_w):
    global next_instruction
    if type_t==type_w:
        return address
    elif type_t=='int' and type_w=='float':
        tmp_addr=new_tmp_addr()
        print('Code\n {}: {}=(float){}'.format(next_instruction,tmp_addr,address))
        patch_dict[next_instruction]='{}=(float){}'.format(tmp_addr,address)
        next_instruction+=1
        return tmp_addr
def check_type(declare_type):
    # while len(declare_type.type)>1:
    #     declare_type=declare_type.type
    while declare_type.number>1:
        declare_type=declare_type.element
    return declare_type.element
def type_conversion():
    pass    
def max_type(expr_1_type,expr_2_type):
    if expr_1_type=='float' or expr_2_type=='float':
        return basic_type(1,'float',8,0)
    else:
        return basic_type(1,'int',4,0)
#loop
def repeat(stack,rear,left):
    m1=stack[rear-4]
    s1=stack[rear-3]
    m2=stack[rear-1]
    b=stack[rear]
    s=non_terminal(left)
    backpatch(b.false,m1.ins)
    backpatch(s1.next,m2.ins)
    s.next=b.true 
    return s
    # return change_stack(s,body_len,rear)
def while_state(stack,rear,left):
    global next_instruction
    m1=stack[rear-4]
    b=stack[rear-3]
    m2=stack[rear-1]
    s1=stack[rear]
    backpatch(s1.next,m1.ins)
    backpatch(b.true,m2.ins)
    # left=left+(0,'')
    s=non_terminal(left)
    s.next=b.false
    print('Code\n {}: goto {}'.format(next_instruction,m1.ins))
    patch_dict[next_instruction]='goto {}'.format(m1.ins)
    next_instruction+=1
    # return change_stack(s,body_len,rear)
    return s
def if_then(stack,rear,left):
    b=stack[rear-3]
    m=stack[rear-1]
    s1=stack[rear]
    backpatch(b.true,m.ins)
    s=non_terminal(left)
    s.next=b.false+s1.next
    return s
    # return change_stack(s,body_len,rear)
def if_then_else(stack,rear,left):
    b=stack[rear-7]
    m1=stack[rear-5]
    s1=stack[rear-4]
    n=stack[rear-3]
    m2=stack[rear-1]
    s2=stack[rear]
    backpatch(b.true,m1.ins)
    backpatch(b.false,m2.ins)
    tmp=s1.next+n.next
    # left=left+(0,'')
    s=non_terminal(left)
    s.next=tmp+s2.next
    return s
    # return change_stack(s,body_len,rear)
# marker
def m_translate(stack,rear,left):
    # left=left+(0,'')
    m=marker(left)
    m.ins=str(next_instruction)
    # return rear
    return m
def n_translate(stack,rear,left):
    global next_instruction
    n=marker(left)
    n.next=[str(next_instruction)]
    print('Code\n {}: goto --'.format(next_instruction))
    patch_dict[next_instruction]='goto '
    next_instruction+=1
    return n
#basic translation
def id_reduce(stack,rear,left):
    identifier=stack[rear]
    e=non_terminal(left)
    id_lexme=identifier.addr
    if id_lexme not in symbol_table:
        row=identifier.token[2]
        error(id_lexme,row)
        # e.addr='Invalid Reference'
        e.error=1
    e.type=symbol_table[id_lexme].type
    e.addr=identifier.addr
    return e
def num_reduce(stack,rear,left):
    num=stack[rear]
    # left=left+(0,'')
    e=non_terminal(left)
    e.addr=num.addr
    e.type=num.type
    return e
def calculate(stack,rear,left):
    global next_instruction
    expr_1=stack[rear-2]
    op=stack[rear-1].token[1]
    expr_2=stack[rear]
    # left=left+(0,'')
    expr=non_terminal(left)
    if expr_1.error==0 and expr_2.error==0:
        expr_1_type=check_type(expr_1.type)
        expr_2_type=check_type(expr_2.type)
        expr.type=max_type(expr_1_type,expr_2_type)
        a1=widen(expr_1.addr,expr_1_type,expr.type.element)
        a2=widen(expr_2.addr,expr_2_type,expr.type.element)
        expr.addr=new_tmp_addr()
        print('Code\n {}: {}={}{}{}'.format(next_instruction,expr.addr,a1,op,a2))
        patch_dict[next_instruction]='{}={}{}{}'.format(expr.addr,a1,op,a2)
        next_instruction+=1
    else:
        expr.error=1
    return expr
    # return change_stack(expr,body_len,rear)
def bracket(stack,rear,left):
    expr_1=stack[rear-1]
    expr=non_terminal(left)
    expr.addr=expr_1.addr
    expr.error=expr_1.error
    expr.type=expr_1.type
    return expr
def relation(stack,rear,left):
    global next_instruction
    expr_1=stack[rear-2]
    relop=stack[rear-1].token[1]
    expr_2=stack[rear]
    b=non_terminal(left)
    b.true=[next_instruction]
    b.false=[next_instruction+1]
    if expr_1.error==0 and expr_2.error==0:
        print('Code\n {}: if {}{}{} goto --'.format(next_instruction,expr_1.addr,relop,expr_2.addr))
        patch_dict[b.true[0]]='if {}{}{} goto '.format(expr_1.addr,relop,expr_2.addr)
        next_instruction+=1
        print('Code\n {}: goto --'.format(next_instruction))
        patch_dict[b.false[0]]='goto '
        patch_goto[b.false[0]]=''
        next_instruction+=1
    else:
        b.error=1
    # return change_stack(b,body_len,rear)
    return b
def id_assignment(stack,rear,left):
    global next_instruction
    identifier=stack[rear-2]
    expr=stack[rear]
    id_lexme=identifier.addr
    s=non_terminal(left)
    s.error=expr.error
    if id_lexme not in symbol_table:
        row=identifier.token[2]
        error(id_lexme,row)
        s.error=1
    elif expr.error==0:
        print('Code\n {}: {}={}'.format(next_instruction,identifier.token[3],expr.addr))
        patch_dict[next_instruction]='{}={}'.format(identifier.token[3],expr.addr)
        next_instruction+=1
    symbol_table[id_lexme].addr=expr.addr  #register id in symbol table
    return s
# declaration
def declare(stack,rear,left):
    identifier=stack[rear]
    T=stack[rear-1]
    symbol_table[identifier.addr]=T
    s=non_terminal(left)
    return s
def T_reduce(stack,rear,left):
    global t,w
    b=stack[rear-1]
    c=stack[rear]
    t=b.type
    w=b.width
    left=left+(0,'')
    T=declaration(c.type,c.width,left)
    return T
def int_reduce(stack,rear,left):
    global t,w
    b_type=basic_type(1,'int',4,0)
    b=declaration(b_type,4,left)
    t='int'
    w=4
    return b
def float_reduce(stack,rear,left):
    global t,w
    b_type=basic_type(1,'float',8,0)
    b=declaration(b_type,8,left)
    t='float'
    w=8
    return b
def c_reduce(stack,rear,left):
    c_type=basic_type(1,t,w,0)
    c=declaration(c_type,w,left)
    return c
def array_reduce_declare(stack,rear,left):
    c_1=stack[rear]
    num=stack[rear-2]
    width=num.addr*c_1.width
    array_type=basic_type(num.addr,c_1.type,width,1)
    c=declaration(array_type,width,left)
    return c
# array operation
def array_assignment(stack,rear,left):
    global next_instruction
    L=stack[rear-2]
    expr=stack[rear]
    s=non_terminal(left)
    if expr.error==0:
        print('Code\n {}: {}[{}]={}'.format(next_instruction,L.base,L.offset,expr.addr))
        patch_dict[next_instruction]='{}[{}]={}'.format(L.base,L.offset,expr.addr)
        next_instruction+=1
    s.error=expr.error
    return s
def array_reduce(stack,rear,left):
    global next_instruction
    l=stack[rear]
    e=non_terminal(left)
    e.addr=new_tmp_addr()
    e.type=l.type
    if l.error==0:
        print('Code\n {}: {}={}[{}]'.format(next_instruction,e.addr,l.base,l.offset))
        patch_dict[next_instruction]='{}={}[{}]'.format(e.addr,l.base,l.offset)
        next_instruction+=1
    e.error=l.error
    return e
def array_id(stack,rear,left):
    global next_instruction
    identifier=stack[rear-3]
    expr=stack[rear-1]
    base=identifier.addr
    error_flag=0
    if base not in symbol_table:
        error(base,identifier.token[2])
        error_flag=1
    array_info=symbol_table[base]   #T: (type,width)=(basic_type(cnt of type elements,type_elemnt),width)
    # if array_info.type.array_flag==0:
    #     print('Semantic Error: Identifier cannot be converted to Array')
    #     error_flag=1
    array_type=array_info.type.element
    offset=new_tmp_addr()
    l=array(base,offset,array_type,error_flag)
    if error_flag==0:
        print('Code\n {}: {}={}*{}'.format(next_instruction,l.offset,expr.addr,l.type.width))
        patch_dict[next_instruction]='{}={}*{}'.format(l.offset,expr.addr,l.type.width)
        next_instruction+=1
    return l
def array_L(stack,rear,left):
    global next_instruction
    L_1=stack[rear-3]
    expr=stack[rear-1]
    base=L_1.base
    tmp_addr=new_tmp_addr()
    offset=new_tmp_addr()
    error_flag=L_1.error
    L_type=L_1.type
    if error_flag==0:
        L_type=L_type.element
        print('Code\n {}: {}={}*{}'.format(next_instruction,tmp_addr,expr.addr,L_type.width))
        patch_dict[next_instruction]='{}={}*{}'.format(tmp_addr,expr.addr,L_type.width)
        next_instruction+=1
        print('Code\n {}: {}={}+{}'.format(next_instruction,offset,L_1.offset,tmp_addr))
        patch_dict[next_instruction]='{}={}+{}'.format(offset,L_1.offset,tmp_addr)
        next_instruction+=1
    L=array(base,offset,L_type,error_flag)
    return L
# connection 
def program_body(stack,rear,left):
    '''
    just return a terminal
    '''
    s=non_terminal(left)
    return s
def cpmd_body(stack,rear,left):
    '''
    l.next=s.ext
    '''
    stmts=stack[rear]
    cpmd_stmt=non_terminal(left)
    cpmd_stmt.next=stmts.next
    cpmd_stmt.error=stmts.error
    return cpmd_stmt
def stmts_stmt(stack,rear,left):
    stmts=non_terminal(left)
    stmt=stack[rear]
    stmts.next=stmt.next
    stmts.error=stmt.error
    return stmts
def stmts_sts_stmt(stack,rear,left):
    stmts=non_terminal(left)
    sts_1=stack[rear-3]
    m=stack[rear-1]
    stmt=stack[rear]
    stmts.next=stmt.next
    backpatch(sts_1.next,m.ins)
    if sts_1.error==1 or stmt.error==1:
        stmts.error=1
    return stmts
def stmt_if(stack,rear,left):
    stmt=non_terminal(left)
    if_stmt=stack[rear]
    stmt.next=if_stmt.next
    stmt.error=if_stmt.error
    return stmt
def e_f(stack,rear,left):
    '''
    e.addr=f.addr
    '''
    expr=non_terminal(left)
    factor=stack[rear]
    expr.addr=factor.addr
    expr.error=factor.error
    expr.type=factor.type
    return expr
translation={
    0:program_body,
    1:cpmd_body,
    2:stmts_stmt,
    3:stmts_sts_stmt,
    4:id_assignment,
    5:while_state,
    6:repeat,
    7:cpmd_body,
    8:cpmd_body,
    9:if_then,
    10:if_then_else,
    11:relation,
    12:relation,
    13:calculate,
    14:calculate,
    15:calculate,
    16:calculate,
    17:calculate,
    18:e_f,
    19:m_translate,
    20:n_translate,
    21:id_reduce,
    22:num_reduce,
    23:bracket,
    24:program_body,
    25:declare,
    26:T_reduce,
    27:int_reduce,
    28:float_reduce,
    29:c_reduce,
    30:array_reduce_declare,
    31:array_assignment,
    32:array_reduce,
    33:array_id,
    34:array_L
}
symble_class={
    'num':number,
    'id':identify,
    'relop':operator,
    'op':operator,
}
def print_patched():
    output=''
    for ins,code in patch_dict.items():
        print('Code\n{}:{}'.format(ins,code))
    print(error_output)
def print_code():
    output=''
    for ins,code in patch_dict.items():
        output+='{}:{}\n'.format(ins,code)
    return output,semantic_error
def error_report():
    output=''
    for each in error_output:
        output+=each
    return output        
def print_symbol_table():
    for key,value in symbol_table.items():
        print('\t SHOW: {}:{}'.format(key,value.type.element))
def choose_class(token):
    if token[1] in symble_class:
        return symble_class[token[1]](token)
    else:
        return non_terminal(token)