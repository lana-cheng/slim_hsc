//bash clonecorr.sh

cd ~/Desktop
echo "InitialPop,Correlation" > ~/Desktop/correlations.csv
for initialpop in $(seq 200 200 2000) //run multiple simulations to test correlation. seq first, increment, last
do
	seed=$RANDOM
	r=$(slim -s $seed -d initialpop=$initialpop INPUT_NAME.slim | grep "^correlation" | cut -d',' -f2)
	echo "$initialpop,$r" >> ~/Desktop/correlations.csv
done