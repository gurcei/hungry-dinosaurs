all:
	cp /c/Users/gurcei/AppData/Roaming/xemu-lgb/mega65/hdos/11.D81 .
	c1541 -attach 11.D81 -read viet.v,s -read thai.v,s -read aus.v,s -read turk.v,s
