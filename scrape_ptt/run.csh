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
./scrape_ptt.py -et 20180429 -out $out_dir -isd 0 -url https://www.ptt.cc/bbs/nba/index.html
