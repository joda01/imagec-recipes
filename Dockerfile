
ARG DEBIAN_VERSION="12.7-slim"

FROM debian:$DEBIAN_VERSION AS build

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# This Dockerfile's base image has a non-root user with sudo access. Use the "remoteUser"
# property in devcontainer.json to use it. On Linux, the container user's GID/UIDs
# will be updated to match your local UID/GID (when using the dockerFile property).
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# [Optional] Update UID/GID if needed
RUN   if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then \
    groupmod --gid $USER_GID $USERNAME \
    && usermod --uid $USER_UID --gid $USER_GID $USERNAME \
    && chown -R $USER_UID:$USER_GID /home/$USERNAME; \
    fi

RUN apt-get update && apt-get install -y autoconf automake libtool curl make g++ unzip checkinstall gdb ninja-build wget libssl-dev pkg-config git default-jre libcurl4-openssl-dev default-jdk


RUN wget https://github.com/Kitware/CMake/archive/refs/tags/v3.25.2.tar.gz -O cmake.tar.gz && \
    tar xf cmake.tar.gz && \
    rm cmake.tar.gz &&\
    cd CMake-* && \
    ./bootstrap --prefix=/usr --no-qt-gui --parallel=8 && \
    make -j8 && \
    make install && \
    cd .. && \
    rm -rf CMake*


#
# Install conan
#
RUN apt-get update && apt-get install -y pip libva-dev libvdpau-dev xkb-data
RUN pip install conan --break-system-packages
RUN pip install conan --upgrade --break-system-packages
RUN pip install cyclonedx-conan --break-system-packages

RUN ldconfig

# pip install typing_extensions --break-system-packages
# pip install fmt --break-system-packages
# pip install tensorpipe --break-system-packages