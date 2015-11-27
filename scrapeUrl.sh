wget -r -l1 --max-redirect 7 --progress=dot --no-check-certificate --read-timeout=8 --timeout=8 --ca-certificate=cert/cacert.perm \
-e robots=off --tries=2 --reject=css,ico,webm,bin,iso,ogv,mov,mp4,png,jpg,gif,jpeg,pdf,doc,js,ppt,xls,zip,gzip,tar,mpg,mpeg,txt,swf,csv,rar,wav,mp3,ogg,avi,ffmpeg,ffmpg,wmv,tif,xlsx,jfif \
--header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36" \
--header="Referer: http://xmodulo.com/" \
--header="Accept:	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" \
--header="Accept-Language:	en-US,en;q=0.8,nl;q=0.6" \
-O ph_raw/$1.html $1 \
--domains $1 -np