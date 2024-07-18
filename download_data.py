from hapi import *
db_begin('data')
wavelength_range = [2500,1500] # in nm
wavenumber_range = [1e7 / x for x in wavelength_range]
fetch('H2O', 1, 1, wavenumber_range[0], wavenumber_range[1])
fetch('CO2', 2, 1, wavenumber_range[0], wavenumber_range[1])
fetch('CH4', 6, 1, wavenumber_range[0], wavenumber_range[1])
fetch('N2O', 4, 1, wavenumber_range[0], wavenumber_range[1])
# 加入别的在该光谱范围有吸收的气体的Name和id，id可以在hapi中查询。