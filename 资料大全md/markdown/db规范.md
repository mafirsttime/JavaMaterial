[toc]



# 数据库设计规范

目的

------

规范化和标准化MySQL规范设计 提高MySQL性能

# 范围

MySQL数据库开发和使用人员

# 基础操作规范

1.数据库访问高峰禁止DDL 2.访问高峰禁止对大表做全表扫描 3.更新和删除单次操作在一万以下串行提交 4.禁止在生产数据库做开发测试

# 数据库设计规范 



## 操作规范

1. 【强制】禁止有super权限的应用程序账号存在
2. 【强制】禁止在生产库做开发测试

1. 【强制】DDL/DML操作必须申请走流程
2. 【强制】访问高峰期禁止执行DDL操作

1. 【强制】对单表的多次alter操作必须合并为一次操作
2. 【强制】禁止人为进行锁表

1. 【强制】删表操作，一律先对表做重命名，禁止直接删表
2. 【强制】批量更新或删除数据必须提前备份，单次操作数据量不能超过5000行

1. 【强制】除支付与订单核心业务，禁止使用主库查询
2. 【强制】禁止对表进行全表扫描，必须使用过滤条件

1. 【强制】禁止存储明文密码
2. 【强制】禁止存放文件、图片等大数据。

1. 【强制】禁止在线上环境进行压力测试。
2. 【推荐】提交线上建表需求，必须注明所有相关SQL

## 设计规范

1.【推荐】字段允许适当冗余，以提高查询性能，但必须考虑数据一致。冗余字段应遵循:

不是频繁修改的字段。 不是 varchar 超长字段，更不能是 text 字段。 正例:商品类目名称使用频率高，字段长度短，名称基本一成不变，可在相关联的表中冗余存 储类目名称，避免关联查询。

2.【推荐】单表行数超过 500 万行或者单表容量超过 2GB，才推荐进行分库分表。

3.【推荐】id必须是主键，每个表必须有主键，且保持增长趋势的， 小型系统可以依赖于 MySQL 的自增主键。

4.【强制】id类型没有特殊要求，必须使用bigint unsigned，禁止使用int，即使现在的数据量很小。

5.【推荐】字段尽量设置为 NOT NULL， 为字段提供默认值。 如字符型的默认值为一个空字符值串’’;数值型默认值为数值 0;逻辑型的默认值为数值 0。

6.【强制】表字符集 utf8mb4，字段字符集 utf8mb4_general_ci

7.【推荐】每个字段和表必须提供清晰的注释

例子： 1 *2* 3* 状态段描述

8.【强制】任何字段如果为非负数，必须是 unsigned

## 命名规范

1.【强制】表达是与否概念的字段，数据类型是 unsigned tinyint(1) ( 0表示否，1表示是)。

正例:表达逻辑删除的字段名 deleted，0表示正常，1表示删除。

2.【强制】表名、字段名必须使用小写字母或数字，禁止出现数字开头，禁止两个下划线中间只 出现数字。

正例:health_user，rdc_config，level3_name 反例:HealthUser，rdcConfig，level_3_name

3.【推荐】所有时间字段，都包含 time关键字

4.【强制】禁用保留字，如 desc、range、match、delayed、count、source 等，请参考 MySQL 官方保留字。

5.【强制】主键索引名为 pk_字段名;唯一索引名为 uk_字段名;普通索引名则为 idx_字段名。

说明:pk *即 primary key;uk* 即 unique key;idx_ 即 index 的简称。

6.【强制】小数类型为 decimal，禁止使用 float 和 double。

说明:float 和 double 在存储的时候，存在精度损失的问题，很可能在值的比较时，得到不 正确的结果。如果存储的数据范围超过 decimal 的范围，建议将数据拆成整数和小数分开存储。

7.【强制】如果存储的字符串长度几乎相等，使用 char 定长字符串类型 比如open_id等。

8.【强制】varchar 是可变长字符串，不预先分配存储空间，长度不要超过 5000，如果存储长 度大于此值，定义字段类型为 text，独立出来一张表，用主键来对应，避免影响其它字段索 引效率。

9.【强制】表必备三字段:id,ctime, mtime,deleted。 说明:其中id必为主键，类型为unsigned bigint、单表时自增、步长为1。

10.【强制】所有命名必须使用全名，有默认约定的除外，如果超过 30 个字符，使用缩写，请尽量名字易懂简短，

如 description -> desc;information -> info;address -> addr 等

11.【推荐】表的命名最好是加上“业务名称_表的作用”。

正例:insu_company / car_config

12.【推荐】库名与应用名称尽量一致。如car

13.【推荐】如果修改字段含义或对字段表示的状态追加时，需要及时更新字段注释

14.【推荐】临时库、临时表名必须以tmp为前缀，以日期为后缀

15.【推荐】备份库、备份表名必须以bak为前缀，以日期为后缀

## 类型规范

1.表示状态字段 使用tinyint 不设置UNSIGNED类型,存储-128到127的整数，负数代表失败或否，正数代表成功或是，注释必须清晰地说明每个枚举的含义 比如审核状态等

2.表示boolean类型的都使用TINYINT(1)，例如 deleted;其余所有时候都使用TINYINT(4)。

TINYINT(4),这个括号里面的数值并不是表示使用多大空间存储，而是最大显示宽度，并且只有字段指定zerofill时有用，没有zerofill，(m)就是无用的,例如id BIGINT ZEROFILL NOT NULL,所以建表时就使用默认就好了，不需要加括号了，除非有特殊需求，例如TINYINT(1)代表boolean类型。 TINYINT(1)，TINYINT(4)都是存储一个字节，并不会因为括号里的数字改变。例如TINYINT(4)存储22则会显示0022，因为最大宽度为4，达不到的情况下用0来补充。

3.【参考】合适的字符存储长度，不但节约数据库表空间、节约索引存储，更重要的是提升检索速度。

| **类型**  | **字节** | **表示范围**                                                |
| --------- | -------- | ----------------------------------------------------------- |
| tinyint   | 1        | 无符号值: 0～255;有符号值： -128~127                        |
| smallint  | 2        | 无符号值: 0～65536;有符号值： -32768~32767                  |
| mediumint | 3        | 无符号值: 0～16777215;有符号值： -8388608~8388607           |
| int       | 4        | 无符号值: 0～4294967295;有符号值： -2147483648～2147483647  |
| bigint    | 8        | 无符号值: 0~((2³²×²)-1);有符号值： -(2³²×²)/2 ~ (2³²×²)/2-1 |

4.非负的数字类型字段，都添加上 UNSINGED

4.【推荐】标准日期时间字段推荐使用timestamp类型，保存未来时间的字段推荐使用datetime类型,不要使用字符串类型。

格式:’YYYY-MM-DD HH:MM:SS’，必须设置默认值。字段中必须设置创建时间(ctime)和更新时间(mtime)

ctime/mtime 默认值使用CURRENT_TIMESTAMP,mtime字段根据业务需求，选择是否使用自动更新。

5.【推荐】字符串VARCHAR(N), 其中 N表示字符个数，请尽量减少 N 的大小；

6.【强制】Blob 和 Text 类型所存储的数据量大，删除和修改操作容易在数 据表里产生大量的碎片，避免使用 Blob 或 Text 类型

## 索引规范

1.【强制】业务上具有唯一特性的字段，即使是多个字段的组合，也必须建成唯一索引。

不要以为唯一索引影响了 insert 速度，这个速度损耗可以忽略，但提高查找速度是明 显的; 另外，即使在应用层做了非常完善的校验控制，只要没有唯一索引，根据墨菲定律，必然有脏数据产生。

2.【强制】超过三个表禁止 join。需要 join 的字段，数据类型必须绝对一致;多表关联查询时， 保证被关联的字段需要有索引(驱动表和被驱动表中关联字段要有索引)，禁止使用Block Nested Loop Join。

即使双表 join 也要注意表索引、SQL 性能。

3.【强制】禁止在索引列进行数学运算和函数运算。

4.【强制】页面搜索严禁左模糊或者全模糊，如果需要请走搜索引擎来解决。 索引文件具有 B-Tree 的最左前缀匹配特性，如果左边的值未确定，那么无法使用此索引。

5.【推荐】如果有 order by 的场景，请注意利用索引的有序性。order by 最后的字段是组合索引的一部分，并且放在索引组合顺序的最后，避免出现 file_sort 的情况，影响查询性能。

正例:where a=? and b=? order by c; 索引:a_b_c 反例:索引中有范围查找，那么索引有序性无法利用，如:WHERE a>10 ORDER BY b; 索引 a_b 无法排序。

6.【推荐】利用覆盖索引来进行查询操作，避免回表。

正例:能够建立索引的种类:主键索引、唯一索引、普通索引，而覆盖索引是一种查询的效果，用explain的结果，extra列会出现:using index。index(a,b,c) 相当于index(a)、index(a,b)、index(a,b,c)

7.【推荐】利用延迟关联或者子查询优化超多分页场景。

说明:MySQL并不是跳过 offset 行，而是取 offset+N 行，然后返回放弃前 offset 行，返回 N 行， 那当 offset 特别大的时候，效率就非常的低下，要么控制返回的总页数，要么对超过特定阈值的页数进行 SQL 改写。

正例:先快速定位需要获取的 id 段，然后再关联: SELECT a.* FROM 表 1 a, (select id from 表 1 where 条件 LIMIT 100000,20 ) b where a.id=b.id 

8.【推荐】SQL 性能优化的目标:至少要达到 range 级别，要求是 ref 级别，如果可以是 consts 最好。

说明: consts 单表中最多只有一个匹配行(主键或者唯一索引)，在优化阶段即可读取到数据。ref 指的是使用普通的索引(normal index)。range 对索引进行范围检索。

反例:explain 表的结果，type=index，索引物理文件全扫描，速度非常慢，这个 index 级 别比较 range 还低，与全表扫描是小巫见大巫。

9.【推荐】建组合索引的时候，区分度最高的在最左边。

正例:如果 where a=? and b=? ，a 列的几乎接近于唯一值，那么只需要单建 idx_a 索引即 可。

说明:存在非等号和等号混合判断条件时，在建索引时，请把等号条件的列前置。如:where a>? and b=? 那么即使 a 的区分度更高，也必须把 b 放在索引的最前列 idx_b_a。

10【推荐】防止因字段类型不同造成的隐式转换，导致索引失效。

例子 关联字段 分别utf8 和utf8mb4 无法使用索引 参考地址：https://mp.weixin.qq.com/s/ns9eRxjXZfUPNSpfgGA7UA?

11.【参考】创建索引时避免有如下极端误解

宁滥勿缺。认为一个查询就需要建一个索引。 宁缺勿滥。认为索引会消耗空间、严重拖慢更新和新增速度。 抵制惟一索引。认为业务的惟一性一律需要在应用层通过“先查后插”方式解决。

12.【推荐】单张表索引不超过5个，单个索引中字段数不能超过5个。

13.【强制】超过三张表禁用join，关联字段数据类型必须统一、必须使用索引，严禁出现BNL查询。

14【推荐】字符串长度超过20的字段，使用前缀索引替代全字段索引，通过count(distinct left(列名, 索引长度))/count(*)的区分度来确定前缀长度。

15.总结

- 索引占磁盘空间，不要重复的索引，尽量短
- 只给常用的查询条件加索引

- 过滤性高的列建索引，取值范围固定的列不建索引
- 唯一的记录添加唯一索引

- 频繁更新的列不要建索引
- 不要对索引列运算

- 同样过滤效果下，保持索引长度最小
- 合理利用组合索引，注意索引字段先后顺序

- 多列组合索引，过滤性高的字段最前
- order by 字段建立索引，避免 filesort

- 组合索引，不同的排序顺序不能使用索引
- <>!=无法使用索引

## SQL规范

1.【强制】不要使用 count(列名)或 count(常量)来替代 count()，count()是 SQL92 定义的 标准统计行数的语法，跟数据库无关，跟 NULL 和非 NULL 无关。

count(*)会统计值为 NULL 的行，而 count(列名)不会统计此列为 NULL 值的行。

2.【强制】不能使用count(distinct col) 计算该列除 NULL 之外的不重复行数，count(distinct col1, col2) 如果其中一列全为NULL，那么即使另一列有不同的值，也返回为0。

3.【强制】当某一列col的值全是 NULL 时，count(col)的返回结果为 0，但 sum(col)的返回结果为 NULL，因此使用 sum()时需注意 NPE 问题。

正例:可以使用如下方式来避免sum的NPE问题:SELECT IF(ISNULL(SUM(g)),0,SUM(g)) FROM table;

4.【强制】使用 ISNULL()来判断是否为 NULL 值。 说明:NULL 与任何值的直接比较都为 NULL。

- NULL<>NULL的返回结果是NULL，而不是false。
- NULL=NULL的返回结果是NULL，而不是true。

- NULL<>1的返回结果是NULL，而不是true。

5.【强制】 在代码中写分页查询逻辑时，若 count 为 0 应直接返回，避免执行后面的分页语句。

6.【强制】不得使用外键与级联，一切外键概念必须在应用层解决。

外键与级联更新适用于单机低并发，不适合分布式、高并发集群;级联更新是强阻 塞，存在数据库更新风暴的风险;外键影响数据库的插入速度。

7.【强制】禁止使用存储过程，存储过程难以调试和扩展，更没有移植性。

8.【强制】数据订正时，删除和修改记录时，要先 select，避免出现误删除，确认无误才能执行更新语句。

9.【推荐】in操作能避免则避免，若实在避免不了，需要仔细评估 in 后边的集合元素数量，控制在 1000 个之内。

10.【推荐】select语句尽量使用具体字段，不使用*。

11.【参考】减少与数据库交互次数，尽量使用长连接，定期释放连接资源。

12.【推荐】不要写一个大而全的数据更新接口。

不管是不是自己的目标更新字 段，都进行 update table set c1=value1,c2=value2,c3=value3; 这是不对的。 执行 SQL 时，不要更新无改动的字段，一是易出错;二是效率低;三是增加 binlog 存储。

13.【推荐】合理使用事务

注意事务两阶段提交特性(影响并发度的操作，安排的事物的最后面)

14.【强制】禁止单条SQL同时更新多个表。

15.【推荐】尽量使用UNION ALL 而不是 UNION。

16.【强制】禁止使用大SQL，要求拆分成小SQL。

17.【强制】防止出现带有隐式转换查询。

情况1:  字符串与数字对比下数据类型转换原则：字符串转数字

情况2: 字符集不同时字符集转换原则：由子集向超集转换

情况3: 在索引字段过滤是存在数学运算

18.【总结】

- 能够快速缩小结果集的 WHERE 条件写在前面，如果有恒量条 件，也尽量放在前面 ，例如 where 1=1
- 避免使用 GROUP BY、DISTINCT 等语句的使用，避免联表查 询和子查询

- 能够使用索引的字段尽量进行有效的合理排列
- 针对索引字段使用 >, >=, =, <, ><=, IF NULL 和 BETWEEN 将会 使用索引，如果对某个索引字段进行 LIKE 查询，使用 LIKE ‘%abc%’ 不能使用索引，使用 LIKE ‘abc%’ 将能够使用索引

- 在 SQL 里禁止使用 MySQL部分自带函数，索引将失效
- 避免直接使用 select *,只取需要的字段，增加使用覆盖索引使用的可能

- 对于大数据量的查询，尽量避免在 SQL 语句中使用 order by 字句
- 连表查询的情况下，要确保关联条件的数据类型一致，避免嵌套子查询

- 对于连续的数值，使用 between 代替 in
- where 语句中不要使用 CASE 条件

- 当只要一行数据时使用 LIMIT 1



## 避免使用数据库保留字

| ADD                | ALL                 | ALTER              |
| ------------------ | ------------------- | ------------------ |
| ANALYZE            | AND                 | AS                 |
| ASC                | ASENSITIVE          | BEFORE             |
| BETWEEN            | BIGINT              | BINARY             |
| BLOB               | BOTH                | BY                 |
| CALL               | CASCADE             | CASE               |
| CHANGE             | CHAR                | CHARACTER          |
| CHECK              | COLLATE             | COLUMN             |
| CONDITION          | CONNECTION          | CONSTRAINT         |
| CONTINUE           | CONVERT             | CREATE             |
| CROSS              | CURRENT_DATE        | CURRENT_TIME       |
| CURRENT_TIMESTAMP  | CURRENT_USER        | CURSOR             |
| DATABASE           | DATABASES           | DAY_HOUR           |
| DAY_MICROSECOND    | DAY_MINUTE          | DAY_SECOND         |
| DEC                | DECIMAL             | DECLARE            |
| DEFAULT            | DELAYED             | DELETE             |
| DESC               | DESCRIBE            | DETERMINISTIC      |
| DISTINCT           | DISTINCTROW         | DIV                |
| DOUBLE             | DROP                | DUAL               |
| EACH               | ELSE                | ELSEIF             |
| ENCLOSED           | ESCAPED             | EXISTS             |
| EXIT               | EXPLAIN             | FALSE              |
| FETCH              | FLOAT               | FLOAT4             |
| FLOAT8             | FOR                 | FORCE              |
| FOREIGN            | FROM                | FULLTEXT           |
| GOTO               | GRANT               | GROUP              |
| HAVING             | HIGH_PRIORITY       | HOUR_MICROSECOND   |
| HOUR_MINUTE        | HOUR_SECOND         | IF                 |
| IGNORE             | IN                  | INDEX              |
| INFILE             | INNER               | INOUT              |
| INSENSITIVE        | INSERT              | INT                |
| INT1               | INT2                | INT3               |
| INT4               | INT8                | INTEGER            |
| INTERVAL           | INTO                | IS                 |
| ITERATE            | JOIN                | KEY                |
| KEYS               | KILL                | LABEL              |
| LEADING            | LEAVE               | LEFT               |
| LIKE               | LIMIT               | LINEAR             |
| LINES              | LOAD                | LOCALTIME          |
| LOCALTIMESTAMP     | LOCK                | LONG               |
| LONGBLOB           | LONGTEXT            | LOOP               |
| LOW_PRIORITY       | MATCH               | MEDIUMBLOB         |
| MEDIUMINT          | MEDIUMTEXT          | MIDDLEINT          |
| MINUTE_MICROSECOND | MINUTE_SECOND       | MOD                |
| MODIFIES           | NATURAL             | NOT                |
| NO_WRITE_TO_BINLOG | NULL                | NUMERIC            |
| ON                 | OPTIMIZE            | OPTION             |
| OPTIONALLY         | OR                  | ORDER              |
| OUT                | OUTER               | OUTFILE            |
| PRECISION          | PRIMARY             | PROCEDURE          |
| PURGE              | RAID0               | RANGE              |
| READ               | READS               | REAL               |
| REFERENCES         | REGEXP              | RELEASE            |
| RENAME             | REPEAT              | REPLACE            |
| REQUIRE            | RESTRICT            | RETURN             |
| REVOKE             | RIGHT               | RLIKE              |
| SCHEMA             | SCHEMAS             | SECOND_MICROSECOND |
| SELECT             | SENSITIVE           | SEPARATOR          |
| SET                | SHOW                | SMALLINT           |
| SPATIAL            | SPECIFIC            | SQL                |
| SQLEXCEPTION       | SQLSTATE            | SQLWARNING         |
| SQL_BIG_RESULT     | SQL_CALC_FOUND_ROWS | SQL_SMALL_RESULT   |
| SSL                | STARTING            | STRAIGHT_JOIN      |
| TABLE              | TERMINATED          | THEN               |
| TINYBLOB           | TINYINT             | TINYTEXT           |
| TO                 | TRAILING            | TRIGGER            |
| TRUE               | UNDO                | UNION              |
| UNIQUE             | UNLOCK              | UNSIGNED           |
| UPDATE             | USAGE               | USE                |
| USING              | UTC_DATE            | UTC_TIME           |
| UTC_TIMESTAMP      | VALUES              | VARBINARY          |
| VARCHAR            | VARCHARACTER        | VARYING            |
| WHEN               | WHERE               | WHILE              |
| WITH               | WRITE               | X509               |
| XOR                | YEAR_MONTH          | ZEROFILL           |





操作规范举例



![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611804963728-bee62d05-eba3-4b51-8eb1-35eae6cc2993.png)



设计规范



![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913244174-c1d7d27f-4cff-4fcc-96ad-fad5d26c72ef.png)

典型分析

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611805246907-9090cf78-de74-4395-9f9d-ae3694a040ee.png)

NOT NULL 约束



![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913546805-75784296-5806-4b02-ab48-02deb83f0969.png)



场景1: count数据丢失

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913571330-e5041f95-359d-4d17-945c-ccfd1d829b8c.png)



场景2: distinct数据丢失

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913845593-1f3c43bc-7c8e-4400-bdc4-d76310106669.png)

场景3: select 丢失

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913891124-94107582-029d-47a5-9204-b50d0d3955ee.png)

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913898829-5baac2cc-c696-46f3-bcf4-1db82381c749.png)

场景4: 空指针

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913948600-e1a640db-791a-48f8-8fc9-b84f78ba1c55.png)



场景5: is not null 约束

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913994883-cd00cc53-ee7d-43b4-aad6-2cef9656176b.png)





order by 

![img](https://cdn.nlark.com/yuque/0/2021/png/12389240/1611913193509-c11b8495-d73c-4adf-982a-fb7a1c0726a4.png)

