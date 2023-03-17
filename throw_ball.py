import random
import turtle
import sys
import numpy as np
import warnings
warnings.filterwarnings("ignore")
turtle.setup(800, 800)
turtle.setworldcoordinates(-1, -1, 600, 600)
turtle.title("抛物线模拟")
# 绘制网格
x_zhou = -200
y_zhou = 800
axes = turtle.Turtle()
axes.speed(0)
axes.pensize(1)
while True:
    axes.penup()
    axes.goto(x_zhou, 800)
    axes.pendown()
    axes.goto(x_zhou, -200)
    x_zhou = x_zhou + 50  # 50为网格间隔
    if x_zhou == 800:
        break
while True:
    axes.penup()
    axes.goto(-200, y_zhou)
    axes.pendown()
    axes.goto(800, y_zhou)
    y_zhou = y_zhou - 50  # 50为网格间隔
    if y_zhou == -800:
        break

# 坐标轴设置，初始化两支画笔，分别为a1和a2表示x轴和y轴
a1 = turtle.Turtle()
a2 = turtle.Turtle()
a1.pencolor('green')
a2.pencolor('green')
a1.speed(0)
a2.speed(0)
a2.setheading(90)

for i in range(0, 500, 25):
    a1.goto(i, 0)
    a2.goto(0, i)
    if i % 100 == 0 and i != 0:
        a1.bk(12.5)
        a2.bk(6.25)
        a1.write(str(i) + "米", font=("Arial", 8, "normal"))
        a2.write(str(i) + "米", font=("Arial", 8, "normal"))
a1.goto(500, 0)
a1.write("x轴\n米", font=("Arial", 16, "normal"))
a2.goto(0, 500)
a2.write("y轴\n米", font=("Arial", 16, "normal"))

# 初始化数据
try:
    val_tmp_v0, val_tmp_h0 = turtle.textinput("初始速度、高度",
                                              "请输入初始速度(0-50)、高度(0-300)，用空格隔开。点击cancel结束动画。").split()
    v0 = float(val_tmp_v0)
    y_init = [float(val_tmp_h0)]
except AttributeError:
    print("输入为空，绘图退出。")
    turtle.done()
    sys.exit(0)
theta = np.radians(0)  # 初始化抛射角（rad）
g = 9.8  # 重力加速度（m/s2）
x = 0.0  # 任意时刻，x方向坐标
y = 0.0  # 任意时刻，y方向坐标
t = 0.0  # 起始时间设置为0
attenuation_factor = 0.0  # 每次小球撞击地面后，速度的衰减倍率，0为不反弹，不可设为1，否则会出现无限循环.
v_x = 0.0  # 任意时刻，x方向上的速度
v_y = 0.0  # 任意时刻，y方向上的速度
x_init = [0]  # t = 0 时x方向的坐标
# y_init = [160]  # t = 0时y方向上的坐标，即起始高度
x_array = []  # 用于存储所有时刻，x方向上坐标
y_array = []  # 用于存储所有时刻，y方向上坐标
my_flag = []  # 用于存储每次循环的标志位，用于判断是否需要标注


# 数据计算函数
def data_calculate(v_in, x_init_in, y_init_in, t_in, x_array_in, y_array_in, y_in, flag_in):
    global v_x, v_y
    v_x_init = v_in * np.cos(theta)  # 斜抛运动x方向上的初速度
    v_y_init = v_in * np.sin(theta)  # 斜抛运动y方向上的初速度
    while v_x_init >= 0.01 * v_in * np.cos(theta):  # 如果x方向上的速度衰减为原来的1%，则退出循环
        if (y_in > 0) or (y_in == 0):  # 如果小球依然在空中
            # 分别计算x, y方向上的速度
            v_x = v_x_init
            v_y = v_y_init - g * t_in

        # 如果小球碰到了地面,就结束循环
        else:
            break

        # 计算坐标点
        x_in = v_x_init * t_in + x_init_in[-1]
        y_in = v_y_init * t_in - 0.5 * g * t_in * t_in + y_init_in[-1]

        # 近似两位小数(处理精度问题)，用于判断是否为整数
        t_in = round(t_in, 2)
        print("时间为：", t_in, "s")
        if t_in.is_integer():
            flag_in.append(1)
        else:
            flag_in.append(0)
        t_in += 0.05  # t越小，轨迹越平滑
        x_array_in.append(x_in)
        y_array_in.append(y_in)
    return x_array_in, y_array_in, flag_in


# 自己的二开，输入初始速度
while (val_tmp_v0 and val_tmp_h0) is not None:
    print("本次试验初始速度v0:", v0)
    print("本次试验初始高度h0:", y_init[0])
    tmp = data_calculate(v0, x_init, y_init, t, x_array, y_array, y, my_flag)
    x_array = tmp[0]
    y_array = tmp[1]
    my_use_flag = tmp[2]  # 用于判断是否有整秒的时间
    # 用turtle模块进行可视化
    print("my_use_flag:", my_use_flag)
    tmp_turtle = turtle.Turtle()

    tmp_turtle.shape("circle")
    tmp_turtle.penup()
    tmp_turtle.goto(x_array[0], y_array[0])
    tmp_turtle.write("初始坐标为：" + str(x_array[0].round(2)) + "，" + str(y_array[0].round(2)),
                     font=("Arial", 10, "normal"))
    tmp_turtle.screen.colormode(255)
    tmp_turtle.pencolor(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
    tmp_turtle.pendown()
    tmp_turtle.width(4)
    for i in range(1, len(x_array)):
        tmp_turtle.goto(x_array[i], y_array[i])
        if my_use_flag[i] == 1:
            print("x_array[i]:", x_array[i])
            tmp_turtle.write(
                "第" + str(i / 20) + "秒的坐标为：\n" + str((x_array[i] / 2).round(2)) + "，" + str(
                    (y_array[i] / 2).round(2)),
                font=("Arial", 10, "normal"))

    x_array.clear()
    y_array.clear()
    my_use_flag.clear()
    try:
        val_tmp_v0, val_tmp_h0 = turtle.textinput("初始速度、高度",
                                                  "请输入初始速度(0-50)、高度(0-300)，用空格隔开。点击cancel结束动画。").split()
        v0 = float(val_tmp_v0)
        y_init = [float(val_tmp_h0)]
    except AttributeError:
        print("输入为空，程序退出。")
        turtle.done()
        sys.exit(0)
turtle.done()
sys.exit(0)
