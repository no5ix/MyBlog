# encoding=utf-8

import random
import copy


def insert_sort(arr, left_index, right_index):
    if not arr:
        return
    for i in xrange(left_index+1, right_index+1):  # 从left_index+1开始, 也就是从第二个开始
        for j in xrange(i, left_index, -1):
            if arr[j] < arr[j-1]:  # 注意保证j-1大于0
                # 通过不断的与前面已经排好序的元素比较并交换,
                arr[j-1], arr[j] = arr[j], arr[j-1]
            else:
                break


def insert_sort_optimized(arr, left_index, right_index):
    if not arr:
        return
    for i in xrange(left_index+1, right_index+1):  # 从left_index+1开始, 也就是从第二个开始
        temp_i_val = arr[i]
        j = i
        while j >= left_index+1:
            if temp_i_val < arr[j-1]:  # 注意保证j-1大于0
                arr[j] = arr[j-1]  # 通过不断的与前面已经排好序的元素比较并直接赋值
                j -= 1
            else:
                break
        arr[j] = temp_i_val  # 已经找到该插入的地方了, 直接赋值


def _merge(arr, left_index, mid_index, right_index):
    """
    归并的具体思路:  
        回到我们玩扑克牌的例子，假设桌上有两堆牌面朝上的牌，每堆都已**排序**，最小的牌在顶上。
        我们希望把这两堆牌合并成单一的排好序的输出堆，牌面朝下地放在桌上。
        我们的基本步骤包括在牌面朝上的两堆牌的顶上两张牌中选取较小的一张，将该牌从其堆中移开（该堆的顶上将
        显露一张新牌）并牌面朝下地将该牌放置到输出堆。
        重复这个步骤，直到一个输入堆为空，这时，我们只是拿起剩余的输入堆并牌面朝下地将该堆放置到输出堆。
    """
    # 注释掉下面这句是因为mid不一定等于(l+r)/2, 比如在`merge_sort_bottom_up()`就有可能
    # mid_index = left_index + (right_index - left_index) / 2
    temp_arr = []
    i = left_index
    j = mid_index + 1
    while i <= mid_index and j <= right_index:
        if arr[i] <= arr[j]:
            temp_arr.append(arr[i])
            i += 1
        else:
            temp_arr.append(arr[j])
            j += 1
    # 这一步是模拟: 直到一个输入堆为空，这时，我们只是拿起剩余的输入堆并牌面朝下地将该堆放置到输出堆。
    temp_arr.extend(arr[i:mid_index+1])
    temp_arr.extend(arr[j:right_index+1])  # 注意右边界是小于等于right_index的
    # 把归并好的数组数据放到原数组left_index到right_index的位置上去
    for m in xrange(0, right_index-left_index+1):
        arr[left_index+m] = temp_arr[m]


def merge_sort(arr, left_index, right_index):
    # 当 `merge_sort()` 递归到left_index等于right_index的时候,
    # 说明left_index, right_index已经相邻了,
    # 说明已经分解到底了, 左右都只剩下一个元素了, 所以此时应该return然后执行 `_merge()` 了
    if not arr or left_index >= right_index:
        return
    # 注意这里不能直接 `mid_index=(left_index+right_index)/2`,
    # 防止当left_index和right_index很大的时候他们之和溢出
    mid_index = left_index + (right_index - left_index) / 2
    merge_sort(arr, left_index, mid_index)
    merge_sort(arr, mid_index+1, right_index)
    _merge(arr, left_index, mid_index, right_index)


def merge_sort_optimized(arr, left_index, right_index):
    # 当 `merge_sort()` 递归到left_index等于right_index的时候,
    # 说明left_index, right_index已经相邻了,
    # 说明已经分解到底了, 左右都只剩下一个元素了, 所以此时应该return然后执行 `_merge()` 了
    if not arr or left_index >= right_index:
        return

    # 优化1:
    #   数据量较小则使用插入排序
    if (right_index - left_index) < 15:
        insert_sort_optimized(arr, left_index, right_index)
        return

    # 注意这里不能直接 `mid_index=(left_index+right_index)/2`,
    # 防止当left_index和right_index很大的时候他们之和溢出
    mid_index = left_index + (right_index - left_index) / 2
    merge_sort(arr, left_index, mid_index)
    merge_sort(arr, mid_index+1, right_index)

    # 优化2:
    #   因为此时arr[mid_index]左边的数组里最大的, 而arr[mid_index+1]是右边最小的,
    #   如果arr[mid_index] <= arr[mid_index+1]则说明这一轮递归的arr的left到right已经是从小到大有序的了
    #   所以只在对于arr[mid_index] > arr[mid_index+1]的情况,进行merge,
    #   对于近乎有序的数组非常有效,但是对于一般情况,有一定的性能损失(因为多了这行代码判断大小)
    if arr[mid_index] > arr[mid_index+1]:
        _merge(arr, left_index, mid_index, right_index)


def merge_sort_bottom_up(arr, left_index, right_index):
    if not arr or left_index >= right_index:
        return
    arr_len = right_index - left_index + 1
    size = 1
    # 注意这里不是 `while size <= arr_len/2`,
    # 比如arr_len=12, size为4的话, 只能把[0, 7]和[8, 11]的两个子数组归并成有序
    # 那只有size为8, 这样2倍size才能把arr全部归并
    # 但size=8的话, 大于arr_len/2了, 所以应该`while size < arr_len`
    while size < arr_len:
        cur_left_index = left_index
        while cur_left_index <= right_index-size:
            cur_mid_index = cur_left_index + size - 1
            possible_right_index = cur_left_index + 2*size - 1
            # possible_right_index有可能已经大于right_index了, 所以要min一下
            cur_right_index = min(possible_right_index, right_index)
            # 归并从i位置开始的两倍size的一组数据
            _merge(arr, cur_left_index, cur_mid_index, cur_right_index)
            cur_left_index += size * 2  # 每次归并完一组数据就i移动size的两倍
        # print "size: %d" % size
        # print arr
        size *= 2  # size从1开始每次增加两倍


def merge_sort_bottom_up_optimized(arr, left_index, right_index):
    if not arr or left_index >= right_index:
        return

    # 优化1:
    #   先以size为16为一组数据来逐个对每组插入排序一遍
    size = 16
    cur_left_index = left_index
    while cur_left_index < right_index:
        possible_right_index = cur_left_index + 2*size - 1
        # possible_right_index有可能已经大于right_index了, 所以要min一下
        cur_right_index = min(possible_right_index, right_index)
        insert_sort(arr, cur_left_index, cur_right_index)
        cur_left_index += size  # 右移到下一个size大小开头位置

    arr_len = right_index - left_index + 1
    # size = 1

    # 注意这里不是 `while size <= arr_len/2`,
    # 比如arr_len=12, size为4的话, 只能把[0, 7]和[8, 11]的两个子数组归并成有序
    # 那只有size为8, 这样2倍size才能把arr全部归并
    # 但size=8的话, 大于arr_len/2了, 所以应该`while size < arr_len`
    while size < arr_len:
        cur_left_index = left_index
        while cur_left_index <= right_index-size:
            cur_mid_index = cur_left_index + size - 1
            possible_right_index = cur_left_index + 2*size - 1
            # possible_right_index有可能已经大于right_index了, 所以要min一下
            cur_right_index = min(possible_right_index, right_index)
            # 归并从i位置开始的两倍size的一组数据
            # 优化2:
            #   因为此时arr[mid_index]左边的数组里最大的, 而arr[mid_index+1]是右边最小的,
            #   如果arr[mid_index] <= arr[mid_index+1]则说明这一轮递归的arr的left到right已经是从小到大有序的了
            #   所以只在对于arr[mid_index] > arr[mid_index+1]的情况,进行merge,
            #   对于近乎有序的数组非常有效,但是对于一般情况,有一定的性能损失(因为多了这行代码判断大小)
            if arr[cur_mid_index] > arr[cur_mid_index+1]:
                _merge(arr, cur_left_index, cur_mid_index, cur_right_index)
            cur_left_index += size * 2  # 每次归并完一组数据就i移动size的两倍
        # print "size: %d" % size
        # print arr
        size *= 2  # size从1开始每次增加两倍


def _partition(arr, left_index, right_index):
    # 选一个元素作为枢轴量,
    # 为了模拟上面这个动画演示, 这里我们选取最左边的元素
    pivot_index = left_index
    pivot = arr[pivot_index]
    # partition_index 在还没开始遍历之前时应该指向待遍历元素的最左边的那个元素的前一个位置
    # 在这里这种写法就是 `left_index`
    # 这才符合partition_index的定义:
    #       partition_indexy指向小于pivot的那些元素的最后一个元素,
    #       即 less_than_pivots_last_elem_index
    # 因为还没找到比pivot小的元素之前,
    # partition_index是不应该指向任何待遍历的元素的
    partition_index = less_than_pivots_last_elem_index = left_index

    i = left_index + 1  # 因为pivot_index取left_index了, 则我们从left_index+1开始遍历
    while i <= right_index:
        if arr[i] < pivot:
            arr[i], arr[partition_index+1] = arr[partition_index+1], arr[i]
            partition_index += 1
        i += 1
    arr[pivot_index], arr[partition_index] = arr[partition_index], arr[pivot_index]
    return partition_index


def quick_sort(arr, left_index, right_index):
    # 如果left等于right则说明已经partition到只有一个元素了, 可以直接return了
    if not arr or left_index >= right_index:
        return
    partition_index = _partition(arr, left_index, right_index)
    # 把partition_index左边的数据再递归快排一遍
    quick_sort(arr, left_index, partition_index-1)
    quick_sort(arr, partition_index+1, right_index)


def _partition_optimized(arr, left_index, right_index):
    # 选一个元素作为枢轴量,
    # 为了模拟上面这个动画演示, 这里我们选取最左边的元素
    pivot_index = left_index

    # 优化1:
    #   随机选一个元素和最左边的交换,
    #   配合下方的`pivot = arr[left_index]`就达到了随机选一个元素当pivot的效果
    rand_index = random.randint(left_index, right_index)
    arr[pivot_index], arr[rand_index] = arr[rand_index], arr[pivot_index]

    pivot = arr[pivot_index]
    # partition_index 在还没开始遍历之前时应该指向待遍历元素的最左边的那个元素的前一个位置
    # 在这里这种写法就是 `left_index`
    # 这才符合partition_index的定义:
    #       partition_indexy指向小于pivot的那些元素的最后一个元素,
    #       即 less_than_pivots_last_elem_index
    # 因为还没找到比pivot小的元素之前,
    # partition_index是不应该指向任何待遍历的元素的
    partition_index = less_than_pivots_last_elem_index = left_index

    i = left_index + 1  # 因为pivot_index取left_index了, 则我们从left_index+1开始遍历
    while i <= right_index:
        if arr[i] < pivot:
            arr[i], arr[partition_index+1] = arr[partition_index+1], arr[i]
            partition_index += 1
        i += 1
    arr[pivot_index], arr[partition_index] = arr[partition_index], arr[pivot_index]
    return partition_index


def quick_sort_optimized(arr, left_index, right_index):
    # 如果left等于right则说明已经partition到只有一个元素了, 可以直接return了
    if not arr or left_index >= right_index:
        return
    # 优化2:
    #   小数组用插排
    if (right_index - left_index) <= 15:
        insert_sort(arr, left_index, right_index)
        return
    partition_index = _partition(arr, left_index, right_index)
    # 把partition_index左边的数据再递归快排一遍
    quick_sort(arr, left_index, partition_index-1)
    quick_sort(arr, partition_index+1, right_index)


def quick_sort_3_ways(arr, left_index, right_index):
    # 如果left等于right则说明已经partition到只有一个元素了, 可以直接return了
    if not arr or left_index >= right_index:
        return
    if (right_index - left_index) <= 15:
        insert_sort(arr, left_index, right_index)
        return

    # 选一个元素作为枢轴量,
    # 为了模拟上面这个动画演示, 这里我们选取最左边的元素
    pivot_index = left_index
    # 随机选一个元素和最左边的交换,
    # 配合下方的`pivot = arr[left_index]`就达到了随机选一个元素当pivot的效果
    rand_index = random.randint(left_index, right_index)
    arr[pivot_index], arr[rand_index] = arr[rand_index], arr[pivot_index]

    pivot = arr[pivot_index]
    # lt_index 指向小于pivot的那些元素的最右边的一个元素,
    # lt_index 即 less_than_pivots_last_elem_index
    # 因为还没找到比pivot小的元素之前,
    # lt_index 是不应该指向任何待遍历的元素的,
    # gt_index 同理, gt_index指向大于pivot的那些元素的最左边的一个元素,
    lt_index = less_than_pivots_last_elem_index = left_index
    gt_index = right_index + 1

    i = left_index + 1  # 因为pivot_index取left_index了, 则我们从left_index+1开始遍历
    while i < gt_index:
        if arr[i] < pivot:
            arr[i], arr[lt_index+1] = arr[lt_index+1], arr[i]
            lt_index += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt_index-1] = arr[gt_index-1], arr[i]
            gt_index -= 1
        else:
            i += 1
    arr[pivot_index], arr[lt_index] = arr[lt_index], arr[pivot_index]

    quick_sort_3_ways(arr, left_index, lt_index)
    quick_sort_3_ways(arr, gt_index, right_index)


# 递归版, 对 pending_heapify_index 元素执行堆化
def _max_heapify_recursive(arr, pending_heapify_index, left_index, right_index):
    if pending_heapify_index >= right_index:  # 当满足此条件, 应该结束`_max_heapify_recursive`递归了
        return
    left_child_index = 2 * (pending_heapify_index-left_index) + 1
    right_child_index = left_child_index + 1

    # 选出 pending_heapify_index 的左右孩子中最大的元素,
    # 并与 pending_heapify_index 元素交换
    cur_max_index = pending_heapify_index
    if left_child_index <= right_index and arr[cur_max_index] < arr[left_child_index]:
        cur_max_index = left_child_index
    if right_child_index <= right_index and arr[cur_max_index] < arr[right_child_index]:
        cur_max_index = right_child_index

    # 若当前已经是最大元素了, 则停止递归, 如果不是则执行交换与继续递归
    if cur_max_index != pending_heapify_index:
        arr[pending_heapify_index], arr[cur_max_index] = arr[cur_max_index], arr[pending_heapify_index]
        # 继续 堆化 cur_max_index 的子元素
        _max_heapify_recursive(arr, cur_max_index, left_index, right_index)


# 对 迭代版, pending_heapify_index 元素执行堆化
def _max_heapify_iterative(arr, pending_heapify_index, left_index, right_index):
    left_child_index = 2 * (pending_heapify_index-left_index) + 1
    while left_child_index <= right_index:
        right_child_index = left_child_index + 1
        # 选出 pending_heapify_index 的左右孩子中最大的元素,
        # 并与 pending_heapify_index 元素交换
        cur_max_index = pending_heapify_index
        if left_child_index <= right_index and arr[cur_max_index] < arr[left_child_index]:
            cur_max_index = left_child_index
        if right_child_index <= right_index and arr[cur_max_index] < arr[right_child_index]:
            cur_max_index = right_child_index

        # 若当前已经是最大元素了, 则直接break, 如果不是则执行交换与继续新一轮的堆化循环
        if cur_max_index != pending_heapify_index:
            arr[pending_heapify_index], arr[cur_max_index] = arr[cur_max_index], arr[pending_heapify_index]
            pending_heapify_index = cur_max_index
            left_child_index = 2 * (pending_heapify_index-left_index) + 1
        else:
            break


def _build_max_heap(arr, left_index, right_index):
    # 建堆, 从最后一个非叶结点开始, 自底向上堆化就建好了一个最大堆
    root_index = left_index
    arr_len = right_index - left_index + 1
    last_none_leaf_index = root_index + (arr_len/2 - 1)

    i = last_none_leaf_index
    while i >= root_index:
        _max_heapify_recursive(arr, i, left_index, right_index)
        i -= 1


def heap_sort(arr, left_index, right_index):
    if not arr or left_index >= right_index or right_index <= 0:
        return
    _build_max_heap(arr, left_index, right_index)
    # 把数组中的第一个元素(即根节点)也就是当前堆的最大元素逐个和数组后面的元素交换
    # 交换后根节点已经违背最大堆性质了, 但其他的元素还是符合最大堆性质的
    # 所以然后要对根节点做一次堆化操作
    cur_right_index = right_index
    root_index = left_index
    while cur_right_index >= root_index:
        arr[root_index], arr[cur_right_index] = arr[cur_right_index], arr[root_index]
        cur_right_index -= 1
        _max_heapify_recursive(arr, root_index, left_index, cur_right_index)


class TreeNode(object):

    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val


def binary_tree_preorder_traversal(root):
    _result_arr = []
    if not root:
        return _result_arr
    _temp_stack = []
    _temp_stack.append(("go", root))
    while _temp_stack:
        _cmd, _cur_node = _temp_stack.pop(-1)
        if _cmd == "print":
            _result_arr.append(_cur_node.val)
            continue
        if _cur_node.right:
            _temp_stack.append(("go", _cur_node.right))
        if _cur_node.left:
            _temp_stack.append(("go", _cur_node.left))
        _temp_stack.append(("print", _cur_node))
    return _result_arr


def binary_tree_inorder_traversal(root):
    _result_arr = []
    if not root:
        return _result_arr
    _temp_stack = []
    _temp_stack.append(("go", root))
    while _temp_stack:
        _cmd, _cur_node = _temp_stack.pop(-1)
        if _cmd == "print":
            _result_arr.append(_cur_node.val)
            continue
        if _cur_node.right:
            _temp_stack.append(("go", _cur_node.right))
        _temp_stack.append(("print", _cur_node))
        if _cur_node.left:
            _temp_stack.append(("go", _cur_node.left))
    return _result_arr


def binary_tree_postorder_traversal(root):
    _result_arr = []
    if not root:
        return _result_arr
    _temp_stack = []
    _temp_stack.append(("go", root))
    while _temp_stack:
        _cmd, _cur_node = _temp_stack.pop(-1)
        if _cmd == "print":
            _result_arr.append(_cur_node.val)
            continue
        _temp_stack.append(("print", _cur_node))
        if _cur_node.right:
            _temp_stack.append(("go", _cur_node.right))
        if _cur_node.left:
            _temp_stack.append(("go", _cur_node.left))
    return _result_arr


def binary_tree_levelorder_traversal(root):
    _result_arr = []
    if not root:
        return _result_arr
    _temp_queue = []
    _temp_queue.append(root)
    while _temp_queue:
        _cur_node = _temp_queue.pop(0)
        _result_arr.append(_cur_node.val)
        if _cur_node.left:
            _temp_queue.append(_cur_node.left)
        if _cur_node.right:
            _temp_queue.append(_cur_node.right)
    return _result_arr


def binary_tree_swap_recursive(root):
    if not root:
        return
    root.left, root.right = root.right, root.left
    binary_tree_swap_recursive(root.left)
    binary_tree_swap_recursive(root.right)


def binary_tree_swap_iterative(root):
    if not root:
        return
    _temp_stack = []
    _temp_stack.append(("go", root))
    while _temp_stack:
        _cmd, _cur_node = _temp_stack.pop(-1)
        if _cmd == "print":
            # 参考前序遍历的迭代写法, 就只有这里改成了swap操作
            _cur_node.left, _cur_node.right = _cur_node.right, _cur_node.left
            continue
        if _cur_node.right:
            _temp_stack.append(("go", _cur_node.right))
        if _cur_node.left:
            _temp_stack.append(("go", _cur_node.left))
        _temp_stack.append(("print", _cur_node))


class LinkList(object):

    def __init__(self, val):
        self.next = None
        self.val = val


def linklist_reverse(head):
    if not head:
        return
    _pre = None
    _cur = head
    _temp_next = head.next
    while _cur:
        # 先用_temp_next保存_cur的下一个节点的信息，
        # 保证单链表不会因为失去_cur节点的next而就此断裂
        _temp_next = _cur.next
        # 保存完_temp_next，就可以让_cur的next指向_pre了
        _cur.next = _pre
        # 让_pre，_cur依次向后移动一个节点，继续下一次的指针反转
        _pre = _cur
        _cur = _temp_next
    return _pre


class GraphBase(object):
    # 图的基类

    def __init__(self, point_count, is_directed):
        # 因为稀疏图一般用邻接表来保存图的顶点数据,
        # 而稠密图一般用邻接矩阵来表示, 所以他们的保存邻接点容器是不同的,
        # 留给具体子类来指定, 此处用 `self.adjacency_container = None`表示即可
        self.adjacency_container = None
        self.is_directed = is_directed  # 是否为有向图
        self.connected_components_count = 0  # 连通分量个数
        self.point_count = point_count

    def graph_dfs(self):
        """
        图的深度优先遍历（DFS）, 深度优先遍历尽可能优先往深层次进行搜索；
        1. 首先访问出发点v，并将其标记为已访问过；
        2. 然后依次从v出发搜索v的每个邻接点w。若w未曾访问过，则以w为新的出发点继续进行深度优先遍历，直至图中所有和源点v有路径相通的顶点均已被访问为止。
        3. 若此时图中仍有未访问的顶点，则另选一个尚未访问的顶点为新的源点重复上述过程，直至图中所有的顶点均已被访问为止。
        """
        visited_arr = []
        for _cur_point_index in xrange(0, len(self.adjacency_container)):
            if _cur_point_index not in visited_arr:
                self._dfs_by_point(_cur_point_index, visited_arr)
                # 运行到此处, 说明已经把所有和_cur_point_index 相连接的点都遍历完了,
                # A-B-C 也算作 A和C相连接的,
                # 其他的点肯定在另一个连接分量中
                self.connected_components_count += 1
        return visited_arr

    def _dfs_by_point(self, cur_point_index, visited_arr):
        visited_arr.append(cur_point_index)
        for _next_point_index in self._iter_adjacent_points(cur_point_index):
            if _next_point_index not in visited_arr:
                self._dfs_by_point(_next_point_index, visited_arr)

    def graph_bfs(self):
        """
        图的广度优先遍历, 也可以称为图的层序遍历, 广度优先遍历按层次优先搜索最近的结点，一层一层往外搜索:
        1. 首先访问出发点v，接着依次访问v的所有邻接点w1、w2......wt，
        2. 然后依次访问w1、w2......wt邻接的所有未曾访问过的顶点。
        3. 以此类推，直至图中所有和源点v有路径相通的顶点都已访问到为止。此时从v开始的搜索过程结束。
        4. 若此时图中仍有未访问的顶点，则另选一个尚未访问的顶点为新的源点重复上述过程，直至图中所有的顶点均已被访问为止。
        """
        result_arr = []
        visited_set = set()  # 用来记录某个顶点是否已经访问过
        _temp_queue = []
        for _cur_point_index in xrange(0, len(self.adjacency_container)):
            if _cur_point_index not in visited_set:
                _temp_queue.append(_cur_point_index)
                visited_set.add(_cur_point_index)
            while _temp_queue:
                _pt = _temp_queue.pop(0)
                result_arr.append(_pt)
                for _next_pt_index in self._iter_adjacent_points(_pt):
                    if _next_pt_index not in visited_set:
                        _temp_queue.append(_next_pt_index)
                        visited_set.add(_next_pt_index)
        return result_arr

    def _iter_adjacent_points(self, cur_point_index):
        """
        因为稀疏图一般用邻接表来保存图的顶点数据,
        而稠密图一般用邻接矩阵来表示,
        所以他们的遍历邻接点的方式是不同的, 留给具体的子类来实现.
        """
        raise NotImplementedError

    def add_edge(self, start_point_index, end_point_index):
        raise NotImplementedError


class SparseGraph(GraphBase):
    # 稀疏图

    def __init__(self, point_count, is_directed):
        super(SparseGraph, self).__init__(point_count, is_directed)
        self.adjacency_container = [[] for _ in xrange(point_count)]  # 邻接表
        self.indegree_list = [ 0 for _ in range(point_count) ]  # 每个顶点的入度, 初始化为0

    def set_adjacency_list(self, adjacency_list):
        self.adjacency_container = adjacency_list

    def _iter_adjacent_points(self, cur_point_index):
        for _adjacent_point_index in self.adjacency_container[cur_point_index]:
            yield _adjacent_point_index

    def add_edge(self, start_point_index, end_point_index):
        self.adjacency_container[start_point_index].append(end_point_index)
        self.indegree_list[end_point_index] += 1
        if not self.is_directed:
            self.adjacency_container[end_point_index].append(start_point_index)

    def topologic_sort(self):
        result_arr = []
        zero_indegree_list = []
        for point_index, cur_indegree in enumerate(self.indegree_list):
            if cur_indegree == 0:
                zero_indegree_list.append(point_index)  # 将所有入度为0的顶点加入列表
        while zero_indegree_list:
            cur_point_index = zero_indegree_list.pop()  # 从列表中取出一个顶点
            result_arr.append(cur_point_index)
            # 将所有v指向的顶点的入度减1，并将入度减为0的顶点加入列表
            for j in self.adjacency_container[cur_point_index]:
                self.indegree_list[j] -= 1
                if self.indegree_list[j] == 0:
                    zero_indegree_list.append(j)  # 若入度为0，则加入列表
        if len(result_arr) != self.point_count:
            return False, result_arr  # 没有输出全部顶点，说明有向图中有回路
        else:
            return True, result_arr
            

class DenseGraph(GraphBase):
    # 稠密图

    def __init__(self, point_count, is_directed):
        super(DenseGraph, self).__init__(point_count, is_directed)
        self.adjacency_container = [
            [0 for _ in xrange(point_count)] for _ in xrange(point_count)
        ]  # 邻接矩阵

    def set_adjacency_matrix(self, adjacency_matrix):
        self.adjacency_container = adjacency_matrix

    def _iter_adjacent_points(self, cur_point_index):
        for _adjacent_point_index, _is_point_adjacent in enumerate(self.adjacency_container[cur_point_index]):
            if not _is_point_adjacent:
                continue
            yield _adjacent_point_index

    def add_edge(self, start_point_index, end_point_index):
        self.adjacency_container[start_point_index][end_point_index] = 1
        if not self.is_directed:
            self.adjacency_container[end_point_index][start_point_index] = 1

    def topologic_sort(self):
        pass  # TODO


# 首先要明确此递归函数的定义: 查看root是否为叶子结点并且root的val是否等于sum_num,
# 然后才开始写代码
def has_path_sum(root, sum_num):
    if not root:
        return False
    # 判断是否为叶子
    if not root.left and not root.left and root.val == sum_num:
        return True
    # 通过递归, 继续查看左右孩子节点是否有 sum_num-root.val
    if has_path_sum(root.left, sum_num-root.val):
        return True
    return has_path_sum(root.right, sum_num-root.val)


def binary_tree_paths(root):
    result_arr = []
    if not root:
        return result_arr
    if not root.left and not root.right:
        result_arr.append(str(root.val))
        return result_arr
    # 获取左孩子的路径
    left_bt_path_arr = binary_tree_paths(root.left)
    for _path in left_bt_path_arr:
        result_arr.append(str(root.val) + "->" + _path)
    # 获取右孩子的路径
    right_bt_path_arr = binary_tree_paths(root.right)
    for _path in right_bt_path_arr:
        result_arr.append(str(root.val) + "->" + _path)
    return result_arr


def path_sum_3(root, sum_num):
    if not root:
        return 0
    path_cnt = 0
    # 先求包括node本身的情况, 此时这轮递归所说的node是代码中的root
    # 这种情况可以用类似于 path_sum问题 的 `has_path_sum`来实现
    path_cnt += _get_path_sum_include_node(root, sum_num)
    # 再求不包括node本身的情况,
    # 直接计算左右孩子往下的路径中和为sum_num(注意不是sum_num-root.val)的路径数量
    path_cnt += path_sum_3(root.left, sum_num)
    path_cnt += path_sum_3(root.right, sum_num)
    return path_cnt


def _get_path_sum_include_node(node, sum_num):
    if not node:
        return 0
    _path_cnt = 0
    if node.val == sum_num:  # node本身值等于sum_num也算一条路径
        _path_cnt += 1
    _path_cnt += _get_path_sum_include_node(node.left, sum_num-node.val)
    _path_cnt += _get_path_sum_include_node(node.right, sum_num-node.val)
    return _path_cnt


def jump_step(step_sum):
    if step_sum == 0:
        return 0
    if step_sum == 1:
        return 1
    if step_sum == 2:
        return 2
    return jump_step(step_sum-1) + jump_step(step_sum-2)


def jump_step_optimized(step_sum, memo=None):
    if step_sum == 0:
        return 0
    if step_sum == 1:
        return 1
    if step_sum == 2:
        return 2
    if memo is None:
        memo = {}
    if step_sum in memo:  # 先判断有没计算过，即看看备忘录有没有
        # 备忘录有，即计算过，直接返回
        return memo[step_sum]
    # 备忘录没有，即没有计算过，执行递归计算,并且把结果保存到备忘录map中
    memo[step_sum] = \
        jump_step_optimized(step_sum-1, memo) + \
        jump_step_optimized(step_sum-2, memo)
    return memo[step_sum]


def jump_step_dynamic_programming(step_sum):
    dp = {}
    dp[0] = 0
    dp[1] = 1
    dp[2] = 2
    for i in xrange(3, step_sum+1):
        # 根据递推公式直接写出
        dp[i] = dp[i-1] + dp[i-2]
    return dp[step_sum]


digits_map = {
    "0": " ",
    "1": "",
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations_of_a_phone_number(digits_str):
    result_str_arr = []
    if not digits_str:
        return result_str_arr
    assert "1" not in digits_str, "we dont proc 1"

    middle_state_container = []
    _get_letter_combination(result_str_arr, digits_str, index=0,
                            middle_state_container=middle_state_container)
    return result_str_arr


def _get_letter_combination(
        result_str_arr, pending_proc_digits_str, index, middle_state_container):
    """
    middle_state_container 中保存了
    此时从 pending_proc_digits_str[0...index-1] 翻译得到的一个字母字符串
    寻找和pending_proc_digits_str[index]匹配的字母,
    获得pending_proc_digits_str[0...index]翻译得到的解
    """
    if index == len(pending_proc_digits_str):
        # 当index等于数字字符串长度的时候说明一轮已经递归到底了,
        # 则当前的 中间状态保存器 middle_state_container 则为一个解
        # 此处需要深拷贝一下, 因为下方代码有个 `middle_state_container.pop(-1)`
        result_str_arr.append(copy.deepcopy(middle_state_container))
        return
    # # 不处理1因为1对应的没字母
    # while pending_proc_digits_str[index] == "1":
    #     index += 1
    #     if index >= len(pending_proc_digits_str):
    #         return
    _cur_letters_str = digits_map[pending_proc_digits_str[index]]
    for _single_letter_str in _cur_letters_str:
        middle_state_container.append(_single_letter_str)
        _get_letter_combination(
            result_str_arr, pending_proc_digits_str, index+1,
            middle_state_container)
        middle_state_container.pop(-1)


class Solution_lc77(object):
    def combine(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[List[int]]
        """
        result_arr = []
        if k <= 0 or k > n or n <= 0:
            return result_arr
        middle_state_container = []
        self._generate_combinations(
            result_arr, n, k, 1, middle_state_container)
        return result_arr

    def _generate_combinations(
            self, result_arr,
            pending_proc_n, pending_prco_k, start_num, middle_state_container):
        """
        求解C(n,k), 当前已经找到的组合存储在 middle_state_container 中,
        需要从start_num开始搜索新的元素
        可以看出跟排列问题的代码模板很像, 
        只有终止递归条件和for循环的start_num不太一样
        """
        if len(middle_state_container) == pending_prco_k:
            result_arr.append(copy.deepcopy(middle_state_container))
            return
        # 每次递归从start_num开始直到 pending_proc_n
        for _cur_num in xrange(start_num, pending_proc_n+1):
            middle_state_container.append(_cur_num)
            self._generate_combinations(
                result_arr, pending_proc_n, pending_prco_k,
                _cur_num+1, middle_state_container)
            middle_state_container.pop(-1)

    def combinations_optimized(self, n, k):
        result_arr = []
        if k <= 0 or k > n or n <= 0:
            return result_arr
        middle_state_container = []
        self._generate_combinations(
            result_arr, n, k, 1, middle_state_container)
        return result_arr

    def _generate_combinations_optimized(
            self, result_arr,
            pending_proc_n, pending_prco_k, start_num, middle_state_container):
        """
        求解C(n,k), 当前已经找到的组合存储在 middle_state_container 中,
        需要从start_num开始搜索新的元素
        可以看出跟排列问题的代码模板很像, 
        只有终止递归条件和for循环的start_num不太一样
        """
        if len(middle_state_container) == pending_prco_k:
            result_arr.append(copy.deepcopy(middle_state_container))
            return
        # # 每次递归从start_num开始直到 pending_proc_n
        # for _cur_num in xrange(start_num, pending_proc_n+1):
        # 剪枝的思想,
        # 还有k - middle_state_container.size()个空位,
        # 所以, [i...n] 中至少要有 k - middle_state_container.size() 个元素
        # i最多为 n - (k - middle_state_container.size()) + 1
        _cur_stop_num = pending_proc_n - (
            pending_prco_k - middle_state_container.size()) + 1
        # 每次递归从start_num开始直到 _cur_stop_num
        for _cur_num in xrange(start_num, _cur_stop_num+1):
            middle_state_container.append(_cur_num)
            self._generate_combinations(
                result_arr, pending_proc_n, pending_prco_k,
                _cur_num+1, middle_state_container)
            middle_state_container.pop(-1)


class Solution_number_of_islands(object):

    def __init__(self):
        self._visited_pos_set = set()
        # 方便搜索点的时候往上下左右搜
        self._move_dir_arr = [(0, -1), (0, 1), (1, 0), [-1, 0]]

    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        if not grid:
            return 0
        islands_cnt = 0
        for x in xrange(0, len(grid)):
            assert (type(grid[x]) is list), ("x = %d" % x)
            for y in xrange(0, len(grid[x])):
                if tuple([x, y]) in self._visited_pos_set:
                    continue
                if grid[x][y] != "1":
                    continue
                self._dfs_islands(grid, x, y)
                islands_cnt += 1  # 一次搜索完成就算有一个岛屿了
        return islands_cnt

    def _dfs_islands(self, grid, x, y):  # x是纵坐标, y是横坐标
        # print "x = %d" % x
        # print "y = %d" % y
        self._visited_pos_set.add(tuple([x, y]))
        # 上下左右四个方向搜索
        for _move_dir in self._move_dir_arr:
            _new_x = x + _move_dir[0]
            _new_y = y + _move_dir[1]
            # 如果超出地图边界了, 注意 x是纵坐标, y是横坐标
            if _new_x >= len(grid) or _new_x < 0 or \
                    _new_y >= len(grid[0]) or _new_y < 0:
                continue
            # 如果已经访问过了
            if tuple([_new_x, _new_y]) in self._visited_pos_set:
                continue
            if grid[_new_x][_new_y] != "1":
                continue
            self._dfs_islands(grid, _new_x, _new_y)


class Solution_integer_break(object):

    def __init__(self):
        self._memo = {}

    # 将n进行分割(至少分割两部分), 可以获得的最大乘积
    def integerBreak(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1:
            return 1
        _res = -1
        if n in self._memo:
            return self._memo[n]
        for i in xrange(1, n):
            # 计算`i + (n-i)`
            _res = max(
                _res,
                i * (n-i),  # 有可能自己本身`i*(n-i)`就是最大的
                i * self.integerBreak(n-i))
        self._memo[n] = _res
        return _res

    def integer_break_dp(self, n):
        # 下面这种A思路是不行的:
        # dp[i]等价于 f(i)，
        # 那么上面针对 f(i) 写的递归公式对 dp[i] 也是适用的，我们拿来试试。
        # 关键语句:
        #  `res = max(res, i * (n - i), max(i * self.integerBreak(n - i)))`
        # 翻译过来就是：`dp[i] = max(_res, i * (n-i), i * dp[n-i])`
        # 则不难得出以下代码, 但因为 dp[n-i] 当前没求出来, 子问题没求出来,
        # 所以原问题也就求不出来了, 所以下面这三行代码是不行的
        # _res = -1
        # for i in xrange(1, n):
            # dp[i] = max(_res, i * (n-i), i * dp[n-i])
        
        # 此时我们得下面这种B思路才行:
        # 我们用一层循环来生成上面这段A思路代码一系列的 n 值。
        # 接着我们还要生成上面A思路代码中一系列的 i 值，
        # 注意到 n - i 是要大于 0 的，
        # 因此 i 只需要循环到 n - 1 即可。
        # 由此不难翻译A思路得出以下代码(j代表n, k代表i):
        # dp[i] = max(dp[i], (i-j)*j, j* dp[i-j])  # j=1...i

        # dp[i] 表示将数字i分割(至少分割成两部分)后得到的最大乘积
        dp = [ float("-inf") for _ in range(n+1) ]
        dp[0] = float("-inf")
        dp[1] = float("-inf")
        dp[2] = 1
        for j in xrange(3, n+1):  # 循环到n
            for k in xrange(1, j):  # 循环到j-1即可
                dp[j] = max(dp[j], k*(j-k), k*dp[j-k])
        return dp[n]


class Solution_stock(object):
    def stock4_maxProfit(self, k, prices):
        """
        :type k: int
        :type prices: List[int]
        :rtype: int
        """
        if not prices or not k:
            return 0
        n = len(prices)
        # 注意: 题中交易的含意是买入和卖出一支股票一次, 才称为一次交易
        # 但我们解题的时候可以把买入就当成一次交易会容易写代码一些,
        # 当然也可以定义dp为买了再卖才算一次交易, 只是代码难写一些, 而且
        # 初始化状态难弄一些
        # dp[i][k][0]为第i天最多可以完成k次交易时手中 无股票时 的最大利润
        # dp[i][k][1]为第i天最多可以完成k次交易时手中 有股票时 的最大利润
        # 为什么下方要初始化为`n+1`呢? 因为我们要求的是第n天最多可以完成k次交易时手中无股票时的最大利润,
        # 而不是第n-1天, 注意我们下方说的第0天并不是数组意义的第1天.
        # 读者可能问为什么不是 dp[n - 1][K][1]？
        # 因为 [1] 代表手上还持有股票，[0] 表示手上的股票已经卖出去了，
        # 很显然后者得到的利润一定大于前者。
        dp = [ [ [ 0 for _ in range(2) ]  for _ in range(k+1) ] for _ in range(n+1) ]
        
        for j in range(n+1):
            dp[j][0][0] = 0  # 第j天0次交易，手上不持有, 故为0
            # 第j天0次交易，手上持有股票, 这是不可能的, 
            # 我们dp对交易的定义是买入就算, 0次交易都没买入股票, 不可能持有股票
            # 所以我们用负无穷来表示, 因为之后我们用max来取值,
            # 如果这里不这样初始化，而是初始化为0，那么我t次交易的无法去做max,
            # max它会取这个0,而不会去取那些负值
            dp[j][0][1] = float("-inf")
            for t in range(k+1):
                # 第0天t次交易，手上持有股票, 这里所说的第0天不是数组的第1天,
                # 第0天是一个不存在的日子, 所以这是不可能的, 
                # 所以我们用负无穷来表示, 因为之后我们用max来取值,
                # 如果这里不这样初始化，而是初始化为0，那么我t次交易的无法去做max,
                # max它会取这个0,而不会去取那些负值
                dp[0][t][1] = float("-inf")
                dp[0][t][0] = 0
        for i in range(1, n+1):
            for t in range(1, k+1):
                # i天t次交易现在手上持有 = max(i-1天t次交易手上持有，i-1天t-1次交易手上不持有 - i天买入价格)
                dp[i][t][1] = max(
                    dp[i-1][t][1],
                    # 为什么是`prices[i-1]`呢? 因为这里的i是第i天,
                    # 根据我们的dp定义, 
                    # 实际上第i=1天对应的是数组中的prices[0]的价格
                    # 我们dp对交易的定义是买入就算, 这里买入一张股票, 得减去`prices[i-1]`
                    # 所以我们这里才`t-1`, 好理解一些
                    dp[i-1][t-1][0] - prices[i-1]
                )
                # i天t次交易现在手上不持有 = max(i-1天t次交易手上不持有，i-1天t次交易手上持有 + i天卖出价格prices)
                dp[i][t][0] = max(
                    dp[i-1][t][0],
                    dp[i-1][t][1] + prices[i-1]
                )

        return dp[n][k][0]
        

class Solution_coin1(object):
    def coinChange(self, coins, amount):
        """
        :type coins: List[int]
        :type amount: int
        :rtype: int
        """
        assert(coins)
        # 用背包的思路
        if amount == 0:
            return 0
        n = len(coins)
        # 如果我们将每种硬币看作是每种物品，面值金额看成是物品的重量，总金额是背包的总容量, 因为硬币无限, 这样此题就是是一个恰好装满的完全背包问题.了。不过这里不是求最多装入多少价值而是求最少装满背包的数目，所以我们只需要将[完全背包](#完全背包问题)的转态转移方程中稍微改改即可:  
        # - dp[i][j]定义为: 用前i种硬币可以抽一些硬币出来装满容量为j的背包的最少硬币数量
        # - 状态转移方程为: `d[i][j] = min(dp[i-1][j], dp[i][j-coins[i-1]])`

        # 因为之后要取min操作, 所以这里初始化为无穷大`float("inf")`
        dp = [ [ float("inf") for _ in range(amount+1) ] for _ in range(n+1) ]
        for k in range(n+1):
            dp[k][0] = 0  # 充满容量为0的背包, 最少的硬币个数为0
        for i in range(n+1):
            for j in range(amount+1):
                if j - coins[i-1] < 0:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = min(
                        dp[i-1][j],
                        dp[i][j-coins[i-1]] + 1
                    )
        return dp[n][amount] if dp[n][amount] != float("inf") else -1


class Solution_coin2(object):
    def change(self, amount, coins):
        """
        :type amount: int
        :type coins: List[int]
        :rtype: int
        """ 
        n = len(coins)
        # dp[i][j]`的定义如下：  
        # 从前`i`种物品里选取若干件物品，当背包容量为`j`时，有`dp[i][j]`种方法可以装满背包。
        dp = [ [ 0 for _ in range(amount+1) ] for _ in range(n+1) ]
        for k in range(n+1):
            # 如果凑出的目标金额为 0，那么 “无为而治” (不用任何硬币)就是唯一的一种凑法。
            dp[k][0] = 1
        for i in range(1, n+1):
            for j in range(1, amount+1):
                if j - coins[i-1] < 0:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] + dp[i][j-coins[i-1]]
        return dp[n][amount]


class Solution_house_robber(object):

    def __init__(self):
        # memo[i] 表示考虑抢劫 nums[i...n-1] 所能获得的最大收益
        self._memo = {}

    def rob(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        return self._try_rob(nums, 0)

    def _try_rob(self, nums_arr, index):
        """
        先套用写一波自顶而下的递归形式的解答,
        然后用记忆化搜索的加个memo的方式优化一波.
        写完此方法之后, 有了大概的思路就能
        根据状态转移方程找出规律改写成自底向上的dp形式(见下方`_try_rob_dp`方法)
        此`_try_rob`方法表示: 考虑抢劫nums[index...nums.size()-1]这个范围的所有房子所能得到的最大收益
        """
        if index in self._memo:
            return self._memo[index]
        if index >= len(nums_arr):
            return 0
        res = 0
        for _i, _num in enumerate(nums_arr):
            if _i < index:
                continue
            res = max(
                res,
                _num + self._try_rob(nums_arr, _i+2),
            )
        self._memo[index] = res
        return res

    def rob_dp_1_other(self, nums_arr):
        if not nums_arr:
            return 0
        if len(nums_arr) == 1:
            return nums_arr[0]
        n = len(nums_arr)
        # dp[index] 表示 抢劫nums[index...nums.size()-1]这个范围的所有房子所能得到的最大收益
        dp = [0] * n
        # 因为我们想求出dp[0], 所以我们从后面开始, 即从n-1开始
        dp[n-1] = nums_arr[n-1]
        dp[n-2] = max(nums_arr[n-1], nums_arr[n-2])
        for i in xrange(n-3, -1, -1):
            for j in xrange(i, n):
                dp[i] = max(
                    dp[i],
                    (nums_arr[j] + (dp[j+2] if j + 2 < n else 0))
                )
        return dp[0]

    def rob1_dp(self, nums_arr):
        if not nums_arr:
            return 0
        n = len(nums_arr)
        dp = [0] * n
        dp[n-1] = nums_arr[n-1]
        dp[n-2] = max(nums_arr[n-1], nums_arr[n-2])
        for i in range(n-3, -1, -1):
            dp[i] = max(dp[i+1], nums_arr[i]+dp[i+2])
        return dp[0]

    def rob1_dp_memo(self, nums_arr):
        return self._do_rob1_dp_memo(nums_arr, 0)

    def _do_rob1_dp_memo(self, nums_arr, index):
        # 我们定义此函数为从index开始偷到最后的房子能偷到的最高总金额
        if index >= len(nums_arr):
            return 0
        if index in self._memo:
            return self._memo[index]
        res = max(
            nums_arr[index] + self._do_rob1_dp_memo(nums_arr, index+2),
            self._do_rob1_dp_memo(nums_arr, index+1),
        )
        self._memo[index] = res
        return res

    def house_rob_detail_seq(self, nums_arr):
        if not nums_arr:
            return 0
        n = len(nums_arr)
        # 根据上述思路, 我们用 dp[i] 表示从第 i 间房屋偷到最后一间能偷窃到的最
        # 高总金额的房子数组子序列
        dp = [ [] for _ in xrange(n) ]
        dp[n-1] = [nums_arr[n-1]]
        dp[n-2] = [max(nums_arr[n-1], nums_arr[n-2])]
        for i in range(n-3, -1, -1):
            if (sum(dp[i+2]) + nums_arr[i]) > sum(dp[i+1]):
                dp[i] = [nums_arr[i]] + dp[i+2]
            else:
                dp[i] = dp[i+1]
        return dp[0]


    def rob3_dp(self, bt):
        # 此函数求出bt为根节点的最大价值
        if not bt:
            return 0
        if bt in memo:
            return memo[bt]
        # 抢, 然后去下下家
        do_it = bt.val + \
            (rob3_dp(bt.left.left) + rob3_dp(bt.left.right) if bt.left else 0) + \
            (rob3_dp(bt.right.left) + rob3_dp(bt.right.left) if bt.right else 0)
        # 不抢, 然后去下家
        not_do_it = rob3_dp(bt.left) + rob3_dp(bt.right)
        res = max(do_it, not_do_it)
        memo[bt] = res
        return res


class Solution_knapsack(object):

    def __init__(self):
        self._memo = None

    def knapsack(self, capacity, weight_arr, value_arr):
        if capacity == 0:
            return 0
        self._memo = [[-1 for j in xrange(capacity)]
                      for i in xrange(len(weight_arr))]
        return self._best_value(capacity, weight_arr, value_arr, 0)

    # 用 [0...index]的物品,填充容积为c的背包的最大价值
    def _best_value(self, capacity, weight_arr, value_arr, index):
        if index >= len(weight_arr) or capacity <= 0:
            return 0
        if self._memo[index][capacity-1] != -1:
            return self._memo[index][capacity-1]
        _res = self._best_value(capacity, weight_arr, value_arr, index + 1)
        if capacity >= weight_arr[index]:
            _res = max(
                _res,
                value_arr[index] + self._best_value(
                    capacity-weight_arr[index], weight_arr, value_arr, index+1)
            )
        self._memo[index][capacity-1] = _res
        return _res

    def knapsack_dp_del(self, capacity, weight_arr, value_arr):
        if capacity == 0:
            return 0
        assert(len(weight_arr) == len(value_arr))
        n = len(weight_arr)
        dp = [[0 for _ in xrange(capacity+1)] for _ in xrange(n)]
        # 动规是从底向上嘛, 先构建dp[0]的东西
        for k in xrange(capacity+1):
            dp[0][k] = value_arr[0] if k >= weight_arr[0] else 0

        for i in xrange(1, n):
            for c in xrange(capacity+1):
                # 根据状态转移方程得出
                dp[i][c] = max(
                    dp[i-1][c],
                    value_arr[i] + dp[i-1][c-weight_arr[i]
                                           ] if c >= weight_arr[i] else 0
                )
        return dp[n-1][capacity]

    def knapsack_dp(self, capacity, weight_arr, value_arr):
        if capacity == 0:
            return 0
        assert(len(weight_arr) == len(value_arr))
        n = len(weight_arr)
        # dp[i][j]表示将前i件物品装进限重为j的背包可以获得的最大价值, 0<=i<=N, 0<=j<=W
        # 那么我们可以将dp[0][0...W]初始化为0，
        # 表示将前0个物品（即没有物品）装入书包的最大价值为0。
        # 那么当 i > 0 时dp[i][j]有两种情况：
        # - 不装入第i件物品，即dp[i−1][j]；
        # - 装入第i件物品（前提是能装下），即dp[i−1][j−w[i-1]] + v[i-1]。
        # 因为我们对dp[i][j]表示将前i件物品装进限重为j的背包可以获得的最大价值
        # 则i=0其实表示的是0个物品,
        # 所以实际对应weight数组和value数组的index应该为i-1
        #
        # 即状态转移方程为
        # dp[i][j] = max(dp[i−1][j], dp[i−1][j−w[i-1]]+v[i-1]) // j >= w[i-1]
        # 所求为dp[n][capacity]
        dp = [[0 for _ in xrange(capacity+1)] for _ in xrange(n+1)]
        # 动规是从底向上嘛, 先构建dp[0]的东西
        for k in xrange(capacity+1):
            # 因为我们对dp[i][j]表示将前i件物品装进限重为j的背包可以获得的最大价值
            # 则i=0其实表示的是0个物品, 所以 = 0
            dp[0][k] = 0

        for i in xrange(1, n+1):
            for j in xrange(capacity+1):
                # 因为我们对dp[i][j]表示将前i件物品装进限重为j的背包可以获得的最大价值
                # 则i=0其实表示的是0个物品,
                # 所以实际对应weight数组和value数组的index应该为i-1
                pack_args_index = i - 1
                if j - weight_arr[pack_args_index] < 0:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = max(
                        dp[i-1][j],
                        value_arr[pack_args_index] + dp[i-1][j-weight_arr[pack_args_index]]
                    )
        return dp[n][capacity]


class Solution_partition_equal_subset_sum(object):

    def __init__(self):
        self._memo = None

    def canPartition_del(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        动规解法
        """
        if not nums or len(nums) < 2 or sum(nums) % 2 != 0:
            return False
        _bag_capcity = sum(nums) / 2
        n = len(nums)
        # 创建二维状态数组，行：物品索引，列：容量（包括 0）
        dp = [[False for _ in xrange(_bag_capcity+1)] for _ in xrange(n)]
        # 先填表格第 0 行，第 1 个数只能让容积为它自己的背包恰好装满
        if nums[0] <= _bag_capcity:
            dp[0][nums[0]] = True
        for i in xrange(1, n):
            for c in xrange(_bag_capcity+1):
                dp[i][c] = dp[i-1][c] or (dp[i-1][c-nums[i]]
                                          if c >= nums[i] else False)
        return dp[n-1][_bag_capcity]

    def canPartition(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        动规解法
        """
        # 特判：如果是奇数，就不符合要求
        if not nums or len(nums) < 2 or sum(nums) % 2 != 0:
            return False
        _bag_capcity = sum(nums) / 2
        n = len(nums)
        # 状态定义：
        # dp[i][j]表示对于容量为 j 的背包，若只是用前 i 个物品(前0个则表示没有物品)，
        # 每个数只能用一次，使得这些数的和恰好等于 j  .
        # (比如说，如果dp[4][9] = true，其含义为：对于容量为 9 的背包，若只是用前 4 个物品，可以有一种方法把背包恰好装满。)。
        # 状态转移方程：很多时候，状态转移方程思考的角度是「分类讨论」，对于「0-1 背包问题」而言就是「当前考虑到的数字选与不选」。
        # - 不选择 nums[i]，则看前i-1个元素的是否能能和为j, 即 `dp[i-1][j]`
        # - 选择 nums[i]，看前i-1个元素的是否能能和为`j-nums[i-1]`, 即`dp[i-1][j- nums[i-1]`
        # **注意上方的`nums[i-1]`, 为什么是i-1呢?**
        # 因为我们对dp[i][j]表示将前i件物品装进限重为j的背包可以获得的最大价值, 则i=0其实表示的是0个物品,
        # 所以实际对应nums数组的index应该为`i-1`
        # 则状态转移方程：
        # dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i-1]]  // j >= nums[i-1]
        dp = [[False for _ in range(_bag_capcity+1)] for _ in range(n+1)]

        dp[0][0] = True  # 前0个则表示没有物品, 可以充满容量为0的背包
        for c in range(1, _bag_capcity+1):
            dp[0][c] = False # 前0个则表示没有物品, 是不可能充满容量大于0的背包的

        for i in range(1, n+1):
            for j in range(_bag_capcity+1):
                if j - nums[i-1] < 0:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] or dp[i-1][j-nums[i-1]]
        return dp[n][_bag_capcity]

    def canPartition_recursion(self, nums):
        if not nums or len(nums) < 2 or sum(nums) % 2 != 0:
            return False
        _sum_num = sum(nums) / 2
        self._memo = [[None for _ in xrange(_sum_num+1)]
                      for _ in xrange(len(nums))]
        return self._try_partition(nums, 0, _sum_num)

    def _try_partition(self, nums, index, sum_num):
        if index >= len(nums) or sum_num < 0:
            return False
        if self._memo[index][sum_num] is not None:
            return self._memo[index][sum_num]
        if sum_num == 0:
            return True
        _res = self._try_partition(nums, index+1, sum_num) or \
            self._try_partition(nums, index+1, sum_num-nums[index])
        self._memo[index][sum_num] = _res
        return _res


class Solution_LIS(object):
    def lengthOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        n = len(nums)
        # 我们定义 `dp[i]` 为选取到第i个数字的时候的最长上升子序列的长度,
        # 注意这里的定义, 第i个数字是一定要选取的.
        dp = [1] * n  # 因为自己本身就是一个长度为1的上升子序列
        dp[0] = 1
        for i in xrange(1, n):
            for j in xrange(0, i):
                # 则我们的状态转移方程为:
                # `dp[i] = max(dp[j]) + 1 , 其中 0 <= j < i 且 nums[j] < nums[i]`
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)


class Solution_lc137(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        counts = [ 0 for _ in range(32) ]
        # 建立一个长度为 32 的数组 counts ，通过以上方法可记录所有数字的各二进制位的 1 的出现次数。
        for cur_num in nums:
            _flag = 1
            for j in range(32):
                if cur_num & _flag:
                    counts[j] += 1
                _flag = _flag << 1
        res = 0
        m = 3
        # 将 counts 各元素对 3 求余，则结果为 “只出现一次的数字” 的各二进制位。
        # 利用 左移操作 和 或运算 ，可将 counts 数组中各二进位的值恢复到数字 res 上
        # 最终返回 res 即可。
        # 实际上，只需要修改求余数值 m ，即可实现解决 除了一个数字以外，
        # 其余数字都出现 m 次 的通用问题.
        for i in range(32):
            res <<= 1
            res |= counts[31-i] % m
		# 那如果想从一个负数的补码还原成python的负数, 
		# 比如把`-3`的补码`0xfffffffd`还原成python的负数,
		#  因为py的整形数字可以视为是以一个无限长的位存储方式来实现的,
		#   所以直接`print 0xfffffffd`他会打印`4294967293`,
		#    因为python把`0xfffffffd`当成了`0x000000000fffffffd`, 
		#    符号位在最前面为0, 当成正数了, 所以我们得对它的后32位之前的所有0都取反变为1,
		#     这样符号位为1才是python存储`-1`的真正补码形式,
		# 	 所以对于一个负数`res`来说, 得这么还原: `~(res ^ 0xffffffff)`, 
		# 	 要先将 末尾32 位取反（即 res ^ 0xffffffff ），再将所有位取反（即 ~ ).
		# 	  两个组合操作实质上是将数字 末尾32 以前的位取反， 末尾32 位不变。
        return res if (counts[31] % m) == 0 else ~(res ^ 0xffffffff)


class Solution_LCS(object):
    def lengthOfLCS(self, str_arr):
        if not str_arr:
            return 0
        assert len(str_arr) == 2
        str_a = str_arr[0]
        str_b = str_arr[1]
        m = len(str_a)
        n = len(str_b)
        if m < 1 or n < 1:
            return 0
        # 我们定义dp[i][j] 为 str_a[0...i] 和str_b[0...j]的最长子序列的长度
        dp = [[0 for _ in xrange(n)] for _ in xrange(m)]
        # 初始化最底层的基础数据
        for k in xrange(n):
            if str_a[0] == str_b[k]:
                for h in xrange(k, n):  # k后面的也都要置为1
                    dp[0][h] = 1
        for k in xrange(m):
            if str_a[k] == str_b[0]:
                for h in xrange(k, m):  # k后面的也都要置为1
                    dp[h][0] = 1

        for i in xrange(1, m):
            for j in xrange(1, n):
                # 根据图中的状态转移方程得出, 有两种情况, 所以if一下
                if str_a[i] == str_b[j]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m-1][n-1]

    def get_lcs_detail_seq_1(self, str_arr):
        if not str_arr:
            return ""
        assert len(str_arr) == 2
        str_a = str_arr[0]
        str_b = str_arr[1]
        m = len(str_a)
        n = len(str_b)
        if m < 1 or n < 1:
            return ""
        # 我们定义dp[i][j] 为 str_a[0...i] 和str_b[0...j]的最长子序列
        dp = [["" for _ in xrange(n)] for _ in xrange(m)]
        # 初始化最底层的基础数据
        for k in xrange(n):
            if str_a[0] == str_b[k]:
                for h in xrange(k, n):  # k后面的也都要置为1
                    dp[0][h] = str_a[0]
        for k in xrange(m):
            if str_a[k] == str_b[0]:
                for h in xrange(k, m):  # k后面的也都要置为1
                    dp[h][0] = str_b[0]

        for i in xrange(1, m):
            for j in xrange(1, n):
                # 根据图中的状态转移方程得出, 有两种情况, 所以if一下
                if str_a[i] == str_b[j]:
                    dp[i][j] = dp[i-1][j-1] + str_a[i]
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m-1][n-1]

    def get_lcs_detail_seq_2(self, str_arr):
        if not str_arr:
            return ""
        assert len(str_arr) == 2
        str_a = str_arr[0]
        str_b = str_arr[1]
        m = len(str_a)
        n = len(str_b)
        if m < 1 or n < 1:
            return ""
        # 我们定义dp[i][j] 为 str_a[0...i] 和str_b[0...j]的最长子序列的长度
        dp = [[0 for _ in xrange(n)] for _ in xrange(m)]
        # 初始化最底层的基础数据
        for k in xrange(n):
            if str_a[0] == str_b[k]:
                for h in xrange(k, n):  # k后面的也都要置为1
                    dp[0][h] = 1
        for k in xrange(m):
            if str_a[k] == str_b[0]:
                for h in xrange(k, m):  # k后面的也都要置为1
                    dp[h][0] = 1

        for i in xrange(1, m):
            for j in xrange(1, n):
                # 根据图中的状态转移方程得出, 有两种情况, 所以if一下
                if str_a[i] == str_b[j]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        # 不管是LCS/LIS/0-1背包问题如果要求最优解的具体情况是哪种,
        # 我们的思路就是要用dp解法求出整个dp数组之后,
        # 然后根据dp的状态定义, 以及dp数组里具体存储了的信息反推回去.
        #
        # 从之前求lcs的代码以及上图中都可以看出,
        # 从dp数组的末尾后面反推回去,
        # 上一个公共字符所在的横纵index肯定在当前横纵index的左上.
        p = len(str_a) - 1
        q = len(str_b) - 1
        _lcs_detail_seq = ""
        while(p >= 0 and q >= 0):
            if(str_a[p] == str_b[q]):
                _lcs_detail_seq = str_a[p] + _lcs_detail_seq
                p -= 1
                q -= 1
            elif(p == 0):
                q -= 1
            elif(q == 0):
                p -= 1
            else:
                # 由dp数组图中可知,
                # 上一个公共字符所在的横纵index肯定在当前横纵index的左上.
                if(dp[p-1][q] > dp[p][q-1]):
                    # dp[p-1][q] 大, 则往左移动, p减一
                    # 这样才能才能找到最大公共子串的上一个公共字符嘛
                    p -= 1
                else:
                    # dp[p][q-1] 大, 则往上移动, q减一
                    # 这样才能才能找到最大公共子串的上一个公共字符嘛
                    q -= 1
        return _lcs_detail_seq


class Solution_build_bt(object):
    def buildTree(self, inorder, postorder):
        """
        :type inorder: List[int]
        :type postorder: List[int]
        :rtype: TreeNode
        """
        if not inorder or not postorder:
            return None

        def _proc_order_arr(
                inorder_left_index, inorder_right_index,
                postorder_left_index, postorder_right_index):
            if inorder_left_index > inorder_right_index or \
                    postorder_left_index > postorder_right_index:
                return None
            # 在后序遍历序列中,最后一个元素为树的根节点
            root_val = postorder[postorder_right_index]
            root_inorder_index = inorder.index(root_val)
            _len_left_child = root_inorder_index-inorder_left_index
            root_node = TreeNode(root_val)

            # 在中序遍历序列中,根节点的左边为左子树(设其长度为len_left), 根节点的右边为右子树
            # 当前后序遍历序列中`[postorder_left_index...len_left-1]`为左子树的结点,
            # 其他的除最后一个结点外都是右子树的结点
            root_node.left = _proc_order_arr(
                inorder_left_index,
                root_inorder_index-1,
                postorder_left_index,
                postorder_left_index + (_len_left_child-1)
            )
            root_node.right = _proc_order_arr(
                root_inorder_index+1,
                inorder_right_index,
                postorder_left_index+(_len_left_child),
                postorder_right_index-1
            )
            return root_node

        return _proc_order_arr(0, len(inorder)-1, 0, len(postorder)-1)


class Solution_LCA(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        if root == p or root == q:  # 找到p或q了, 则返回p或q
            return root
        # 没找到p或q, 而且已经找到底, 越过叶子节点了, 则返回None
        if root is None:
            return None
        # 到 左子树 去找
        left_child_find_res = self.lowestCommonAncestor(root.left, p, q)
        # 到 右子树 去找
        right_child_find_res = self.lowestCommonAncestor(root.right, p, q)
        if not left_child_find_res:
            # 当 left 为空 ，right 不为空 ：p,q 都不在 root 的左子树中，直接返回 right
            return right_child_find_res
        if not right_child_find_res:
            return left_child_find_res
        # 当 left 和 right 同时不为空 ：
        # 说明 p,q 分列在 当前 root 的 异侧 （分别在 左 / 右子树），
        # 因此 当前的root 为p/g最近公共祖先，返回 root ；
        return root


class Solution_lc39(object):
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if not candidates:
            return []
        res_arr = []
        middle_state_arr = []
        self._generate_combinations(
            candidates, target, 0, res_arr, middle_state_arr)
        return res_arr

    def _generate_combinations(
            self, candidates_arr, cur_target_num, start_index, res_arr, middle_state_arr):
        if cur_target_num < 0:
            return
        if cur_target_num == 0:
            res_arr.append(copy.deepcopy(middle_state_arr))
            return
        # 这个cur_index是用来去重的
        for cur_index in range(start_index, len(candidates_arr)):
            middle_state_arr.append(candidates_arr[cur_index])
            cur_target_num -= candidates_arr[cur_index]
            self._generate_combinations(
                candidates_arr, cur_target_num, cur_index, res_arr, middle_state_arr)
            cur_target_num += candidates_arr[cur_index]
            middle_state_arr.pop(-1)


class Solution_lc40(object):
    # [lc40](https://leetcode-cn.com/problems/combination-sum-ii)
    def combinationSum2(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if not candidates:
            return []
        res_arr = []
        middle_state_arr = []
        self._generate_combinations(
            candidates, target, 0, res_arr, middle_state_arr)
        return res_arr

    def _generate_combinations(
            self, candidates_arr, cur_target_num, start_index, res_arr, middle_state_arr):
        if cur_target_num < 0:
            return
        if cur_target_num == 0:
            res_arr.append(copy.deepcopy(middle_state_arr))
            return
        # 这个cur_index是用来去重的
        for cur_index in range(start_index, len(candidates_arr)):
            middle_state_arr.append(candidates_arr[cur_index])
            cur_target_num -= candidates_arr[cur_index]
            self._generate_combinations(
                candidates_arr, cur_target_num,
                cur_index+1,
                res_arr, middle_state_arr)
            cur_target_num += candidates_arr[cur_index]
            middle_state_arr.pop(-1)


class Solution_lc47(object):
    # [lc47](https://leetcode-cn.com/problems/permutations-ii)
    def __init__(self):
        self._used = []

    def permuteUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        middle_arr = []
        res_arr = []
        nums.sort()
        self._used = [False for _ in range(len(nums))]
        self._generate_permutation(nums, 0, res_arr, middle_arr)
        return res_arr

    def _generate_permutation(
            self, nums, cnt, res_arr, middle_arr):
        if cnt == len(nums):
            # 当cnt等于数字字符串长度的时候说明一轮已经递归到底了,
            # 则当前的 中间状态保存器 middle_state_container 则为一个解
            # 此处需要深拷贝一下, 因为下方代码有个 `middle_state_container.pop(-1)`
            res_arr.append(copy.deepcopy(middle_arr))
            return
        for i in range(len(nums)):
            if self._used[i]:
                # 如果本轮递归 used_num_set 已经有_single_num 了,
                # 说明当前排列 middle_state_container 中已经有 _single_num 了
                # 那不应该再加入到这个排列中了
                continue
            if self._used[i-1] == False and (i > 0 and nums[i] == nums[i-1]):
                continue
            self._used[i] = True
            middle_arr.append(nums[i])
            self._generate_permutation(
                nums,
                cnt+1,
                res_arr, middle_arr)
            # 本轮递归完毕后要清空相应记录的状态, 这就是回溯,
            # 递归本身会记录一些状态当退出的时候他会自动清除状态,
            # 那我们自己额外记录的状态, 比如 self._used_num_set 和
            # middle_state_container 的状态应该自己手动清除
            middle_arr.pop(-1)
            self._used[i] = False


class Solution_lc46(object):
    # [lc46](https://leetcode-cn.com/problems/permutations/)
    def __init__(self):
        self._used = []

    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        middle_arr = []
        res_arr = []
        self._used = [False for _ in range(len(nums))]
        self._generate_permutation(nums, 0, res_arr, middle_arr)
        return res_arr

    def _generate_permutation(
            self, nums, cnt, res_arr, middle_arr):
        if cnt == len(nums):
            # 当cnt等于数字字符串长度的时候说明一轮已经递归到底了,
            # 则当前的 中间状态保存器 middle_state_container 则为一个解
            # 此处需要深拷贝一下, 因为下方代码有个 `middle_state_container.pop(-1)`
            res_arr.append(copy.deepcopy(middle_arr))
            return
        for i in range(len(nums)):
            if self._used[i]:
                # 如果本轮递归 used_num_set 已经有_single_num 了,
                # 说明当前排列 middle_state_container 中已经有 _single_num 了
                # 那不应该再加入到这个排列中了
                continue
            self._used[i] = True
            middle_arr.append(nums[i])
            self._generate_permutation(
                nums,
                cnt+1,
                res_arr, middle_arr)
            # 本轮递归完毕后要清空相应记录的状态, 这就是回溯,
            # 递归本身会记录一些状态当退出的时候他会自动清除状态,
            # 那我们自己额外记录的状态, 比如 self._used_num_set 和
            # middle_state_container 的状态应该自己手动清除
            middle_arr.pop(-1)
            self._used[i] = False


class Solution_multi_arr_sum(object):
    # 题目: 4 个数组，目标值 target，每个数组各找一个数，使得 4 个数和为 target，
    # 数组没有顺序，找到所有不重复的组合，
    # 要求时间复杂度 O(n^2)
    def multi_arr_sum(self, nums_arrs, target_sum_num):
        if not nums_arrs:
            return []
        middle_arr = []
        res_arr = []
        self._generate_result(
            nums_arrs, target_sum_num, 0, res_arr, middle_arr)
        return res_arr

    def _generate_result(
            self, nums_arrs, target_sum_num,
            start_i_index,
            res_arr, middle_arr):
        if target_sum_num < 0:
            return
        if len(middle_arr) == len(nums_arrs):
            if target_sum_num == 0:
                res_arr.append(copy.deepcopy(middle_arr))
            return
        for i in range(start_i_index, len(nums_arrs)):
            for j in range(0, len(nums_arrs[i])):
                middle_arr.append(nums_arrs[i][j])
                self._generate_result(
                    nums_arrs, target_sum_num-nums_arrs[i][j],
                    i+1,
                    res_arr, middle_arr
                )
                middle_arr.pop(-1)


class Solution_bigo_thread_permute(object):
    def __init__(self):
        self._used = None
        self._thread_str_arr = [["A", "B", "C", "D"], ["E", "F", "G", "H"]]
        # self._thread_str_arr = [["A", "B"], ["E"]]

    def bigo_thread_permute(self):
        middle_arr = []
        res_arr = []
        # 方便精准的查询每个字母是否被使用以及
        # 方便保证abcd和efgh各自的顺序性时剪枝
        self._used = [
            [False for _ in range(len(self._thread_str_arr[i]))]
            for i in range(len(self._thread_str_arr))
        ]
        _str_2_index_map = {}
        for i, _sub_arr in enumerate(self._thread_str_arr):
            for j, _str in enumerate(_sub_arr):
                # 存好str和他们的数组的index的对应关系
                _str_2_index_map[_str] = [i, j]
        self._generate_permute(_str_2_index_map, 0, res_arr, middle_arr)
        return res_arr

    def _generate_permute(self, str_2_index_map, cnt, res_arr, middle_arr):
        if cnt == len(str_2_index_map):
            res_arr.append(copy.deepcopy(middle_arr))
            return
        for _str, _index_list in str_2_index_map.iteritems():
            i = _index_list[0]
            j = _index_list[1]
            # 剪枝: 为了保证abcd和efgh各自的顺序性,
            # 拿当前的j和used多维数组里i数组里的已经use的最大的max_j来作比较
            # 如果小于等于则剪枝,
            # j大于max_j才能保证添加到middle_arr里的abcd和efgh各自的顺序性
            if j <= self._get_used_max_index_j(i):
                continue
            if self._used[i][j]:
                continue
            self._used[i][j] = True
            middle_arr.append(_str)
            self._generate_permute(str_2_index_map, cnt+1, res_arr, middle_arr)
            middle_arr.pop(-1)
            self._used[i][j] = False

    def _get_used_max_index_j(self, i):
        _max_index_j = -1
        for _cur_index_j, _is_used in enumerate(self._used[i]):
            if _is_used:
                _max_index_j = _cur_index_j
        return _max_index_j


class Solution_sum_paths(object):
    def sum_paths(self, root, sum):
        if not root:
            return []
        path_arr = []
        # 先求包括node本身的情况, 此时这轮递归所说的node是代码中的root
        # 再求不包括node本身的情况, 左右孩子的情况,
        # 这样也就达到了把每个结点都当做是root然后向下寻找路径的目的
        path_arr.extend(self._get_sum_paths(root, sum))
        path_arr.extend(self.sum_paths(root.left, sum))
        path_arr.extend(self.sum_paths(root.right, sum))
        return path_arr

    def _get_sum_paths(self, cur_root, sum_num):
        if not cur_root:
            return []
        path_str_arr = []
        # if sum_num == 0:
        #     pass  # 不能这么写, 这么写的话, 拿不到之前的那个 cur_root 了
        if sum_num - cur_root.val == 0:  # 此时就已经找到了一个解
            path_str_arr.append(str(cur_root.val))
            return path_str_arr

        left_path_str_arr = self._get_sum_paths(
            cur_root.left, sum_num-cur_root.val)
        for _cur_path_str in left_path_str_arr:
            path_str_arr.append(str(cur_root.val) + "->" + _cur_path_str)

        right_path_str_arr = self._get_sum_paths(
            cur_root.right, sum_num-cur_root.val)
        for _cur_path_str in right_path_str_arr:
            path_str_arr.append(str(cur_root.val) + "->" + _cur_path_str)

        return path_str_arr


class Solution_jzo15(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        # 我们采取用1每次左移一位然后与n做位与运算即可
        i = 1
        cnt = 0
        move_cnt = 0
        while i:
            if n & i:
                cnt += 1
            i = i << 1
            move_cnt += 1
            if move_cnt >= 64:
                # 因为python的int型是无限长度的...
                # 所以要用64次限制一下..
                break
        return cnt


class Solution_lc887(object):
    # [lc887](https://leetcode-cn.com/problems/super-egg-drop/)
    # `N`层的楼，然后给你`K`个鸡蛋（`K`至少为 1）
    def superEggDrop2(self, K, N):
        """
        :type K: int
        :type N: int
        :rtype: int
        * 鸡蛋掉落，鹰蛋（Leetcode 887）：（经典dp）
        * 有 K 个鸡蛋，有 N 层楼，用最少的操作次数 F 检查出鸡蛋的质量。
        *
        * 思路：
        * 本题应该逆向思维，若你有 K 个鸡蛋，你最多操作 F 次，求 N 最大值。
        *
        * dp[k][f] = dp[k][f-1] + dp[k-1][f-1] + 1;
        * 解释：
        * 0.dp[k][f]：如果你还剩 k 个蛋，且只能操作 f 次了，所能确定的楼层。
        * 1.dp[k][f-1]：蛋没碎，因此该部分决定了所操作楼层的上面所能容纳的楼层最大值
        * 2.dp[k-1][f-1]：蛋碎了，因此该部分决定了所操作楼层的下面所能容纳的楼层最大值
        * 又因为第 f 次操作结果只和第 f-1 次操作结果相关，因此可以只用一维数组。
        *
        * 时复：O(K*根号(N))
        """
        dp = [[0 for _ in range(K+1)] for _ in range(N+1)]
        i = 0
        while dp[i][K] < N:
            i += 1
            for j in range(1, K+1):
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j] + 1
        return i

    def superEggDrop(self, K, N):
        memo = dict()

        def dp(K, N):
            # base case
            if K == 1:
                return N
            if N == 0:
                return 0
            # 避免重复计算
            if (K, N) in memo:
                return memo[(K, N)]

            res = float('INF')
            # 穷举所有可能的选择
            for i in range(1, N + 1):
                res = min(res,
                          max(
                              dp(K, N - i),
                              dp(K - 1, i - 1)
                          ) + 1
                          )
            # 记入备忘录
            memo[(K, N)] = res
            return res
        return dp(K, N)

    def superEggDrop_dp(self, K, N):
        """
        :type K: int
        :type N: int
        :rtype: int
        """
        # dp[k][n]: 表示为当前状态为 k 个鸡蛋，面对 n 层楼的
        # 这个状态下最坏的情况的最少的扔鸡蛋的次数
        dp = [[p for p in range(N+1)] for _ in range(K+1)]
        for t in range(2, K+1):
            for q in range(1, N+1):
                for m in range(1, q):
                    dp[t][q] = min(
                        dp[t][q],
                        max(
                            dp[t-1][m-1],  # 碎了
                            dp[t][q-m],  # 没碎
                        ) + 1
                    )
        return dp[K][N]


class Solution_lc114(object):
    # [lc114](https://leetcode-cn.com/problems/flatten-binary-tree-to-linked-list/)
    def flatten(self, root):
        """
        :type root: TreeNode
        :rtype: None Do not return anything, modify root in-place instead.
        """ 
        if not root:
            return
        self.flatten(root.left)
        self.flatten(root.right)
        temp_left = root.left
        temp_right = root.right

        root.left = None
        root.right = temp_left

        root_r = root
        while (root_r.right):
            root_r = root_r.right
        root_r.right = temp_right



if __name__ == "__main__":

    sort_algo_func_list = [
        insert_sort,
        merge_sort, merge_sort_bottom_up, merge_sort_bottom_up_optimized,
        quick_sort, quick_sort_optimized, quick_sort_3_ways,
        heap_sort,
    ]
    test_sort_arr_list = [
        [4, 3, 5, 1, 88, 0, -7, 2, 66, -58],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 3, 5, 1, 88, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 0, -7, 2, 66, -58],
        [4, 3, 5, 1, 88, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 0, -7, 2, 66, -58],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 0, -7, 2, 66, -58, 4, 3, 5, 1, 88],
        [0, -7, 2, 66, -58, 4, 3, 5, 1, 884, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [-3, -7, 1, 2, 3, 4, 5, 6, 7, 8, 21, 42, 87, 99, 66, 32, 91, 19, 28],
        [8, 7, 6, 5, 4, 3, 2, 1, 0, -1, 21, 42, 87, 99, 66, 32, 91, 19, 28],
    ]
    for _sort_algo in sort_algo_func_list:
        print _sort_algo.__name__
        is_test_pass = True
        for _test_arr in test_sort_arr_list:
            _copy_test_arr = copy.deepcopy(_test_arr)
            _sort_algo(_copy_test_arr, 0, len(_copy_test_arr)-1)
            # print _copy_test_arr
            pre_elem = _copy_test_arr[0]
            for _elem in _copy_test_arr:
                if _elem < pre_elem:
                    print "is not ordered: " + str(_test_arr)
                    is_test_pass = False
                    break
        print "-------------test " + \
            ("pass" if is_test_pass else "not pass") + \
            "---------------"

    print "\n"

    _bt_a = TreeNode('a')
    _bt_b = TreeNode('b')
    _bt_c = TreeNode('c')
    _bt_d = TreeNode('d')
    _bt_e = TreeNode('e')
    _bt_f = TreeNode('f')
    _bt_g = TreeNode('g')
    _bt_a.left = _bt_b
    _bt_b.left = _bt_c
    _bt_b.right = _bt_d
    _bt_d.left = _bt_e
    _bt_d.right = _bt_f
    _bt_e.right = _bt_g

    bt_traversal_func_list = {
        binary_tree_preorder_traversal: ['a', 'b', 'c', 'd', 'e', 'g', 'f'],
        binary_tree_inorder_traversal: ['c', 'b', 'e', 'g', 'd', 'f', 'a'],
        binary_tree_postorder_traversal: ['c', 'g', 'e', 'f', 'd', 'b', 'a'],
        binary_tree_levelorder_traversal: ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    }
    for _bt_traversal_func, _pass_result_arr in bt_traversal_func_list.iteritems():
        print _bt_traversal_func.__name__
        print "------------test " + \
            ("pass" if _bt_traversal_func(_bt_a) == _pass_result_arr else "not pass") + \
            "---------------"

    print ""

    _copy_bt_a = copy.deepcopy(_bt_a)
    binary_tree_swap_recursive(_copy_bt_a)
    print "after binary_tree_swap_recursive, levelorder traversal:"
    print binary_tree_levelorder_traversal(_copy_bt_a)

    _copy_bt_a = copy.deepcopy(_bt_a)
    binary_tree_swap_iterative(_copy_bt_a)
    print "after binary_tree_swap_iterative, levelorder traversal:"
    print binary_tree_levelorder_traversal(_copy_bt_a)

    print "\n"

    _ll_a = LinkList('a')
    _ll_b = LinkList('b')
    _ll_c = LinkList('c')
    _ll_d = LinkList('d')
    _ll_e = LinkList('e')
    _ll_a.next = _ll_b
    _ll_a.next.next = _ll_c
    _ll_a.next.next.next = _ll_d
    _ll_a.next.next.next.next = _ll_e

    print "after linklist_reverse: --------------"
    new_head = linklist_reverse(_ll_a)
    i = new_head
    while i:
        print i.val, "->",
        i = i.next

    print "\n"

    temp_adjacency_list = [
        [1, 2, 5, 6],
        [0],
        [0],
        [4, 5],
        [3, 5, 6],
        [0, 3, 4],
        [0, 4],
    ]
    test_sparse_graph = SparseGraph(point_count=len(
        temp_adjacency_list), is_directed=False)
    test_sparse_graph.set_adjacency_list(temp_adjacency_list)
    print "test_sparse_graph graph dfs: --------------"
    print test_sparse_graph.graph_dfs()
    print "test_sparse_graph graph bfs: --------------"
    print test_sparse_graph.graph_bfs()
    test_sparse_graph = SparseGraph(point_count=6, is_directed=True)
    test_sparse_graph.add_edge(5, 2)
    test_sparse_graph.add_edge(5, 0)
    test_sparse_graph.add_edge(4, 0)
    test_sparse_graph.add_edge(4, 1)
    test_sparse_graph.add_edge(2, 3)
    test_sparse_graph.add_edge(3, 1)
    print "test_sparse_graph topologic_sort: --------------"
    print test_sparse_graph.topologic_sort()

    # 这个邻接矩阵表示的和上面那个邻接表 temp_adjacency_list 是同一个图
    temp_adjacency_matrix = [
        [0, 1, 1, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 0, 0],
    ]
    test_dense_graph = DenseGraph(point_count=len(
        temp_adjacency_matrix), is_directed=False)
    test_dense_graph.set_adjacency_matrix(temp_adjacency_matrix)
    print "test_dense_graph graph dfs: --------------"
    print test_dense_graph.graph_dfs()
    print "test_dense_graph graph bfs: --------------"
    print test_dense_graph.graph_bfs()

    print "\n"

    bt_5 = TreeNode(5)
    bt_4a = TreeNode(4)
    bt_8 = TreeNode(8)
    bt_11 = TreeNode(11)
    bt_13 = TreeNode(13)
    bt_4b = TreeNode(4)
    bt_7 = TreeNode(7)
    bt_2 = TreeNode(2)
    bt_1 = TreeNode(1)

    bt_5.left = bt_4a
    bt_5.right = bt_8
    bt_4a.left = bt_11
    bt_11.left = bt_7
    bt_11.right = bt_2
    bt_8.left = bt_13
    bt_8.right = bt_4b
    bt_13.right = bt_1

    print "path_sum: --------------"
    print "5: " + str(has_path_sum(bt_5, sum_num=5))
    print "0: " + str(has_path_sum(bt_5, sum_num=0))
    print "22: " + str(has_path_sum(bt_5, sum_num=22))
    print "13: " + str(has_path_sum(bt_5, sum_num=13))
    print "17: " + str(has_path_sum(bt_5, sum_num=17))
    print "27: " + str(has_path_sum(bt_5, sum_num=27))
    print "20: " + str(has_path_sum(bt_5, sum_num=20))

    print ""

    print "binary_tree_paths: --------------"
    print binary_tree_paths(bt_5)

    print ""

    print "path_sum_3: --------------"
    print "5: " + str(path_sum_3(bt_5, sum_num=5))
    print "0: " + str(path_sum_3(bt_5, sum_num=0))
    print "22: " + str(path_sum_3(bt_5, sum_num=22))
    print "13: " + str(path_sum_3(bt_5, sum_num=13))
    print "17: " + str(path_sum_3(bt_5, sum_num=17))
    print "27: " + str(path_sum_3(bt_5, sum_num=27))
    print "20: " + str(path_sum_3(bt_5, sum_num=20))

    print ""

    print "jump_step: --------------"
    print "jump_step_optimized(4): " + str(jump_step_optimized(4))
    print "jump_step_optimized(55): " + str(jump_step_optimized(55))
    print "jump_step_optimized(9): " + str(jump_step_optimized(9))
    print "jump_step(4): " + str(jump_step(4))
    print "jump_step(9): " + str(jump_step(9))
    print "jump_step_dynamic_programming(4): " + \
        str(jump_step_dynamic_programming(4))
    print "jump_step_dynamic_programming(9): " + \
        str(jump_step_dynamic_programming(9))
    print "jump_step_dynamic_programming(55): " + \
        str(jump_step_dynamic_programming(55))

    print ""

    print "letter_combinations_of_a_phone_number: --------------"
    print "letter_combinations_of_a_phone_number('23'):"
    print str(letter_combinations_of_a_phone_number("23"))
    print "letter_combinations_of_a_phone_number('46'):"
    print str(letter_combinations_of_a_phone_number("46"))
    # print "letter_combinations_of_a_phone_number('146'):"
    # print str(letter_combinations_of_a_phone_number("146"))
    # print "letter_combinations_of_a_phone_number('416'):"
    # print str(letter_combinations_of_a_phone_number("416"))
    print "letter_combinations_of_a_phone_number('234'):"
    print str(letter_combinations_of_a_phone_number("234"))

    print ""

    print "combinations: --------------"
    print "Solution_lc77().combine(2, 1):"
    print str(Solution_lc77().combine(2, 1))
    print "Solution_lc77().combine(4, 2):"
    print str(Solution_lc77().combine(4, 2))
    print "Solution_lc77().combinations_optimized(2, 1):"
    print str(Solution_lc77().combinations_optimized(2, 1))
    print "Solution_lc77().combinations_optimized(4, 2):"
    print str(Solution_lc77().combinations_optimized(4, 2))

    print ""

    print "Solution_number_of_islands: --------------"
    print """
        grid = [
            ["1","1","1","1","0"],
            ["1","1","0","1","0"],
            ["1","1","0","0","0"],
            ["0","0","0","0","0"]
        ] 
    """
    test_grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    snoi1 = Solution_number_of_islands()
    print " Solution_number_of_islands.numIslands(grid):" + str(
        snoi1.numIslands(test_grid))
    print """ 
        grid =  [
            ["1","1","0","0","0"],
            ["1","1","0","0","0"],
            ["0","0","1","0","0"],
            ["0","0","0","1","1"]
        ]
    """
    test_grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    snoi2 = Solution_number_of_islands()
    print " Solution_number_of_islands.numIslands(grid):" + str(
        snoi2.numIslands(test_grid))

    print ""

    print "integer_break: --------------"
    print "integer_break(2):"
    print str(Solution_integer_break().integerBreak(2))
    print "integer_break(10):"
    print str(Solution_integer_break().integerBreak(10))
    print "integer_break_dp(10):"
    print str(Solution_integer_break().integer_break_dp(10))

    print ""

    print "house_robber: --------------"
    print "house_robber([6,6,4,8,4,3,3,10]):"
    print str(Solution_house_robber().rob([6, 6, 4, 8, 4, 3, 3, 10]))
    print "house_robber([183,2219,57,193,94,233,202,154,65,240,97]):"
    print str(Solution_house_robber().rob(
        [183, 2219, 57, 193, 94, 233, 202, 154, 65, 240, 97]))
    print "house_robber([1, 2, 3, 1]):"
    print str(Solution_house_robber().rob([1, 2, 3, 1]))
    print "house_robber([2, 7, 9, 3, 1]):"
    print str(Solution_house_robber().rob([2, 7, 9, 3, 1]))
    print "house_robber_dp_1([6,6,4,8,4,3,3,10]):"
    # print str(Solution_house_robber().rob_dp_1([6, 6, 4, 8, 4, 3, 3, 10]))
    # print "house_robber_dp_1([1, 2, 3, 1]):"
    # print str(Solution_house_robber().rob_dp_1([1, 2, 3, 1]))
    # print "house_robber_dp_1([2, 7, 9, 3, 1]):"
    # print str(Solution_house_robber().rob_dp_1([2, 7, 9, 3, 1]))
    # print "house_robber_dp_1([183,2219,57,193,94,233,202,154,65,240,97]):"
    # print str(Solution_house_robber().rob_dp_1(
    #     [183, 2219, 57, 193, 94, 233, 202, 154, 65, 240, 97]))
    print "house_robber_rob1_dp([6,6,4,8,4,3,3,10]):"
    print str(Solution_house_robber().rob1_dp([6, 6, 4, 8, 4, 3, 3, 10]))
    print "house_robber_rob1_dp([1, 2, 3, 1]):"
    print str(Solution_house_robber().rob1_dp([1, 2, 3, 1]))
    print "house_robber_rob1_dp([2, 7, 9, 3, 1]):"
    print str(Solution_house_robber().rob1_dp([2, 7, 9, 3, 1]))
    print "house_robber_rob1_dp([183,2219,57,193,94,233,202,154,65,240,97]):"
    print str(Solution_house_robber().rob1_dp(
        [183, 2219, 57, 193, 94, 233, 202, 154, 65, 240, 97]))
    print "house_robber_rob1_dp_memo([6,6,4,8,4,3,3,10]):"
    print str(Solution_house_robber().rob1_dp_memo([6, 6, 4, 8, 4, 3, 3, 10]))
    print "house_robber_rob1_dp_memo([1, 2, 3, 1]):"
    print str(Solution_house_robber().rob1_dp_memo([1, 2, 3, 1]))
    print "house_robber_rob1_dp_memo([2, 7, 9, 3, 1]):"
    print str(Solution_house_robber().rob1_dp_memo([2, 7, 9, 3, 1]))
    print "house_robber_rob1_dp_memo([183,2219,57,193,94,233,202,154,65,240,97]):"
    print str(Solution_house_robber().rob1_dp_memo(
        [183, 2219, 57, 193, 94, 233, 202, 154, 65, 240, 97]))
    
    print "house_robber_house_rob_detail_seq([1, 2, 3, 1]):"
    print str(Solution_house_robber().house_rob_detail_seq([1, 2, 3, 1])) 


    print ""

    print "knapsack: --------------"
    print "knapsack(8, [7, 2, 4, 3], [9, 3, 2, 1]):"
    print Solution_knapsack().knapsack(8, [7, 2, 4, 3], [9, 3, 2, 1])
    print "knapsack(5, [1, 2, 3], [6, 10, 12]):"
    print Solution_knapsack().knapsack(5, [1, 2, 3], [6, 10, 12])
    print "knapsack_dp(8, [7, 2, 4, 3], [9, 3, 2, 1]):"
    print Solution_knapsack().knapsack_dp(8, [7, 2, 4, 3], [9, 3, 2, 1])
    print "knapsack_dp(5, [1, 2, 3], [6, 10, 12]):"
    print Solution_knapsack().knapsack_dp(5, [1, 2, 3], [6, 10, 12])

    print ""

    print "partition_equal_subset_sum: --------------"
    print "canPartition([9, 5]):"
    print Solution_partition_equal_subset_sum().canPartition([9, 5])
    print "canPartition([1, 2, 3, 6]):"
    print Solution_partition_equal_subset_sum().canPartition([1, 2, 3, 6])
    print "canPartition([1, 27, 35, 61]):"
    print Solution_partition_equal_subset_sum().canPartition([1, 27, 35, 61])
    print "canPartition([1, 8, 3, 6]):"
    print Solution_partition_equal_subset_sum().canPartition([1, 8, 3, 6])
    print "canPartition([1, 21, 3, 4, 7, 161]):"
    print Solution_partition_equal_subset_sum(
    ).canPartition([1, 21, 3, 4, 7, 161])
    print "canPartition_recursion([9, 5]):"
    print Solution_partition_equal_subset_sum().canPartition_recursion([9, 5])
    print "canPartition_recursion([1, 2, 3, 6]):"
    print Solution_partition_equal_subset_sum(
    ).canPartition_recursion([1, 2, 3, 6])
    print "canPartition_recursion([1, 27, 35, 61]):"
    print Solution_partition_equal_subset_sum(
    ).canPartition_recursion([1, 27, 35, 61])
    print "canPartition_recursion([1, 8, 3, 6]):"
    print Solution_partition_equal_subset_sum(
    ).canPartition_recursion([1, 8, 3, 6])
    print "canPartition_recursion([1, 21, 3, 4, 7, 161]):"
    print Solution_partition_equal_subset_sum(
    ).canPartition_recursion([1, 21, 3, 4, 7, 161])

    print ""

    print "partition_equal_subset_sum: --------------"
    print "LIS([0,8,4,12,2, 16]):"
    print Solution_LIS().lengthOfLIS([0, 8, 4, 12, 2, 16])

    print ""

    print "partition_equal_subset_sum: --------------"
    print "LCS(['ABCD', 'AEBD']):"
    print Solution_LCS().lengthOfLCS(['ABCD', 'AEBD'])
    print "LCS(['ABCDefscgiqh', 'ABEDeabgiyy4q.h']):"
    print Solution_LCS().lengthOfLCS(['ABCDefscgiqh', 'ABEDeabgiyy4q.h'])
    print "get_lcs_detail_seq_1(['ABCD', 'AEBD']):"
    print Solution_LCS().get_lcs_detail_seq_1(['ABCD', 'AEBD'])
    print "get_lcs_detail_seq_1(['ABCDefscgiqh', 'ABEDeabgiyy4q.h']):"
    print Solution_LCS().get_lcs_detail_seq_1(
        ['ABCDefscgiqh', 'ABEDeabgiyy4q.h'])
    print "get_lcs_detail_seq_2(['ABCD', 'AEBD']):"
    print Solution_LCS().get_lcs_detail_seq_2(['ABCD', 'AEBD'])
    print "get_lcs_detail_seq_2(['ABCDefscgiqh', 'ABEDeabgiyy4q.h']):"
    print Solution_LCS().get_lcs_detail_seq_2(
        ['ABCDefscgiqh', 'ABEDeabgiyy4q.h'])

    print ""

    print "----------Solution_build_bt-------"
    bt_root_node = Solution_build_bt().buildTree(
        [9, 3, 15, 20, 7],
        [9, 15, 7, 20, 3],
    )
    print bt_root_node.val
    print bt_root_node.left.val
    print bt_root_node.right.val

    print ""

    print "----------Solution_LCA-------"
    test_lca_bt = TreeNode(1)
    test_lca_bt.left = TreeNode(2)
    test_lca_bt.right = TreeNode(3)
    test_lca_bt.left.left = TreeNode(4)
    test_lca_bt.left.right = TreeNode(5)
    test_lca_bt.left.right.left = TreeNode(51)
    test_lca_bt.left.right.right = TreeNode(52)
    test_lca_bt.right.left = TreeNode(6)
    test_lca_bt.right.right = TreeNode(7)

    print Solution_LCA().lowestCommonAncestor(
        test_lca_bt, test_lca_bt.left.left, test_lca_bt.left.right).val
    print Solution_LCA().lowestCommonAncestor(
        test_lca_bt, test_lca_bt.left.right, test_lca_bt.right.left).val
    print Solution_LCA().lowestCommonAncestor(
        test_lca_bt, test_lca_bt.left.left, test_lca_bt.left.right.left).val

    print ""

    print "----------combinationSum-------"
    print 'Solution_lc39().combinationSum([2, 3, 6, 7], 7) :'
    print Solution_lc39().combinationSum([2, 3, 6, 7], 7)
    print 'Solution_lc39().combinationSum([2, 3, 6, 7, 1], 7) :'
    print Solution_lc39().combinationSum([2, 3, 6, 7, 1], 7)
    print 'Solution_lc39().combinationSum([2, 3, 6, 7, 1, 1], 7) :'
    print Solution_lc39().combinationSum([2, 3, 6, 7, 1, 1], 7)

    print ""

    print "----------combinationSum2-------"
    print 'Solution_lc40().combinationSum2([2, 3, 6, 7], 7) :'
    print Solution_lc40().combinationSum2([2, 3, 6, 7], 7)
    print 'Solution_lc40().combinationSum2([2, 3, 6, 7, 1], 7) :'
    print Solution_lc40().combinationSum2([2, 3, 6, 7, 1], 7)
    print 'Solution_lc40().combinationSum2([2, 3, 6, 7, 1, 1], 7) :'
    print Solution_lc40().combinationSum2([2, 3, 6, 7, 1, 1], 7)

    print ""

    print "permutations: --------------"
    print "permutations([1]):"
    print str(Solution_lc46().permute([1]))
    print "permutations([2, 3]):"
    print str(Solution_lc46().permute([2, 3]))
    print "permutations([1, 4, 6]):"
    print str(Solution_lc46().permute([1, 4, 6]))

    print ""

    print "----------permuteUnique-------"
    print 'Solution_lc47().permuteUnique([1, 1, 2]) :'
    print Solution_lc47().permuteUnique([1, 1, 2])

    print ""

    print "----------multi_arr_sum-------"
    print 'Solution_multi_arr_sum().multi_arr_sum([[1, 2], [3, 4], [5, 6, 9], [7, 8]], 18) :'
    print Solution_multi_arr_sum().multi_arr_sum(
        [[1, 2], [3, 4], [5, 6, 9], [7, 8]], 18)

    print ""

    print "----------bigo_thread_permute()-------"
    print 'Solution_bigo_thread_permute().bigo_thread_permute() :'
    print Solution_bigo_thread_permute().bigo_thread_permute()

    print ""

    print "----------sum_paths()-------"
    """
               1
             /  \
            2     3
           /\    / \
          8  6   5  7
    """
    bt = TreeNode(1)
    bt.left = TreeNode(2)
    bt.right = TreeNode(3)
    bt.left.left = TreeNode(8)
    bt.left.right = TreeNode(6)
    bt.right.right = TreeNode(7)
    bt.right.left = TreeNode(5)

    cp_bt = copy.deepcopy(bt)
    print Solution_sum_paths().sum_paths(cp_bt, 9)
    print Solution_sum_paths().sum_paths(cp_bt, 10)
    print Solution_sum_paths().sum_paths(cp_bt, 11)
    print Solution_sum_paths().sum_paths(cp_bt, 8)

    print ""

    print Solution_jzo15().hammingWeight(5)
    print Solution_jzo15().hammingWeight(0b0111)
    print Solution_jzo15().hammingWeight(-2)

    print ""

    print "Solution_lc887().superEggDrop(2, 100) : "
    print Solution_lc887().superEggDrop(2, 100)

    print ""

    print "Solution_lc114().flatten() : "
    cp_bt = copy.deepcopy(bt)
    Solution_lc114().flatten(cp_bt)