# 测试绘图
import math

import matplotlib.pyplot as plt
import numpy as np

l1 = list(range(20))
l2 = list(map(lambda x: (x - 10) ** 2 / 5, l1))
l3 = list(map(lambda x: (math.sin(x) + 1) * 10, l1))
l4 = np.random.randint(0, 20, 20)

plt.plot(l1, l2, l1, l3, l1, l4)
plt.ylabel('Foo')
# plt.axis([-1, 8, 0, 6])
plt.show()
# plt.savefig('test', dpi=600)
