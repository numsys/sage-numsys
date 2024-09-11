FROM ubuntu:22.04

RUN apt update && apt install -y ssh htop tmux sudo git curl 

RUN username="docky" && addgroup -gid 1000 $username && mkdir -p "/home/$username" && cp -a /root/. "/home/$username" && adduser --uid 1000 --home "/home/$username" --gid 1000 --quiet --disabled-password --gecos "Mr. $username User,,,"  $username  && usermod -p "Q4FXCUcqOWdDE" $username && sudo usermod -a -G sudo $username && chown -R "$username.$username" "/home/$username"

WORKDIR /home/docky/app
ENV HOME=/home/docky

ENV TZ=Europe/Budapest
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

USER docky
