#Still not working properly, ignore this. You can jump to part_3
#Ian Duleba 28/09/2017
#The script takes temp_1.DAT as input and outputs the hand and the first card played to temp_final.DAT

#bidding strings that we need to get rid of now
st1="|sv|e|mb|1N|mb|p|mb|p|mb|p|"
st2="|sv|e|mb|p|mb|1N|mb|p|mb|p|mb|p"
st3="|sv|e|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"
st4="|sv|e|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"

st5="|sv|o|mb|1N|mb|p|mb|p|mb|p|"
st6="|sv|o|mb|p|mb|1N|mb|p|mb|p|mb|p"
st7="|sv|o|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"
st8="|sv|o|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"

st9="|sv|n|mb|1N|mb|p|mb|p|mb|p|"
st10="|sv|n|mb|p|mb|1N|mb|p|mb|p|mb|p"
st11="|sv|n|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"
st12="|sv|n|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"

st13="|sv|b|mb|1N|mb|p|mb|p|mb|p|"
st14="|sv|b|mb|p|mb|1N|mb|p|mb|p|mb|p"
st15="|sv|b|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"
st16="|sv|b|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"

st17="|sv|0|mb|1N|mb|p|mb|p|mb|p|"
st18="|sv|0|mb|p|mb|1N|mb|p|mb|p|mb|p"
st19="|sv|0|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"
st20="|sv|0|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"


f = open("temp_1.DAT","r")
myList = []

filen=""
filen_aux=""
i=0

#decides if the string s is a card in the format of the lin files, like 'hT' or 'S9'
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

	#get rid of unnecessary strings and split
	#not very readable, I know.
	temp1=line1.replace("\n","").replace("\r","").replace("-pc","").replace("-pg","").replace(":pn","").replace(":qx","").replace("-qx","").replace("-nt","").replace("-mc","").replace(st20,"|").replace(st19,"|").replace(st18,"|").replace(st17,"|").replace(st16,"|").replace(st15,"|").replace(st14,"|").replace(st13,"|").replace(st12,"|").replace(st11,"|").replace(st10,"|").replace(st9,"|").replace(st8,"|").replace(st7,"|").replace(st6,"|").replace(st5,"|").replace(st4,"|").replace(st3,"|").replace(st2,"|").replace(st1,"|").replace("pc|","").split("|")
	temp2=line2.replace("\n","").replace("\r","").replace("-pc","").replace("-pg","").replace(":pn","").replace(":qx","").replace("-qx","").replace("-nt","").replace("-mc","").split("|")
	
	#check if pair is proper(if they are from the same file). In principle we don't need to do this
	#extract_part1.py already fixed any improperness, but one can never be too safe. 
	if(temp1[0]!=temp2[0]):
		print("Error!", temp1[0], temp2[0])
		break

	#temp1[5] are the hands
	#print temp1, temp2
	if len(temp1)<6:
		continue
	if(len(temp1[5])==72 or len(temp1[5])==54):#4 players with all the information of the hands

		if(temp1[6]=='pg'):#first card is in line2
			if(is_card(temp2[1])):
				1#print temp1[5]+"|"+temp2[1]
			else:
				print temp2, "One"
				break
		else:
			if(is_card(temp1[6])):
				1#print temp1[5]+"|"+temp1[6]
			else:
				if(temp1[6]=='nt'): #fucking dialog. I will create a script to burn them all. Let them rot in hell.
					if(is_card(temp2[1])):
						1#print temp1[5]+"|"+temp2[1]
					else:
						1#er=er+1 #too much dialog, aint nobody got time for that. I'll deal with this shit later.
				
				elif(temp1[6]!='mb'):
					1#er=er+1
					#print temp1, temp1[6], "Two"

	else:#some hands only show the cards of three players
		if (len(temp1[3])==72):
			er=er+1
			print temp1, temp2

print er #=40, not gonna make a big difference
f.close()
