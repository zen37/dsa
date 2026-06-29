'''
Given an integer array nums and an integer k, return true if there are 
two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.

nums = [1, 2, 3, 1]
k = 3
True

nums = [1, 0, 1, 1]
k = 1
True

{
1: [0, 2, 3]
0: [1]

}

nums = [1, 2, 3, 2, 1]
k = 10
False 

4 <= 10 

Approaches:
0. Brute Force 
1. Dictionary with the element as the key, pos array as value 

2. Dictionary with last seen index as value 
  a. Check edge cases (if k == 0 or len(nums) == 1)
  b. Init dictionary
  c. Loop through nums
    1. If key does not exist, add with index as value
    2. If key exists, check distance between current value and existing key
      If distance <= k: return True
      Else replace existing value for that key with the current index 
  d. If we do all of this and never meet the requirements then it must be False 

https://leetcode.com/problems/contains-duplicate-ii/description/ 