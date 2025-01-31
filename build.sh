#cd recipes/fbgemm/all
#conan create . --version=0.8.0 --build=missing

#cd recipes/openmp/all
#conan create . --version=system --build=missing

#cd recipes/sleef/all
#conan create . --version=3.6.1 --build=missing

#cd recipes/libtorch/all
#conan create . --version=2.4.0 --build=missing -c tools.system.package_manager:mode=install



#cd recipes/tensorflow-lite/all
#conan create . --version=2.18.0 --build=missing -v -c tools.system.package_manager:mode=install

cd recipes/gemmlowp/all
conan create . --version=cci.20210928 --build=missing -v -c tools.system.package_manager:mode=install