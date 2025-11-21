FROM debian

ARG user=developer
ARG uid=1000
ARG gid=1000

#basic setup
RUN apt-get update
RUN apt-get install sudo -y

#create user
RUN groupadd -g ${gid} ${user}
RUN useradd -m -u ${uid} -g ${gid} ${user}

# # add user to sudo group
RUN usermod -aG sudo ${user}
# # modify sudoers, sudo without password
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
# #user is ready to go, switch it
USER ${user}
WORKDIR /home/${user}

# #install other required tools
RUN sudo apt install cmake make binutils git python3 gcc-arm-none-eabi gdb file -y

ADD --chown=${uid}:${gid} toolchain /home/${user}/toolchain

CMD ["bash"]