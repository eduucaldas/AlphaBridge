#remove from temp.DAT lines that are not paired.
# Results in temp_extract1.DAT (done by hand and that's obviously not good. Need to change it later)

f = open("temp.DAT","r")
myList = []

filen=""
filen_aux=""
i=0

for line in f:
	temp=line.replace("\n","").replace("\r","").replace("-pc","").replace("-pg","").replace(":pn","").replace(":qx","").replace("-qx","").replace("-nt","").replace("-mc","").split("|")

	filen_aux=filen
	filen=temp[0]

	if(filen!=filen_aux and i%2==1):
		print line
		i=i+1
	i=i+1
f.close()
