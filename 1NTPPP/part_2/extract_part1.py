#Ian Duleba 28/09/2017

# We treat lines that are not paired in temp.DAT.
# Results in temp_1.DAT

f = open("temp.DAT","r")
f2 = open("temp_1.DAT","w")

#file name
filen=""
filen_aux="" #previous line file name

i=0

#auxiliar list. It will contain the previous lines
lis=[]

for line in f:
	lis.append(line)
	#remove weird strings to get the name of the file in a particular line
	temp=line.replace("\n","").replace("\r","").replace("-pc","").replace("-pg","").replace(":pn","").replace(":qx","").replace("-qx","").replace("-nt","").replace("-mc","").split("|")

	#update names
	filen_aux=filen
	filen=temp[0]

	if(filen!=filen_aux and i%2==1): #bad pairs, they will be copied twice
		f2.write(lis[-2]) #print the previous line again
		i=i+1

	#copy
	f2.write(line)
	i=i+1

f2.close()
f.close()
