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
 * Servlet implementation class Reduce
 */
@WebServlet("/Reduce")
public class Reduce extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Reduce() {
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
		if(session.getAttribute("page")==null){
			s="1";
			session.setAttribute("page",1);
		}else{
			s=session.getAttribute("page").toString();
		}
		int page=Integer.parseInt(s);
		if(page>=2){
			page-=1;
			session.setAttribute("page",page);	
		}
		response.sendRedirect("BatchQuery");
	}

}
