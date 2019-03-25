package com.fuwu.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import com.fuwu.vo.Classification;
import com.mysql.jdbc.Statement;


public class Test {

	List<Classification> list=new ArrayList<Classification>();
	Conn conn=null;
	PreparedStatement ps=null;
	ResultSet rs=null;
	Connection connection=null;
	
	public Test() {	
		conn=new Conn();
	}
	/**
	 * 获取数据库数据并存入队列
	 * @param start
	 * @return
	 */
	public List<Classification> query(int start){
		connection=conn.getConnection();
		if(list.size()!=0){
			list.clear();
		}
		int start1=start;
		String sql="Select context,type from Classification limit "+start1+",100";
		try {
			ps=connection.prepareStatement(sql);
			rs=ps.executeQuery();
			while(rs.next()){
				list.add(new Classification(rs.getString("context"), rs.getString("type")));	
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}finally{
			try {
				rs.close();
				ps.close();
				connection.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
		return list;
	}
//	/**
//	 * 
//	 * 计算数据库数据条数
//	 * 计算分页数
//	 * @param args
//	 */
	public int number(){
		String sql= "select count(0) from Classification";		 
		try {
			ps = conn.getConnection().prepareStatement(sql);
		} catch (SQLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		try {
			rs = ps.executeQuery();
		} catch (SQLException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		 
		int rowCount = 0;
		try {
			if(rs.next())
			{
			    rowCount=rs.getInt(1);
			    return rowCount;
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return 0;
		
	}
	/**
	 * 查询指定商品的标签
	 * @param args
	 */
	public Classification single(String context){
		Classification classification=null;
		String cString=context;
		connection=conn.getConnection();
		classification=queryy(connection,cString);
//		String sql="Select context,type from Classification where context= '"+cString+"'";
//		String sql="select context,type from Classification where context='"+cString+"'";
//		System.out.println(context);
//		try {
//			ps=connection.prepareStatement(sql);
//			rs=ps.executeQuery();
//			System.out.println("******这里是单一查询函数");
//			
//			while(rs.next()){
//				System.out.println(rs.getString("context")+ rs.getString("type"));
//				return new Classification(rs.getString("context"), rs.getString("type"));	
//			}
//		} catch (SQLException e) {
//			e.printStackTrace();
//		}finally{
			try {
				rs.close();
				ps.close();
				connection.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		
		return classification;
	}
	
	public Classification  queryy(Connection connection,String cString){
		String sql="select context,type from Classification where context='"+cString+"'";
		try {
			ps=connection.prepareStatement(sql);
			rs=ps.executeQuery();
			System.out.println("******这里是单一查询函数");
			
			while(rs.next()){
				System.out.println(rs.getString("context")+ rs.getString("type"));
				return new Classification(rs.getString("context"), rs.getString("type"));	
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public void closeAll(Connection connection){
		try{
			rs.close();
			ps.close();
			connection.close();
		}
		catch (Exception e) {
			// TODO: handle exception
		}
	}
	public static void main(String[] args) {
		Test test=new Test();
//		test.query(0);
//		test.query(2);
//		for(Classification c:test.list){
//			System.out.print(c.getId()+"  ");
//		}
		System.out.println(test.single("服务外包").toString());
	}
}
