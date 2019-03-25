package com.fuwu.sevlet;

import java.io.IOException;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.fuwu.dao.Test;
import com.fuwu.vo.Classification;

/**
 * Servlet implementation class Next
 */
@WebServlet("/Next")
public class Next extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Next() {
        super();
        // TODO Auto-generated constructor stub
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
		session.setAttribute("num",num+100);	
		Test test=new Test();		
		List<Classification> list=test.query(num+100);
		session.setAttribute("list", list);
		request.getRequestDispatcher("/tip1.jsp").forward(request, response);
	}

}
