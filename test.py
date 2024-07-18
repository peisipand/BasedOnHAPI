import matplotlib.pyplot as plt

config = {
    "font.family": "serif",  # 使用衬线体
    "font.serif": ["SimSun-ExtB"],  # 全局默认使用衬线宋体
    "font.size": 14,  # 五号，10.5磅
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",  # 设置 LaTeX 字体，stix 近似于 Times 字体
}
plt.rcParams.update(config)


fig, ax = plt.subplots(figsize=(5, 5))
ax.plot([i / 10.0 for i in range(10)], [i / 10.0 for i in range(10)])
# 中西混排，西文使用 LaTeX 罗马体
ax.set_title("能量随时间变化\n$\mathrm{Change\ in\ energy\ over\ time}$")
ax.set_xlabel("时间（$\mathrm{s}$）")
ax.set_ylabel("能量（$\mathrm{J}$）")

# 坐标系标签使用西文字体
ticklabels_style = {
    "fontname": "Times New Roman",
    "fontsize": 12,  # 小五号，9磅
}
plt.xticks(**ticklabels_style)
plt.yticks(**ticklabels_style)
plt.legend(["测试曲线"])
plt.show()

