# 图书借阅管理系统

## 模拟学生在图书馆借阅图书的管理内容，包括查询图书、借书、借阅后的查询、统计、超期罚款等的处理情况。

1. 可随时查询出可借阅图书的详细情况，如图书便号、图书名称、出版日期、出版社、图书存放位置、图书总数量等，这样便于学生选借。
2. 学生查询图书情况后即可借阅所需图书。可借阅多种图书，每种图书一般只借一本，若已有图书超期请交清罚金后才能开始本次借阅。
3. 为了唯一标识每一学生，图书室办借书证需如下信息：学生姓名、学生系别、学生所学专业、借书上限数及唯一的借书证号。
4. 每一学生一次可借多本书，但不能超出该生允许借阅上限数（上限数自定）。每个学生可多次借阅，允许重复借阅同一本书。规定借书期限为两个月，超期每天罚两分（自定）。

## 要求：

1. 能对各库表进行输入、修改、删除、添加、查询等基本操作
2. 能明细查询某学生的借书情况及图书的借出情况
3. 能统计出某图书的总借出数量与库存量及某学生借书总数，当天为止总罚金等。
4. 其他必要的查询、统计功能。

## 使用注意

1. 需要SQL server作为数据库的依赖
2. 数据库默认连接方式为TCP/IP sa账户 密码123456 连接配置在model/database文件里改

## 截图

### 登录

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/signin.png" width="100%" height="100%">

### 注册

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/signup.png" width="100%" height="100%">

### 管理员

* 图书管理

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/1.png" width="100%" height="100%">

* 插入新书

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/2.png" width="100%" height="100%">

* 用户管理

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/3.png" width="100%" height="100%">

* 修改用户信息

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/4.png" width="100%" height="100%">

* 借阅管理

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/5.png" width="100%" height="100%">

* 借阅日志管理

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/6.png" width="100%" height="100%">

### 学生

* 图书查询

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/s1.png" width="100%" height="100%">

* 借阅管理

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/s2.png" width="100%" height="100%">

* 日志查询

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/s3.png" width="100%" height="100%">

* 个人信息管理

<img src="https://github.com/ssynn/library_system/blob/master/screenshots/s4.png" width="100%" height="100%">