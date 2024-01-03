from hapi import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

def convert_atm_2_ppm(gas):
  R = 8.314
  T2 = 273.15
  P2 = 101325
  V2_gas = gas * 1e-2  # Assume area is 1m2
  n2_gas = (P2 * V2_gas) / (R * T2)
  T = temper
  P = pre  # in Pa
  V = 1000  # in m3
  n_air = (P * V) / (R * T)  # in mol
  vmr_gas = np.divide(n2_gas, n_air) * 1e6  # in ppm
  vmr_gas[-1] = vmr_gas[-2]
  return vmr_gas

def calc_optical_depth(gas_name,gas_vmr,PTH,min,max):
  x = 0
  normalized_P = PTH[:, 0] / PTH[0,0]
  height_level = np.diff(PTH[:, 2])
  height_level = np.append(height_level, 0)
  for i in range(36):
    nu, coef = absorptionCoefficient_Lorentz(SourceTables=[gas_name], Diluent={'air': 1},
                                             Environment={'T': PTH[i, 1], 'p': normalized_P[i]}, OmegaStep=0.1,
                                             OmegaRange=[min, max], HITRAN_units=False)  # False 代表 cm-1
    x += coef * gas_vmr[i] / 1e6 * height_level[i] * 1000 * 100
  return nu, x

db_begin('data')
# 需要修改波长范围
wavelength_range = [2500,1600] # in nm
wavenumber_range = [1e7 / x for x in wavelength_range]
# fetch('H2O', 1, 1, wavenumber_range[0], wavenumber_range[1])
# fetch('N2O', 4, 1, wavenumber_range[0], wavenumber_range[1])
# gases = {'CO2','H2O','N2O','O2','CH4'}
# for gas in gases:
#     fetch(gas, 1, 1, wavenumber_range[0], wavenumber_range[1])
#     print(gas)
# Read atmospheric profile

filename = 'tape6_1976'
with open(filename,'r') as f:
  lines = f.readlines()
PTH = np.loadtxt(lines[113:149], usecols=(2,3,1))
profile = np.loadtxt(lines[155:191], usecols=(np.arange(3, 15)))
pre = PTH[:,0] * 100 # in Pa
temper = PTH[:,1] # in K
height = PTH[:,2] # in km
h2o = profile[:,0] # in atm*cm / km
o3 = profile[:,1] # in atm*cm / km
co2 = profile[:,2] # in atm*cm / km
co = profile[:,3] # in atm*cm / km
ch4 = profile[:,4] # in atm*cm / km
n2o = profile[:,5] # in atm*cm / km
# Calculate ppm using atm*cm/km
vmr_h2o = convert_atm_2_ppm(h2o)
vmr_o3 = convert_atm_2_ppm(o3)
vmr_co2 = convert_atm_2_ppm(co2)
vmr_co = convert_atm_2_ppm(co)
vmr_ch4 = convert_atm_2_ppm(ch4)
vmr_n2o = convert_atm_2_ppm(n2o)

# 计算光学厚度
nu,depth_h2o = calc_optical_depth('H2O',vmr_h2o,PTH,wavenumber_range[0],wavenumber_range[1])
# nu,depth_o3 = calc_optical_depth('O3',vmr_o3,PTH,wavenumber_range[0],wavenumber_range[1])
nu,depth_co2 = calc_optical_depth('CO2',vmr_co2,PTH,wavenumber_range[0],wavenumber_range[1])
nu,depth_ch4 = calc_optical_depth('CH4',vmr_ch4,PTH,wavenumber_range[0],wavenumber_range[1])
# nu,depth_n2o = calc_optical_depth('N2O',vmr_n2o,PTH,wavenumber_range[0],wavenumber_range[1])
plt.plot(1e7 / nu, depth_h2o, ls="-", lw=2)
plt.plot(1e7 / nu, depth_co2, ls="-", lw=2)
plt.plot(1e7 / nu, depth_ch4, ls="-", lw=2)
# plt.plot(1e7 / nu, depth_n2o, ls="-", lw=2)
plt.legend(['H2O','CO2','CH4']) #打出图例
plt.yscale('log')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Optical depth')
plt.show()
savefig('optical_depth.png', dpi=300)
np.savetxt('H2O-optical-depth.csv',np.vstack((1e7 / nu,depth_h2o)).T,delimiter=',')
np.savetxt('CO2-optical-depth.csv',np.vstack((1e7 / nu,depth_co2)).T,delimiter=',')
np.savetxt('CH4-optical-depth.csv',np.vstack((1e7 / nu,depth_ch4)).T,delimiter=',')