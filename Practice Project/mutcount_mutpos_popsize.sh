//bash mutcount_mutpos_popsize.sh

cd ~/Desktop
name="INPUT_NAME"
slim -d "mut_count_file='mut_counts.csv'" -d "mut_pos_file='mut_positions.csv'" -d "pop_size_file='pop_size_file.csv'" "$name"