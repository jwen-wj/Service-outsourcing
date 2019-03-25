package com.fuwu.sevlet;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.channels.NonReadableChannelException;
import java.sql.Connection;
import java.util.ArrayList;
import java.util.List;

import javax.enterprise.inject.New;
import javax.jms.Session;
import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.servlet.http.Part;

import org.apache.taglibs.standard.lang.jstl.test.StaticFunctionTests;

import com.csvreader.CsvReader;
import com.fuwu.dao.Conn;
import com.fuwu.dao.ReaderTest;
import com.fuwu.dao.Test;
import com.fuwu.vo.Classification;

/**
 * Servlet implementation class BatchQuery
 */
@WebServlet("/BatchQuery")
@MultipartConfig
public class BatchQuery extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public BatchQuery() {
        super();
        // TODO Auto-generated constructor stub
    }
    @Override
    public void init() throws ServletException {
    	// TODO Auto-generated method stub
    	super.init();
    	
    }
	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doPost(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	int rowNum = 1;
	List<Classification> list_1=new ArrayList<Classification>();
	List<Classification> list_2=new ArrayList<Classification>();
	Test test= new Test();
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		list_1.clear();
		list_2.clear();
		
		//读文件
		HttpSession session=request.getSession();
		String s;
		if(session.getAttribute("page")==null){
			s="1";
			session.setAttribute("page",1);
			System.out.println("页码记录没有");
		}else{
			
			s=session.getAttribute("page").toString();
			System.out.println("有页码记录"+s);
		}
		//System.out.println("********这是servlet");
		int page=Integer.parseInt(s);
		String fileSavingPath=request.getSession().getAttribute("file").toString();
		ReaderTest.getReader(fileSavingPath);
		list_1=ReaderTest.read((page-1)*100);
		Connection connection=new Conn().getConnection();
		for (Classification c:list_1) {
			//System.out.println("************这是遍历文件内容查找数据库的列表遍历");
			Classification d=test.queryy(connection, c.getContext());
			if(d==null){
				list_2.add(new Classification(c.getContext(), " "));
			}else {
				list_2.add(d);
			}			
		}
		test.closeAll(connection);
		request.getSession().setAttribute("list2", list_2);
		request.getRequestDispatcher("/tip3.jsp").forward(request, response);
	}

}
