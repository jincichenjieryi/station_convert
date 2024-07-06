import tkinter as tk
from tkinter import ttk
import re
import os
import sys
from tkinter import font

output_data = ""
var_prefix_check = 0
prefix = ""
var_decimal_places_check = 0
decimal_places = 0

# 程序说明
PROGRAM_INSTRUCTION = """主要功能：\n
1、横断面数据的相互转换。\n
2、桩号格式的相互转换：把上方示例中的第2、3列无视，只看第1列选择号数，即可直接转换桩号\n
\n
操作方法：\n
1、窗口左上第一个框内是1号数据，往右是2号，以此类推\n
2、点击“开始转换”前，检查输入格式，和输出格式是否选择正确\n
3、勾选小数位数，并输入数字，即可选择输出结果保留几位小数\n
4、勾选添加前缀并输入，即可在输出结果中添加前缀\n
"""

# 发布版本更新记录
UPDATE = """更新记录：\n
v1.1\n
1、输入和输出选择框中，默认勾选1号\n
2、当输入格式是1号，则程序自动勾选前缀框，并提取前缀赋给输出格式\n
"""

"""
内部开发版本更新记录：
7.04
1、输入和输出选择框中，默认勾选1号
2、当输入格式是1号，则程序自动勾选前缀框，并提取前缀赋给输出格式
6.14
更新控件位置布置方式，改为相对位置
6.13
更新输入框及输出框滚动条
"""

"""
更新计划：
1、给输入和输出框增加滑块
2、修改控件位置布置方式，改为相对位置
"""



def set_var_prefix_check(_int):
    global var_prefix_check
    var_prefix_check = _int


def set_prefix(_str):
    global prefix
    prefix = _str


def set_var_decimal_places_check(_int):
    global var_decimal_places_check
    var_decimal_places_check = _int


def set_decimal_places(_int):
    global decimal_places
    decimal_places = int(_int)


def get_output_data():
    return output_data


class StationConvert:
    """
    桩号转换

    :param ipt:str
    :param opt:str
    """
    def __init__(self, ipt, opt):

        self.input_data = self.str_2_list(ipt)
        self.stn = []   # 标准桩号格式[公里数,米数,平距,高程]
        self.output_data = opt
        self.LIST_COLUMN = self.cal_list_column()

    @staticmethod
    def str_2_list(_str):
        """
        把传入的字符串转成列表
        param: _str :传入的字符串
        return: 转换后的列表
        """

        lines = _str.split('\n')  # 按换行符分割字符串，得到行列表
        data_list = []  # 存储最终结果的列表

        for line in lines:
            if line.strip():  # 确保当前行不为空
                line_list = line.split('\t')  # 按制表符分割当前行，得到单词列表
                formatted_line = []  # 存储格式化后的当前行的列表
                for item in line_list:
                    if item.strip():  # 确保当前单词不为空
                        formatted_line.append(item.strip())  # 去除首尾空格后添加到当前行列表
                if formatted_line:  # 如果当前行不为空，则添加到结果列表中
                    data_list.append(formatted_line)
        return data_list
    # 桩号数字转换成桩号格式

    @staticmethod
    def custom_round(number, digits=0):
        """
        采用四舍五入方法，对数字进行舍入

        :param number:float（需舍入的数字）
        :param digits:int（保留的小数位数）
        """
        factor = 10 ** int(digits)
        return int(number * factor + 0.5) / factor

    def cal_list_column(self):
        """获取列表列数"""
        column = 1
        for line in self.input_data:
            if len(line) > 1:
                column = len(line)
        return column

    def divide_station(self, _list, part):
        """
        将桩号拆分成公里和米

        -part1: [YX41+100,1,2]>>[41,100,1,2]

        -part2: [41100,1,2]>>[41,100,1,2]

        Args:
            :param _list:待处理的列表
            :param part:功能选择参数

        returns:
            转换后的列表
        """
        output_list = []
        if self.LIST_COLUMN == 1:
            if part == 1:
                for line in _list:
                    line[0] = str(line[0])
                    match = re.match(r'^[A-Za-z]+(\d+)\+(\d{3}(?:\.\d*)?)$', line[0])
                    if match:
                        num1, num2 = match.groups()
                        output_list.append([int(num1), float(num2)])
            elif part == 2:
                for line in _list:
                    line[0] = str(line[0])
                    match = re.match(r'^(\d+)(\d{3}(?:\.\d*)?)$', line[0])
                    # (?:\.\d*)?：非捕获组，匹配小数点后跟任意数量的数字，表示小数部分是可选的
                    if match:
                        num1, num2 = match.groups()
                        output_list.append([int(num1), float(num2)])
        else:
            if part == 1:
                for line in _list:
                    line[0] = str(line[0])
                    match = re.match(r'^[A-Za-z]+(\d+)\+(\d{3}(?:\.\d*)?)$', line[0])
                    if match:
                        num1, num2 = match.groups()
                        output_list.append([int(num1), float(num2), line[1], line[2]])
            elif part == 2:
                for line in _list:
                    line[0] = str(line[0])
                    match = re.match(r'^(\d+)(\d{3}(?:\.\d*)?)$', line[0])
                    # (?:\.\d*)?：非捕获组，匹配小数点后跟任意数量的数字，表示小数部分是可选的
                    if match:
                        num1, num2 = match.groups()
                        output_list.append([int(num1), float(num2), line[1], line[2]])
        return output_list

    """输入转换成标准格式"""
    def fmt01_stn(self):
        self.stn = self.divide_station(self.input_data, 1)

    def fmt02_stn(self):
        for line in self.input_data:
            line[0] = float(line[0])*1000
        self.stn = self.divide_station(self.input_data, 2)

    def fmt03_stn(self):
        self.stn = self.divide_station(self.input_data, 2)

    def fmt04_stn(self):
        data = []
        station = ''
        for line in self.input_data:
            if "+" in line[0]:
                station = line[0]
                continue
            data.append([station, line[0], line[1]])
        self.stn = self.divide_station(data, 1)

    """小数位数操作"""
    def decimal_places(self):
        if var_decimal_places_check == 1:
            if decimal_places == 0:     # 当用户选择保留0位小数时，把self.stn中的米数，即self.stn[1]转变成整数
                for line in self.stn:
                    line[1] = int(self.custom_round(line[1], decimal_places))
                    if line[1] >= 1000:     # 四舍五入后，米数大于1000，则需进位到公里数
                        line[1] -= 1000
                        line[0] += 1
            else:
                for line in self.stn:
                    line[1] = self.custom_round(line[1], decimal_places)
                    if line[1] >= 1000:     # 四舍五入后，米数大于1000，则需进位到公里数
                        line[1] -= 1000
                        line[0] += 1

    """由标准格式转换为输出格式"""
    def stn_fmt01(self):
        opt = []
        if self.LIST_COLUMN == 1:
            for line in self.stn:
                opt.append([prefix+str(line[0])+"+"+str(line[1])])
            self.output_data = self.list_2_str(opt)
        else:
            for line in self.stn:
                opt.append([prefix+str(line[0])+"+"+str(line[1]), line[2], line[3]])
            self.output_data = self.list_2_str(opt)

    def stn_fmt02(self):
        opt = []
        if self.LIST_COLUMN == 1:
            for line in self.stn:
                opt.append([line[0]+line[1]/1000])
            self.output_data = self.list_2_str(opt)
        else:
            for line in self.stn:
                opt.append([line[0]+line[1]/1000, line[2], line[3]])
            self.output_data = self.list_2_str(opt)
        self.output_data = self.list_2_str(opt)

    def stn_fmt03(self):
        opt = []
        if self.LIST_COLUMN == 1:
            for line in self.stn:
                opt.append([line[0]*1000+line[1]])
            self.output_data = self.list_2_str(opt)
        else:
            for line in self.stn:
                opt.append([line[0]*1000+line[1], line[2], line[3]])
            self.output_data = self.list_2_str(opt)

    def stn_fmt04(self):
        opt = {}
        if self.LIST_COLUMN != 1:
            for line in self.stn:
                station = prefix+str(line[0])+"+"+str(line[1])
                if station not in opt:
                    opt[station] = []
                opt[station].append([line[2], line[3]])
            self.output_data = self.dic_2_str(opt)

    @staticmethod
    def dic_2_str(_dic):
        """
        字典转字符串
        :param _dic :传入的字典
        :return: 字符串
        """
        opt = ""
        for station, points in _dic.items():
            opt += station + '\n'   # 写入桩号
            for point in points:
                opt += point[0]+'\t'+point[1]+'\n'  # 写入平距和高程
        return opt

    @staticmethod
    def list_2_str(_list):
        """
        列表转字符串
        :param _list：传入的列表
        :return 字符串
        """
        opt = ""
        for line in _list:
            for i in line:
                opt += str(i)+'\t'
            opt += '\n'

        return opt


def station_convert(ipt_data, ipt_num, opt_num):
    """
    主函数

    :param ipt_data:str
    :param ipt_num:（1~4）输入数据格式编号
    :param opt_num:（1~4）输出数据格式编号
    """
    global output_data
    global var_prefix_check
    global prefix
    s = StationConvert(ipt_data, output_data)

    if ipt_data == "":    # 用户未输入数据
        pass
    if not var_prefix_check:    # 前缀框未选中
        prefix = ""

    if ipt_num == 1: s.fmt01_stn()
    elif ipt_num == 2: s.fmt02_stn()
    elif ipt_num == 3: s.fmt03_stn()
    elif ipt_num == 4: s.fmt04_stn()

    if var_decimal_places_check == 1:
        s.decimal_places()

    if opt_num == 1: s.stn_fmt01()
    elif opt_num == 2: s.stn_fmt02()
    elif opt_num == 3: s.stn_fmt03()
    elif opt_num == 4: s.stn_fmt04()

    output_data = s.output_data



# 获取脚本路径
def get_script_dir():
    """
    获取脚本路径
    :return: 当前脚本路径
    """
    # 获取脚本文件的路径
    script_path = sys.argv[0]
    # 将路径转换为绝对路径
    script_path = os.path.abspath(script_path)
    # 获取脚本所在目录
    script_dir = os.path.dirname(script_path)

    return script_dir


def read_txt(file_path):
    """
    逐行读取txt文件内容
    :param file_path: 文件路径
    :return: 文件内容字符串
    """
    content = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                content += line
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except UnicodeDecodeError:
        print(f"Error: Could not decode the file at {file_path}. It may not be UTF-8 encoded.")
    except IOError as e:
        print(f"Error: Could not read the file at {file_path}. {e}")

    return content


class Application(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.root = master

        # 设置窗口大小、居中、标题
        self.root.title("数据格式转换")
        self.root_width = 900
        self.root_height = 1000
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (self.root_width, self.root_height, (screenwidth - self.root_height) / 2,
                                    (screenheight - self.root_height) / 2)
        self.root.geometry(geometry)

        # 设置标准字体
        self.title_font = font.Font(family="微软雅黑",size=18)
        self.btn_font = font.Font(family="微软雅黑", size=12)

        # 创建IntVar变量来跟踪复选框的状态
        self.var_prefix_check = tk.IntVar()
        self.var_decimal_check = tk.IntVar()
        self.var_ipt_fmt = tk.IntVar()
        self.var_opt_fmt = tk.IntVar()

        self.data_format_num = 4
        # 创建组件
        self.createWidget()
        self.bind_button()
        self.program_prompt()

        self.input_data = ""
        self.output_data = ""

        """设置控件位置参数初始值"""
        # 说明区位置参数
        self.instr_width = 180
        self.instr_height = 160
        self.instr_x = 20
        self.instr_y = 100
        self.instr_spacing = 20

        # 操作区位置参数
        self.spacing_opr_instr = 20

        # 改变窗口尺寸时，动态调整控件尺寸及位置
        self.root.bind("<Configure>", self.win_resize)

    def createWidget(self):
        """创建组件"""
        # 创建样式
        style = ttk.Style()
        style.theme_use('default')
        style.configure('CustomScrollbar.Vertical.TScrollbar',
                        troughcolor='white',
                        background='white',
                        arrowcolor='black')
        """程序说明"""
        # 程序说明文本
        data_format = []
        for i in range(1, self.data_format_num+1):
            _list = []
            data_format.append(_list)
        data_format[0] = """YX41+300	0	185.03
YX41+300	10.16	180.53
YX41+300	18.55	175.85
YX41+400	0	179.06
YX41+400	10.06	177.74
YX41+400	18.15	175.73
YX41+500	0	181.58
YX41+500	18.01	178.58
YX41+500	31.65	178.91
"""
        data_format[1] = """41.3	0	185.03
41.3	5.3	180.53
41.3	8.5	175.85
41.4	0	179.06
41.4	10.4	177.74
41.4	20.31	175.73
41.5	0	181.58
41.5	8.1	178.58
41.5	13.64	178.91
        """
        data_format[2] = """41300	0	185.03
41300	10.16	180.53
41300	18.55	175.85
41400	0	179.06
41400	10.06	177.74
41400	18.15	175.73
41500	0	181.58
41500	18.01	178.58
41500	31.65	178.91       
        """
        data_format[3] = """YX41+300	
0	185.03
10.16	180.53
18.55	175.85
YX41+400	
0	179.06
10.06	177.74
18.15	175.73
YX41+500	
0	181.58
18.01	178.58
31.65	178.91
"""
        # 文本框
        # 行号从1开始，列号从0开始
        self.instruction = tk.Frame(self.root)
        instr_text = []
        for i in range(1, self.data_format_num+1):
            instr = tk.Text(self.instruction, width=25)
            instr.pack(side=tk.LEFT, expand=True)
            instr.insert(1.0,  data_format[i-1])
            instr.config(state=tk.DISABLED)    # 设置多行文本控件为只读
            instr_text.append(instr)

        # 返回按钮
        self.btn_back = tk.Button(self.root,text="返回", font=self.btn_font)
        self.btn_back.place(x=20, y=20, width=60, height=40)

        """操作区"""
        self.operation_area = tk.Frame(self.root)

        # 输入框及滚动条
        self.ipt = tk.Text(self.operation_area)
        self.ipt_scrollbar = ttk.Scrollbar(self.operation_area, orient='vertical', command=self.ipt.yview,
                                           style='CustomScrollbar.Vertical.TScrollbar')
        self.ipt.config(yscrollcommand=self.ipt_scrollbar.set)

        # 输入数据格式选择框
        self.ipt_radio = tk.Frame(self.operation_area)
        self.ipt_instr_text = tk.Label(self.ipt_radio, text="选择输入的数据格式", font=20, fg="red")
        self.ipt_radio01 = tk.Radiobutton(self.ipt_radio, text="01", value=1, variable=self.var_ipt_fmt)
        self.ipt_radio02 = tk.Radiobutton(self.ipt_radio, text="02", value=2, variable=self.var_ipt_fmt)
        self.ipt_radio03 = tk.Radiobutton(self.ipt_radio, text="03", value=3, variable=self.var_ipt_fmt)
        self.ipt_radio04 = tk.Radiobutton(self.ipt_radio, text="04", value=4, variable=self.var_ipt_fmt)
        self.var_ipt_fmt.set(1)

        # 开始转换按钮
        self.btn_start = tk.Button(self.operation_area,text="开始转换", font=self.btn_font)

        # 前缀复选框
        self.prefix_check = tk.Checkbutton(self.operation_area,text="添加前缀", variable=self.var_prefix_check)
        self.prefix_check["command"] = self.toggle_entry
        self.prefix_check["font"] = self.btn_font
        # 前缀输入框
        self.prefix_ipt = tk.Entry(self.operation_area, state=tk.DISABLED)

        # 小数位数复选框
        self.decimal_check = tk.Checkbutton(self.operation_area,text="小数位数", variable=self.var_decimal_check)
        self.decimal_check["command"] = self.toggle_entry
        self.decimal_check["font"] = self.btn_font
        # 小数位数输入框
        self.decimal_places_ipt = tk.Entry(self.operation_area, state=tk.DISABLED)

        # 输出数据格式选择框
        self.opt_radio = tk.Frame(self.operation_area)
        self.opt_instr_text = tk.Label(self.opt_radio, text="选择输出的数据格式", font=20, fg="red")
        self.opt_radio01 = tk.Radiobutton(self.opt_radio, text="01", value=1, variable=self.var_opt_fmt)
        self.opt_radio02 = tk.Radiobutton(self.opt_radio, text="02", value=2, variable=self.var_opt_fmt)
        self.opt_radio03 = tk.Radiobutton(self.opt_radio, text="03", value=3, variable=self.var_opt_fmt)
        self.opt_radio04 = tk.Radiobutton(self.opt_radio, text="04", value=4, variable=self.var_opt_fmt)
        self.var_opt_fmt.set(1)

        # 数据输出预览框及滚动条
        self.opt = tk.Text(self.operation_area)
        self.opt_scrollbar = ttk.Scrollbar(self.operation_area, orient='vertical', command=self.opt.yview,
                                           style='CustomScrollbar.Vertical.TScrollbar')
        self.opt.config(yscrollcommand=self.opt_scrollbar.set)

    def place_widget(self):
        """设置控件尺寸及位置"""
        """程序说明区"""
        self.instruction.place(x=20, y=100, width=self.root_width-40, height=self.instr_height)

        """操作区"""
        # 基础尺寸860*700
        opr_area_width = self.root_width-40
        opr_area_height = self.root_height-(self.instr_height+self.instr_y+self.spacing_opr_instr)-20
        self.operation_area.place(x=20, y=self.instr_height+self.instr_y+self.spacing_opr_instr, width=opr_area_width,
                                  height=opr_area_height)
        # 输入及输出框的宽度和高度
        spacing = 60    # 输入框与中间按钮的距离，也是输出框与中间按钮的距离
        text_width = (opr_area_width-20-spacing-80-spacing-20)/2
        text_height = opr_area_height-60

        # 输入及输出数据格式选择框
        radio_h = 60
        self.ipt_radio.place(x=0, y=0, width=text_width, height=radio_h)
        self.ipt_instr_text.pack(side=tk.TOP)
        self.ipt_radio01.pack(side=tk.LEFT, expand=True)
        self.ipt_radio02.pack(side=tk.LEFT, expand=True)
        self.ipt_radio03.pack(side=tk.LEFT, expand=True)
        self.ipt_radio04.pack(side=tk.LEFT, expand=True)

        self.opt_radio.place(x=text_width+spacing*2+100, y=0, width=text_width, height=radio_h)
        self.opt_instr_text.pack(side=tk.TOP)
        self.opt_radio01.pack(side=tk.LEFT, expand=True)
        self.opt_radio02.pack(side=tk.LEFT, expand=True)
        self.opt_radio03.pack(side=tk.LEFT, expand=True)
        self.opt_radio04.pack(side=tk.LEFT, expand=True)

        # 输入框及滚动条
        self.ipt.place(x=0, y=radio_h, width=text_width, height=text_height)
        self.ipt_scrollbar.place(x=+text_width, y=radio_h, width=20, height=text_height)
        # 开始转换按钮
        self.btn_start.place(x=(opr_area_width-80)/2, y=(opr_area_height-40)/2, width=80, height=40)
        # 前缀勾选框及输入框
        self.prefix_check.place(x=(opr_area_width-160)/2, y=radio_h+60, width=100, height=40)
        self.prefix_ipt.place(x=(opr_area_width-160)/2+100, y=radio_h+70, width=60, height=20)
        # 小数位数勾选框及输入框
        self.decimal_check.place(x=(opr_area_width-160)/2, y=radio_h, width=100, height=40)
        self.decimal_places_ipt.place(x=(opr_area_width-160)/2+100, y=radio_h+10, width=60, height=20)
        # 输出框及滚动条
        self.opt.place(x=text_width+spacing*2+100, y=radio_h, width=text_width, height=text_height)
        self.opt_scrollbar.place(x=text_width*2+spacing*2+100, y=radio_h, width=20, height=text_height)

    def toggle_entry(self):
        """
        启用或禁用输入框，取决于复选框的选中状态。
        """
        if self.var_prefix_check.get():  # 如果复选框被选中
            self.prefix_ipt.configure(state=tk.NORMAL)
            set_var_prefix_check(1)
        else:  # 如果复选框未被选中
            self.prefix_ipt.configure(state=tk.DISABLED)
            set_var_prefix_check(0)

        if self.var_decimal_check.get():  # 如果复选框被选中
            self.decimal_places_ipt.configure(state=tk.NORMAL)
            set_var_decimal_places_check(1)
        else:  # 如果复选框未被选中
            self.decimal_places_ipt.configure(state=tk.DISABLED)
            set_var_decimal_places_check(0)

    def program_prompt(self):
        """给输入框增加默认提示"""
        self.prompt_text = "\n输入“说明”\n\n然后点击“开始转换”\n\n以获取使用说明"
        self.ipt.insert("1.0", self.prompt_text)
        self.ipt.tag_add("prompt", "1.0", "end")
        self.ipt.tag_config("prompt", foreground="grey")
        self.ipt.bind("<FocusIn>", self.ipt_focus_in)
        self.ipt.bind("<FocusOut>", self.ipt_focus_out)

    def ipt_focus_in(self, event):
        if event.widget.get("1.0", "end-1c") == self.prompt_text:
            event.widget.delete("1.0", "end")
            event.widget.tag_remove("prompt", "1.0", "end")
            event.widget.config(fg='black')

    def ipt_focus_out(self, event):
        if not event.widget.get("1.0", "end-1c").strip():
            event.widget.insert("1.0", self.prompt_text, ("prompt",))
            event.widget.tag_add("prompt", "1.0", "end")
            event.widget.config(fg='grey')

    def back(self, event=None):
        """
        返回上一级菜单
        """
        self.root.destroy()

    def ipt_fmt(self):
        return self.var_ipt_fmt.get()

    def opt_fmt(self):
        return self.var_opt_fmt.get()

    def reply(self, command):
        """
        输入框输入指定指令，在输出框进行回复

        return TRUE:输入正确的指令并已进行回复
        FALSE: 未回复
        """
        rpl = ""
        if command == "author" or command == "作者":
            rpl = "5-0"
        elif command == "更新内容" or command == "更新" or command == "更新记录":
            rpl = UPDATE
        elif command == "说明" or command == "程序说明":
            rpl = PROGRAM_INSTRUCTION
        else:
            return False

        self.opt.delete("1.0", tk.END)
        self.opt.insert("1.0", rpl)
        return True

    def start(self, event=None):
        """
        button: 开始转换数据
        """
        # 行号从1开始，列号从0开始
        self.input_data = self.ipt.get(1.0, "end").strip()  # strip():去掉前后的空白字符

        # 若进行的是指令回复，则不需要桩号转换，直接退出
        if self.reply(self.input_data):
            return

        # 小数位数复选框选中，则根据输入的位数对桩号进行舍入
        if self.var_decimal_check.get() == 1:
            set_var_decimal_places_check(1)
            set_decimal_places(self.decimal_places_ipt.get())
        # 前缀复选框选中，则添加前缀
        if self.var_prefix_check.get() == 1:
            set_var_prefix_check(1)
            set_prefix(self.prefix_ipt.get())
        # 若输入格式是1号，则程序需自动勾选前缀框，并提取前缀赋给输出格式
        if self.ipt_fmt() == 1:
            self.var_prefix_check.set(1)
            self.prefix_ipt.configure(state=tk.NORMAL)
            set_var_prefix_check(1)
            match = re.search(r'\b([A-Za-z]+)\d+\+\d+\b', self.input_data)
            self.prefix_ipt.delete("0", tk.END)
            self.prefix_ipt.insert("0", match[1])
            set_prefix(match.group(1))
        station_convert(self.input_data, self.ipt_fmt(), self.opt_fmt())   # 把数据传入data_convert方法
        self.output_data = get_output_data()    # 用get_output_data方法把结果传回当前窗口

        self.opt.delete("1.0", tk.END)   # 输出结果前先清空输出框
        self.insert_opt_data(self.output_data)    # 输出结果

    def insert_opt_data(self, opt_data):
        self.opt.insert(1.0, opt_data)

    def win_resize(self,event=None):
        # 获取当前窗口大小
        self.root_width = self.root.winfo_width()
        self.root_height = self.root.winfo_height()

        # 动态调整控件大小和位置
        self.instr_spacing = (self.root_width - self.instr_width * 4 - 20*2)/7
        self.place_widget()

    def bind_button(self):
        """
        事件绑定
        """
        self.btn_back.bind('<Button>', self.back)
        self.btn_start.bind('<Button>', self.start)


if __name__ == '__main__':
    root = tk.Tk()
    Application(root)
    root.mainloop()


# def main():
#
#     fmt01 = """
# YX41+300.3333	0	185.03
# YX41+300	10.16	180.53
# YX41+300	18.55	175.85
# YX41+400	0	179.06
# YX41+400	10.06	177.74
# YX41+400	18.15	175.73
# YX41+500	0	181.58
# YX41+500	18.01	178.58
# YX41+500	31.65	178.91
#     """
#     fmt04 = """YX41+300
# 0	185.03
# 10.16	180.53
# 18.55	175.85
# YX41+400
# 0	179.06
# 10.06	177.74
# 18.15	175.73
# YX41+500
# 0	181.58
# 18.01	178.58
# 31.65	178.91
# """
#     fmt05 = """
# YX41+300
# YX41+300.333
# YX41+999.999
# YX41+400
# YX41+400
#         """
#     station_convert(fmt04, 4, 1)
#
#     print(output_data)
#
#
# if __name__ == '__main__':
#     main()
