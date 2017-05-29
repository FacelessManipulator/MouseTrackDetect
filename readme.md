# 数据特征
给出的数据中只包含轨迹点(x,y,t)的数据，从轨迹点的数据中大致能得到速度和角度。  
在notebook里我试着用matplotlib画了一些样例图，觉得可以从这几方面入手收集特征数据：
- 抖动的时间:人的轨迹大多包含了抖动，反映在轨迹上就是剧烈的角度变化，而有些做的不好的robot要么画直线要么画曲线，所以抖动可以作为一个特征。我觉得这个特征可以用角度变化率较大区域的总时间代表。
- 速度:
	- 不知为何有些robot喜欢在开始的时候停顿(或慢)，而人大多是急性子，开始快后面慢。把时间等切成x份，分别算出每份的平均速度，大概可以反映这个特征。
	- 速度分布人与机器也有区别，可以仿照上一条把不同速度的时间聚合一下
	- 有些robot速度的局部抖动很有规律，连个sin都不是，学了那么多个月没用上的傅立叶变换感觉终于能用一下了
	- 最后还是没用上傅里叶变换，因为把速度当自变量把时间一聚合，特征已经很明显了。
- 加速度
	- 分布上明显不同，无论是x还是y轴
- 角度
	- robot角度分布更集中，轻微的抖动对角度影响很大
	- 人有更大概率负角度
