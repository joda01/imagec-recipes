from conan import ConanFile
from conan.tools.cmake import cmake_layout

class ImageC(ConanFile):
    name = "ImageC-Libs"
    version = "1.0"
    license = "AGPL"
    author = "Joachim Danmayr <your.email@example.com>"
    url = "https://github.com/your/repo"
    description = "An example Hello World project"
    topics = ("conan", "image-processing", "example")
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    exports_sources = "src/*"
    
    def requirements(self):
        self.requires("qt/6.7.1", force=True)
        self.requires("libgd/2.3.3")
        self.requires("opencv/4.10.0")
        self.requires("catch2/3.7.0")
        self.requires("pugixml/1.14")
        self.requires("nlohmann_json/3.11.3")
        self.requires("libxlsxwriter/1.1.8")
        self.requires("duckdb/1.1.3")
        self.requires("cpp-httplib/0.19.0", force=True)
        self.requires("openssl/3.4.1")
        self.requires("qcustomplot/2.1.1")
        self.requires("onnx/1.17.0", force=True)
        self.requires("rapidyaml/0.7.1")
        self.requires("cli11/2.5.0")
        self.requires("cereal/1.3.2")
        self.requires("tensorflow-lite/2.15.0")
        self.requires("onnxruntime/1.18.1")
        self.requires("mlpack/4.4.0")
        self.requires("llvm-openmp/17.0.6")
        #self.requires("libtorch/2.4.0") 
        self.requires("matplotplusplus/1.2.2")
        self.requires("flatbuffers/23.5.26", override=True)
        self.requires("protobuf/3.21.12", override=True)
        self.requires("xkbcommon/1.6.0", override=True)
        self.requires("libpq/15.5", override=True)
        self.requires("abseil/20240116.1", override=True)
        self.requires("libbacktrace/cci.20240730", override = True)
        self.requires("xnnpack/cci.20240229", override = True)
        self.requires("boost/1.86.0", override = True)
        

    def layout(self):
        cmake_layout(self)
