#in latest debian, arm-none-eabi is version 15. which is based on binutils 2.44
# that requires some changes in example project,
# my tests linking failed similar to: (https://community.arm.com/support-forums/f/compilers-and-libraries-forum/57077/binutils-2-44-and-gcc-15-1-0---dangerous-relocation-unsupported-relocation-error-when-trying-to-build-u-boot)
# so we need to fix arm-none-eabi to version 15:12.2.rel1-1, which is default on bookworm
# once we found a solution to the example project, we can upgrade debian
FROM debian:bookworm

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
RUN sudo apt install cmake make binutils git python3 gcc-arm-none-eabi gdb file gdb-multiarch -y

ADD --chown=${uid}:${gid} toolchain /home/${user}/toolchain

CMD ["bash"]