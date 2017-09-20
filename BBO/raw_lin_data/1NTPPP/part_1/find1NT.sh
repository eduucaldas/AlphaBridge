#Ian Duleba 13/09/2017
#run this script in the same folder as https://github.com/eitazhou/bridge_played_hands/tree/master/raw_lin_data
#we will search for specific strings (st1,st2,st3,st4) and append results (2 consecutive lines) from grep to file temp.DAT
#we are interested in:
#P P P 1NT P P P
#P P 1NT P P P
#P 1NT P P P
#1NT P P P

st1="|sv|o|mb|1N|mb|p|mb|p|mb|p|"
st2="|sv|o|mb|p|mb|1N|mb|p|mb|p|mb|p"
st3="|sv|o|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"
st4="|sv|o|mb|p|mb|p|mb|p|mb|1N|mb|p|mb|p|mb|p"

dir="000"

for i in `seq 0 423`; #423 folders
	do
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
	done        



