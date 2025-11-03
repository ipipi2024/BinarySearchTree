import random

class Node:
	'''
		Node class for our BST.
		@attributes:
			key: A key that allows for the ordering of the objects in our BST.
			Each key object must overload the following operations.
				-> __le__ 
				-> __eq__ 
				-> __lt__ 

			value: Each key could have an associated value. If not specified, value is None. 
			left, right: Pointers to the left and right subtrees.
			size: The size, or the number of elements in the entire subtree. 	
	'''
	def __init__(self, key, value, left = None, right = None):
		self.key = key
		self.value = value
		self.left = left 
		self.right = right 
		self.update_size()

	def update_size(self):
		''' 
			Updates the size field based on the sizes of the left and right subtrees.
		'''
		self.size = (self.left.size if self.left else 0) + (self.right.size if self.right else 0) + 1
	
	def __str__(self):
		'''
			Returns a string representation of the Node. 
			If key is an object of a user-defined type, it must override the __str__ method.
		'''
		return f"key = {self.key}; value = {self.value}"

class BST:
	'''
		This class implements a BST data structure that can be effectively used as a dictionary (or map).
		@attributes:
			root: A pointer to the root node of the BST.
			size: The total number of elements currently stored in the BST.
	'''
	def __init__(self, root = None):
		self.root = root 

	def __len__(self):
		'''
			This function returns the size of the BST.
		'''
		return self.root.size if self.root else 0
	
	def insert(self, key, value = None):
		'''
			Inserts a new key and its associated value into the BST.
			This makes the BST behave as a map data structure.
			This function does a simple insert. Does not balance the tree.
			To insert while maintaining balance, call balanced_insert.
			This is a wrapper function that calls recursive_insert.
		'''
		self.root = self.recursive_insert(self.root, key, value)

	def recursive_insert(self, x, k, v):
		'''
			Performs the actual insert operation on a key k, value v, at node x.
			Returns the root node of the tree after insertion of key k.
		'''
		# Base case: if x is None, create a new node
		if x is None:
			return Node(k, v)

		# Recursive case: insert in left or right subtree
		if k < x.key:
			x.left = self.recursive_insert(x.left, k, v)
		else:
			x.right = self.recursive_insert(x.right, k, v)

		# Update size after insertion
		x.update_size()
		return x

	def find(self, key):
		'''
			Finds if a key is present in the BST.
			Returns the following values.
				- If the key is present, returns the corresponding item (key and value pair).
			  - If multiple keys are present, any one of the valid items are returned.
				- If the key is absent, returns (None, None)
			This is a wrapper function that calls recursive_find.
		'''
		return self.recursive_find(self.root, key)

	def recursive_find(self, x, k):
		'''
			Performs the actual find operation on a key k, at node x.
			Returns the item (key and value) if the key and the value are present.
			Else returns None, None
		'''
		# Base case: if x is None, key not found
		if x is None:
			return (None, None)

		# If key matches current node, return the item
		if k == x.key:
			return (x.key, x.value)

		# Recursively search in left or right subtree
		if k < x.key:
			return self.recursive_find(x.left, k)
		else:
			return self.recursive_find(x.right, k)

	def min(self):
		'''
			This function returns the item (key and value pair) of the smallest key.
			Could return any item if tied for the smallest.
			If the BST contains nothing, then None is returned.
			This function is a wrapper function that calls iterative_min. 
			The function iterative_min is necessary because it may be called by other functions
			to get the minimum in a subtree.
		'''
		return self.iterative_min(self.root) 
	
	def iterative_min(self, r): 
		'''
			Takes a Node (subtree rooted at) r, and returns the minimum item (key and value pair) in its subtree.
		'''
		# If tree is empty, return (None, None)
		if r is None:
			return (None, None)

		# The minimum is the leftmost node
		current = r
		while current.left is not None:
			current = current.left

		return (current.key, current.value)

	def max(self):
		'''
			This function returns the item (key and value pair) of the largest key.
			Could return any item if tied for the largest.
			If the BST contains nothhing, then None is returned.
			This function is a wrapper function that calls iterative_max. 
			The function iterative_max is necessary because it may be called by other functions
			to get the maximum in a subtree.
		'''
		return self.iterative_max(self.root) 

	def iterative_max(self, r): 
		'''
			Takes a Node object, and returns the maximum item (key and value pair) in its subtree.
		'''
		# If tree is empty, return (None, None)
		if r is None:
			return (None, None)

		# The maximum is the rightmost node
		current = r
		while current.right is not None:
			current = current.right

		return (current.key, current.value)

	def pred(self, key):
		'''
			Returns the largest item (key and value pair) that is smaller or equal to key
			If no such key exists, then (None, None) is returned.
		'''
		result = (None, None)
		current = self.root

		while current is not None:
			if current.key <= key:
				# Current node is a valid predecessor
				result = (current.key, current.value)
				# Try to find a larger predecessor in the right subtree
				current = current.right
			else:
				# Current node is too large, search in left subtree
				current = current.left

		return result

	def succ(self, key):
		'''
			Returns the smallest item (key and value pair) that is greater or equal to key
			If no such key exists, then (None, None) is returned.
		'''
		result = (None, None)
		current = self.root

		while current is not None:
			if current.key >= key:
				# Current node is a valid successor
				result = (current.key, current.value)
				# Try to find a smaller successor in the left subtree
				current = current.left
			else:
				# Current node is too small, search in right subtree
				current = current.right

		return result

	def findparent(self, key):
		'''
			Finds and returns the parent Node of the node containing the given key.
			This is a helper function used internally by other BST methods.
			Returns None if:
				- The tree is empty
				- The key is not found in the tree
				- The key is the root (root has no parent)
		'''
		# Check if tree is empty
		if self.root is None:
			return None

		# Check if root has size 1 (only root exists) or if key equals root key
		if self.root.size == 1 or self.root.key == key:
			return None

		# Start from root as parent
		parent = self.root

		while True:
			if key < parent.key:
				# Search in left subtree
				if parent.left is None:
					# Reached end of tree, key not found
					return None
				elif key == parent.left.key:
					# Found the key in left child
					return parent
				else:
					# Move to left child and continue
					parent = parent.left
			else:
				# Search in right subtree (key >= parent.key)
				if parent.right is None:
					# Reached end of tree, key not found
					return None
				elif key == parent.right.key:
					# Found the key in right child
					return parent
				else:
					# Move to right child and continue
					parent = parent.right

	def delete(self, key, value = None):
		'''
			Deletes key and its associated value from the BST.
			If key is not present in the BST, then nothing happens. Nothing is returned.
			Even if the key is present, it only removes an element that matches both the key
			and its value. So, multiple keys that have different values are not removed.
			If two or more nodes contains the same key, value pair, then any one of them is removed.
			This function does a simple delete. Does not balance the tree.
			To delete while maintaining balance, call balanced_delete.
			This is a wrapper function that calls recursive_delete.
		'''
		self.root = self.recursive_delete(self.root, key, value)

	def recursive_delete(self, x, k, v):
		'''
			Performs the actual delete operation on a key k, at node x.
			Returns the root node of the tree after deletion of key k.
		'''
		pass

	def select(self, k):
		'''
			Returns the kth smallest item (key and value pair) in the BST. 
			Constraints: 1 <= k <= n
			 - Throws an assert error if k is less than 1 or greater than n
			Examples:
				if k == 1: returns the min element
				if k == n: returns the max element
				if k = n // 2: returns the median element
			This is a wrapper function that calls recursive_select.
		'''
		return self.recursive_select(self.root, k)

	def recursive_select(self, x, k):
		'''
			Performs the actual select function, at node x, for the kth smallest key.
			Constraints: 1 <= k <= n
			 - Throws an assert error if k is less than 1 or greater than n
		'''
		assert(k >= 1 and k <= x.size) # Keep this assert statement
		pass
	
	def inorder(self):
		'''
			Returns the keys of an inorder traversal of the BST.
			Returns a generator object that can be iterated over.
			This is a wrapper function that calls recursive_inorder.
		'''
		yield from self.recursive_inorder(self.root)

	def recursive_inorder(self, x):
		'''
			Performs the actual inorder traversal of the tree.
			Returns a generator object that can be iterated over to produce the traversal.
		'''
		pass

	def split(self, key):
		'''
			Splits the tree at key. Returns two BST objects. The first is the left side of 
			the split, which contains all keys <= key. The second is the right side of 
			the split, which contains all keys > key.
			This is a wrapper function that calls recursive_split.
		'''
		l, r = self.recursive_split(self.root, key)
		L = BST(l)
		R = BST(r)
		return L, R

	def recursive_split(self, x, key):
		'''
			Performs the actual split, at node x, based on key.
			Returns the root nodes of the two sides of the split.
		'''
		pass

	def join(l, r):
		'''
			Joins two BSTs together, where all keys in l are strictly smaller than all keys in r. 
			Otherwise undersirable effects may occur.
			Note;
				- l is always the tree with smaller keys
				- r is always the tree with larger keys
				- Do not call r.join(l); Can cause undesirable effects.
			The result of the join is stored in the calling object, i.e., l.
			This is a wrapper function that calls recursive_join.
		'''
		l.root = l.recursive_join(l.root, r.root)

	def recursive_join(self, l, r):
		'''
			Performs the actual join. Combines subtrees represented by root nodes l and r together.
			Note that every key in l is strictly smaller than every key in r. Otherwise, undesirable 
			effects may occur.
		'''
		pass

	def balanced_insert(self, key, value = None):
		'''
			Inserts a key and value into the BST. Performs a randomized balancing mechanism.
			Every element of the tree is equally likely to be the root. So, the height is 
			balanced with high probability.
			This is a wrapper function that calls our recursive_balanced_insert.
		''' 
		self.root = self.recursive_balanced_insert(self.root, key, value)

	def recursive_balanced_insert(self, x, k, v):
		'''
			Performs the actual insert of a key k with value v, at node (or subtree rooted at) x.
			Returns the root node of the tree after insertion.
			Performs a balancing mechanism in a probabilistic way.
			Otherwise, we recursively insert in the left or right subtree of the root based on the 
			comparison with the root.
			With probability 1 / (size of the tree + 1), the new key is inserted at the root (by calling split)
		'''
		pass

	def balanced_delete(self, key, value = None):
		'''
			Removes a node with key (and corresponding value) in the tree. If there are multiple nodes with the same key,
			the topmost node is removed.
			Performs balancing mechanism on the tree. The found node for deletion is replaced 
			with a join of its left and right subtrees.
			Note that the join is based on the sizes of these trees, always recursing on the 
			smaller tree. So this operation is always O(log n).
			This is a wrapper function that calls recursive_balanced_delete.
		'''
		self.root = self.recursive_balanced_delete(self.root, key, value)

	def recursive_balanced_delete(self, x, k, v):
		'''
			Performs the actual delete of key k and value v, at node (or subtree rooted at) x.
		'''
		pass

	def clear(self):
		'''
			Clears all the nodes in the tree.
			This is performed using a postorder traversal.
			This is a wrapper function that calls recursive_clear.
		'''
		self.recursive_clear(self.root)
		self.root = None
	
	def recursive_clear(self, x):
		'''
			Performs the actual clear, at node x. 
			Clears all nodes in x's subtree using a postorder traversal.
			Then deletes x.
		'''
		pass
		# use del x to delete the memory allocated with node x.
