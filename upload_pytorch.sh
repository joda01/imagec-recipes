cd recipes/libtorch/all
conan create . --profile ../../../profiles/profile_linux --version=2.7.1 --build=missing --update -s os=Linux -s arch=x86_64 -o *:with_cuda=False
conan create . --profile ../../../profiles/profile_linux --version=2.7.1 --build=missing --update -s os=Linux -s arch=x86_64 -o *:with_cuda=True

conan create . --profile ../../../profiles/profile_win_msvc --version=2.7.1 --build=missing --update -s os=Windows -s arch=x86_64 -o *:with_cuda=False
conan create . --profile ../../../profiles/profile_win_msvc --version=2.7.1 --build=missing --update -s os=Windows -s arch=x86_64 -o *:with_cuda=True

conan create . --profile ../../../profiles/profile_macos --version=2.7.1 --build=missing --update -s os=Macos -s arch=x86_64 -o *:with_cuda=False
cd ../..


conan upload libtorch/2.7.1  -r=imageclibs