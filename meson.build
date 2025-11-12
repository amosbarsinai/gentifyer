project('gentifyer', 'cpp',
  version : '0.1',
  default_options : ['warning_level=3', 'cpp_std=c++14']
)

inc = include_directories('include')

ncurses_dep = dependency('ncurses')

spdlog_proj = subproject('spdlog')
spdlog_dep = spdlog_proj.get_variable('spdlog_dep')

exe = executable('gentifyer',
  'src/main.cpp',
  'src/screen.cpp',
  include_directories : inc,
  dependencies : [ncurses_dep, spdlog_dep],
  install : true
)
