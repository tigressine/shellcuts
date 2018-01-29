# Part of Shellcuts by Tgsachse.
# Builds the Shellcuts .deb package.

mkdir -p shellcuts/DEBIAN
mkdir -p shellcuts/usr/bin
mkdir -p shellcuts/usr/share/doc/shellcuts
mkdir -p shellcuts/usr/share/man/man1
mkdir -p shellcuts/usr/share/shellcuts

cp docs/CHANGES.txt shellcuts/usr/share/doc/shellcuts
cp docs/LICENSE.txt shellcuts/usr/share/doc/shellcuts
cp docs/README.rst shellcuts/usr/share/doc/shellcuts
cp docs/META.txt shellcuts/usr/share/doc/shellcuts
cp docs/shellcuts.1 shellcuts/usr/share/man/man1

cp source/bin/sc-init shellcuts/usr/bin
cp source/bin/sc-handler shellcuts/usr/bin
cp source/share/shellcuts.sh shellcuts/usr/share/shellcuts

cp debian/control shellcuts/DEBIAN
cp debian/postinst shellcuts/DEBIAN

dpkg --build shellcuts

rm -r shellcuts/
