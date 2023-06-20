fileN=${1/md\//}
echo $fileN
# s5 revealjs
pandoc -t s5 -s $1 -o html/${fileN/md/html} 
