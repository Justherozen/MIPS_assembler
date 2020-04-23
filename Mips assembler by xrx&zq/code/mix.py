import re
import os,sys,stat
path = os.getcwd()
import tkinter as tk
from tkinter import *
from tkinter import filedialog,dialog
from tkinter import scrolledtext
import tkinter.messagebox 
import time
#global readjudge
readjudge=0
#global writejudge
writejudge=0
binorhex=False



all_ch = {
    'add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor', 'slt', 'sltu',
    'sllv', 'srlv', 'srav', 'addi', 'addiu', 'andi', 'ori', 'xori', 'beq',
    'bne', 'slti', 'sltiu', 'j', 'jal', 'sll', 'srl', 'sra', 'jr', 'lw', 'sw',
    'lui', '$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3', '$t0',
    '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$s0', '$s1', '$s2',
    '$s3', '$s4', '$s5', '$s6', '$s7', '$t8', '$t9', '$k0', '$k1', '$gp',
    '$sp', '$fp', '$ra'
}
r_1 = {
    'add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor', 'slt', 'sltu',
    'sllv', 'srlv', 'srav'
}
r_2 = {'sll', 'srl', 'sra'}
i_1 = {'addi', 'addiu', 'andi', 'ori', 'xori', 'slti', 'sltiu'}
i_2 = {'lhx', 'lh', 'lwx', 'lw', 'lhux', 'lhu', 'shx', 'sh', 'swx', 'sw'}
i_3 = {'beq', 'bne'}
j_1 = {'j', 'jal'}

r_type1 = {
    'add': '100000',
    'addu': '100001',
    'sub': '100010',
    'subu': '100011',
    'and': '100100',
    'or': '100101',
    'xor': '100110',
    'nor': '100111',
    'slt': '101010',
    'sltu':
    '101011',  # It's an I-type instruction with the same form as r_type1.
    'sllv': '000100',
    'srlv': '000110',
    'srav': '000111'
}

r_type2 = {'sll': '000000', 'srl': '000010', 'sra': '000011'}

i_type1 = {
    'addi': '001000',
    'addiu': '001001',
    'andi': '001100',
    'ori': '001101',
    'xori': '001110',
    'slti':
    '001010',  # It's an R-type instruction with the same form as i_type1.
    'sltiu': '001011'
}

i_type2 = {
    'lhx': '100000',
    'lh': '100001',
    'lwx': '100010',
    'lw': '100011',
    'lhux': '100100',
    'lhu': '100101',
    'shx': '101000',
    'sh': '101001',
    'swx': '101010',
    'sw': '101011'
}

i_type3 = {
    'beq': '000100',
    'bne': '000101',
}

j_type = {'j': '000010', 'jal': '000011'}

reg_code = {
    '$zero': '00000',
    '$at': '00001',
    '$v0': '00010',
    '$v1': '00011',
    '$a0': '00100',
    '$a1': '00101',
    '$a2': '00110',
    '$a3': '00111',
    '$t0': '01000',
    '$t1': '01001',
    '$t2': '01010',
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$s0': '10000',
    '$s1': '10001',
    '$s2': '10010',
    '$s3': '10011',
    '$s4': '10100',
    '$s5': '10101',
    '$s6': '10110',
    '$s7': '10111',
    '$t8': '11000',
    '$t9': '11001',
    '$k0': '11010',
    '$k1': '11011',
    '$gp': '11100',
    '$sp': '11101',
    '$fp': '11110',
    '$ra': '11111'
}          


r_type1_re = {'100000': 'add',
 '100001': 'addu', 
 '100010': 'sub', 
 '100011': 'subu', 
 '100100': 'and', 
 '100101': 'or', 
 '100110': 'xor', 
 '100111': 'nor', 
 '101010': 'slt', 
 '101011': 'sltu', 
 '000100': 'sllv', 
 '000110': 'srlv', 
 '000111': 'srav'}

r_type2_re = {'000000': 'sll', '000010': 'srl', '000011': 'sra'}

i_type1_re = {'001000': 'addi', 
    '001001': 'addiu', 
    '001100': 'andi', 
    '001101': 'ori', 
    '001110': 'xori', 
    '001010': 'slti', 
    '001011': 'sltiu'}

i_type2_re = {'100000': 'lhx', 
    '100001': 'lh', 
    '100010': 'lwx',
    '100011': 'lw',
    '100100': 'lhux',
    '100101': 'lhu',
    '101000': 'shx', 
    '101001': 'sh', 
    '101010': 'swx', 
    '101011': 'sw'}

i_type3_re = {'000100': 'beq', '000101': 'bne'}

j_type_re = {'000010': 'j', '000011': 'jal'}

reg_code_re = {'00000': '$zero', 
    '00001': '$at', 
    '00010': '$v0', 
    '00011': '$v1', 
    '00100': '$a0', 
    '00101': '$a1', 
    '00110': '$a2', 
    '00111': '$a3', 
    '01000': '$t0', 
    '01001': '$t1', 
    '01010': '$t2', 
    '01011': '$t3', 
    '01100': '$t4', 
    '01101': '$t5', 
    '01110': '$t6', 
    '01111': '$t7', 
    '10000': '$s0', 
    '10001': '$s1', 
    '10010': '$s2', 
    '10011': '$s3', 
    '10100': '$s4', 
    '10101': '$s5', 
    '10110': '$s6', 
    '10111': '$s7', 
    '11000': '$t8', 
    '11001': '$t9', 
    '11010': '$k0', 
    '11011': '$k1', 
    '11100': '$gp', 
    '11101': '$sp', 
    '11110': '$fp', 
    '11111': '$ra'}

def showhelpmessage():
    tk.messagebox.showinfo(title='Help', message='Welcome to my mini assembler!click "open" to open files of mips code or \
machine code(.txt .coe .bin and some other file formats are supported).click "assemble" to convert mips code into machine code,click "disassemble" to convert machine code into mips \
code,origin code is shown on the left while the result is on the right.Make sure to click the right button and enjoy yourself!') 

def openmytxt(vara):
    if(vara==1):
        text.delete('1.0','end')
    global readjudge
    readjudge=1
    default_dir = r"文件路径"
    global file_path 
    file_path= filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
    #f1 = open(path + '\\mips.txt')
    f1=open(file_path,encoding='utf-8')
    global instructions
    instructions = f1.readlines()
    text.insert(INSERT, "this is original code\n")
    with open(file_path,encoding='utf-8') as f111:
        for each_line in f111:
            text.insert(INSERT, each_line)
    text.insert(INSERT, "\n")
    

def showtranslatemips(varb):
    if(varb==1):
        text2.delete('1.0','end')
    global writejudge
    writejudge=1
    global lines
    lines = []
    global lists
    lists = []
    global position
    position = []
    global ch
    ch = []
    i = 0
    newinstructions=(text.get("1.0","end")).split("\n")
    if (newinstructions[0]=="this is original code"):
        newinstructions.pop(0)    
    newinstructions.pop()
    for instruction in newinstructions:
        try:
            instruction=instruction.strip()
            if instruction=="":
                continue
            if(instruction[0:2]=="0x" or instruction[0:2]=="0X"):
                instruction=instruction[2:]#去除0x
                instruction=bin(int(instruction,16))[2:]
            else:
                instruction=bin(int(instruction,16))[2:]
                print(instruction)
            instruction=instruction.zfill(32)
            lines.append(instruction.strip())
            i = i + 1
        except ValueError:
            instruction="11111111111111111111111111111111"
    j = 0
    text2.insert(INSERT, "this is mips code\n")
    os.chmod(os.path.split(os.path.realpath(__file__))[0],stat.S_IRWXO) 
    f2 = open(os.path.split(os.path.realpath(__file__))[0]+"\mipsfrommachine.txt", 'w')    
    for line in lines:
        if (line=="00000000000000000000000000000000"):
            result3="nop"
        elif (line[0:6]) in i_type1_re.keys():
            result3=transfer_i_type1_re(line)
        elif (line[0:6]) in i_type2_re.keys():
            result3=transfer_i_type2_re(line)
        elif (line[0:6]) in i_type3_re.keys():
            result3=transfer_i_type3_re(line)
        elif (line[0:6]) in j_type_re.keys():
            result3=transfer_j_type_re(line)
        elif line[0:6]=="000000":
            if (line[26:32]) in r_type1_re.keys():
                result3=transfer_r_type1_re(line)
            elif(line[26:32]) in r_type2_re.keys():
                result3=transfer_r_type2_re(line)
            else:
                result3=transfer_special_r_type_re(line)
        else:
            result3 ="there is error in this line!!!"
        #Result2 = '0b' + result2
        print(result3)
        f2.write(result3+"\n")
        text2.insert(INSERT, result3+'\n')
        j = j + 1
    f2.close()
    
def showtranslatemachine(varb):
    if(varb==1):
        text2.delete('1.0','end')
    global writejudge
    writejudge=1
    global lines
    lines = []
    global lists
    lists = []
    global position
    position = []
    global ch
    ch = []
    i = 0
    newinstructions=(text.get("1.0","end")).split("\n")
    if (newinstructions[0]=="this is original code"):
        newinstructions.pop(0) 
    newinstructions.pop()
    for instruction in newinstructions:
        instruction=instruction.strip()
        if instruction=="":
            continue
        if instruction[0] == '#':
            continue
        if instruction.find(':') != -1:
            cut = re.split(r'[:|#]', instruction)
            position.append(i)
            ch.append(cut[0])
            if(cut[1].strip()!=""):
                instruction = cut[1]
            else:
                instruction=""
        if(instruction[0:5]=="move "):
            instruction="or "+instruction[5:]+",$zero"
        if(instruction[0:4]=="not "):
            instruction="nor "+instruction[4:]+",$zero"
        if(instruction[0:6]=="clear "):
            instruction="add "+instruction[6:]+",$zero,$zero"        
        if(instruction[0:4]=="Bgt "or instruction[0:4]=="bgt "):
            newcut=instruction[4:].split(',')
            instruction="slt "+newcut[1]+","+newcut[0]+","+"$t0"
            lines.append(instruction.lstrip())
            i = i + 1  
            instruction="bne $t0,$zero,"+newcut[2]          
        if(instruction[0:4]=="Bge " or instruction[0:4]=="bge "):
            newcut=instruction[4:].split(',')
            instruction="slt "+newcut[0]+","+newcut[1]+","+"$t0"
            lines.append(instruction.lstrip())
            i = i + 1  
            instruction="beq $t0,$zero,"+newcut[2] 
        if(instruction[0:4]=="Blt " or instruction[0:4]=="blt "):
            newcut=instruction[4:].split(',')
            instruction="slt "+newcut[0]+","+newcut[1]+","+"$t0"
            lines.append(instruction.lstrip())
            i = i + 1  
            instruction="bne $t0,$zero,"+newcut[2] 
        if(instruction[0:4]=="Ble "or instruction[0:4]=="ble "):
            newcut=instruction[4:].split(',')
            instruction="slt "+newcut[1]+","+newcut[0]+","+"$t0"
            lines.append(instruction.lstrip())
            i = i + 1  
            instruction="beq $t0,$zero,"+newcut[2] 
        if(instruction.strip()!=""):
            lines.append(instruction.lstrip())
            i = i + 1
    for line in lines:
        tmp = re.split(' |,|\n|\(|\)', line)
        result1 = [x.strip() for x in tmp if x.strip() != '']
        lists.append(result1)
    j = 0
    text2.insert(INSERT, "this is machine code\n")
    text2.insert(INSERT, "memory_initialization_radix=16\n")
    text2.insert(INSERT, "memory_initialization_vector=\n")
    os.chmod(os.path.split(os.path.realpath(__file__))[0],stat.S_IRWXO) 
    with open(os.path.split(os.path.realpath(__file__))[0]+"\machinecodefrommips.txt", 'w') as f2:
        for mips in lists:
            for t in range(1, len(mips)):
                try:
                    index = ch.index(mips[t])
                    if mips[0] in j_1:
                        mips[t] = position[index]
                    else:
                        mips[t] = position[index]-j-1
                except ValueError:
                    continue
            try:
                if mips[0] in r_1:
                    result2 = transfer_r_type1(mips)
                elif mips[0] in r_2:
                    result2 = transfer_r_type2(mips)
                elif mips[0] in i_1:
                    result2 = transfer_i_type1(mips)
                elif mips[0] in i_2:
                    result2 = transfer_i_type2(mips)
                elif mips[0] in i_3:
                    result2 = transfer_i_type3(mips)
                elif mips[0] in j_1:
                    result2 = transfer_j_type(mips)
                else:
                    result2 = transfer_special_type(mips)
                Result2 = '0b' + result2
                if(binorhex):
                    print(Result2)
                    f2.write(Result2 + '\n')
                    text2.insert(INSERT, Result2 + '\n')
                else:
                    print("{:#010x}".format((int(Result2, 2))))
                    f2.write("{:#010x}".format((int(Result2, 2))) + '\n')
                    text2.insert(INSERT, "{:#010x}".format((int(Result2, 2)))+ '\n')
            except ValueError:
                print("Error this line")
                f2.write("Error this line" + '\n')
                text2.insert(INSERT, "Error this line" + '\n')
            j = j + 1
    f2.close()
    
            

def binary(num, bit):
    return (bin(((1 << bit) - 1) & num)[2:]).zfill(bit)


def transfer_r_type1_re(line):
    #                                       rd                                 rs                       rt
    result=r_type1_re[line[26:32]]+" "+reg_code_re[line[16:21]]+','+reg_code_re[line[6:11]]+','+reg_code_re[line[11:16]]
    return result


def transfer_r_type2_re(line):
    result=r_type2_re[line[26:32]]+" "+reg_code_re[line[16:21]]+','+reg_code_re[line[11:16]]+','+str(int((line[21:26]),2))
    return result



def transfer_i_type1_re(line):
    if(line[16]=="1"):   
        result=i_type1_re[line[0:6]]+" "+reg_code_re[line[11:16]]+','+reg_code_re[line[6:11]]+',-'+str(65536-int((line[16:32]),2))
    else: 
        result=i_type1_re[line[0:6]]+" "+reg_code_re[line[11:16]]+','+reg_code_re[line[6:11]]+','+str(int((line[16:32]),2))
    return result
 

def transfer_i_type2_re(line):
    result=i_type2_re[line[0:6]]+" "+reg_code_re[line[11:16]]+','+str(int((line[16:32]),2)) +"("+reg_code_re[line[6:11]]+')'
    return result

def transfer_i_type3_re(line):
    if(line[16]=="1"):   
        result=i_type3_re[line[0:6]]+" "+reg_code_re[line[6:11]]+','+reg_code_re[line[11:16]]+',-'+str(65536-int((line[16:32]),2))
    else:
        result=i_type3_re[line[0:6]]+" "+reg_code_re[line[6:11]]+','+reg_code_re[line[11:16]]+','+str(int((line[16:32]),2))
    return result


def transfer_j_type_re(line):
    result=j_type_re[line[0:6]]+" "+str(int((line[6:32]),2))
    return result


def transfer_special_r_type_re(line):
    result="jr"+ reg_code_re[line[6:11]]


def binary(num, bit):
    return (bin(((1 << bit) - 1) & num)[2:]).zfill(bit)


def transfer_r_type1(mips):
    result = '000000' + reg_code[mips[2]] + reg_code[mips[3]] + reg_code[
        mips[1]] + '00000' + r_type1[mips[0]]
    return result


def transfer_r_type2(mips):
    result = '00000000000' + reg_code[mips[2]]  + reg_code[
        mips[1]] + binary(int(mips[3]), 5) + r_type2[mips[0]]
    return result


def transfer_i_type1(mips):
    result = i_type1[mips[0]] + reg_code[mips[2]] + reg_code[mips[1]] + binary(
        int(mips[3]), 16)
    return result


def transfer_i_type2(mips):
    result = i_type2[mips[0]] + reg_code[mips[3]] + reg_code[mips[1]] + binary(
        int(mips[2]), 16)
    return result


def transfer_i_type3(mips):
    result = i_type3[mips[0]] + reg_code[mips[1]] + reg_code[mips[2]] + binary(
        int(mips[3]), 16)
    return result


def transfer_j_type(mips):
    tmp = int(mips[1])
    result = j_type[mips[0]] + binary(tmp, 26)
    return result


def transfer_special_type(mips):
    result="There is an error in this line"#'000000000000000000000000000000000'
    if mips[0] == 'jr':
        result = '000000' + reg_code[
            mips[1]] + '00000' + '00000' + '00000' + '001000'
    elif mips[0] == 'lui':
        result = '001111' + '00000' + reg_code[mips[1]] + binary(
            int(mips[2]), 16)
    elif mips[0] == 'bgezal':
        result = '000001' + reg_code[mips[1]] + '10001' + binary(
            int(mips[2]), 16)
    elif mips[0] == 'jalr':
        result = '000000' + reg_code[mips[1]] + '00000' + reg_code[
            mips[2]] + '00000' + '001001'
    elif mips[0] == 'mfc0':
        result = '010000' + '00000' + reg_code[mips[1]] + reg_code[
            mips[2]] + '00000' + '000000'
    elif mips[0] == 'mtc0':
        result = '010000' + '00100' + reg_code[mips[1]] + reg_code[
            mips[2]] + '00000' + '000000'
    elif mips[0] == 'eret':
        result = '010000' + '10000' + '00000' + '00000' + '00000' + '011000'
    elif mips[0] == 'syscal':
        result = '000000' + '00000' + '00000' + '00000' + '00000' + '001100'
    elif mips[0] == 'mul':
        result = '011100' + reg_code[mips[2]] + reg_code[mips[3]] + reg_code[
            mips[1]] + '00000' + '000010'
    elif mips[0] == 'mult':
        result = '000000' + reg_code[mips[1]] + reg_code[
            mips[2]] + '00000' + '00000' + '011000'
    elif mips[0] == 'multu':
        result = '000000' + reg_code[mips[1]] + reg_code[
            mips[2]] + '00000' + '00000' + '011001'
    elif mips[0] == 'div':
        result = '000000' + reg_code[mips[1]] + reg_code[
            mips[2]] + '00000' + '00000' + '011010'
    elif mips[0] == 'divu':
        result = '000000' + reg_code[mips[1]] + reg_code[
            mips[2]] + '00000' + '00000' + '011011'
    elif mips[0] == 'mfhi':
        result = '000000' + '00000' + '00000' + reg_code[
            mips[1]] + '00000' + '00000' + '010000'
    elif mips[0] == 'mflo':
        result = '000000' + '00000' + '00000' + reg_code[
            mips[1]] + '00000' + '00000' + '010010'
    elif mips[0] == 'mthi':
        result = '000000' + reg_code[
            mips[1]] + '00000' + '00000' + '00000' + '010001'
    elif mips[0] == 'mtlo':
        result = '000000' + reg_code[
            mips[1]] + '00000' + '00000' + '00000' + '010011'
    return result

def save_file():
    global file_path
    global file_text
    file_path = filedialog.asksaveasfilename(title=u'save files')
    print('保存文件：', file_path)
    file_text = text2.get('2.0','end')
    if file_path is not None:
        with open(file=file_path, mode='a+', encoding='utf-8') as file:
            file.write(file_text)
        dialog.Dialog(None, {'title': 'File Modified', 'text': '保存完成', 'bitmap': 'warning', 'default': 0,
                'strings': ('OK','cancel')})
        print('保存完成')

def hexchange():
    global binorhex
    binorhex=~binorhex
    showtranslatemachine(writejudge)


def destroybegin():
    global beginindexd
    beginindex=1
    textbegin.destroy()
    label_img.destroy()
    window.geometry('580x665')
    label_img.destroy()
    global sc1
    sc1=tk.Scrollbar(window,width=10)
    sc1.set(0.2,0)
    sc1.pack(side=tk.LEFT,fill=tk.Y)
    global sc2
    sc2=tk.Scrollbar(window,width=10)
    sc2.set(0.2,0)
    sc2.pack(side=tk.RIGHT,fill=tk.Y)
    global text
    text =Text(window, width=40,height=38,yscrollcommand=sc1.set)
    global text2
    text2 =Text(window, width=40,height=38,yscrollcommand=sc2.set)
    # 两个控件关联
    text.place(x=20,y=40)
    text2.place(x=270,y=40)
    #text.config(yscrollcommand=b1.set)
    global b1
    b1 = tk.Button(window, text='open', width=10,height=1, command=lambda:openmytxt(readjudge))
    b1.place(x=25,y=3)
    global b2
    b2 = tk.Button(window, text='assemble', width=10,height=1, command=lambda:showtranslatemachine(writejudge))
    b2.place(x=110,y=3)
    global b3
    b3 = tk.Button(window, text='disassemble', width=10,height=1, command=lambda:showtranslatemips(writejudge))
    b3.place(x=195,y=3)
    global b4
    b4 = tk.Button(window, text='help', width=10,height=1, command=showhelpmessage)
    b4.place(x=470,y=3)
    global b5
    b5 = tk.Button(window, text='save', width=10,height=1, command=save_file)
    b5.place(x=390,y=3)
    global b6
    b6 = tk.Button(window, text='switch hex/bin', width=15,height=1, command=hexchange)
    b6.place(x=280,y=3)
    window.title('Mini mips assembler designed by Knox Xiao')
    sc1.config(command=text.yview)
    sc2.config(command=text2.yview)
    print(sys.path[0])
    photo2 = PhotoImage(file=os.path.split(os.path.realpath(__file__))[0]+'\source\mips2.gif')
    labe2_img = tk.Label(window, image = photo2)
    labe2_img.pack()
    labe2_img.place(relx=0.1, rely=0.832)
    window.mainloop()

def main():
    beginindex=0
    global finename
    filename = sys.argv[0]
    global dirname
    dirname = os.path.dirname(filename)
    global abspath
    abspath = os.path.abspath(dirname)
    global window
    window = Tk()
    window.geometry('533x331') 
    window.title('Welcome to my mini mips assembler')
    photo1 = PhotoImage(file=os.path.split(os.path.realpath(__file__))[0]+'\source\mips.gif')
    global label_img
    label_img = tk.Label(window, image = photo1)
    label_img.place(relx=0.0, rely=0.0)
    label_img.pack(side=tk.RIGHT)
    global textbegin
    textbegin = Text(window,width=100,height=1)
    textbegin.pack()
    textbegin.place(relx=0.0, rely=0.95)
    textbegin.insert(INSERT,"initializing......")
    label_img.after(1200, destroybegin)
    window.mainloop()

if __name__ == "__main__":
    myt0=time.process_time()
    main()



