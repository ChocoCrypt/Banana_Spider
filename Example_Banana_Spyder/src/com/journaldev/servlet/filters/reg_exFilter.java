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

import org.apache.commons.validator.routines.RegexValidator;

@WebFilter("/reg_exFilter")
public class reg_exFilter implements Filter {

	private ServletContext context;

	public void destroy() {
		// TODO Auto-generated method stub
	}

	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		
		// Getting if is secure code or not
		Globals globals = Globals.getInstance();
		boolean secure = globals.getsecure();
		
		// Se obtiene parametro del campo reg-ex
		String regex = request.getParameter("reg-ex");
		
		// Se crea validador con la expresion regular que queremos que evalue cada entrada
		boolean valid = new RegexValidator("[A-z\\s0-9.&,]*[@$#/\"%=+<>^*]+[A-z\\s0-9.&,@$#/\\\"%=+<>^]*").isValid(regex);
		
		//Si el input no hizo match, es porque no tiene caracteres especiales, entonces se pasa al siguiente filtro
		if (!valid || !secure) {
			chain.doFilter(request, response);
		}
		// como hay caracteres especiales, se rechaza peticion
		else {
			request.setAttribute("<Error", "Esto no es un E-mail>");
			PrintWriter out= response.getWriter();
			out.println("<font color=red>Error, el campo reg-ex contiene caracteres no permitidos</font>");
			RequestDispatcher rd = request.getRequestDispatcher("login.html");
			rd.include(request, response);	
		}
	}

	public void init(FilterConfig fConfig) throws ServletException {
		this.context = fConfig.getServletContext();
		this.context.log("reg_exFilter initialized");
	}

}
