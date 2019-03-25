package com.fuwu.sevlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.fuwu.dao.Test;
import com.fuwu.vo.Classification;

/**
 * Servlet implementation class SingleQuery
 */
@WebServlet("/SingleQuery")
public class SingleQuery extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public SingleQuery() {
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
		request.setCharacterEncoding("UTF-8");
		Object object=request.getParameter("singlequery");
		Classification classification = null;
		if(object!=""&&object!=null){
			String context=object.toString();
			Test test=new Test();
			System.out.println(context);
//			System.out.println(test.single("服务外包").toString()+"***********");
			if(test.single(context)!=null){
				classification=test.single(context);
				//System.out.println(classification.toString());
				request.setAttribute("singlequery", classification);
			}	
		}
		
		request.getRequestDispatcher("tip2.jsp").forward(request, response);
	}

}
