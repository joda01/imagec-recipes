from conan import ConanFile
from conan.tools.files import copy, get, rmdir
import os
import zipfile

class LibTorchConan(ConanFile):
    name = "libtorch"
    version = "2.7.1"
    description = "Precompiled LibTorch binaries for multiple platforms"
    license = "BSD-3-Clause"
    url = "https://pytorch.org"
    settings = "os", "arch", "build_type"
    package_type = "shared-library"
    exports_sources = "*"
    options = {
        "with_cuda": [True, False]
    }
    default_options = {
        "with_cuda": True
    }


    def build(self):
        self.output.info("=== BUILD() CALLED ===")
        os_str = str(self.settings.os) 
        platform_key = {
            "Windows": "windows",
            "Linux": "linux",
            "Macos": "macos"
        }[os_str]

        if self.options.with_cuda and platform_key == "macos":
            raise ConanInvalidConfiguration("CUDA is not supported on macOS.")

        variant = "cuda" if self.options.with_cuda else "cpu"

        archive_name = {
            ("windows", "cpu"): "libtorch-win-shared-with-deps-2.7.1+cpu.zip",
            ("windows", "cuda"): "libtorch-win-shared-with-deps-2.7.1+cu128.zip",
            ("linux", "cpu"): "libtorch-cxx11-abi-shared-with-deps-2.7.1+cpu.zip",
            ("linux", "cuda"): "libtorch-cxx11-abi-shared-with-deps-2.7.1+cu128.zip",
            ("macos", "cpu"): "libtorch-macos-arm64-2.7.1.zip"
        }[(platform_key, variant)]

        archive_path = os.path.join(
            self.source_path, "downloads", platform_key, variant, archive_name
        )

        print("Archive: " + archive_path)

        self.output.info(f"Looking for archive: {archive_path}")
        if not os.path.exists(archive_path):
            raise Exception(f"Archive not found: {archive_path}")

        # Extract zip to build folder
        self.output.info(f"Extracting {archive_path}")
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(self.build_folder)


    def package(self):
        self.output.info("=== PACKAGE() CALLED ===")
        tmp = src=os.path.join(self.build_folder,"libtorch", "lib")
        print("Copy from: " + tmp)

        copy(self, "*", src=os.path.join(self.build_folder,"libtorch", "lib"), dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*", src=os.path.join(self.build_folder,"libtorch", "include"), dst=os.path.join(self.package_folder, "include"))
        copy(self, "*", src=os.path.join(self.build_folder,"libtorch", "share"), dst=os.path.join(self.package_folder, "share"))
        copy(self, "*", src=os.path.join(self.build_folder,"libtorch", "bin"), dst=os.path.join(self.package_folder, "bin"), keep_path=True)

    def package_info(self):
        # Assume the shipped cmake config files are in <package_folder>/share/cmake/Torch
        cmake_dir = os.path.join(self.package_folder, "share", "cmake", "Torch")
        self.cpp_info.builddirs = [cmake_dir]

        # Also expose libs and include paths
        self.cpp_info.includedirs = ["include","include/torch/csrc/api/include"]
        self.cpp_info.libdirs = ["lib"]

