#!/bin/sh
# Use this script to release a new version of Adagios

current_version=$(grep ^__version__ nago/__init__.py | awk '{ print $3 }')
current_release=1

echo    "Current version is: $current_version"
echo -n "New version number: "
read new_version

echo new version: $new_version


echo "### Updating version number"
sed -i "s/^__version__.*/__version__ = \'$new_version\'/" nago/__init__.py

echo "### commiting and tagging current git repo"
git commit nago/__init__.py -m "Bumped version number to $new_version" > /dev/null
git tag pynag-${new_version}-${current_release} -a -m "Bumped version number to $new_version" 

# The following 2 require access to git repositories and pypi
echo "### Pushing commit to github"
git push origin master || exit 1
git push --tags origin master || exit 1
echo "Building package and uploading to pypi"
python setup.py build sdist upload || exit 1
