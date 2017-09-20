#outputs the hand and the first card played
#http://www.bridgebase.com/tools/handviewer.html?bbo=y&linurl=http://www.bridgebase.com/tools/vugraph_linfetch.php?id=XXXXX

st1="|sv|o|mb|1N|mb|p|mb|p|mb|p|"
st2="|sv|o|mb|p|mb|1N|mb|p|mb|p|mb|p|"
st3="|sv|o|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p|"
st4="|sv|o|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p|"


f = open("temp2.DAT","r")
myList = []

filen=""
filen_aux=""
i=0

#decides if the string s is a card, like 'hT' or 'S9'
def is_card(s):
	if(len(s)!=2):
		return False
	if(s[0]!='S' and s[0]!='s' and s[0]!='H' and s[0]!='h' and s[0]!='D' and s[0]!='d' and s[0]!='C' and s[0]!='c'):
		return False
	if(s[1]!='2' and s[1]!='3' and s[1]!='4' and s[1]!='5' and s[1]!='6' and s[1]!='7' and s[1]!='8' and s[1]!='9' and s[1]!='T' and s[1]!='J' and s[1]!='Q' and s[1]!='K' and s[1]!='A' and s[1]!='t' and s[1]!='j' and s[1]!='q' and s[1]!='k' and s[1]!='a'):
		return False
	return True

#there are instances where this happens: "|sv|o|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p|mb|p|pg||"
#errors
er=0

while True:
	line1 = f.readline()
	line2 = f.readline()
	if not line2: break  # EOF

	temp1=line1.replace("\n","").replace("\r","").replace("-pc","").replace("-pg","").replace(":pn","").replace(":qx","").replace("-qx","").replace("-nt","").replace("-mc","").replace(st4,"|").replace(st3,"|").replace(st2,"|").replace(st1,"|").replace("pc|","").split("|")
	temp2=line2.replace("\n","").replace("\r","").replace("-pc","").replace("-pg","").replace(":pn","").replace(":qx","").replace("-qx","").replace("-nt","").replace("-mc","").split("|")
	
	#check if pair is proper(if they are from the same file)
	if(temp1[0]!=temp2[0]):
		print("Error!")
		break

	#temp1[5] is the hands
	#print temp1
	if(len(temp1[5])==72):
		if(temp1[6]=='pg'):#first card is in line2
			if(is_card(temp2[1])):
				print temp1[5]+"|"+temp2[1]
			else:
				print temp2, "One"
				break
		else:
			if(is_card(temp1[6])):
				print temp1[5]+"|"+temp1[6]
			else:
				if(temp1[6]=='nt'):
					if(is_card(temp2[1])):
						print temp1[5]+"|"+temp2[1]
					else:
						er=er+1 #too much dialog, aint nobody got time for that
				
				elif(temp1[6]!='mb'):
					er=er+1
					#print temp1, temp1[6], "Two"
	else:#some hands only show the cards of three players
		er=er+1
print er #=40, not gonna make a big difference
f.close()
