#!/usr/bin/python3
# python3 2f_3f.py [peers] [only_optimal]

from math import floor
import sys


def get_faulty_in_2f_1(all_peers):
	return floor(all_peers/2 + 1)


def get_faulty_in_3f_1(all_peers):
	return floor(all_peers/3*2 + 1)


def main(limit, only_optimal):
	reached_diffs = []

	print(" peers | 2f + 1 | 3f + 1 | diff")
	print("--------------------------------")

	for i in range(1, limit+1):
		faulty_2f = get_faulty_in_2f_1(i)
		faulty_3f = get_faulty_in_3f_1(i)

		diff = faulty_3f - faulty_2f
		if not only_optimal or only_optimal and diff not in reached_diffs:
			reached_diffs.append(diff)
			print(f"{str(i).rjust(6)} | {str(faulty_2f).rjust(6)} | {str(faulty_3f).rjust(6)} | {str(diff).rjust(4)}")

if __name__=="__main__":
	if len(sys.argv) < 3:
		print("Usage: python3 2f_3f.py [peers] [only_optimal]")
		exit()

	peers = int(sys.argv[1])
	only_optimal = sys.argv[2] == "True"

	main(peers, only_optimal)
