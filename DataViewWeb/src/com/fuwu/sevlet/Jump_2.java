package com.fuwu.sevlet;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Servlet implementation class Jump_2
 */
@WebServlet("/Jump_2")
public class Jump_2 extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Jump_2() {
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
		int page=Integer.parseInt(request.getParameter("jump2").toString())-1;
		if(page>=0){
			HttpSession session=request.getSession();
			String s;
			if(session.getAttribute("page")==null){
				s="1";
				session.setAttribute("page",1);
			}else{
				session.setAttribute("page", page);
				s=session.getAttribute("page").toString();
			}
			int num=Integer.parseInt(s);
			if(page<0){
				response.sendRedirect("BatchQuery");
			}
			session.setAttribute("page",num+1);	
		}
		response.sendRedirect("BatchQuery");
	}

}
