package com.stack1;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.naming.Binding;
import javax.naming.NamingEnumeration;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class JNDIReaderServlet extends HttpServlet{

        public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws IOException{

                String message = "No message";
                try{
                        message = getJndiInfo();
                }
                catch(NamingException e){
                        message = e.getMessage();
                }
 
                PrintWriter out = response.getWriter();
                out.println("<html>");
                out.println("<body>");
                out.println("<h1>Hello Servlet Get</h1>");
                out.println("<p>JNDI nameInNamespace is: "+ message +"</p>");
 
                try{
                        InitialContext ctx = new InitialContext();
                        NamingEnumeration i = ctx.listBindings(message);
                        while (i.hasMore()) {
                                Binding binding=(Binding)i.next();
                                String name = binding.getName();
                        }
                } catch(NamingException ne){
                        out.println("<p>JNDI ERROR "+ne.getMessage()+"</p>");

                }

                out.println("</body>");
                out.println("</html>");
        }
 
        public String getJndiInfo()throws NamingException{
                InitialContext ctx = new InitialContext();
                String ns = ctx.getNameInNamespace();
                return(ns);
        }
 
        public void iterate () throws NamingException{
                InitialContext ctx = new InitialContext();
                NamingEnumeration i = ctx.listBindings("");
                while (i.hasMore()) {
                        Binding binding=(Binding)i.next();
                        String name = binding.getName();
                }
        }
}
