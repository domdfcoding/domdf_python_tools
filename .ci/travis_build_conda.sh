#!/bin/bash

set -e -x

if [ $TRAVIS_PYTHON_VERSION == 3.6 ]; then


  python3 ./make_conda_recipe.py || exit 1

  # Switch to miniconda
  source "$HOME/miniconda/etc/profile.d/conda.sh"
  hash -r
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda
  conda install conda-build
  conda install anaconda-client
  conda info -a
  conda config --add channels domdfcoding || exit 1
  conda config --add channels conda-forge || exit 1

  python -m anaconda || exit 1

  conda build conda --output-folder conda/dist

  for f in conda/dist/noarch/domdf_python_tools-*.tar.bz2; do
    echo "$f"
    conda install $f || exit 1
    if [ -z "$TRAVIS_TAG" ]; then
      echo "Skipping deploy because this is not a tagged commit"
    else
      if [ $TRAVIS_PYTHON_VERSION == 3.6 ]; then
        echo "Deploying to Anaconda.org..."
        anaconda -t $ANACONDA_TOKEN upload $f || exit 1
        echo "Successfully deployed to Anaconda.org."
      else
          echo "Skipping deploy because this is not the required runtime"
      fi
    fi
  done

else
  echo "Skipping building conda package because this is not the required runtime"
fi

exit 0
