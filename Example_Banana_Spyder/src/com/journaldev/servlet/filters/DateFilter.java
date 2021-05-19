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
import java.util.Calendar;
import org.apache.commons.validator.routines.CalendarValidator;


@WebFilter("/DateFilter")
public class DateFilter implements Filter {

	private ServletContext context;

	public void destroy() {
		// TODO Auto-generated method stub
	}

	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {

		String date = request.getParameter("date");
		
		// Getting if is secure code or not
		Globals globals = Globals.getInstance();
		boolean secure = globals.getsecure();
		
		if (!secure) {
			// Como la fecha es valida, tomamos la fecha actual
			chain.doFilter(request, response);
			return;
		}
		
		// Se manejan la clase calendar de java, por lo que el validador de apache ofrece convertir el string a esta clase
		// y luego se comparan las fechas.
		Calendar date_to_cal = CalendarValidator.getInstance().validate(date, "yyyy-mm-dd");		
		
		// La fecha esta en formato calendar de java valido
		if (date_to_cal != null) {
			
			Calendar recent_date = Calendar.getInstance();
			
			//le restamos 865 semanas (6055 dias) a la fecha actual
			//recent_date.add(Calendar.DAY_OF_MONTH, -6055);
			
			// finalmente se compara esta resta con la fecha del input
			// Observe que si la fecha del input es mayor que la fecha actual - 865 semanas, entonces el input tiene una edad menor de 865 semanas
			int compare = date_to_cal.compareTo(recent_date);

			// value returned indicates the comparision result			
			// negative integer means that input is at least of 865 weeks
			if (compare <= 0) {
				// Como la fecha es valida, tomamos la fecha actual
				chain.doFilter(request, response);
			}
			
			//si el input fue una fecha valida pero no cumplio el requisito de edad, tambien se hace dispatch
			else {
				request.setAttribute("<Error", "Esto no es una fecha valida>");
				PrintWriter out= response.getWriter();
				out.println("<font color=red>Error, Esto no es una fecha Valida, debes tener mas edad para ingresar</font>");
				RequestDispatcher rd = request.getRequestDispatcher("login.html");
				rd.include(request, response);
			}

		}
		
		// Si la fecha es null es porque el validador no pudo convertir a clase de calendar (fecha mal puesta, se usa dispatch)
		else {
			request.setAttribute("<Error", "Esto no es una fecha valida>");
			PrintWriter out= response.getWriter();
			out.println("<font color=red>Error, Esto no es una fecha Valida</font>");
			RequestDispatcher rd = request.getRequestDispatcher("login.html");
			rd.include(request, response);
		}
		
	}

	public void init(FilterConfig fConfig) throws ServletException {
		this.context = fConfig.getServletContext();
		this.context.log("DateFilter initialized");
	}

}
