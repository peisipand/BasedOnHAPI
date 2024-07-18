# 读取csv，重新绘制滑动平均的图
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import pandas as pd
import numpy as np
from matplotlib import font_manager#导入字体管理模块
my_font = font_manager.FontProperties(fname="C:/WINDOWS/Fonts/STSONG.TTF")
# 定义滑动平均函数
def np_move_avg(a,n,mode="same"):
    return(np.convolve(a, np.ones((n,))/n, mode=mode))
df_trans = pd.read_csv("df_trans.csv",encoding="utf-8")
gases = ['CO2','H2O','N2O','CH4']

# # 绘制图像
width_in_cm = 18 # 图像宽度
height_in_cm = 11 # 图像高度
fs = 12 # 字体大小

# 绘制透过率
fig = plt.figure(figsize=(width_in_cm / 2.54,height_in_cm /2.54))  # 这里的单位是 英寸 inch，1 in = 2.54 cm
for gas in gases:
    y_av = np_move_avg(df_trans[gas], 40) # 40个点滑动平均
    plt.plot(df_trans['wavelength'], y_av, ls="-", lw=2) # lw 控制线条的宽度

plt.legend(['$CO_2$','$H_2O$','$N_2O$','$CH_4$'], fontsize=fs)  # 打出图例
plt.xlabel('波长 (nm)',fontproperties = my_font, fontsize=fs)
plt.ylabel('透过率',fontproperties = my_font, fontsize=fs)
savefig('Transmittance_cn.png', dpi=300)
plt.show()