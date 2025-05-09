from conan import ConanFile
from conan.tools.microsoft import check_min_vs
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, rm, rmdir
from conan.tools.build import check_min_cppstd
from conan.tools.scm import Version
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
import os

required_conan_version = ">=1.53.0"

class RapidYAMLConan(ConanFile):
    name = "rapidyaml"
    description = "a library to parse and emit YAML, and do it fast."
    license = "MIT",
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/biojppm/rapidyaml"
    topics = ("yaml", "parser", "emitter")
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_default_callbacks": [True, False],
        "with_tab_tokens": [True, False],
        "with_default_callback_uses_exceptions": [True, False],
        "with_assert": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_default_callbacks": True,
        "with_tab_tokens": False,
        "with_default_callback_uses_exceptions": False,
        "with_assert": False,
    }

    @property
    def _minimum_cpp_standard(self):
        return 11

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if Version(self.version) < "0.4.0":
            del self.options.with_tab_tokens
        if Version(self.version) < "0.6.0":
            del self.options.with_default_callback_uses_exceptions
            del self.options.with_assert

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        # with_default_callback_uses_exceptions should only be valid if with_default_callbacks is true
        if not self.options.with_default_callbacks:
            self.options.rm_safe("with_default_callback_uses_exceptions")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        if Version(self.version) < "0.6.0":
            self.requires("c4core/0.1.11", transitive_headers=True)
        else:
            self.requires("c4core/0.2.0", transitive_headers=True)

    def validate(self):
        check_min_cppstd(self, self._minimum_cpp_standard)
        check_min_vs(self, 190)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["RYML_DEFAULT_CALLBACKS"] = self.options.with_default_callbacks
        if Version(self.version) >= "0.4.0":
            tc.variables["RYML_WITH_TAB_TOKENS"] = self.options.with_tab_tokens
        if Version(self.version) >= "0.6.0":
            tc.variables["RYML_DEFAULT_CALLBACK_USES_EXCEPTIONS"] = self.options.with_default_callback_uses_exceptions
            tc.variables["RYML_USE_ASSERT"] = self.options.with_assert
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE.txt", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rm(self, "*.natvis", os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "ryml")
        self.cpp_info.set_property("cmake_target_name", "ryml::ryml")
        self.cpp_info.libs = ["ryml"]

