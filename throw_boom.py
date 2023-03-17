import os
import random
import sys
import turtle
import numpy as np
import psutil
import ctypes


# 使用提醒：有效打击值为30

# 判断是否在控制台运行,0为控制台，1为Windows
def check_console():
    image_name = 'explorer.exe'
    s = psutil.Process().parent()
    if s.name() == image_name or s.parent().name() == image_name:
        return 1
    return 0


# 静态资源路径或者是控制台资源路径
ship_PATH = os.path.abspath(os.path.join(sys._MEIPASS, ".", "ship.gif")) if check_console() else "./ship.gif"
fire_PATH = os.path.abspath(os.path.join(sys._MEIPASS, ".", "fire.gif")) if check_console() else "./fire.gif"
plane_PATH = os.path.abspath(os.path.join(sys._MEIPASS, ".", "plane.gif")) if check_console() else "./plane.gif"
logo_PATH = os.path.abspath(os.path.join(sys._MEIPASS, ".", "logo.ico")) if check_console() else "./logo.ico"

# DPI缩放相关代码
ctypes.windll.shcore.SetProcessDpiAwareness(True)  # 0为系统缩放，1为程序缩放
# DPI缩放相关代码结束

turtle.setup(1400, 950)
turtle.setworldcoordinates(-1, -1, 1400, 950)
turtle.title("抛物线模拟")
turtle.bgpic(ship_PATH)

# 好像是访问了父类的匿名函数。
turtle.Screen().cv._rootwindow.resizable(False, False)  # 禁止调整窗口大小
turtle.Screen().cv._rootwindow.iconbitmap("logo.ico")  # 设置窗口图标，修改了tkinter库中的_init_.py文件，让logo用到了全局图标。

# 绘制网格
# x_zhou = -400
# y_zhou = 1000
# axes = turtle.Turtle()
# axes.speed(0)
# axes.hideturtle()  # 隐藏画笔,增加画图速度
# axes.pensize(1)
# while True:
#     axes.penup()
#     axes.goto(x_zhou, 1000)
#     axes.pendown()
#     axes.goto(x_zhou, -400)
#     x_zhou = x_zhou + 25  # 50为网格间隔，更多的格子。1格为22.5单位长度
#     if x_zhou == 1000:
#         break
# while True:
#     axes.penup()
#     axes.goto(-400, y_zhou)
#     axes.pendown()
#     axes.goto(1000, y_zhou)
#     y_zhou = y_zhou - 25  # 50为网格间隔，更多的格子。1格为22.5单位长度
#     if y_zhou == -1000:
#         break
# 绘制网格结束

# 坐标轴设置，初始化两支画笔，分别为a1和a2表示x轴和y轴
a1 = turtle.Turtle()
a2 = turtle.Turtle()
a1.pencolor('green')
a2.pencolor('green')
a1.speed(0)
a2.speed(0)
a2.setheading(90)

for i in range(0, 901, 25):
    a2.goto(0, i)
    if i % 100 == 0 and i != 0:
        a2.bk(6.25)
        a2.write(str(i / 20) + "米", font=("Arial", 10, "normal"))

a2.goto(0, 920)
a2.write("  y", font=("Arial", 16, "bold"))

for i in range(0, 1300, 25):
    a1.goto(i, 0)
    if i % 100 == 0 and i != 0:
        a1.bk(12.5)
        a1.write(str(i / 20) + "米", font=("Arial", 10, "normal"))
a1.goto(1350, 0)
a1.write("  x", font=("Arial", 16, "bold"))

try:
    val_x = float(
        turtle.Screen().numinput("飞机与小船相距的距离", "范围：-1至40，-1为随机投弹。\n点击Cancel结束绘图。", 20, -1,
                                 40)) * 10
    # 如果输入为-1则随机投弹
    if val_x == -10:
        val_x = random.randint(0, 300)
    else:
        val_x = 400 - val_x
    # val_tmp_v0, val_tmp_h0 = turtle.textinput("初始速度、高度",
    #                                           "请输入初始速度(0-30)、高度(0-300)，用空格隔开。点击cancel结束动画。").split()
    # v0 = float(val_tmp_v0)
    y_init = [450]
except TypeError:
    print("输入为空，绘图退出。")
    turtle.done()
    sys.exit(0)

# 如果输入为-1则随机投弹
if val_x == -1:
    val_x = random.randint(0, 300)

theta = np.radians(0)  # 初始化抛射角（rad）
g = 100  # 重力加速度（m/s2）
x = 0.0  # 任意时刻，x方向坐标
y = 0.0  # 任意时刻，y方向坐标
t = -0.05  # 起始时间设置为-0.05,为了让小球在t=0时，在计算x轴位置时多了一次循环，多增加0.05s的时间，确保飞机在t=0时，刚好位于起始位置
attenuation_factor = 0.0  # 每次小球撞击地面后，速度的衰减倍率，0为不反弹，不可设为1，否则会出现无限循环.
v_x = 0.0  # 任意时刻，x方向上的速度
v_y = 0.0  # 任意时刻，y方向上的速度
x_init = [0]  # t = 0 时x方向的坐标
# y_init = [160]  # t = 0时y方向上的坐标，即起始高度
x_array = []  # 用于存储所有时刻，x方向上坐标
y_array = []  # 用于存储所有时刻，y方向上坐标
my_flag = []  # 用于存储每次循环的标志位，用于判断是否需要标注


# 数据计算函数
def data_calculate(v_in, x_init_in, y_init_in, t_in, x_array_in, y_array_in, y_in, val_fire_x, flag_in):
    # flag_in是用来判断是否进行到整秒，整秒进行标注，0为不需要，1为需要
    global v_x, v_y, val_x
    v_x_init = v_in * np.cos(theta)  # 斜抛运动x方向上的初速度
    v_y_init = v_in * np.sin(theta)  # 斜抛运动y方向上的初速度
    t_line = 0  # 用于记录直线运动的时间
    while v_x_init >= 0.01 * v_in * np.cos(theta):  # 如果x方向上的速度衰减为原来的1%，则退出循环
        if (y_in > 0) or (y_in == 0):  # 如果小球依然在空中
            # 分别计算x, y方向上的速度
            v_x = v_x_init
            v_y = v_y_init - g * t_in
        # 如果小球碰到了地面,就结束循环
        else:
            break

        t_in += 0.05  # t越小，轨迹越平滑，但是计算量越大

        # 近似两位小数(处理精度问题)，用于判断是否为整数
        # t_in = round(t_in, 2)

        # if t_in.is_integer():
        #     flag_in.append(1)
        # else:
        #     flag_in.append(0)

        # 判断抛炸弹的位置
        # if val_fire_x < val_x:  # 如果小球还没有到达指定位置,做直线运动
        if val_fire_x < val_x:  # 如果小球还没有到达指定位置,做直线运动
            t_line += 0.05
            # 若没有落地则，计算直线运动路线
            x_in = v_x_init * t_in + x_init_in[-1]
            y_in = v_y_init * t_in + y_init_in[-1]  # 不下降
            val_fire_x += 0.05 * v_x_init  # 0.05为每秒移动的距离
            # 为了第一秒飞机位置刚好在起点，t0时刻设为-0.05秒，因为x_in不能先赋给x_array_in，所以多了一层循环，列表里存了0秒时刻的值
            x_array_in.append(x_in * 2)
            y_array_in.append(y_in * 2)

            # 判断是否为整秒，此思路有误，方法无用
            flag_in.append(0)

        else:  # 如果小球已经到达指定位置，抛下炸弹，做平抛运动
            # 若已经落地则，计算平抛运动路线
            x_in = v_x_init * t_in + x_init_in[-1]
            y_in = v_y_init * t_in - 0.5 * g * (t_in - t_line) * (t_in - t_line) + y_init_in[-1]
            x_array_in.append(x_in * 2)
            y_array_in.append(y_in * 2)

            # 判断是否为整秒,此思路有误，方法无用
            if round(t_in, 2).is_integer():
                flag_in.append(1)
            else:
                flag_in.append(0)

    # print(x_array_in, "\n", y_array_in)
    return x_array_in, y_array_in, flag_in


# 自己的二开，输入初始速度
while val_x is not None:

    tmp = data_calculate(100.0, x_init, y_init, t, x_array, y_array, y, 0.0, my_flag)
    # 速度固定为每次移动20m/s，高度固定为450m，投弹x轴位置可变。
    x_array = tmp[0]
    y_array = tmp[1]
    my_use_flag = tmp[2]  # 用于判断是否有整秒的时间点，有则进行标注

    # 用turtle模块进行可视化
    turtle.register_shape(plane_PATH)
    turtle.register_shape(fire_PATH)

    # 飞机和导弹的轨迹
    fly_turtle = turtle.Turtle()
    fly_turtle.speed(0)
    fly_turtle.shape(plane_PATH)
    fly_turtle.penup()
    fly_turtle.goto(x_array[0], y_array[0])
    fly_turtle.screen.colormode(255)
    fly_turtle.pencolor(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    fly_turtle.pendown()
    fly_turtle.width(4)

    fire_turtle = turtle.Turtle()
    fire_turtle.speed(0)
    fire_turtle.shape(fire_PATH)
    fire_turtle.penup()
    fire_turtle.hideturtle()
    fire_turtle.goto(x_array[0], y_array[0])
    fire_turtle.screen.colormode(255)
    fire_turtle.pencolor(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    fire_turtle.width(4)
    # print("应该在这里显示", val_x * 2)

    for i in range(1, len(x_array)):
        fire_turtle.goto(x_array[i], y_array[i])
        fly_turtle.goto(x_array[i], y_array[0])

        if fire_turtle.pos()[0] >= val_x * 2:
            # print("投弹，开始计算抛物线", fire_turtle.pos())
            fire_turtle.showturtle()
            fire_turtle.pendown()
            if round(y_array[i], 1) % 20 == 0:
                print("my_i:", i, "y_array", y_array[i])
                # 用时间判断的下落有误，数组中寻找整秒的Y轴坐标输出即可。
                # if my_use_flag[i] == 1:
                # if i % 20 == 0:
                # print(i, "y_array[i]:", y_array[i])
                # fire_turtle.stamp()  # 画出投弹的位置,这个有问题，第二次投弹时，第一次印章会消失。
                fire_turtle.write("(" +
                                  str((x_array[i] / 20).round(2)) + "，" + str(
                    (y_array[i] / 20).round(2)) + ")",
                                  font=("Arial", 10, "normal"))
    x_array.clear()
    y_array.clear()
    my_use_flag.clear()
    try:
        val_x = float(
            turtle.numinput("飞机与小船相距的距离", "范围：-1至40，-1为随机投弹。\n点击Cancel结束绘图。", 20, -1, 40)) * 10
        # val_tmp_v0, val_tmp_h0 = turtle.textinput("初始速度、高度",
        #                                           "请输入初始速度(0-30)、高度(0-300)，用空格隔开。点击cancel结束动画。").split()
        # v0 = float(val_tmp_v0)

        # 如果输入为-1则随机投弹
        if val_x == -10:
            val_x = random.randint(0, 300)
        else:
            val_x = 400 - val_x
        y_init = [450]
    except TypeError:
        print("输入为空，程序退出。")
        turtle.done()
        sys.exit(0)

turtle.done()
sys.exit(0)
