package com.journaldev.servlet.filters;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;

import org.apache.commons.validator.routines.EmailValidator;

@WebFilter("/EmailFilter")
public class EmailFilter implements Filter {

	private ServletContext context;

	public void destroy() {
		// TODO Auto-generated method stub
	}

	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		
		// Getting if is secure code or not
		Globals globals = Globals.getInstance();
		boolean secure = globals.getsecure();
				
		String email = request.getParameter("user");
		boolean valid = EmailValidator.getInstance().isValid(email);
		if (valid || !secure) {
			chain.doFilter(request, response);
		}
		else {
			request.setAttribute("<Error", "Esto no es un E-mail>");
			PrintWriter out= response.getWriter();
			out.println("<font color=red>Error, Esto no es un E-mail</font>");
			RequestDispatcher rd = request.getRequestDispatcher("login.html");
			rd.include(request, response);
			
		}
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	public void init(FilterConfig fConfig) throws ServletException {
		this.context = fConfig.getServletContext();
		this.context.log("EmailFilter initialized");
	}

}
