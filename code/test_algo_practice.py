# encoding=utf-8

import random
import copy


class Solution_lc41(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        思路: 使用座位交换法
        根据题意可知，缺失的第一个整数是在 [1, len + 1] 之间，
        那么我们可以遍历数组，然后将对应的数据填充到对应的位置上去，比如 1 就填充到 nums[0] 的位置， 2 就填充到 nums[1]
        如果填充过程中， nums[i] < 1 && nums[i] > len，那么直接舍弃
        填充完成，我们再遍历一次数组，如果对应的 nums[i] != i + 1，那么这个 i + 1 就是缺失的第一个正数

        比如 nums = [7, 8, 9, 10, 11], len = 5
        我们发现数组中的元素都无法进行填充，直接舍弃跳过，
        那么最终遍历数组的时候，我们发现 nums[0] != 0 + 1，即第一个缺失的是 1 

        比如 nums = [3, 1, 2], len = 3
        填充过后，我们发现最终数组变成了 [1, 2, 3]，每个元素都对应了自己的位置，那么第一个缺失的就是 len + 1 == 4
        """ 
        if not nums:
            return 1
        n = len(nums)
        for i in range(n):
            _pending_swap_index = nums[i] - 1
            # 只有在 nums[i] 是 [1, len] 之间的数，并且不在自己应该呆的位置， nums[i] != i + 1 ，
            # 并且 它应该呆的位置没有被相同的值占有（即存在重复值占有）	nums[nums[i] - 1] != nums[i] 的时候才进行交换
            # 为什么使用 while ？ 因为交换后，原本 i 位置的 nums[i] 已经交换到了别的地方，
            # 交换后到这里的新值不一定是适合这个位置的，因此需要重新进行判断交换
            # 如果使用 if，那么进行一次交换后，i 就会 +1 进入下一个循环，那么交换过来的新值就没有去找到它该有的位置
            # 比如 nums = [3, 4, -1, 1] 当 3 进行交换后， nums 变成 [-1，4，3，1]，
            # 此时 i == 0，如果使用 if ，那么会进入下一个循环， 这个 -1 就没有进行处理
            while(n >= nums[i] >= 1 and nums[i] != i+1 and \
                    nums[i] != nums[_pending_swap_index]):
                # `nums[i] != nums[_pending_swap_index]` 是为了防止
                # nums[i] 和 nums[_pending_swap_index] 这两个数是相等的导致
                # while死循环
                self._swap(nums, i, _pending_swap_index)
                _pending_swap_index = nums[i] - 1

        for i in range(n):
            if nums[i] != i + 1:
                return i + 1                
        return n + 1
        
    def _swap(self, arr, index1, index2):
        arr[index1], arr[index2] = arr[index2], arr[index1]


class Solution_find_top_k_num(object):
    def find_top_k_num(self, nums_arr, nums_arr_len, top_k):
        assert nums_arr, "nums is empty."
        assert nums_arr_len > 0, "nums is empty."
        if top_k > nums_arr_len or top_k < 0:
            return None
        left_index = 0
        right_index = nums_arr_len - 1
        _p_index = self._partition(nums_arr, left_index, right_index)
        while _p_index != top_k-1:
            _p_index = self._partition(nums_arr, left_index, right_index)
            if _p_index < top_k-1:
                left_index = _p_index + 1
            elif _p_index > top_k-1:
                right_index = _p_index - 1
        return nums_arr[_p_index]

    def _partition(self, nums_arr, left_index, right_index):
        pivot_index = left_index
        _partition_index = pivot_index
        for i in range(pivot_index+1, right_index+1):
            if nums_arr[i] <= nums_arr[pivot_index]:
                nums_arr[_partition_index+1], nums_arr[i] = \
                    nums_arr[i], nums_arr[_partition_index+1]
                _partition_index += 1
        nums_arr[_partition_index], nums_arr[pivot_index] = \
            nums_arr[pivot_index], nums_arr[_partition_index]
        return _partition_index



if __name__ == "__main__":
    
    print "----------firstMissingPositive-------"  
    print 'Solution_lc41().firstMissingPositive([1, 2, 3]) :'
    print Solution_lc41().firstMissingPositive([1, 2, 3])
    print 'Solution_lc41().firstMissingPositive([3, 4, -1, 1]) :'
    print Solution_lc41().firstMissingPositive([3, 4, -1, 1])
    print 'Solution_lc41().firstMissingPositive([0, 7, 9, 12]) :'
    print Solution_lc41().firstMissingPositive([0, 7, 9, 12])

    print ""

    print "----------find_top_k_num-------"  
    print 'Solution_find_top_k_num().find_top_k_num([1, 2, 3], 3, 2) :'
    print Solution_find_top_k_num().find_top_k_num([1, 2, 3], 3, 2)
    print 'Solution_find_top_k_num().find_top_k_num([3, 1, 6, 9, 2], 5, 4) :'
    print Solution_find_top_k_num().find_top_k_num([3, 1, 6, 9, 2], 5, 4)
    print 'Solution_find_top_k_num().find_top_k_num([3, 1, 16, 9, 22], 5, 2) :'
    print Solution_find_top_k_num().find_top_k_num([3, 1, 16, 9, 22], 5, 2)