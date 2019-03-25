<%@ page language="java" import="java.util.*" contentType="text/html; charset=utf-8"%>
<%
String path = request.getContextPath();
String basePath = request.getScheme()+"://"+request.getServerName()+":"+request.getServerPort()+path+"/";
%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
  <base href="<%=basePath%>">
    
    <title>数据显示</title>
    
	<meta http-equiv="pragma" content="no-cache">
	<meta http-equiv="cache-control" content="no-cache">
	<meta http-equiv="expires" content="0">    
	<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
	<meta http-equiv="description" content="This is my page">
	<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
     <link rel="stylesheet" href="show.css" type="text/css">
  	<link href="css/bootstrap.css" rel="stylesheet">
	<script src="js/jquery-1.11.3.min.js"></script>
	<script src="js/bootstrap.js"></script>
    </style>
	</head>
  <body>
  <div class="container">
  <div class="container-fluid">
  <div class="row">
	<div class="header">
    </div>
      </div>
	
	</div>
	  </div>
	
	  
	<div class="row">
		<div class="col-md-2">
			<div class="panel-group">
				<div class="panel panel-success">
					<div href="#collapseA" data-parent="#box" data-toggle="collapse" class="panel-heading">
						<a href="#" class="panel-title">View mode</a>
					</div>
				</div>
				<div class="panel-collapse collapse in" id="collapseA">
				    <div class="panel-body">
					  <ul class="nav nav-pills nav-stacked">
						<li><a href="showdata"  >Direct display</a></li>
						<li><a href="tip2.jsp" >Search Display</a></li>
						<li><a href="tip3.jsp" >Batch query</a></li>
					  </ul>
				    </div>
				</div>
			</div>
		</div>
		<div class="col-md-10">
		    <div class="breadcrumb" style="height:50px">
		    	<ul class="breadcrumb">
		    		<li><span class="glyphicon glyphicon-home"></span>   &nbsp;&nbsp; DATA</li>
		    		
		    	</ul>
		    </div>
			<div class="panel panel-success" id="tip1">
				<div class="panel-heading">
					<a href="#" class="title">data display</a>
				</div>
				<div class="panel panel-body">
				
					<table class="table table-striped table-hover" >
						<thead>
							<tr >
								<td colspan="8">
									<form action="Jump_1" method="post">
									<ul class="pagination">
										<li><a href="showdata"><</a></li>
										<%int a= (int)session.getAttribute("num")/100+1;%>
										<li><a href="tip1.jsp"><%=a %></a></li>
										<li><a href="Next">></a></li>
										<li><span>跳转到第<input value="0" name="jump1" style="width: 30px">页，共<c:out value="${sessionScope.j1}" />页</span></li>
										<li><span><input type="submit" value="确定"/></span></li>
									</ul>
									</form>
								</td>
							</tr>
							<tr>
								<th style="text-align: center;">描述</th>
								<th style="text-align: center;">分类</th>
							</tr>
						</thead>
						<c:forEach items="${sessionScope.list}" var="goodss"> 
    	    			<tr>
    	    				<td><c:out value="${goodss.context}" /></td>
							<td><c:out value="${goodss.type}" /></td>
						</tr>			
						</c:forEach>
						
						<tfoot>
							<tr >
								<td colspan="8">
									<form action="Jump_1" method="post">
									<ul class="pagination">
										<li><a href="showdata"><</a></li>
										<%int b= (int)session.getAttribute("num")/100+1;%>
										<li><a href="tip1.jsp"><%=b %></a></li>
										<li><a href="Next">></a></li>
										<li><span>跳转到第<input value="0" name="jump1" style="width: 30px">页，共<c:out value="${sessionScope.j1}" />页</span></li>
										<li><span><input type="submit" value="确定"/></span></li>
									</ul>
									</form>
								</td>
							</tr>
						</tfoot>
					</table>
				</div>
			</div>
		</div>
	</div>
  </body>
</html>
