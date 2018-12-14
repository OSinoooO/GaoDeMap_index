-----copyright版权-----
运行方式： python3 run.py

author: OSin
date: 2018/12/14
version: 1.0

*目前还没有处理验证码问题
    若获取不到结果，需要到官网手动解锁验证码，再把网页 cookie 复制到 run.conf 文件下替换。

*linux下运行需要手动进行配置

input文件夹：
    1.city_names.txt文件：把需要查询的地址写入该文件。地址间用 "," 分隔（注意是英文字符）。
    2.run.conf文件：保存cookie。

output文件夹：
    infos文件：保存坐标结果

