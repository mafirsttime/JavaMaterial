



mac下配置命令总结-mac命令总结：
ls -G   #展示颜色





# Brew list

Logback 集成优化项： https://www.pianshen.com/article/6238630710/

redis启动停止：

任意路径执行 redis-server /usr/local/etc/redis.conf

停止：redid-cli shutdown ，kill -9 进程的pid，强行终止Redis进程可能会导致redis持久化丢失

当用ctrl+c退出的时候，发现redis服务也同时停止了，是因为redis.conf的守护进程没有配置为yes





# JVM总结-jvm调优





```java
FusionUtil:

@Resource(name = "fusion")
private RedisTemplate<String, String> redisTemplate;  //这里是读取fusion配置，没有设置线程池

2、都封装再：RedisConfig
@Bean(name = "fusionUtil")

private StringRedisTemplate redisTemplate;
    public FusionUtil(String host, int port, String password, int maxIdle, int maxTotal, long maxWaitMillis, int index) {

          private static final int MAX_IDLE = 200; //最大空闲连接数
    private static final int MAX_TOTAL = 1024; //最大连接数
    private static final long MAX_WAIT_MILLIS = 10000; //建立连接最长等待时间
     120Wqps/135台机器，大概9Kqps每台，所以1024线程还是少的。

      
      
3. @Resource(name = "taskExecutor")
    private ThreadPoolTaskExecutor taskEx
  #3个 判定接口都用改线程池， JudgeIdsImpl JudgeCalImpl JudgeCrmImpl
  
  1. JudgeIdsImpl  每个tagId 查询fusion等操作
  2.JudgeCalImpl  每个tagId，查询叶子节点，判断是否命中等。

  @Bean(name = "taskExecutor")
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        // 设置核心线程数，目前qps=30-700
        executor.setCorePoolSize(50);
        // 设置最大线程数
        executor.setMaxPoolSize(500);
        // 设置队列容量
        executor.setQueueCapacity(Integer.MAX_VALUE);    # 可减小，即可执行。
  
  4.  貌似没有地方用到：
    @Bean
    public RestTemplate restTemplate() {
        HttpComponentsClientHttpRequestFactory httpRequestFactory = new HttpComponentsClientHttpRequestFactory(HttpClientBuilder.create()
                .setMaxConnTotal(40)
                .setMaxConnPerRoute(40)
                .build());
        httpRequestFactory.setConnectionRequestTimeout(150);
        httpRequestFactory.setConnectTimeout(150);
        httpRequestFactory.setReadTimeout(150);
        RestTemplate restTemplate = new RestTemplate(httpRequestFactory);
        restTemplate.setInterceptors(Collections.singletonList(httpLogInterceptor()));
        restTemplate.getMessageConverters()
                .add(0, new StringHttpMessageConverter(StandardCharsets.UTF_8));
        return restTemplate;
    }
       
       1.0使用：
         static {
        HttpClientBuilder hcb = HttpClientBuilder.create().setMaxConnTotal(2000).setMaxConnPerRoute(100);
         //这里定义：2000 线程，100并发。
        HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(hcb.build());

        requestFactory.setConnectTimeout(connTimeout);
        requestFactory.setReadTimeout(readTimeout);

        restTemplate = new RestTemplate(requestFactory);
        restTemplate.getMessageConverters().add(new TextMappingJackson2HttpMessageConverter());
        LOG.info("create restTemplate with connTimeout = " + connTimeout + ", readTimeout = " + readTimeout);
    }
```







## 线程池的坑

先看下 FutureTask 的状态。前面我们看到了初始化状态是NEW，其他状态说明如下。

```
private static final int NEW          = 0; 新的任务，初始状态
private static final int COMPLETING   = 1; 当任务被设置结果时，处于COMPLETING状态，这是一个中间状态。
private static final int NORMAL       = 2; 表示任务正常结束。
private static final int EXCEPTIONAL  = 3; 表示任务因异常而结束
private static final int CANCELLED    = 4; 任务还未执行之前就调用了cancel(true)方法，任务处于CANCELLED
private static final int INTERRUPTING = 5; 当任务调用cancel(true)中断程序时，任务处于INTERRUPTING状态，这是一个中间状态。
private static final int INTERRUPTED  = 6; 任务调用cancel(true)中断程序时会调用interrupt()方法中断线程运行，任务状态由INTERRUPTING转变为INTERRUPTED
```

作者：但莫
链接：https://juejin.cn/post/6864474891308482573
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

结论： 如果线程池的拒绝策略设置成DiscardPolicy或者DiscardOldestPolicy，通过Future获取执行结果，可能导致线程会一直阻塞。

DiscardPolicy 和 DiscardOldestPolicy 代码如下。他们有一个共同点就是没有处理task的状态。

# 解决方案

1. 使用带超时时间的get方法，这样使用DiscardPolicy拒绝策略不会一直阻塞。
2. 如果一定要使用Discardpolicy 拒绝策略，需要自定义拒绝策略。

```
public void rejectedExecution(Runnable runable, ThreadPoolExecutor e) {
    if (! e.isShutdown()) {
        if(null ! = runable && runable instanceof FutureTask){
            ((FutureTask) runable).cancel(true);
          }
      }
}
```







```java
DEMO:

-server -Xrs -Xmx5120m -Xms1536m -Xmn512m -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC

-XX:+CMSParallelRemarkEnabled -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods

-XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70 -XX:SurvivorRatio=8

 

G1使用不分区内存, 一块一块,占用内存大.

-XX:+UseG1GC -XX:ConcGCThreads=2 -XX:+UseStringDeduplication -XX:G1ReservePercent=15 -XX:MaxMetaspaceSize=512m


```

 



```
]$   ps -ef|grep java
xiaoju      530      1  0 Nov25 ?        00:04:32 /usr/local/jdk1.8.0_65/bin/java -Dfile.encoding=UTF-8 -server -XX:SurvivorRatio=4 -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=50 -XX:+UseParNewGC -Xmn128m -Xmx256m -Xms256m -XX:-HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=../ -cp .:/usr/local/java/lib:/home/xiaoju/ep/as/lib/apollo-ans-2.0.8.jar:/home/xiaoju/ep/as/lib/apollo-message-2.5.3.jar:/home/xiaoju/ep/as/lib/asm-5.2.jar:/home/xiaoju/ep/as/lib/common-http-2.2.2.jar:/home/xiaoju/ep/as/lib/common-log-2.2.2.jar:/home/xiaoju/ep/as/lib/commons-2.2.2.jar:/home/xiaoju/ep/as/lib/commons-codec-1.9.jar:/home/xiaoju/ep/as/lib/commons-collections-3.2.2.jar:/home/xiaoju/ep/as/lib/commons-configuration-1.10.jar:/home/xiaoju/ep/as/lib/commons-io-2.5.jar:/home/xiaoju/ep/as/lib/commons-lang-2.4.jar:/home/xiaoju/ep/as/lib/commons-lang3-3.7.jar:/home/xiaoju/ep/as/lib/commons-logging-1.1.1.jar:/home/xiaoju/ep/as/lib/commons-pool2-2.4.2.jar:/home/xiaoju/ep/as/lib/curator-client-2.9.0.jar:/home/xiaoju/ep/as/lib/curator-framework-2.9.0.jar:/home/xiaoju/ep/as/lib/curator-recipes-2.9.0.jar:/home/xiaoju/ep/as/lib/degrade_sdk_java-1.0.11.jar:/home/xiaoju/ep/as/lib/didilog-0.0.9.2.jar:/home/xiaoju/ep/as/lib/engine-2.9.9.jar:/home/xiaoju/ep/as/lib/fluent-hc-4.5.1.jar:/home/xiaoju/ep/as/lib/guava-19.0.jar:/home/xiaoju/ep/as/lib/guava-retrying-2.0.0.jar:/home/xiaoju/ep/as/lib/httpclient-4.5.1.jar:/home/xiaoju/ep/as/lib/httpcore-4.4.3.jar:/home/xiaoju/ep/as/lib/httpmime-4.5.1.jar:/home/xiaoju/ep/as/lib/jackson-annotations-2.9.6.jar:/home/xiaoju/ep/as/lib/jackson-core-2.9.6.jar:/home/xiaoju/ep/as/lib/jackson-databind-2.9.6.jar:/home/xiaoju/ep/as/lib/jackson-module-mrbean-2.9.6.jar:/home/xiaoju/ep/as/lib/javax.servlet-api-3.1.0.jar:/home/xiaoju/ep/as/lib/jcl-over-slf4j-1.7.25.jar:/home/xiaoju/ep/as/lib/jedis-2.9.0.jar:/home/xiaoju/ep/as/lib/jetty-http-9.4.8.v20180619.jar:/home/xiaoju/ep/as/lib/jetty-io-9.4.8.v20180619.jar:/home/xiaoju/ep/as/lib/jetty-server-9.4.8.v20180619.jar:/home/xiaoju/ep/as/lib/jetty-util-9.4.8.v20180619.jar:/home/xiaoju/ep/as/lib/jline-0.9.94.jar:/home/xiaoju/ep/as/lib/joda-time-2.9.9.jar:/home/xiaoju/ep/as/lib/jsr305-2.0.2.jar:/home/xiaoju/ep/as/lib/jul-to-slf4j-1.7.25.jar:/home/xiaoju/ep/as/lib/kafka-clients-2.2.0.jar:/home/xiaoju/ep/as/lib/kryo-5.0.3.jar:/home/xiaoju/ep/as/lib/ks-common-2.2.2.jar:/home/xiaoju/ep/as/lib/ks-sdk-2.2.2.jar:/home/xiaoju/ep/as/lib/log4j-1.2.16.jar:/home/xiaoju/ep/as/lib/log4j-over-slf4j-1.7.25.jar:/home/xiaoju/ep/as/lib/logback-classic-1.2.3.jar:/home/xiaoju/ep/as/lib/logback-core-1.2.3.jar:/home/xiaoju/ep/as/lib/lz4-java-1.5.0.jar:/home/xiaoju/ep/as/lib/metric-1.5-20170427.122839-1.jar:/home/xiaoju/ep/as/lib/minlog-1.3.1.jar:/home/xiaoju/ep/as/lib/netty-3.7.0.Final.jar:/home/xiaoju/ep/as/lib/objenesis-3.1.jar:/home/xiaoju/ep/as/lib/reflectasm-1.11.9.jar:/home/xiaoju/ep/as/lib/sdk-2.9.9.jar:/home/xiaoju/ep/as/lib/slf4j-api-1.7.25.jar:/home/xiaoju/ep/as/lib/snappy-java-1.1.7.2.jar:/home/xiaoju/ep/as/lib/zookeeper-3.4.6.jar:/home/xiaoju/ep/as/lib/zstd-jni-1.3.8-1.jar:/home/xiaoju/ep/as/bin/apollo-agent-2.9.3.jar:/home/xiaoju/ep/as/conf com.xiaoju.apollo.agent.AgentMain


xiaoju     1042      1  3 Nov25 ?        04:05:29 /usr/local/java/bin/java -Xms10240m -Xmx10240m -Xss2m -XX:+UseG1GC -XX:+DisableExplicitGC -XX:MaxGCPauseMillis=200 -XX:+PrintFlagsFinal -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCApplicationStoppedTime -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=./dump -jar /home/xiaoju/task-manager/task-manager.jar


```

任务统计：

```shell
/tag-service/logs$ ll -h |grep didi.log.2021-11-26
-rw-rw-r-- 1 xiaoju xiaoju 779M Nov 26 00:59 didi.log.2021-11-26-00
-rw-rw-r-- 1 xiaoju xiaoju 470M Nov 26 01:59 didi.log.2021-11-26-01
-rw-rw-r-- 1 xiaoju xiaoju 338M Nov 26 02:59 didi.log.2021-11-26-02
-rw-rw-r-- 1 xiaoju xiaoju 232M Nov 26 03:59 didi.log.2021-11-26-03
-rw-rw-r-- 1 xiaoju xiaoju 204M Nov 26 04:59 didi.log.2021-11-26-04
-rw-rw-r-- 1 xiaoju xiaoju 324M Nov 26 05:59 didi.log.2021-11-26-05
-rw-rw-r-- 1 xiaoju xiaoju 764M Nov 26 06:59 didi.log.2021-11-26-06
-rw-rw-r-- 1 xiaoju xiaoju 2.0G Nov 26 07:59 didi.log.2021-11-26-07
-rw-rw-r-- 1 xiaoju xiaoju 2.6G Nov 26 08:59 didi.log.2021-11-26-08
-rw-rw-r-- 1 xiaoju xiaoju 2.3G Nov 26 09:59 didi.log.2021-11-26-09
-rw-rw-r-- 1 xiaoju xiaoju 2.2G Nov 26 10:59 didi.log.2021-11-26-10
-rw-rw-r-- 1 xiaoju xiaoju 1.9G Nov 26 11:59 didi.log.2021-11-26-11
-rw-rw-r-- 1 xiaoju xiaoju 1.9G Nov 26 12:59 didi.log.2021-11-26-12
-rw-rw-r-- 1 xiaoju xiaoju 1.9G Nov 26 13:59 didi.log.2021-11-26-13
-rw-rw-r-- 1 xiaoju xiaoju 2.1G Nov 26 14:59 didi.log.2021-11-26-14
-rw-rw-r-- 1 xiaoju xiaoju 2.1G Nov 26 15:59 didi.log.2021-11-26-15
-rw-rw-r-- 1 xiaoju xiaoju 2.4G Nov 26 16:59 didi.log.2021-11-26-16
-rw-rw-r-- 1 xiaoju xiaoju 2.8G Nov 26 17:59 didi.log.2021-11-26-17




```

![image-20211126120818866](https://i.loli.net/2021/11/26/ltEswYgzb7Mk2Sv.png)

代码改动： 

```java

//httpClient  spring 集成的restTemplate 参数调整方式。 下面的配置httpClient最大连接无效。
PoolingHttpClientConnectionManager manager = new PoolingHttpClientConnectionManager();
        // 每个路由上的最大并发数
        manager.setDefaultMaxPerRoute(200);
        // 最大并发连接数
        manager.setMaxTotal(5000);

        HttpClientBuilder hcb = HttpClientBuilder.create();
        HttpClient hc = hcb.setConnectionManager(manager).build();

        HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(hc);
        requestFactory.setConnectTimeout(connTimeout);
        requestFactory.setReadTimeout(readTimeout);

        restTemplate = new RestTemplate(requestFactory);
        restTemplate.getMessageConverters().add(new TextMappingJackson2HttpMessageConverter());
        LOG.info("create restTemplate with connTimeout = " + connTimeout + ", readTimeout = " + readTimeout);   

//httpClient  spring 集成的restTemplate 参数调整方式。配置有效。
static {
        HttpClientBuilder hcb = HttpClientBuilder.create().setMaxConnTotal(5000).setMaxConnPerRoute(200);
        HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory(hcb.build());
        requestFactory.setConnectTimeout(connTimeout);
        requestFactory.setReadTimeout(readTimeout);

        restTemplate = new RestTemplate(requestFactory);
        restTemplate.getMessageConverters().add(new TextMappingJackson2HttpMessageConverter());
        LOG.info("create restTemplate with connTimeout = " + connTimeout + ", readTimeout = " + readTimeout);
    }

spring:
  # yml配置的优先级高于java配置；如果yml配置和java配置同时存在，则yml配置会覆盖java配置
  http-client:
    pool:
      #连接池的最大连接数，0代表不限；如果取0，需要考虑连接泄露导致系统崩溃的后果
      maxTotalConnect: 1000
      #每个路由的最大连接数,如果只调用一个地址,可以将其设置为最大连接数
      maxConnectPerRoute: 200
      # 指客户端和服务器建立连接的超时时间,ms , 最大约21秒,因为内部tcp在进行三次握手建立连接时,默认tcp超时时间是20秒
      connectTimeout: 3000
      # 指客户端从服务器读取数据包的间隔超时时间,不是总读取时间,也就是socket timeout,ms
      readTimeout: 5000
      # 从连接池获取连接的timeout,不宜过大,ms
      connectionRequestTimout: 200
      # 重试次数
      retryTimes: 3
      charset: UTF-8
      # 长连接保持时间 单位s,不宜过长
      keepAliveTime: 10
      # 针对不同的网址,长连接保持的存活时间,单位s,如果是频繁而持续的请求,可以设置小一点,不建议设置过大,避免大量无用连接占用内存资源
      keepAliveTargetHost:
        www.baidu.com: 5
————————————————
版权声明：本文为CSDN博主「zzzgd816」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/zzzgd_666/article/details/88858181
```

1. SpringAsyncConfig  
2. 

### 异步日志：

#### 当Logger碰上Async：AsyncLogger

这是另一个具有异步体质的组件，与AsyncAppender不同，AsyncLogger使用的是第三方的异步PC框架LMAX，其中的核心阻塞队列采用了Disruptor，我在前面的文章[Disruptor实践](https://bryantchang.github.io/2019/01/15/disruptor/)中已经简单，Disruptor有两种方式，一种是普通的方式，也是我再那篇文章重点介绍的；另一种则是Translator方法，这种方法是保证publish方法一定会成功执行。



jvm参数：

/usr/local/java/bin/java -Xms6G -Xmx6G -Xss2m -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:G1LogLevel=finest -XX:MaxGCPauseMillis=20 -XX:+PrintFlagsFinal -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintTenuringDistribution -XX:+PrintHeapAtGC -XX:+PrintReferenceGC -XX:+PrintGCApplicationStoppedTime -Xloggc:/home/xiaoju/logs/tag-serv-8080/gc-%t.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=14 -XX:GCLogFileSize=100M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/xiaoju/tag-serv-8080-dump -DAPP_ID=1 -DPORT=8080 -D911nodeName=tag-serv-8080-limit-flow -jar /home/xiaoju/tag-service-online/tag-services.jar --server.port=8080





嘉华：

```
1. 去掉表达式流程中的Fork/Join之前考虑过，但是对原有代码会有大量改动。
2. 原有代码有大量先将复杂对象tostring再调用log方法导致即使使用异步日志记录依然有性能问题，所以国庆前那次优化是把几个核心链路上的日志都去掉，上周五的问题猜测是其他路径的日志也碰到一样的问题，周日已经处理了还没有全量上线。另外今天早上发现还有一个链路也有类似问题。这些链路的QPS去掉日志后可以从1000多2000上升到8000到12000，从火焰图上看去掉日志后节省了日志处理和GC的消耗。

3. 优化Spring路由，这是一个常见的问题，在国庆前完成但是没有上线。按照预发压测优化后CPU大概降低15%，QPS增加大概7%。
4. 人群判定1.0使用mvel表达式，一个常见的表达式执行大概占1.29%的cpu。对于线上某些涉及大量IN逻辑的查询（比如城市id）保存的表达式是使用OR将这些条件串联起来。在一个涉及200个城市的查询中，若果传入无效的城市mvel表达式执行的耗时会增加十倍。这个问题可以通过在保存表示式的时候写成arrays contains来解决。这个收益可能没有那么大，目前也没有实现。
5. 判定路径上目前同步发送监控数据，OdMonitorService执行大概占9%的cpu。这个收益可能没有那么大，目前也没有实现。
```

多人群判定，超时》单日志记录下来。





## **1.1** ***\*jstack分析\****

1. 找到进程ps -ef|grep ,或者jps

导出堆栈信息，查询进程PID为8564     jstack -l 8564 > 8564.stack  （文本文件即可）

3。下载8564.stack并打包为zip格式上传到[GCeasy](http://gceasy.io/index.jsp)，生成分析报告如下：

## gceasy 平台

线程7种状态：

<img src="https://upload-images.jianshu.io/upload_images/4208000-ade49093fb0fb2ae.png" alt="img" style="zoom:50%;" />



![image-20211123194609829](https://i.loli.net/2021/11/23/KwdocU1j7A3XqSI.png)





###  找到进程最耗时线程：  

 top -Hp 46924命令获得最耗费资源的线程号(pid), TIME列就是各个Java线程耗费的CPU时间

https://blog.csdn.net/Roy_70/article/details/78021551  

![image-20211117125418199](https://i.loli.net/2021/11/17/x1YUio3FCnkMtXz.png)



**使用printf处理线程的16进制形式**

```shell
[root@VM_101_10_centos output]#  printf "%x\n" 15852 
3dec
```

**使用jstack查找耗时线程的堆栈**

```html
[root@VM_101_10_centos output]#  jstack 15834 |grep 3dec
"VM Periodic Task Thread" os_prio=0 tid=0x00007f0350135000 nid=0x3dec waiting on condition 
```

```
jstack -l 67136 | grep 1065b -A20
```







### s10 工具：

1、 IBM的jca工具:IBM Thread and Monitor Dump Analyzer for Java  

https://www.ibm.com/support/pages/ibm-thread-and-monitor-dump-analyzer-java-tmda

 

2、在线分析工具，Spotify提供的Web版在线分析工具，可以将锁或条件相关联的线程聚合到一起。

[http://spotify.github.io/threaddump-analyzer](http://spotify.github.io/threaddump-analyzer/) 

 

 

### 线程状态分析 

\1. 首先关注BLOCKED 状态的线程，分析调用栈

\2. 再关注WAITING 状态的线程，分析调用栈

\3. 结合经验看问题

入手总结 4种情况：2种等待+死锁+阻塞

Deadlock：表示有死锁
Waiting on condition：等待某个资源或条件发生来唤醒自己。具体需要结合jstacktrace来分析，比如线程正在sleep，网络读写繁忙而等待
Blocked：阻塞
Waiting on monitor entry：在等待获取锁

https://www.jianshu.com/p/00b0455cd69c 

####  线程的状态说明

```
NEW：未启动的。不会出现在Dump中。
RUNNABLE：在虚拟机内执行的。运行中状态，可能里面还能看到locked字样，表明它获得了某把锁。
BLOCKED：受阻塞并等待监视器锁。被某个锁(synchronizers)給block住了。
WATING：无限期等待另一个线程执行特定操作。等待某个condition或monitor发生，一般停留在park(), wait(), sleep(),join() 等语句里。
TIMED_WATING：有时限的等待另一个线程的特定操作。和WAITING的区别是wait() 等语句加上了时间限制 wait(timeout)。
TERMINATED：已退出的。
```

Monitor

 在多线程的 JAVA程序中，实现线程之间的同步，就要说说 Monitor。 Monitor是 Java中用以实现线程之间的互斥与协作的主要手段，它可以看成是对象或者 Class的锁。每一个对象都有，也仅有一个 monitor。

```
进入区(Entrt Set)：表示线程通过synchronized要求获取对象的锁。如果对象未被锁住,则迚入拥有者;否则则在进入区等待。一旦对象锁被其他线程释放,立即参与竞争。
拥有者(The Owner)：表示某一线程成功竞争到对象锁。
等待区(Wait Set) ：表示线程通过对象的wait方法,释放对象的锁,并在等待区等待被唤醒。
```

 一个 Monitor在某个时刻，只能被一个线程拥有，该线程就是 “Active Thread”，而其它线程都是 “Waiting Thread”，分别在两个队列 “ Entry Set”和 “Wait Set”里面等候。在 “Entry Set”中等待的线程状态是 “Waiting for monitor entry”，而在“Wait Set”中等待的线程状态是 “in Object.wait()”。



## 命令总结

| 命令   | 作用                                       |
| ------ | ------------------------------------------ |
| jps    | 基础工具                                   |
| jstack | 查看某个Java进程内的线程堆栈信息           |
| jmap   | jmap导出堆内存，然后使用jhat来进行分析     |
| jhat   | jmap导出堆内存，然后使用jhat来进行分析     |
| jstat  | JVM统计监测工具                            |
| hprof  | hprof能够展现CPU使用率，统计堆内存使用情况 |



### ForkJoinPool总结：

> ForkJoinPool 主要用于实现“分而治之”的算法，特别是分治之后递归调用的函数，例如 quick sort 等。
> ForkJoinPool 最适合的是计算密集型的任务，如果存在 I/O，线程间同步，sleep() 等会造成线程长时间阻塞的情况时，最好配合使用 ManagedBlocker。



## gc分析：

![image-20211221204801917](https://s2.loli.net/2021/12/21/RZmy5JP7FzLQ9H3.png)

![image-20211221204828111](https://s2.loli.net/2021/12/21/zDXOBdhUMc3JHZA.png)

![image-20211221204916560](https://s2.loli.net/2021/12/21/Bd9jJZkwG1gUC8M.png)



![image-20211221204930491](https://s2.loli.net/2021/12/21/gF7lfy2haGjxpqV.png)

![image-20211221204944711](https://s2.loli.net/2021/12/21/4l1qsNi7YkhdKQS.png)

![image-20211221205029811](https://s2.loli.net/2021/12/21/FtdmSAeZfKob2OC.png)





