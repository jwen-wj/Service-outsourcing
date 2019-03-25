package com.fuwu.sevlet;

import java.io.IOException;
import java.util.List;

import javax.security.auth.message.callback.PrivateKeyCallback.Request;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.fuwu.dao.Conn;
import com.fuwu.dao.Test;
import com.fuwu.vo.Classification;

/**
 * Servlet implementation class showdata
 */
@WebServlet("/showdata")
public class Showdata extends HttpServlet {
	private static final long serialVersionUID = 1L;
//	private static final int sumpage = 0;
	int sumpage=0;
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Showdata() {
        super();
        // TODO Auto-generated constructor stub
        Test test=new Test();		
		List<Classification> list=test.query(0);
		sumpage=test.number();
		
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
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		HttpSession session=request.getSession();
		String s;
		if(session.getAttribute("num")==null){
			s="0";
			session.setAttribute("num",0);
		}else{
			s=session.getAttribute("num").toString();
		}
		int num=Integer.parseInt(s);
		if(num>=100){
			num-=100;
			session.setAttribute("num",num);	
		}
		Test test=new Test();		
		List<Classification> list=test.query(num);	
		//System.out.println(num);
		session.setAttribute("list", list);
		
		request.getSession().setAttribute("j1", sumpage/100+1);
		request.getRequestDispatcher("/tip1.jsp").forward(request, response);
	}
}
