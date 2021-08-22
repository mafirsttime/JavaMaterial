





[toc]



# 资源申请

阿里云控制台：https://schedulerx2.console.aliyun.com/cn-beijing/InstanceList?namespace=6775da2a-f6d6-4ab8-9ced-848e37eb36e6&source=schedulerx

阿里云帮助文档：https://help.aliyun.com/product/147760.html?spm=5176.14256785.schedulerxContainer.8.6fbd126ddPbiwu

申请阿里云RAM用户分布式任务调度schedulerx2控制台权限，截止文档编写截止（2021-03-29），企业微信审批流程没有相应资源申请，可以发邮件to运维，参考内容如下：

阿里云分布式任务调度schedulerx2控制台权限

  【用途】XXXXXX

**！！！注意！！！**

每个子账号配置的定时任务只对当前账号可见，需要to运维申请分配给其他账号可见，以备不时之需！  【】

## 使用说明

【第一步】各环境命名空间已经创建好，只需选择相应空间，对应nacos配置namespace

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617076299089-169eea1a-b90b-4125-a886-dcaaf2fe94bd.png)

【第二】创建应用

【**！！！注意！！！**】
1、域华北2（北京）必须与应用服务器同一个



3、创建应用后“应用ID/应用key”列，“应用Key”对应nacos配置appKey

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617076427953-6032757a-3e76-4cc6-95d5-5a0e9005bd0c.png)

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077030408-0d2b3d42-4005-4a67-924f-5d283893ea2b.png)

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077073365-3de7760b-c94d-4a68-be67-0b0f465a9d03.png)

【第三步】创建任务【**！！！注意！！！**】

1、GroupID对应nacos配置groupId

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617076655953-c26094d3-5487-47e3-89f8-86f5e29ac1ee.png)

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077433365-15309c83-450a-4312-8eea-18d68c85d06c.png)

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077499018-e343971e-ebf6-44f1-b7a0-7f85cec13d38.png)

# ![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077554124-b0ddfa76-b097-4584-8b18-be44929b1085.png)

【第四步】运行一次，验证

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077625313-366ccb83-a5cc-4c46-abbb-17e104171fb4.png)

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617077736831-80d6bfd2-d263-4c31-a805-fc267f8a6dde.png)

# 应用配置

## 引入依赖

<dependency>

   <groupId>com.aliyun.schedulerx</groupId>

   <artifactId>schedulerx2-spring-boot-starter</artifactId>

   <version>1.2.4</version>

</dependency>

## Nacos配置

**配置示例（！！！请根据实际应用配置！！！）**

```yaml
spring:

   schedulerx2:

​    appKey: ZQLHPfmy6ssm3a9iiBTsmA==  （创建应用图）

​    groupId: gd-bank-center （如图）

​    namespace: 6c73b0a4-3539-4ba4-908d-9372a89804b4 （对应上图命名空间地址）

​    endpoint: addr-bj-internal.edas.aliyun.com （参考官方，北京域生产环境固定值）

​    enabled: true （开启任务）
```



## 代码实现

![img](https://cdn.nlark.com/yuque/0/2021/png/12476753/1617076798389-d0650fc5-ae28-46c6-a220-de8fd0c9946a.png)

```java
package com.gd.gcmp.bankcenter.timer;

import com.alibaba.schedulerx.worker.domain.JobContext;
import com.alibaba.schedulerx.worker.processor.JavaProcessor;
import com.alibaba.schedulerx.worker.processor.ProcessResult;
import com.gd.gcmp.bankcenter.domain.IAcctStatusSyncService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

*/**
\* *** **@Title:**  *AccNoSyncProcessor.java
\* *** **@Description:** *查询众邦二类户状态同步
\* *** **@Author** *mkwang
\* *** **@Date** *2021/3/22 10:38
\* *** **@Version** *0.0.1
\* *** **@Company:** *北京爱车家网络科技有限公司
\* ***/
*@Component
@Slf4j
public class AcctStatusSyncProcessor extends JavaProcessor {



  @Autowired
   IAcctStatusSyncService iAcctStatusSyncService;
   
   @Override
   public ProcessResult process(JobContext jobContext) throws Exception {

​    *log*.info("######二类户状态同步定时任务启动...");
​     //查询新增数据同步表
​     iAcctStatusSyncService.queryNewUidToTable();
​     //查询同步数据发送MQ 生产者
​     iAcctStatusSyncService.queryUidToMQ();
​     return new ProcessResult(true);
   }

}
```

## 趟过的坑

### 任务不执行排查

解决：1、确认定时任务服务与应用服务在同一个域

​         2、确认nacos配置中，命名空间、appKey、groupid与控制台配置一致

   3、重写的方法中不能添加事务注解！！！

![img](https://cdn.nlark.com/yuque/0/2021/png/12568213/1617092638246-dfc6fc65-8169-43e1-9d47-30eb335feae3.png)![img](https://cdn.nlark.com/yuque/0/2021/png/12568213/1617092641204-dda44ab6-bda3-4d98-aeec-3b6908ef021d.png)



