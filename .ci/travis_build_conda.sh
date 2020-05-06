#!/bin/bash

set -e -x

export VERSION_NO="$TRAVIS_TAG"

python3 ./make_conda_recipe.py || exit 1

# Switch to miniconda
source "$HOME/miniconda/etc/profile.d/conda.sh"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a
conda config --add channels domdfcoding || exit 1
conda build conda --output-directory conda/dist


for f in ../conda/dist/noarch/domdf_python_tools-*.tar.bz2; do
  conda install $f || exit 1
  if [ -z "$TRAVIS_TAG" ]; then
    echo "Skipping deploy because this is not a tagged commit"
  else
    echo "Deploying to Anaconda.org..."
    anaconda -t $ANACONDA_TOKEN upload $f || exit 1
    echo "Successfully deployed to Anaconda.org."
  fi
done


