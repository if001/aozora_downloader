# readme
青空文庫の本をダウンロードする


## 作者ごとのzipファイルをダウンロードする

`sh download_zip.sh {author_id}`

svn commandを使う。存在しない場合は `sudo apt install subversion`


## clean up
`python format_file.py -id {author_id}`

`/out_{author_id}`のディレクトリ以下にformatされたファイルが出力される

`out_{author_id}/edit`: utf-8化、formatされたtxt

`out_{author_id}/org`: orignalのtxt

出力ファイルは以下のような、文ごとに改行、不要部分が削除された型になる。

```
sentence1\n
sentence2\n
sentence3\n
.
.
.
```

`python format_file.py -id {author_id} --kepp_title`

`option --keep_title`で出力ファイルの先頭をタイトルにする
