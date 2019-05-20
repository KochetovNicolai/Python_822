cmake_minimum_required(VERSION 3.9)

project(MyProject)
set(CMAKE_CXX_STANDARD 17)
include_directories(./textures)
add_executable(MyProject ./sources/MapGenerator.py) 
