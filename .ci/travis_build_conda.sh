#!/bin/bash
# This file is managed by `git_helper`. Don't edit it directly

set -e -x

if [ $TRAVIS_PYTHON_VERSION == 3.6 ]; then


  python3 ./make_conda_recipe.py || exit 1

  # Switch to miniconda
  source "$HOME/miniconda/etc/profile.d/conda.sh"
  hash -r
  conda activate base
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda
  conda install conda-build
  conda info -a
  
  conda config --add channels domdfcoding || exit 1
  
  conda config --add channels conda-forge || exit 1
  
  conda build conda --output-folder conda/dist

else
  echo "Skipping building conda package because this is not the required runtime"
fi

exit 0
