[toc]



# 请求：

https://blog.csdn.net/shangrila_kun/article/details/89600874  

下面是对@PathVariable，@RequestParam，@RequestBody三者的比较

注解	支持的类型	支持的请求类型	支持的Content-Type	请求示例

##  



@PathVariable	url	GET	所有	/test/{id}
@RequestParam	url	GET	所有	/test?id=1
Body	POST/PUT/DELETE/PATCH	form-data或x-www.form-urlencoded	id:1
@RequestBody	Body	POST/PUT/DELETE/PATCH	json	{"id":1}
将接口改成以@RequestBody注解方式接受json请求数据，而后将接收到的json数据转化为json对象，可以使用json对象的get()方法取得参数值，代码如下：

```java
@PostMapping("/account")
public Object insertAccount(@RequestBody JSONObject jsonParam) {
	String userName=jsonParam.get("userName").toString()
	...
```



