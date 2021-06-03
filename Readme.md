# 北海板卡
## 节点连接
SSH 登陆跳板机： 
- 159.226.41.100（所外）
- 10.30.16.1（所内）

用户名sdc05，密码：sdc05huomiao，端口2234

跳板机需要ssh密钥登陆，附件中有私钥

在计算所内网直接ssh root@10.30.12.2 连接到riscv-debian里面，用户名和密码是root

# 服务 
## 在线应用
- redis
- socialnetwork
### Redis
- 板卡下载
```
apt install redis
```
- 修改redis配置文件
```
vim /etc/redis/redis.conf
# 一定要修改绑定IP，否则跳板机无法访问
bind 10.30.12.2 127.0.0.1
```
- 启动服务
```
redis-server /etc/redis/redis.conf
```

### Redis 负载发生器

这里的负载发生器用的是redis-cluster-bench。负载发生器位置是`/home/sdc05/SDC_Bench-master/x86/redis-cluster-bench`

测试负载：
```
./redis-cluster-bench -h 10.30.12.2 -p 6379 -n 10000000 -c 3 -t set --interval 1
```
### socialnetwork
- 源码参加github：https://github.com/Cuiyus/RISCV-Spec/tree/master/socialnetwork
- 启动
```
python3 index.py
```
### socialnetwork负载访问

```
curl -d 1 10.30.12.2:5000
```
