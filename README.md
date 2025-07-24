# TheDev
```
这是一个杂乱的项目,承载了一个野生程序员几年的时间在写代码这件事上的挣扎与思考。
取名dev是希望它永远正在开发中，只有一个开发分支，也不会有release版本。
```
### 一个简洁的Python后端
```
基于 tornado 选择它的原因并不是因为它
1. 基于协程的高性能http服务
2. 良好的架构设计(像大多数开源软件，充满很多冗余代码)    
只是因为它支持websocket，可以做一些和前端实时通信的东西
```
### 一个简洁的Ts前端库
```
只用了webpack，笔者相信没有vue，没有react，没有anglur，前端的事情也能很舒服。
前端之所以恶心在于js的弱类型，所以有了typescript。
当然vue，react，angule也都是不错的东西
```
### 没有数据库
```
因为用json文件也很舒服，但有在文件读写的模块留了db的口子。
希望有朝一日由于业务的性能瓶颈，会使用到db
```
### 一些算法的理解和有难度的编程题目
##### CodingGame OwareAlpha
[文档](doc\algo\game\oa\readme.md)
[游戏链接](https://www.codingame.com/ide/puzzle/oware-abapa)
[alt](doc/algo/game/oa/image.png)
##### CodingGame mad-pod-racing
[文档](doc\algo\game\mpr\readme.md)
[游戏链接](https://www.codingame.com/ide/puzzle/mad-pod-racing)
[alt](doc/algo/game/mpr/image.png)
### 一些web小游戏
### 一些杂七杂八的工具
## Todo
```
python -m app.yly.game.envs.oa.test
python -m app.yly.game.envs.mpr.test debug

```

## 编程
1. 尽量扩展代码，少新增代码。感觉不好的东西就该删除
3. 大多数人并不笨，那些难题也没有想象的那么难，只是没有遇到一个合适的场景，合适的人帮助你真正理解问题





