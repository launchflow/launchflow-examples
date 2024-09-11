FROM httpd:2.4

RUN sed -i 's/Listen 80/Listen 8080/' /usr/local/apache2/conf/httpd.conf

RUN echo '<html>\n\
    <head>\n\
    <title>Hello from LaunchFlow</title>\n\
    </head>\n\
    <body>\n\
    <h1>Hello from LaunchFlow!</h1>\n\
    </body>\n\
    </html>' > /usr/local/apache2/htdocs/index.html
