cmake_minimum_required(VERSION 3.10...3.28)

project(aii601_cgal_voronoi)
find_package(CGAL REQUIRED)

# Creates the executable, with CGAL's own compile/link flags applied.
create_single_source_cgal_program("vd_2_point_location.cpp")
# end of the file
