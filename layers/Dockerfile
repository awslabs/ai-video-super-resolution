FROM public.ecr.aws/amazonlinux/amazonlinux:latest

RUN yum install autoconf automake bzip2 bzip2-devel cmake freetype-devel gcc gcc-c++ git libtool make pkgconfig zlib-devel openssl-devel zip -y && mkdir ~/ffmpeg_sources

RUN cd ~/ffmpeg_sources && \
    curl -O -L https://www.nasm.us/pub/nasm/releasebuilds/2.15.05/nasm-2.15.05.tar.bz2 && \
    tar xjvf nasm-2.15.05.tar.bz2 && \
    cd nasm-2.15.05 && \
    ./autogen.sh && \
    ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" && \
    make && \
    make install
    
RUN cd ~/ffmpeg_sources && \
    curl -O -L https://ffmpeg.org/releases/ffmpeg-4.4.tar.bz2 && \
    tar xjvf ffmpeg-4.4.tar.bz2 && \
    cd ffmpeg-4.4 && \
    PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
      --prefix="$HOME/ffmpeg_build" \
      --pkg-config-flags="--static" \
      --extra-cflags="-I$HOME/ffmpeg_build/include" \
      --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
      --extra-libs=-lpthread \
      --extra-libs=-lm \
      --bindir="$HOME/bin" \
      --enable-openssl \
      --enable-static \
      --disable-ffmpeg \
      --disable-shared \
      --disable-ffplay \
      --disable-doc && \
    PATH="$HOME/bin:$PATH" make &&\
    make install &&\
    hash -r
    
RUN mkdir -p /packages/bin
RUN cp ~/bin/ffprobe /packages/bin

WORKDIR /packages
RUN zip -r9 /packages/ffprobe.zip .