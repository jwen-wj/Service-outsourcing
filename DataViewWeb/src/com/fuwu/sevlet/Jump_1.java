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
 * Servlet implementation class Jump
 */
@WebServlet("/Jump_1")
public class Jump_1 extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Jump_1() {
        super();
        // TODO Auto-generated constructor stub
        Test test=new Test();		
		List<Classification> list=test.query(0);
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
		//System.out.println(request.getParameter("jump1"));
		int page=Integer.parseInt(request.getParameter("jump1").toString())-1;
		if(page>=0){
			HttpSession session=request.getSession();
			String s;
			if(session.getAttribute("num")==null){
				s="0";
				session.setAttribute("num",0);
			}else{
				page*=100;
				session.setAttribute("num", page);
			}
			
			Test test=new Test();		
			List<Classification> list=test.query(page);	
			//System.out.println(num);
			session.setAttribute("list", list);
			request.getRequestDispatcher("/tip1.jsp").forward(request, response);
		}
		else {
			request.getRequestDispatcher("/tip1.jsp").forward(request, response);
		}
	}

}
