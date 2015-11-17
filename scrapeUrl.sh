wget -r -l2 --max-redirect 7 --progress=dot --no-check-certificate --read-timeout=8 --timeout=8 --ca-certificate=cert/cacert.perm \
-U Mozilla -e robots=off --tries=2 --reject=css,ico,webm,bin,iso,ogv,mov,mp4,png,jpg,gif,jpeg,pdf,doc,js,ppt,xls,zip,gzip,tar,mpg,mpeg,txt,swf,csv,rar,wav,mp3,ogg,avi,ffmpeg,ffmpg,wmv,tif,xlsx,jfif \
 -O raw_html/$1.html $1 \
--domains $1 -np
