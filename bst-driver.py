
import sys
import traceback
import random
from bst import BST

def bst_test_suite(n, t, insert, delete):
	'''
		An entire test suite for a BST implementation.
		Tests the following functions.
		- insert or balanced_insert (The insert function to test is passed.)
		- delete or balanced_delete (The delete function to test is passed.)
		- len
		- find, in
		- min
		- max
		- pred
		- succ
		- select
		- inorder 
		- split
		- join
		- balanced_insert
		- balanced_delete
		- clear
	'''
	l = [i for i in range(100, n+100)]
	lset = {x for x in l}
	random.shuffle(l)

	# Testing insert and find
	# inserting keys 100 to n + 100 in random order into the BST.
	# t = BST()
	for x in l:
		insert(x)

	# finding keys 100 to n+100 in the BST.
	for x in sorted([x for x in lset]):
		s, y = t.find(x)
		if not s:
			raise Exception (f"Error 1: {x} is not present. But it should be inserted in the BST. Either your insert or find is wrong.")
			
	# Check size of the tree after insert.
	if len(t) != len(l):
		raise Exception (f"Error 2: The size of the tree does not match after insertions. Either your insert or find is wrong.")

	# Testing delete.
	# deleting random keys from the BST.
	dset = set() # Used for checking.
	for i in range(n // 5):
		x = random.randint(101, n+98) # makes sure that min is 100 and max is n+99
		if x in dset:
			continue
		delete(x)
		dset.add(x)
		lset.remove(x)
	for x in dset:
		s, y = t.find(x) 
		if s:
			raise Exception (f"Error 3: Element {x} was deleted, but present. Delete function is not correct.")
	# Check size of the tree after delete.
	if len(t) != n - len(dset):
		raise Exception (f"Errror 4: The size of the tree does not match after deletions. Possibly something wrong with delete.")

	# Testing min and max.
	if t.min()[0] != 100:
		raise Exception (f"Error 5: minimum function returned incorrectly. Minimum should be {100}, but you returned {t.min()[0]}")
	if t.max()[0] != n+99:
		raise Exception (f"Error 6: maximum function returned incorrectly. Minimum should be {n+99}, but you returned {t.max()[0]}")

	# inserting keys in the beginning.
	for i in range(100-1, 100-6, -1):
		t.insert(i)
		lset.add(i)

	# inserting keys in the end.
	for i in range(n+100, n+105):
		t.insert(i)
		lset.add(i)

	# Check if every element in lset is in t.
	for x in sorted([x for x in lset]):
		s, y = t.find(x) 
		if not s:
			raise Exception (f"Error 7: {x} is not present. But it should be inserted in the BST. Either your insert or find is wrong.")

	# Check if every element in t is in lset.
	ino = t.inorder()
	for x, _ in ino:
		if x not in lset:
			raise Exception (f"Error 8: There is a mismatch for element {x}. It exists in your tree, but was not inserted (or inserted and deleted.) Any of the following functions could be incorrect -- insert, find, delete, inorder.")

	# Deleting smallest or largest
	for i in range(100-1, 100-6, -1):
		t.delete(i)
		lset.remove(i)
	# Deleting keys in the end.
	for i in range(n+100, n+105):
		t.delete(i)
		lset.remove(i)

	# Printing after deletion by calling inorder.
	ino = t.inorder()
	lsorted = sorted([x for x in lset])
	for (k, _), x in zip(ino, lsorted):
		if k != x:
			raise Exception (f"Error 9: The inorder traversal of the tree is not correct. Errors may be in other functions, like delete.")

	# Testing min and max again
	if t.min()[0] != 100:
		raise Exception (f"Error 10: minimum function returned incorrectly. Minimum should be {100}, but you returned {t.min()[0]}")
	if t.max()[0] != n+99:
		raise Exception (f"Error 11: maximum function returned incorrectly. Maximum should be {100}, but you returned {t.min()[0]}")

	# removing keys close to 100 + n/3 and 100 + 2n/3
	for i in range(100 + n // 3, 100 + n // 3 - 5, -1):
		if i in lset:
			t.delete(i)
			lset.remove(i)
	for i in range(100 + 2 * n // 3, 100 + 2 * n // 3 - 5, -1):
		if i in lset:
			t.delete(i)
			lset.remove(i)

	# Testing pred
	fset = [t.min()[0]-1, t.min()[0], 100 + n // 3, 100 + 2 * n // 3, t.max()[0], t.max()[0]+1]
	preds = [None, t.min()[0], 100 + n // 3 - 5, 100 + 2 * n // 3 - 5, t.max()[0], t.max()[0]]
	if 100 + n // 3 - 5 not in lset:
		t.insert(100 + n // 3 - 5)
		lset.add(100 + n // 3 - 5)
	if 100 + 2 * n // 3 - 5 not in lset:
		t.insert(100 + 2 * n // 3 - 5)
		lset.add(100 + 2 * n // 3 - 5)
	for x, y in zip(fset, preds):
		k, _ = t.pred(x)
		if k != y:
			raise Exception (f"Error 12: pred function returned incorrectly for {x}. Should return {y}. You returned {k}")

	# Testing succ
	if 100 + n // 3 + 1 not in lset:
		t.insert(100 + n // 3 + 1)
		lset.add(100 + n // 3 + 1)
	if 100 + 2 * n // 3 + 1 not in lset:
		t.insert(100 + 2 * n // 3 + 1)
		lset.add(100 + 2 * n // 3 + 1)
	fset = [t.min()[0]-1, t.min()[0], 100 + n // 3 - 4, 100 + 2 * n // 3 - 4, t.max()[0], t.max()[0]+1]
	succs = [t.min()[0], t.min()[0], 100 + n // 3 + 1, 100 + 2 * n // 3 + 1, t.max()[0], None]
	for x, y in zip(fset, succs):
		k, _ = t.succ(x)
		if k != y:
			raise Exception (f"Error 13: succ function returned incorrectly for {x}. Should return {y}. You returned {k}")

	# Testing select and rank
	ino = t.inorder()
	for (k, _), i in zip(ino, range(1, len(t)+1)):
		x, _ = t.select(i)
		# i2 = t.rank(k)
		if k != x:
			raise Exception (f"Error 16: select function returned inccorrectly. Selecting the {i}th smallest returned {x}, when it should have returned {k}")
		# if i2 != i:
		# 	raise Exception (f"Error 17: rank function returned inccorrectly. Rank of {k} returned {i2}, when it should actually return {i}")

	# Testing split. Splitting on key 100 + n // 3.
	l1, r1 = t.split(100 + n // 3)
	l1set = sorted([x for x in lset if x <= 100 + n // 3])
	r1set = sorted([x for x in lset if x > 100 + n // 3])
	inol = l1.inorder()
	for (x, _), y in zip(inol, l1set):
		if x > 100 + n // 3:
			raise Exception ("Error 18: split function on {100 + n // 3} contains {x} on the left tree. Incorrect key on the left side of the split.")
		if x != y:
			raise Exception ("Error 19: split function on {100 + n // 3} does not match the correct order of keys on the left side. Expected {y}, found {x}.")
	inor = r1.inorder()
	for (x, _), y in zip(inor, r1set):
		if x <= 100 + n // 3:
			raise Exception ("Error 20: split function on {100 + n // 3} contains {x} on the right tree. Incorrect key on the right side of the split.")
		if x != y:
			raise Exception ("Error 21: split function on {100 + n // 3} does not match the correct order of keys on the right side. Expected {y}, found {x}.")

	# Splitting again. Splitting right side on key 100 + 2 * n // 3	
	l2, r2 = r1.split(100 + 2 * n // 3)
	l2set = sorted([x for x in r1set if x <= 100 + 2 * n // 3])
	r2set = sorted([x for x in r1set if x > 100 + 2 * n // 3])
	inol = l2.inorder()
	for (x, _), y in zip(inol, l2set):
		if x > 100 + 2 * n // 3:
			raise Exception ("Error 22: split function on {100 + 2 * n // 3} contains {x} on the left tree. Incorrect key on the left side of the split.")
		if x != y:
			raise Exception ("Error 23: split function on {100 + 2 * n // 3} does not match the correct order of keys on the left side. Expected {y}, found {x}.")
	inor = r2.inorder()
	for (x, _), y in zip(inor, r2set):
		if x <= 100 + 2 * n // 3:
			raise Exception ("Error 24: split function on {100 + 2 * n // 3} contains {x} on the right tree. Incorrect key on the right side of the split.")
		if x != y:
			raise Exception ("Error 25: split function on {100 + 2 * n // 3} does not match the correct order of keys on the right side. Expected {y}, found {x}.")

	# Testing join
	l1.join(l2)
	for (k1, _), k2 in zip(l1.inorder(), sorted([x for x in lset])):
		if k1 != k2:
			raise Exception (f"Error 26: join function incorrect. Key {k2} expected. Got {k1}.")
	
	# Testing clear
	t.clear()
	if len(t) != 0:
		raise Exception (f"Error 27: Did not clear or delete all nodes properly.")
	
	return True

def bst_test_suite_wrapper(n, t, insert = None, delete = None):
	if not insert:
		insert = t.insert
	if not delete:
		delete = t.delete
	return bst_test_suite(n, t, insert, delete)

if __name__ == "__main__":
	try:
		t = BST() 
		n = 100
		if bst_test_suite_wrapper(n, t, t.insert, t.delete):
			print(f"Yay! Passed all tests for n = {n}.")
		
		n = 500_000
		if bst_test_suite_wrapper(n, t, t.balanced_insert, t.balanced_delete):
			print(f"Yay! Passed all tests for n = {n}.")

	except Exception as e:
		print(e)
		print(traceback.print_exc())
