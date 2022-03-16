





### 介绍一下你知道哪几种消息队列，该如何选择呢？

![图片](https://mmbiz.qpic.cn/mmbiz_png/hvUCbRic69sDaYzFdqyEg6aPkmRlO4QJ0DSDtRpzfNW27Cicp4ZP6gASfRy94pnF6HELzoL3Tx2MJn8o9ocdstTA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

https://mmbiz.qpic.cn/mmbiz_png/hvUCbRic69sDaYzFdqyEg6aPkmRlO4QJ0DSDtRpzfNW27Cicp4ZP6gASfRy94pnF6HELzoL3Tx2MJn8o9ocdstTA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1



# redis面试题

voltile-lru 从已经设置过期时间的数据集中挑选最近最少使用的数据淘汰

voltile-ttl 从已经设置过期时间的数据库集当中挑选将要过期的数据

voltile-random 从已经设置过期时间的数据集任意选择淘汰数据

allkeys-lru 从数据集中挑选最近最少使用的数据淘汰

allkeys-random 从数据集中任意选择淘汰的数据

no-eviction 禁止驱逐数据

**Redis** **当中有哪些数据结构**

字符串 String、字典 Hash、列表 List、集合 Set、有序集合 SortedSet。如果是高级用户，那么还会有，如果你是 Redis 中高级用户，还需要加上下面几种数据结构 HyperLogLog、Geo、Pub/Sub。

**假如** **Redis** **里面有** **1** **亿个** **key****，其中有** **10w** **个** **key** **是以某个固定的已知的前缀开头的，如**

**果将它们全部找出来？**

使用 keys 指令可以扫出指定模式的 key 列表。

对方接着追问：如果这个 redis 正在给线上的业务提供服务，那使用 keys 指令会有什么问

题？

这个时候你要回答 redis 关键的一个特性：redis 的单线程的。keys 指令会导致线程阻塞一

段时间，线上服务会停顿，直到指令执行完毕，服务才能恢复。这个时候可以使用 scan 指

令，scan 指令可以无阻塞的提取出指定模式的 key 列表，但是会有一定的重复概率，在客

户端做一次去重就可以了，但是整体所花费的时间会比直接用 keys 指令长。

**使用** **Redis** **做过异步队列吗，是如何实现的**

使用 list 类型保存数据信息，rpush 生产消息，lpop 消费消息，当 lpop 没有消息时，可

以 sleep 一段时间，然后再检查有没有信息，如果不想 sleep 的话，可以使用 blpop, 在没

有信息的时候，会一直阻塞，直到信息的到来。redis 可以通过 pub/sub 主题订阅模式实现

一个生产者，多个消费者，当然也存在一定的缺点，当消费者下线时，生产的消息会丢失。

**Redis** **如何实现延时队列**

使用 sortedset，使用时间戳做 score, 消息内容作为 key,调用 zadd 来生产消息，消费者

使用 zrangbyscore 获取 n 秒之前的数据做轮询处理。





