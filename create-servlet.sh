#!/bin/sh

SERVLET_NAME=$1
rm -rI ${SERVLET_NAME}

# Create WAR file structure
echo "Creating WAR directory structure"
mkdir -p ${SERVLET_NAME}/src/co/uk/bobclarke
mkdir -p ${SERVLET_NAME}/WEB-INF/classes

# Create java file
echo "Creating ${SERVLET_NAME}.java"
cat > ${SERVLET_NAME}/src/co/uk/bobclarke/${SERVLET_NAME}.java <<EOF1
package co.uk.bobclarke;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
 

public class ${SERVLET_NAME} extends HttpServlet{

        public void doGet ( HttpServletRequest request, HttpServletResponse response) throws IOException {
                PrintWriter out = response.getWriter();
                out.println("<html>");
                out.println("<body>");
                out.println("<p>Hello World</p>");
                out.println("</body>");
                out.println("</html>");
        }
}
EOF1

# Create deployment descriptor
echo "Creating web.xml"
cat > ${SERVLET_NAME}/WEB-INF/web.xml <<EOF2
<?xml version="1.0" encoding="UTF-8"?>
<web-app version="2.4" xmlns="http://java.sun.com/xml/ns/j2ee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
        <servlet>
                <servlet-name>${SERVLET_NAME}</servlet-name>
                <servlet-class>co.uk.bobclarke.${SERVLET_NAME}</servlet-class>
        </servlet>

        <servlet-mapping>
                <servlet-name>${SERVLET_NAME}</servlet-name>
                <url-pattern>/${SERVLET_NAME}</url-pattern>
        </servlet-mapping>
</web-app>
EOF2

# Compile
echo "Compiling ${SERVLET_NAME}.java"
javac -classpath /home/autowas/was/dev/JavaEE/j2ee.jar ${SERVLET_NAME}/src/co/uk/bobclarke/${SERVLET_NAME}.java -d ${SERVLET_NAME}/WEB-INF/classes

# Create WAR file
echo "Creating ${SERVLET_NAME}.war"
jar -cvf ${SERVLET_NAME}.war -C ${SERVLET_NAME} .
