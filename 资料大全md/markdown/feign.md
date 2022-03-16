



[toc]

# 参考资料

- 什么是 Feign
- Feign 和 Openfeign 的区别
- OpenFeign 的启动原理
- OpenFeign 的工作原理
- OpenFeign 如何负载均衡

## Feign 的底层原理，总结如下：

1. 通过 @EnableFeignCleints 注解启动 Feign Starter 组件
2. Feign Starter 在项目启动过程中注册全局配置，扫描包下所有的 @FeignClient 接口类，并进行注册 IOC 容器
3. @FeignClient 接口类被注入时，通过 FactoryBean#getObject 返回动态代理类
4. 接口被调用时被动态代理类逻辑拦截，将 @FeignClient 请求信息通过编码器生成 Request
5. 交由 Ribbon 进行负载均衡，挑选出一个健康的 Server 实例
6. 继而通过 Client 携带 Request 调用远端服务返回请求响应
7. 通过解码器生成 Response 返回客户端，将信息流解析成为接口返回数据

虽然 Feign 体量相对小，但是想要一篇文章完全描述，也不太现实，所以这里都是挑一些核心点讲解，没有写到的地方还请见谅



# 1 

@FeignClient注解主要被@Target({ElementType.TYPE})修饰，表示该注解主要使用在接口上。它具备了如下的属性：

- name:指定FeignClient的名称，如果使用了Ribbon，name就作为微服务的名称，用于服务发现。
- url:url一般用于调试，可以指定@FeignClient调用的地址。
- decode404: 当发生404错误时，如果该字段为true，会调用decoder进行解码，否则抛出FeignException.
- configuration:Feign配置类，可以自定或者配置Feign的Encoder，Decoder，LogLevel，Contract。
- fallback:定义容错的处理类，当调用远程接口失败或者超时时，会调用对应的接口的容错逻辑，fallback指定的类必须实现@Feign标记的接口。
- fallbacjFactory:工厂类，用于生成fallback类实例，通过这个属性可以实现每个接口通用的容错逻辑们介绍重复的代码。
- path：定义当前FeignClient的统一前缀。

# 什么是 Feign

Feign 是声明式 Web 服务客户端，它使编写 Web 服务客户端更加容易

Feign 不做任何请求处理，通过处理注解相关信息生成 Request，并对调用返回的数据进行解码，从而实现 **简化 HTTP API 的开发**

![image-20210813002638439](/Users/mac/Library/Application Support/typora-user-images/image-20210813002638439.png)

如果要使用 Feign，需要创建一个接口并对其添加 Feign 相关注解，另外 Feign **还支持可插拔编码器和解码器**，致力于打造一个轻量级 HTTP 客户端

# Feign 和 Openfeign 的区别

Feign 最早是由 **Netflix 公司进行维护的**，后来 Netflix 不再对其进行维护，最终 **Feign 由社区进行维护**，更名为 Openfeign

> 为了少打俩字，下文简称 Opefeign 为 Feign

```xml
dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

Spring Cloud 添加了对 Spring MVC 注解的支持，并支持使用 Spring Web 中默认使用的相同 HttpMessageConverters

另外，Spring Cloud 老大哥同时集成了 Ribbon 和 Eureka 以及 Spring Cloud LoadBalancer，以在使用 Feign 时提供负载均衡的 HTTP 客户端

> 针对于注册中心的支持，包含但不限于 Eureka，比如 Consul、Naocs 等注册中心均支持

在我们 SpringCloud 项目开发过程中，使用的大多都是这个 Starter Feign

因为生产者使用 Nacos，所以消费者除了开启 Feign 注解，同时也要开启 Naocs 服务注册发现

```java
@RestController @EnableFeignClients
@EnableDiscoveryClient @SpringBootApplication
public class NacosConsumeApplication {
    public static void main(String[] args) {
        SpringApplication.run(NacosConsumeApplication.class, args);
    }

    @Autowired private DemoFeignClient demoFeignClient;

    @GetMapping("/test")
    public String test() {
        String result = demoFeignClient.sayHello("公号-源码兴趣圈");
        return result;
    }
}
```



# Feign 的启动原理

在类上标记此注解 @EnableFeignClients

注解内部的方法就不说明了，不加会有默认的配置，感兴趣可以跟下源码

```kotlin
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
@Import(FeignClientsRegistrar.class)
public @interface EnableFeignClients {...}
```

前三个注解看着平平无奇，重点在第四个 @Import 上，一般使用此注解都是想要动态注册 Spring Bean 的

# 注入@Import

通过名字也可以大致猜出来，这是 Feign 注册 Bean 使用的，使用到了 Spring 相关的接口，一起看下起了什么作用

![img](https:////upload-images.jianshu.io/upload_images/25454423-64c8d6258b9c59d5.image?imageMogr2/auto-orient/strip|imageView2/2/w/640/format/webp)

ResourceLoaderAware、EnvironmentAware 为 FeignClientsRegistrar 中两个属性**resourceLoader、environment** 赋值，对 Spring 了解的小伙伴理解问题不大

ImportBeanDefinitionRegistrar 负责动态注入 IOC Bean，分别注入 Feign 配置类、FeignClient Bean



```java
// 资源加载器，可以加载 classpath 下的所有文件
private ResourceLoader resourceLoader;
// 上下文，可通过该环境获取当前应用配置属性等
private Environment environment;

@Override
public void setEnvironment(Environment environment) {
    this.environment = environment;
}

@Override
public void setResourceLoader(ResourceLoader resourceLoader) {
    this.resourceLoader = resourceLoader;
}

@Override
public void registerBeanDefinitions(AnnotationMetadata metadata, BeanDefinitionRegistry registry) {
   // 注册 ＠EnableFeignClients 提供的自定义配置类中的相关 Bean 实例
    registerDefaultConfiguration(metadata,registry);
    // 扫描 packge，注册被 @FeignClient 修饰的接口类为 IOC Bean
    registerFeignClients(metadata, registry);
}
```

# 添加全局配置



作者：一线开发者
链接：https://www.jianshu.com/p/442d55faf1b2
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。





