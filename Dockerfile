FROM centos
 
RUN yum install -y vim && yum install -y gzip && yum install -y ansible && yum install -y openssh-server && yum install -y python  && yum install -y sshpass && yum install -y openssh && yum install -y openssh-clients && yum install -y MySQL-pytho* && yum install -y mysql
WORKDIR /DS_ANALYZE
COPY ./ /DS_ANALYZE
COPY hosts /etc/ansible/hosts
RUN chmod 777 *
RUN mkdir /var/run/sshd
RUN echo 'root:root123' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
EXPOSE 22
RUN ssh-keygen -A
ENV ANSIBLE_HOST_KEY_CHECKING=False
CMD ["/usr/sbin/sshd", "-D"]
