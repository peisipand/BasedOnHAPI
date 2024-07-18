from hapi import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
# 需要修改的参数
wavelength_range = [2500,1500] # in nm，该范围要属于 download_data.py 中的范围
gases = ['CO2','H2O','N2O','CH4'] #
# 输出的美国1976标准大气廓线来自于MODTRAN，MODTRAN提供的浓度单位是ATM CM / KM，convert_atm_2_ppm 将单位转换为 ppm
# Calculate ppm using atm*cm/km
def convert_atm_2_ppm(atm_gas):
  R = 8.314
  T2 = 273.15
  P2 = 101325
  V2_gas = atm_gas * 1e-2  # Assume area is 1m2
  n2_gas = (P2 * V2_gas) / (R * T2)
  T = temper
  P = pre  # in Pa
  V = 1000  # in m3
  n_air = (P * V) / (R * T)  # in mol
  vmr_gas = np.divide(n2_gas, n_air,out=np.zeros_like(n_air), where=n_air != 0) * 1e6  # in ppm，忽略 除数为0的警告
  vmr_gas[-1] = vmr_gas[-2]
  return vmr_gas

def calc_optical_depth(gas_name,vmr_gas,PTH,min,max):
  x = 0
  normalized_P = PTH[:, 0] / PTH[0,0]
  height_level = np.diff(PTH[:, 2])
  height_level = np.append(height_level, 0)
  for i in range(36):
    nu, coef = absorptionCoefficient_Lorentz(SourceTables=[gas_name], Diluent={'air': 1},
                                             Environment={'T': PTH[i, 1], 'p': normalized_P[i]}, OmegaStep=0.1,
                                             OmegaRange=[min, max], HITRAN_units=False)  # False 代表 coef的单位是 ppm-1;True 代表 coef的单位是 molec-1
    x += coef * vmr_gas[i] / 1e6 * height_level[i] * 1000 * 100
  return nu, x
db_begin('data')
wavenumber_range = [1e7 / x for x in wavelength_range]
# Read atmospheric profile from MODTRAN
filename = 'tape6_1976'
with open(filename,'r') as f:
  lines = f.readlines()
PTH = np.loadtxt(lines[113:149], usecols=(2,3,1))
profile = np.loadtxt(lines[155:191], usecols=(np.arange(3, 15)))
pre = PTH[:,0] * 100 # in Pa
temper = PTH[:,1] # in K
height = PTH[:,2] # in km
H2O = profile[:,0] # in atm*cm / km
O3 = profile[:,1] # in atm*cm / km
CO2 = profile[:,2] # in atm*cm / km
CO = profile[:,3] # in atm*cm / km
CH4 = profile[:,4] # in atm*cm / km
N2O = profile[:,5] # in atm*cm / km
# 创建两个空的 DataFrame
df_optical_depth = pd.DataFrame(columns=gases,dtype=object)
df_trans = pd.DataFrame(columns=gases,dtype=object)
for i in range(len(gases)):
    gas = gases[i]
    print(gas)
    vmr_gas = convert_atm_2_ppm(eval(gas))
    print(vmr_gas)
    nu, optical_depth = calc_optical_depth(gas, vmr_gas, PTH, wavenumber_range[0], wavenumber_range[1])
    trans = np.exp(-optical_depth)
    df_optical_depth[gas] = optical_depth
    df_trans[gas] = trans
print(df_optical_depth)
# # 绘制图像
width_in_cm = 15 # 图像宽度
height_in_cm = 11 # 图像高度
fs = 12 # 字体大小

# 绘制光学厚度
fig = plt.figure(figsize=(width_in_cm / 2.54,height_in_cm /2.54))  # 这里的单位是 英寸 inch，1 in = 2.54 cm
plt.plot(1e7 / nu, df_optical_depth, ls="-", lw=2) # lw 控制线条的宽度
plt.legend(gases,fontsize=fs) #打出图例
plt.yscale('log')
plt.xlabel('Wavelength (nm)',fontsize=fs)
plt.ylabel('Optical depth',fontsize=fs)
savefig('optical_depth.png', dpi=300)

# 绘制透过率
fig = plt.figure(figsize=(width_in_cm / 2.54,height_in_cm /2.54))  # 这里的单位是 英寸 inch，1 in = 2.54 cm
plt.plot(1e7 / nu, df_trans, ls="-", lw=2) # lw 控制线条的宽度
plt.legend(gases,fontsize=fs) #打出图例
plt.xlabel('Wavelength (nm)',fontsize=fs)
plt.ylabel('Transmittance',fontsize=fs)
savefig('Transmittance.png', dpi=300)
plt.show()

## 保存数据
df_optical_depth.insert(loc=0, column='wavelength', value= 1e7 / nu)
df_optical_depth.to_csv("df_optical_depth.csv")

df_trans.insert(loc=0, column='wavelength', value= 1e7 / nu)
df_trans.to_csv("df_trans.csv")
