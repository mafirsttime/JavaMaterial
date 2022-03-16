



# guava核心包

## 参考资料:

https://juejin.im/post/5b8df63c6fb9a019e04ebaf4

https://blog.csdn.net/a953713428/article/details/92159746



https://juejin.cn/post/6935313799746420766   个人专栏-guava调研-caffeine调研

调研方向:

1. guava缓存使用(加载缓存的模式) , 使用中问题,guava命中率监控等,
2. gson使用,性能分析
3. 并发包使用优缺点,
4. lambda表达式等等,
5. 

# Guava是什么

\1. 是google一套开源java核心类库(类似于core java)

\2. [collect](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/collect/package-summary.html) (通用集合和集合工具) #简单整理

\3. * [graph](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/graph/package-summary.html) (图相关api)

\4. functional types (函数式编程) 差异

\5. * 内存缓存 (cache)

\6. [util.concurrent](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/util/concurrent/package-summary.html) (并发工具)

\7. [io](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/io/package-summary.html) (java IO的工具类和工具方法)

\8. [hash](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/hash/package-summary.html) (hash函数和相关结构) 提供比 Object.hashCode() 更复杂的 hash 方法, 提供 Bloom filters.

\9. [primitives](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/primitives/package-summary.html) (静态工具类for java原生数据类型)

\10. Reflection (java反射工具类)

\11. [base](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/base/package-summary.html) (基本工具类和接口)

\12. eventbus (事件编程) 基于发布-订阅模式的组件通信，但是不需要明确地注册在委托对象中。 #梳理

\13. [annotations](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/annotations/package-summary.html) (通用注解很多@Beta)

\14. [math](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/math/package-summary.html)

\15. [net](http://google.github.io/guava/releases/snapshot/api/docs/com/google/common/net/package-summary.html)



- com.google.common.annotations：普通注解类型。
- com.google.common.base：基本工具类库和接口。
- com.google.common.cache：缓存工具包，非常简单易用且功能强大的JVM内缓存。
- com.google.common.collect：带泛型的集合接口扩展和实现，以及工具类，这里你会发现很多好玩的集合。
- com.google.common.eventbus：发布订阅风格的事件总线。
- com.google.common.hash： 哈希工具包。
- [com.google.common.io](http://com.google.common.io/)：I/O工具包。
- com.google.common.math：原始算术类型和超大数的运算工具包。
- [com.google.common.net](http://com.google.common.net/)：网络工具包。
- com.google.common.primitives：八种原始类型和无符号类型的静态工具包。
- com.google.common.reflect：反射工具包。
- com.google.common.util.concurrent：多线程工具包。

## Guava特点：

作为Google 开发的开源JAVA库之后所以能那么流行，我认为有几点原因

\1. 可以给开发者提供JDK之外的便利功能，使开发者能够方便的使用一些原先需要自己手写的Utility功能

\2. 可以强制（对就是强制）开发者摒弃一些不好的编程习惯，虽然这些习惯可能是JAVA本身的语言缺陷造成的

\3. 使开发者改进自己的程序模式和架构。这一点可以在 Guava 的 例如 EventBus，Filter， Ordering 等功能加以体现。



## Guava Optional

使用Optional最为NULL的替代品：例如当一个Map的get方法返回null 的时候，你完全不知道是Map中没有这个key值，还是有key值，但是这个key值对应的value是空。

Optional<Integer> possible = Optional.of(5);
possible.isPresent(); // returns true
possible.get(); // returns 5

Optional的主旨是用一个非NULL的Object去代替Null的使用，然后用isPresent方法是判断这个Object所带变的对象是否为空。



## 防御性编程

通常用来检测方法的参数的正确性，在方法的开始就对参数一定的断言，如果断言失败，就抛出异常，从而导致快速失败，guava中Preconditions类用来完成这样的检测工作。

Guava的preconditions有这样几个优点:



## 集合类

### 1.集合的创建

```java
// 普通Collection的创建
List<String> list = Lists.newArrayList();
Set<String> set = Sets.newHashSet();
Map<String, String> map = Maps.newHashMap();

// 不变Collection的创建
ImmutableList<String> iList = ImmutableList.of("a", "b", "c");
ImmutableSet<String> iSet = ImmutableSet.of("e1", "e2");
ImmutableMap<String, String> iMap = ImmutableMap.of("k1", "v1", "k2", "v2");
```

### 集合工具类

### 为什么使用不可变集合

不可变对象有很多优点，包括：

当对象被不可信的库调用时，不可变形式是安全的；
不可变对象被多个线程调用时，不存在竞态条件问题
不可变集合不需要考虑变化，因此可以节省时间和空间。所有不可变的集合都比它们的可变形式有更好的内存利用率（分析和测试细节）；
不可变对象因为有固定不变，可以作为常量来安全使用。

### 不可变集合可以用如下多种方式创建：


• copyOf 方法，如 ImmutableSet.copyOf(set);
• of 方法，如 ImmutableSet.of(“a”, “b”, “c”)或 ImmutableMap.of(“a”, 1, “b”, 2);
• Builder 工具，如
public static final ImmutableSet<Color> GOOGLE_COLORS =
ImmutableSet.<Color>builder()
.addAll(WEBSAFE_COLORS)
.add(new Color(0, 191, 255))
.build();

### 关联可变集合和不可变集合

https://guava.dev/releases/snapshot-jre/api/docs/ 开放api

| **可变集合接口**       | **属于****JDK****还是****Guava** | **不可变版本**              |
| ---------------------- | -------------------------------- | --------------------------- |
| Collection             | JDK                              | ImmutableCollection         |
| List                   | JDK                              | ImmutableList               |
| Set                    | JDK                              | ImmutableSet                |
| SortedSet/NavigableSet | JDK                              | ImmutableSortedSet          |
| Map                    | JDK                              | ImmutableMap                |
| SortedMap              | JDK                              | ImmutableSortedMap          |
| Multiset               | Guava                            | ImmutableMultiset           |
| SortedMultiset         | Guava                            | ImmutableSortedMultiset     |
| Multimap               | Guava                            | ImmutableMultimap           |
| ListMultimap           | Guava                            | ImmutableListMultimap       |
| SetMultimap            | Guava                            | ImmutableSetMultimap        |
| BiMap                  | Guava                            | ImmutableBiMap              |
| ClassToInstanceMap     | Guava                            | ImmutableClassToInstanceMap |
| Table                  | Guava                            | ImmutableTable              |



## guava cache

### 创建缓存2种方式:

```java

//缓存2种实现方式 : 1. CacheLoader实现方式``LoadingCache<String,String> cahceBuilder=CacheBuilder````.newBuilder()````.build(``new` `CacheLoader<String, String>(){````@Override````public` `String load(String key) ``throws` `Exception {````String strProValue=``"hello "``+key+``"!"``;````return` `strProValue;````}````});``cahceBuilder.put(``"begin"``, ``"code"``);``System.out.println(cahceBuilder.get(``"begin"``)); ``//code``//2.缓存的 callback实现方式``Cache<String, String> cache = CacheBuilder.newBuilder().maximumSize(``1000``).build();``String resultVal = cache.get(``"code"``, ``new` `Callable<String>() {````public` `String call() {````String strProValue=``"begin "``+``"code"``+``"!"``;````return` `strProValue;````}``});``System.out.println(``"value : "` `+ resultVal); ``//value : begin code!
```



### 缓存回收

基于容量的回收（size-based eviction）

定时回收（Timed Eviction）


CacheBuilder 提供两种定时回收的方法：
• expireAfterAccess(long, TimeUnit)：缓存项在给定时间内没有被读/写访问，则回收。请注意这种缓存的
回收顺序和基于大小回收一样。
• expireAfterWrite(long, TimeUnit)：缓存项在给定时间内没有被写访问（创建或覆盖），则回收。如果认
为缓存数据总是在固定时候后变得陈旧不可用，这种回收方式是可取的。



基于引用的回收（Reference-based Eviction）
通过使用弱引用的键、或弱引用的值、或软引用的值，Guava Cache 可以把缓存设置为允许垃圾回收.

显式清除缓存
任何时候，你都可以显式地清除缓存项，而不是等到它被回收：
• 个别清除：Cache.invalidate(key)
• 批量清除：Cache.invalidateAll(keys)
• 清除所有缓存项：Cache.invalidateAll()

### 移除监听器

通过 CacheBuilder.removalListener(RemovalListener)，你可以声明一个监听器，以便缓存项被移除时做一 些额外操作。缓存项被移除时，RemovalListener 会获取移除通知[RemovalNotification]，其中包含移除原因[RemovalCause]、键和值。

默认情况下，监听器方法是在移除缓存时同步调用的。因为缓存的维护和请求响应通常是同时进行的，代价高昂的监听器方法在同步模式下会拖慢正常的缓存请求。在这种情况下，你可以使用 RemovalListeners.asynchronous(RemovalListener, Executor)把监听器装饰为异步操作。

\#1 was removed, cause is EXPIRED

### 缓存统计功能

CacheBuilder.recordStats()用来开启 Guava Cache 的统计功能。统计打开后，Cache.stats()方法会返回 C
acheStats 对象以提供如下统计信息：
• hitRate()：缓存命中率；
• averageLoadPenalty()：加载新值的平均时间，单位为纳秒；
• evictionCount()：缓存项被回收的总数，不包括显式清除。


CacheStats{hitCount=1, missCount=2, loadSuccessCount=1, loadExceptionCount=1, totalLoadTime=312716967, evictionCount=2}



## functional types (函数式编程)

注意事项:

1. jdk8引入lambda表达式,在函数式接口定义和使用上由于 guava

\2. 过度使用 Guava 函数式编程会导致冗长、混乱、可读性差而且低效的代码。这是迄今为止最容易（也是最经常）被滥用的部分.



Guava 提供两个基本的函数式接口：
• Function<A, B>，它声明了单个方法 B apply(A input)。Function 对象通常被预期为引用透明的——没有
副作用——并且引用透明性中的”相等”语义与 equals 一致，如 a.equals(b)意味着 function.apply(a).eq
uals(function.apply(b))。
• Predicate，它声明了单个方法 boolean apply(T input)。Predicate 对象通常也被预期为无副作用函
数，并且”相等”语义与 equals 一致。



对比Java8函数式接口



## 并发编程

对JDK的并发进行抽象，提供了可回调的Future。对应的包：com.google.common.util.concurrent

ListenableFuture可以允许你注册回调方法(callbacks)，在运算（多线程执行）完成的时候进行调用, 或者在运算（多线程执行）完成后立即执行。这样简单的改进，使得可以明显的支持更多的操作，这样的功能在JDK concurrent中的Future是不支持的。



## 事件总线-发布订阅机制


提供了非常松散的发布和订阅方式，同时提供了同步和异步的订阅者执行方式，对应的包：com.google.common.eventbus

整理步骤: 详见演示demo

### 1.1、创建事件

EventBus类，是guava中消息发布和订阅的类，即订阅者通过EventBus注册并订阅事件，发布者将事件发送至EventBus中，EventBus将事件顺序的通知给时间订阅者，所以，这里有一个特别重要的注意点：事件处理器必须迅速处理完事件,否则可能会导致事件堆积。

### 1.2、创建监听

监听类，即订阅类

### 1.3、订阅事件-支持异步执行

调用EventBus的register方法完成注册。

### 1.4、发布事件

调用EventBus.post方法发送事件，EventBus会轮流调用所有的接受类型是发送事件类型的订阅者。



## gson API和性能对比

常用API:

```
String json = gson.toJson(Arrays.asList(jack1, jack2));

final String json=gson.toJson(new Person[]{jack1,jack2});final Person []jacks=gson.fromJson(json,Person[].class);
官方文档: https://github.com/google/gson/blob/master/UserGuide.md
```



4类json解析性能对比,基于JMH基准测试

json反序列化:

## jdk8 和guava 简单对比-选型

函数式编程,jdk8优于guava

https://my.oschina.net/sunhaojava/blog/907493

| 类型       | 选型                | 备注                                                         |
| ---------- | ------------------- | ------------------------------------------------------------ |
| 缓存       | guava caffeine      |                                                              |
| 集合类操作 | guava               |                                                              |
| 函数式编程 | jdk8                | JDK8 lambda表达式简化函数式接口写法                          |
| json解析   | gson或fastjson      | 优缺点和适用场景参见gson                                     |
| 异常处理   | guava Preconditions | 原理: throws Exception ,`多个Exception可以统一catch处理`或者继续向上抛异常 |



# Caffeine

SpringFramework5.0（SpringBoot2.0）放弃了Google的GuavaCache，选择了**「Caffeine」**

## GuavaCache和Caffeine差异

1. 剔除算法方面，GuavaCache采用的是**「LRU」**算法，而Caffeine采用的是**「Window TinyLFU」**算法，这是两者之间最大，也是根本的区别。
2. 立即失效方面，Guava会把立即失效 (例如：expireAfterAccess(0) and expireAfterWrite(0)) 转成设置最大Size为0。这就会导致剔除提醒的原因是SIZE而不是EXPIRED。Caffiene能正确识别这种剔除原因。
3. 取代提醒方面，Guava只要数据被替换，不管什么原因，都会触发剔除监听器。而Caffiene在取代值和先前值的引用完全一样时不会触发监听器。
4. 异步化方方面，Caffiene的很多工作都是交给线程池去做的（默认：ForkJoinPool.commonPool()），例如：剔除监听器，刷新机制，维护工作等。



Caffeine API和guava 相似度90%.

## 性能分析:



Caffeine Cache提供了三种缓存填充策略：手动、同步加载和异步加载。

### 1.手动加载

在每次get key的时候指定一个同步的函数，如果key不存在就调用这个函数生成一个值。

### 2. 同步加载

构造Cache时候，build方法传入一个CacheLoader实现类。实现load方法，通过key加载value。

### 3. 异步加载

AsyncLoadingCache是继承自LoadingCache类的，异步加载使用Executor去调用方法并返回一个CompletableFuture。异步加载缓存使用了响应式编程模型。

## 过期策略:

Caffeine的过期机制都是在构造Cache的时候申明，主要有如下几种：

1. expireAfterWrite：表示自从最后一次写入后多久就会过期；

2. expireAfterAccess：表示自从最后一次访问（写入或者读取）后多久就会过期；

3. expireAfter：自定义过期策略；

   

   `// 基于不同的到期策略进行退出``LoadingCache<String, Object> cache2 = Caffeine.newBuilder()``.expireAfter(``new` `Expiry<String, Object>() {``@Override``public` `long` `expireAfterCreate(String key, Object value, ``long` `currentTime) {``return` `TimeUnit.SECONDS.toNanos(seconds);``}``@Override``public` `long` `expireAfterUpdate(``@Nonnull` `String s, ``@Nonnull` `Object o, ``long` `l, ``long` `l1) {``return` `0``;``}``@Override``public` `long` `expireAfterRead(``@Nonnull` `String s, ``@Nonnull` `Object o, ``long` `l, ``long` `l1) {``return` `0``;``}``}).build(key -> function(key));`

## 刷新机制

在构造Cache时通过refreshAfterWrite方法指定刷新周期，例如refreshAfterWrite(10, TimeUnit.SECONDS)表示10秒钟刷新一次：

1. 构造cache时指定多久刷新一次缓存key 2.需要读一次缓存才能用V2版本值 更新到本地缓存中.
2. 适用场景: 在新value更新之前,默认使用旧Value值的场景.

需要注意的是，Caffeine的刷新机制是**「被动」**的。举个例子，假如我们申明了10秒刷新一次。我们在时间T访问并获取到值v1，在T+5秒的时候，数据库中这个值已经更新为v2。但是在T+12秒，即已经过了10秒我们通过Caffeine从本地缓存中获取到的**「还是v1」**，并不是v2。在这个获取过程中，Caffeine发现时间已经过了10秒，然后会将v2加载到本地缓存中，下一次获取时才能拿到v2。即它的实现原理是在get方法中，调用afterRead的时候，调用refreshIfNeeded方法判断是否需要刷新数据。这就意味着，如果不读取本地缓存中的数据的话，无论刷新时间间隔是多少，本地缓存中的数据永远是旧的数据！

refreshAfterWrite是在指定时间内没有被创建/覆盖，则指定时间过后，再次访问时，会去刷新该缓存，在新值没有到来之前，始终返回旧值

- 跟expire的区别是，指定时间过后，expire是remove该key，下次访问是同步去获取返回新值；而refresh则是指定时间后，不会remove该key，下次访问会触发刷新，新值没有回来时返回旧值

