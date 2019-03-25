# 数据可视化web端

## 功能简介

Web端采用MVC架构，实现**整体数据显示**、**单一查询**和**批量查询**这三个功能。其中整体数据显示以分页表格的形式呈现数据库中所有的数据（450万条打好标签的数据）；单一查询通过搜索商品信息，显示出对应的分类信息；批量查询通过上传文件的方式显示出该文件所有的商品信息以及对应的分类信息。

## 开发工具与技术

|   分类  | 名称 |   版本   |
| :-----: | :----: | :-----: |
| 开发工具 | MyEclipse |   4.6.1   |
| 应用平台 | Tomcat |   9.0   |
| 开发平台 | JDK |   1.8.0   |
| 数据库平台 | Mysql |   5.7.21   |


## 操作指南

**Two choices**   

1.Clone `DataViewWeb`;基于`MyEclipse`软件;点击运行`WebRoot`里的`index.jsp`.  
  
2.直接点击该地址:[数据可视化web端](http://bestdoublelin.com:8080/fuwu/showdata).

## 注意事项

* 上传文件格式必须为 utf-8（只能是utf-8，utf-8-bom等的编码都不可以）编码的csv文件。
* 上传文件时，必须要先选择文件并上传后才可以查询。
* 手动输入单一查询必须注意空格，部分商品的描述是带有空格的。
* 单一查询，点击查询后发现没有结果，没有反应，是因为数据库中没有此条信息。

## 图示

    整体数据显示
![](https://github.com/Cynicicm/Service-outsourcing/blob/master/DataViewWeb/Image/%E6%95%B4%E4%BD%93%E6%95%B0%E6%8D%AE%E6%98%BE%E7%A4%BA.png)  


    单一数据查询
![](https://github.com/Cynicicm/Service-outsourcing/blob/master/DataViewWeb/Image/%E5%8D%95%E4%B8%80%E6%95%B0%E6%8D%AE%E6%9F%A5%E8%AF%A2.png)  


    批次数据查询
![](https://github.com/Cynicicm/Service-outsourcing/blob/master/DataViewWeb/Image/%E6%89%B9%E6%AC%A1%E6%95%B0%E6%8D%AE%E6%9F%A5%E8%AF%A2.png)  

## 开发人员  

**感谢[张琳琳同学](https://github.com/bestdoubleLin)**
