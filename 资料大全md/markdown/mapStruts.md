



# 参考资料

https://www.cnblogs.com/mmzs/p/12735212.html  入门

文档地址：http://mapstruct.org/documentation/stable/reference/html/   

- Github地址：https://github.com/mapstruct/mapstruct/
- 使用例子：https://github.com/mapstruct/mapstruct-examples
- [Homepage](http://mapstruct.org/)
- [Source code](https://github.com/mapstruct/mapstruct/)
- [Downloads](https://sourceforge.net/projects/mapstruct/files/)
- [Issue tracker](https://github.com/mapstruct/mapstruct/issues)
- [User group](https://groups.google.com/forum/?hl=en#!forum/mapstruct-users)
- [CI build](https://github.com/mapstruct/mapstruct/actions/)


## mapStruts总结：

1.  基础用法：
2. https://blog.csdn.net/qq_40194399/article/details/110162124



```java
@Mapper(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE, unmappedTargetPolicy = ReportingPolicy.IGNORE)  //类转换中的 空值 或者没有对应的属性 ，不需要再 mappings 忽略了，自动忽略
public interface CouponGroupStartConverter {

    CouponGroupStartConverter INSTANCE = Mappers.getMapper(CouponGroupStartConverter.class);

  //java表达式集成到代码中
    @Mappings(value = {
        @Mapping(target = "url",expression = "java(com.gd.aep.common.constant.Constants.COUPON_GROUP_SHOW_URL_PREFIX+bo.getId())")
    })
    CouponGroupResponse toCouponGroupResponse(CouponGroupBO bo);
  
  @Mappings(value = {
        @Mapping(target = "id", expression = "java(entity.getId().toString())")
    })
    MainPageBO toMainPageBO(MainPageEntity entity);
  
  
  
  @Mappings(value = {
        @Mapping(target = "couponTemplateList", source = "couponTemplateList"),
        @Mapping(target = "couponTemplateIds", source = "couponTemplateIds"),
    })
  @Mapping(target = "applyReason",expression = "java(com.gd.aep.tp.common.constant.OrderRefundReasonEnum.getEnum(paramters.getApplyReason()).getDesc())"),
        @Mapping(target = "applyType",expression = "java(com.gd.aep.tp.common.constant.AfterSaleTypeEnum.REFUND.getCode())"),
        @Mapping(target = "auditStatus",expression = "java(com.gd.aep.tp.common.constant.AfterSaleAuditStatusEnum.AUDIT_SUCCESS.getCode())"),
  
  //日期和 string转换- mapstruct日期字符串
  CreateOrderConverter INSTANCE = Mappers.getMapper(CreateOrderConverter.class);

    @Mapping(source = "validityStartTime", target = "validityStartTime", qualifiedByName = "toDateString")
    @Mapping(source = "validityEndTime", target = "validityEndTime", qualifiedByName = "toDateString")
    VerificationRuleKey toKey(ItemVerificationRuleDTO dto);

    @Named("toDateString")
    default String toDateString(Date date) {
        if (date == null) {
            return null;
        }
        return DateFormatUtils.format(date, "yyyy-mm-dd");
    }
  
  /** 2个参数的对应 返回类赋值，	
  */
   @Mapping(source = "result.skuSpeResults", target = "skuSpeResults")
    @Mapping(source = "param.context", target = "context")
    @Mapping(source = "param.skuNum", target = "skuNum")
    @Mapping(source = "param.skuId", target = "skuId")
    OrderSkuCommonResult toOrderSkuCommonResult(SkuDTO result, OrderSkuCommonParam param);


```



### **引发的错误:**

```java
 Ambiguous mapping methods found for mapping collection element to 
 dto.TicketDTO: dto.TicketDTO mapToTicketDTO(model.Ticket ticket), 
 dto.TicketWithCommentsDTO mapToTicketWithCommentsDTO(model.Ticket ticket).
```

**最佳答案 **: https://mapstruct.org/documentation/stable/reference/html/

好吧，事实证明这是一个简单的修复，确实是缺少的配置问题。缺少的是`@IterableMapping`批注。

一旦将`elementTargetType`设置为正确的类型，一切都会按预期进行。 关于java - 如何从相同的源类映射扩展的DTO

```java
@IterableMapping(elementTargetType = TicketDTO.class)
    List<TicketDTO> mapToTicketDTOList(Collection<Ticket> tickets);
```

## 1 

## 7.更新现有的Bean

 

>   某些情况下，你需要不创建目标类型的新实例，而是更新该类型的现有实例的映射。可以通过为目标对象添加参数并使用@MappingTarget标记此参数来实现此类映射。

数据类型转换： 格式转换等

![img](https://img-blog.csdnimg.cn/img_convert/67f6aa2c839147c89a941d04c0bf3f1c.png)



## 映射集合，各种map 和list 都可以转换

>   在映射集合的时候，我们同样可以进行类型之间的转换，如下所示使用@MapMapping注解指定输出类型即可。
>
>  当然MapStruct也支持其他各种类型的集合映射

![img](https://img-blog.csdnimg.cn/img_convert/4047e0983874a8b43e0631535eb14f8d.png)

## 12.映射枚举

    MapStruct支持生成将一个Java枚举类型映射到另一个Java枚举类型的方法。默认情况下，源枚举中的每个常量都映射到目标枚举类型中具有相同名称的常量。如果需要，可以使用@ValueMapping注解将源枚举中的常量映射到具有其他名称的常量。源枚举中的几个常量可以映射到目标类型中的相同常量。
    
    Student中是SexEnum枚举，而StudentVO中是Sex2Enum，且枚举中的值是一致时，我们需要将Student中的映射到StudentVO中，此时只需要使用@Mapping来指定映射源和目标源的名称即可
————————————————
版权声明：本文为CSDN博主「大猫的Java笔记（公众号同号）」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_40194399/article/details/110162124



## 14.自定义映射


    在某些情况下，可能需要定制生成的映射方法，在目标对象中设置一个无法由MapStruct生成的方法实现时，可以使用自定义映射来完成。假如我们的StudentVO中的age是无法生成的。
    
    首先定义类，然后实现Mapper接口，在重写的方法中写上需要的逻辑，且在Mapper接口中加入@DecorateWith注解，指定自定义映射的class。
————————————————
版权声明：本文为CSDN博主「大猫的Java笔记（公众号同号）」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_40194399/article/details/110162124



### beanUtil.copyProperties问题：

1. Spring的BeanUtils的CopyProperties方法需要对应的属性有getter和setter方法；
2. 如果存在属性完全相同的内部类，但是不是同一个内部类，即分别属于各自的内部类，则spring会认为属性不同，不会copy；
3. 泛型只在编译期起作用，不能依靠泛型来做运行期的限制；
4. 最后，spring和apache的copy属性的方法源和目的参数的位置正好相反，所以导包和调用的时候都要注意一下。









