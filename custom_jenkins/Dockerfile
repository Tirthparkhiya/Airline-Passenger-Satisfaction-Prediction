FROM jenkins/jenkins:lts

USER root

# Add Jenkins user to Docker group
RUN groupadd -f docker && usermod -aG docker jenkins

RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker


USER jenkins







