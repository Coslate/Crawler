#! /bin/csh -f

set out_dir = "./output"

if ( -d $out_dir ) then
    rm -rf $out_dir
    mkdir $out_dir
else 
    mkdir $out_dir
endif


#./scrape_ptt.py -et 20180429 -key BOX -out $out_dir -isd 1 > title_list.log
#./scrape_ptt.py -et 20180429 -key 爆雷魔 -out $out_dir -isd 1 > title_list.log
#./scrape_ptt.py -et 20180429 -out $out_dir -isd 0 -url https://www.ptt.cc/bbs/nba/index.html
# -key support multiple keywords : keyword1_keyword2_keyword3_..._keywordn
./scrape_ptt.py -et 20180510 -out $out_dir -isd 0 -url https://www.ptt.cc/bbs/nba/index.html -key lwei781_msdie911545

# auto-extract image in beauty. For example
./scrape_ptt.py -et 20180805 -out ./beauty_20180806_20180805 -url https://www.ptt.cc/bbs/Beauty/index.html -isd 1 -thnum_push 49 -out_img_folder img_folder > debug.log
