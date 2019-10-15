ch = ['V','S','P','O','S','C','L','O','K','E','D','S','P','E','V']
encoded = []
decode = []

for i in ch:
	encoded[i] = chr(ord(ch[i]))

for i in range(26):
	for x in ch:
		decode[x] = (encoded[x]-i)%26
	print(decode)
	