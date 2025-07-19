def count_1_to_10():
	for i in range(1, 11):
		if i == 10:
			print(i)
		else:
			print(i, end=', ')
		

def main():
	print("Let's count from 1 to 10!")
	count_1_to_10()

main()

