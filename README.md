# imagec-recipes

Contains conan recipes of the external libs used in ImageC.
Libs are built for Linux, MacOS and Windows and stored in the imagec artifactory reachable under https://imagec.org:4431/.
ImageC uses the artifactory as lib cache to speed up the build process.

## Dep graph

To get the dependency graph execute:

```
conan install . --profile profiles/profile_linux --output-folder=build --build=missing --format=json > build.json
conan remote add imageclibs https://imagec.org:4431/artifactory/api/conan/imageclibs
conan graph info . -r=imageclibs --format=html > graph.html
```

git diff --no-index Utils_a.cc Utils.cc > utils.patch
