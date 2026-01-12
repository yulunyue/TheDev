# board_state 设计

# board_move 设计
相对于board_state

# 3*3*3 井字棋环境
python -m tool.c5_main 3_3_3 actor names=rd,rd
python -m tool.c5_main 3_3_3 fight names=rd,ad10,mc100 turn=4

# 6*4*4 的简单环境
## 对比rd ad1 ad2 ad3 四种状态
python -m tool.c5_main 6_6_4 fight names=rd,ad1,ad2,ad3 turn=4
正常应该为 rd<ad1<ad2<ad3

python -m tool.c5_main 6_6_4 fight names=gomo664_1500,ad2
python -m tool.c5_main 6_6_4 train name=gomo664_1500

和随机看看Gomo强度,PK下
python -m tool.c5_main 8_8_5 fight names=ad3,gomo885 turn=1
python -m tool.c5_main 8_8_5 actor names=ad3,gomo885

# gomo
gomo的一个action数据是 state=4*m*n,probs=m*n,winne=1
state 为什么需要4个维度？
[0] 表示自己的旗子 [1] 表示对手的旗子 [2] 表示空棋子 [3] 表示下一个可以放置的验收
多个维度虽然增加了内存但是信息分离有利于训练和机器学习

