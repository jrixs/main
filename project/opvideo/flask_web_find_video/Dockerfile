FROM centos:7

#RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN  yum -y install  python36-pip python36-devel openldap-devel gcc; yum clean all

RUN pip3.6 install --upgrade pip
RUN pip3.6 install flask
RUN pip3.6 install requests
RUN pip3.6 install python-ldap
RUN pip install PyMySQL
ADD src /data/
RUN chmod +x /data/start.py

CMD /data/start.py
