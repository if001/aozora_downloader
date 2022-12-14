#/bin/sh
# 江戸川 乱歩 001779
# if cannot use svn command,
# sudo apt install subversion

id=$1
svn export https://github.com/aozorabunko/aozorabunko/trunk/cards/${id}/files/
rm files/*png
rm files/*html
mv files ${id}
