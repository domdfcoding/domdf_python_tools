# fix these
declare -a errors=(
  E301 E302 E303 E304 E305 E306 E502 E265
  W291 W292 W293 W391 E226 E225 E241
  )

# Only warn for these
declare -a warnings=(
  E101 E111 E112 E113 E121 E122 E124 E125
  E127 E128 E129 E131 E133 E201 E202 E203
  E211 E222 E223 E224 E225 E227 E228 E231
  E242 E251 E261 E262 E271 E272 E402
  E703 E711 E712 E713 E714 E721 W503 W504
  )

if [ -z "$(git status --porcelain --untracked-files=no)" ] || [ $1 == "-f" ]; then
  # Working directory clean

  for error in "${errors[@]}"
  do
    echo "Correcting $error"
    autopep8 --in-place --select "$error" -a --recursive domdf_python_tools/
    flake8 --select "$error" domdf_python_tools/
    autopep8 --in-place --select "$error" -a --recursive tests/
    flake8 --select "$error" tests/

  done

  for warning in "${warnings[@]}"; do
    echo "Searching for $warning"
    flake8 --select "$warning" domdf_python_tools/
    flake8 --select "$warning" tests/
  done

  exit 0

else
  # Uncommitted changes
  >&2 echo "git working directory is not clean"
  exit 1

fi



