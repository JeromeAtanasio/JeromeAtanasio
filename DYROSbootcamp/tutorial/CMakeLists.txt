cmake_minimum_required (VERSION 2.6)

project (Tutorial) # 프로젝트 이름 정의

# include_directories("include/my_math") #포함 디렉토리 추가

add_library(MathFunctions mysqrt.cpp) #라이브러리 추가
Add_executable(Tutorial tutorial.cpp) #실행파일 추가

Target_link_libraries(Tutorial MathFunctions) #라이브러리 링크