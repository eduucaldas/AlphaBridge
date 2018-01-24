#Ian Duleba 13/09/2017 - update 28/09/2017
#You should run this script in the same folder as raw_lin_data
#output the results to temp.DAT
#we will search for specific strings (st1,...,st20) and append results (2 consecutive lines) from grep to file temp.DAT
#we are interested in:
#P P P 1NT P P P
#P P 1NT P P P
#P 1NT P P P
#1NT P P P

#strings we are looking for
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

dir="000"

for i in `seq 0 423`; #423 folders
	do
		#defining the name of the folder
		if [ $i -lt 10 ]; then
			dir="00$i"
		else
			if [ $i -lt 100 ]; then
				dir="0$i"
			else
				dir="$i"
			fi
		fi

		#find patterns
		#echo $dir
		grep -r -A1 --no-group-separator $st1 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st2 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st3 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st4 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st5 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st6 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st7 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st8 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st9 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st10 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st11 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st12 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st13 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st14 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st15 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st16 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st17 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st18 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st19 $dir/* >> temp.DAT
		grep -r -A1 --no-group-separator $st20 $dir/* >> temp.DAT
		
	done        



