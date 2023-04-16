all:
	cp /c/Users/gurcei/AppData/Roaming/xemu-lgb/mega65/hdos/11.D81 .
	# c1541 -attach 11.D81 -read viet.v,s -read thai.v,s -read aus.v,s -read turk.v,s -read onion.v,s -read mega65.v,s -read songs.p,s
	# c1541 -attach /c/Users/gurcei/AppData/Roaming/xemu-lgb/mega65/hdos/11.D81 -delete test.v -write uzbek.v "test.v,s"
	# c1541 -attach /c/Users/gurcei/AppData/Roaming/xemu-lgb/mega65/hdos/11.D81 -delete test.v -write tiger.v "test.v,s"
	# c1541 -attach /c/Users/gurcei/AppData/Roaming/xemu-lgb/mega65/hdos/11.D81 -delete turk.v -write turk.v "turk.v,s"
