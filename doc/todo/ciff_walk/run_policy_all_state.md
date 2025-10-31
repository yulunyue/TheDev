'int' object has no attribute 'get_dst


策略都在三次迭代后收敛到 -10 不合理

增加debug 日志，发现value 只迭代了一次
load 函数重载的问题 
GET NEW RULE 重载函数，为了避免传参错误，应该是无参函数
悬崖里也有评分，悬崖状态应该没action