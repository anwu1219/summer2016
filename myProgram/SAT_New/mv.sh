for file in *.cnf
do 
    x = $((RANDOM % 5))
    echo x
    if [$(x) -eq 1] 
    then
	mv $file testset; 
    else 
	mv $file trainset; 
    fi; 
done
