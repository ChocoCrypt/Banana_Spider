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

import org.apache.commons.validator.routines.CodeValidator;
import org.apache.commons.validator.routines.CreditCardValidator;

@WebFilter("/Credit_CardFilter")
public class Credit_CardFilter implements Filter {

	private ServletContext context;

	public void destroy() {
		// TODO Auto-generated method stub
	}

	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
		
		// Getting if is secure code or not
		Globals globals = Globals.getInstance();
		boolean secure = globals.getsecure();
		
		// Se recibe el parametro que nos interesa en este filtro, ademas se le quitan los espacios
		String cred = request.getParameter("credit-card");
		// S crea el validador (solo Visa)
		CreditCardValidator val = new CreditCardValidator(
				new CodeValidator[] {CreditCardValidator.VISA_VALIDATOR
				});
		// Se mira si el input si es una tarjeta valida
		boolean valid = false;
		if(cred != null)
		    valid = val.isValid(cred.replace(" ",""));
		
		// Si es valida, se pasa al siguiente filtro, si no, se rechaza peticion
		if (valid || !secure) {
			chain.doFilter(request, response);
		}
		else {
			request.setAttribute("Error", "Esto no es una tarjeta de Credito>");
			PrintWriter out= response.getWriter();
			out.println("<font color=red>Error, La tarjeta de Credito no es valida...Ademas debe ser VISA</font>");
			RequestDispatcher rd = request.getRequestDispatcher("login.html");
			rd.include(request, response);
			
		}
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	public void init(FilterConfig fConfig) throws ServletException {
		this.context = fConfig.getServletContext();
		this.context.log("Credit_CardFilter initialized");
	}

}
