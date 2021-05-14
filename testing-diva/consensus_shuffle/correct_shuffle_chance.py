# python3 correct_shuffle_chance.py [total peers] [up peers]

def chance(total, up):
	c = 1
	print(f"[#] c = 1")
	for i in range(1, up):
		c *= (up-i) / (total-i)
		print(f"[#] c *= ({up-i}) / ({total-i}) \t=> {round(c,3)}")
	return c


if __name__ == "__main__":
	from sys import argv

	if len(argv) < 3:
		print("[!] Usage: python3 correct_shuffle_chance.py [total peers] [up peers]")

	else:
		total, up = int(argv[1]), int(argv[2])
		c = chance(total, up)

		print(f"[*] Chance to get a correct shuffle is about 1 to {'%.3g' % (1/c)}.")