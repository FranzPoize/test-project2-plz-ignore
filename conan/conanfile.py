from conans import ConanFile, tools
from conans.errors import ConanException
from conan.tools.cmake import CMake

from os import path
import semver


class Project2Conan(ConanFile):
    name = "project2"
    license = "MIT"
    author = "adnn"
    url = "https://github.com/franzpoize/test-project1-plz-ignore"
    description = "Shoot them urp!"
    topics = ("opengl", "2D", "game")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "build_devmode": [True, False],
        "build_tests": [True, False],
        "shared": [True, False],
    }
    default_options = {
        "build_devmode": False,
        "build_tests": False,
        "shared": False,
    }

    requires = (
        ("project3/a657d69c1a@adnn/develop"),
    )


    generators = "cmake_paths", "cmake_find_package_multi", "CMakeToolchain"
    build_policy = "missing"
    # Otherwise, conan removes the imported imgui backends after build()
    # they are still required for the CMake config phase of package()
    keep_imports = True

    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto",
        "submodule": "recursive",
    }

    def _generate_cmake_configfile(self):
        """ Generates a conanuser_config.cmake file which includes the file generated by """
        """ cmake_paths generator, and forward the remaining options to CMake. """
        with open("conanuser_config.cmake", "w") as config:
            config.write("message(STATUS \"Including user generated conan config.\")\n")
            # avoid path.join, on Windows it outputs '\', which is a string escape sequence.
            config.write("include(\"{}\")\n".format("${CMAKE_CURRENT_LIST_DIR}/conan_paths.cmake"))
            config.write("set({} {})\n".format("BUILD_tests", self.options.build_tests))


    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake


    def configure(self):
        tools.check_min_cppstd(self, "17")


    def generate(self):
        self._generate_cmake_configfile()


    def build(self):
        cmake = self._configure_cmake()
        cmake.build()


    def package(self):
        cmake = self._configure_cmake()
        cmake.install()


    def package_info(self):
        pass
