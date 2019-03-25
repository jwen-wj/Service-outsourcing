<%@ page language="java" import="java.util.*" contentType="text/html; charset=utf-8" %>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <base href="<%=basePath%>">
    
    <title>My JSP 'index.jsp' starting page</title>
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">    
	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
	<meta http-equiv="description" content="This is my page">
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
  </head>
  <style type="text/css">
	
	ul{
		list-style-type:none;
	}
	
	a{
		text-decoration:none;
		out-line: none;
		color: #000;
	}
	</style>
  <body>
    
    <h1 align="center">物品分类</h1>
    <hr>
    <div align="center">
    <table>
    	<th>
    		<td>描述</td>
    		<td>分类</td>
    	</th>    
    	<c:forEach items="${sessionScope.list}" var="goodss"> 
    	    <tr>
    	    	<td><c:out value="${goodss.context}" /></td>
				<td><c:out value="${goodss.type}" /></td>
			</tr><br><br><br>			
		</c:forEach>
	</table>
	</div>
	<form action="showdata" method="post">
	<input type="submit" value="上一页">
	</form>
	<form action="Next" method="post">
	<h5>当前页:<c:out value="${sessionScope.num%2+sessionScope.num/2+1}" /></h5>
	<input type="submit" value="下一页">
	</form>
  </body>
</html>
