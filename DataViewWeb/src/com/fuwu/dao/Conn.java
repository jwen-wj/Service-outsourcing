package com.fuwu.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Conn {

	Connection conn=null;
	public Connection getConnection() {
		try {
			Class.forName("com.mysql.jdbc.Driver");
			conn=DriverManager.getConnection("jdbc:mysql://47.107.50.165:3306/fuwu?characterEncoding=utf-8", "root", "root");
			return conn;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public void search(int start){
		Connection conn=this.getConnection();
		PreparedStatement ps=null;
		ResultSet rs=null;
		int start1=start;
		String sql="Select context,type from Classification limit "+start1+",100";
		try {
			ps=conn.prepareStatement(sql);
			rs=ps.executeQuery();
			while(rs.next()){
				System.out.print(rs.getInt("id")+"  ");				
			}
			System.out.println();
		} catch (SQLException e) {
			e.printStackTrace();
		}finally{
			try {
				rs.close();
				ps.close();
				conn.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
		
	}
	
	public static void main(String[] args) {
		Conn conn=new Conn();
		conn.search(0);
		conn.search(2);
	}
}
