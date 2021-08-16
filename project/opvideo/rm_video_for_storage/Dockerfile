FROM centos:7

#RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN  yum -y install  python36-pip  ; yum clean all

RUN pip3.6 install --upgrade pip
RUN pip install PyMySQL
ADD src /data/
RUN chmod +x /data/rm_opvideo.py

CMD /data/rm_opvideo.py
