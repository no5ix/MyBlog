---
title: 数据结构四之链表进阶
date: 2014-12-22 23:19:21
tags:
- DataStructure
- CPP
- Algo
- noodle
categories:
- Algo
---


只谈一下单链表, 链表实在是太重要, 是前面两篇说算法博客的基础, 了解了其应用和衍生, 再去了解其本身就有动力了



# 存储结构
```
typedef struct Node
{
	DataType data;
	struct Node *next;
}Node, *Node_Ptr;
```

{% asset_img advanced_linked_list_1.png %}

- 链表中第一个结点的存储位置叫做头指针
- 头指针和头结点不同，头结点即第一个结点，头指针是指向第一个结点的指针。链表中可以没有头结点，但不能没有头指针。
- 如果链表有头结点，那么头指针就是指向头结点数据域的指针。
- 单链表也可以没有头结点

**头结点的优点: **

- 头结点是为了操作的统一与方便而设立的，放在第一个元素结点之前，其数据域一般无意义（当然有些情况下也可存放链表的长度、用做监视哨等等）。
- 有了头结点后，对在第一个元素结点前插入结点和删除第一个结点，其操作与对其它结点的操作统一了。


## 有头结点和无头结点的建立链表方法头插法 

``` cpp
include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct Link {
    int  elem;
    struct Link *next;
}link;
//无头结点链表的头插法实现函数
link * creatLink(int * arc, int length) {
    int i;
    //最初状态下，头指针 H 没有任何结点，所以，插入第一个元素，就相当于是创建结点 H
    link * H =(link*)malloc(sizeof(link));
    H->elem = arc[0];
    H->next = NULL;
    //如果采用头插法插入超过 1 个元素，则可添加到第一个结点 H 之前
    for (i = 1; i<length; i++) {
        link * a = (link*)malloc(sizeof(link));
        a->elem = arc[i];
        //插入元素时，首先将插入位置后的链表链接到新结点上
        a->next = H;
        //然后再链接头指针 H
        H = a;
    }
    return H;
}
//有头结点链表的头插法实现函数
link * HcreatLink(int * arc, int length) {
    int i;
    //创建头结点 H，其链表的头指针也是 H
    link * H = (link*)malloc(sizeof(link));
    H->elem = 0;
    H->next = NULL;
    //采用头插法创建链表
    for (i = 0; i<length; i++) {
        link * a = (link*)malloc(sizeof(link));
        a->elem = arc[i];
        //首先将插入位置之后的链表链接到新结点 a 上
        a->next = H->next;
        //将新结点 a 插入到头结点之后的位置
        H->next = a;
    }
    return H;
}
//链表的输出函数
void display(link *p) {
    while (p) {
        printf("%d ", p->elem);
        p = p->next;
    }
    printf("\n");
}
int main() {
    int a[3] = { 1,2,3 };
    //采用头插法创建无头结点链表
    link * H = creatLink(a, 3);
    display(H);
    //采用头插法创建有头结点链表
    link * head = HcreatLink(a, 3);
    display(head);
    //使用完毕后，释放即可
    free(H);
    free(head);
    return 0;
}
```

运行结果：
```
3 2 1
0 3 2 1
```
提示：没有 0 的为无头结点的头插法输出结果，有 0 的为有头结点的头插法的输出结果


**. . .**<!-- more -->


# 在O(1)时间删除链表结点

给定单链表的头指针和一个结点指针, 定义一个函数在 O(1)时间删除该结点.

思路 : 

如果要遍历找到该结点的前一个结点p, 来改变结点p的下一个结点指向的这种解法肯定是O(n)时间复杂度了. 
**那是不是一定需要得到被删除的结点的前一个结点呢？**
答案是否定的。我们可以很方便地得到要删除的结点的下一个结点。如果我们把下一个结点的内容复制到需要删除的结点上覆盖原有的内容，再把下一个结点删除，那是不是就相当于把当前需要删除的结点删除了？

# 找一个单链表的中间结点


算法思想 : 

(**快慢指针的使用**)设置两个指针，一个每次移动两个位置，一个每次移动一个位置，当第一个指针到达尾节点时，第二个指针就达到了中间节点的位置

# 判断链表中是否有环


算法思想 : 

(**快慢指针的使用**)链表中有环，其实也就是自相交. 用两个指针pslow和pfast从头开始遍历链表，pslow每次前进一个节点，pfast每次前进两个结点，若存在环，则pslow和pfast肯定会在环中相遇，若不存在，则pslow和pfast能正常到达最后一个节点

# 判断两个链表是否相交, 假设两个链表均不带环


算法思想 : 

如果两个链表相交于某一节点，那么在这个相交节点之后的所有节点都是两个链表所共有的。也就是说，如果两个链表相交，那么最后一个节点肯定是共有的。先遍历第一个链表，记住最后一个节点，然后遍历第二个链表，到最后一个节点时和第一个链表的最后一个节点做比较，如果相同，则相交，否则不相交。

# 从尾到头打印链表

有两种解法 : 

- **反转链表解法** : 反转链表之后再从头到尾打印 (这样会改变原来的链表)
- **栈存储解法**(比较简单, 本文不详讲了) : 用栈存储之后再逐个出栈一一打印 (这样不会改变原来的链表)

## 反转链表解法

比如一个链表:
头结点->A->B->C->D->E
反转成为:
头结点->E->D->C->B->A

### 算法思想 : 

第一轮 : 头结点->A->B->C->D->E
第二轮 : 头结点->B->A->C->D->E
第三轮 : 头结点->C->B->A->D->E
第四轮 : 头结点->D->C->B->A->E
第五轮 : 头结点->E->D->C->B->A

### 算法cpp实现：

手写的代码， 已经跑过了，可直接用
下面代码中反转函数为 ReverseList ， 且有详细注释以及总结

``` c++ LinkedList.h
#pragma once

struct TList
{
	struct TList *pNext;
	void *pData;
};
typedef struct TList *LPTLIST;

void AppendElem(LPTLIST *ppstHead);

void ReverseList(LPTLIST *ppstHead);

void PrintList(LPTLIST *ppstHead);

void DestroyList(LPTLIST *ppstHead);
```


``` c++ LinkedList.cpp
#include "LinkedList.h"
#include <iostream>

using std::cout;
using std::endl;
using std::cin;

void AppendElem(LPTLIST *ppstHead)
{
	if (!ppstHead)
	{
		cout << "ppstHead is null" << endl;
		return;
	}

	if (!*ppstHead)
	{
		*ppstHead = new TList;
		if (!*ppstHead)
		{
			cout << "*ppstHead malloc error" << endl;
			return;
		}
		(*ppstHead)->pData = nullptr;
		(*ppstHead)->pNext = nullptr;
	}

	LPTLIST temp_elem_ptr = *ppstHead;

	cout << "input '.' to finish" << endl;

	char key_data = '.';
	while (1)
	{
		cin >> key_data;
		if (key_data != '.')
		{

			char * temp_key_data = new char;
			if (!temp_key_data)
			{
				cout << "temp_key_data malloc error" << endl;
				return;
			}
			*temp_key_data = key_data;

			LPTLIST new_elem_ptr = new TList;
			if (!new_elem_ptr)
			{
				cout << "new_elem malloc error" << endl;
				return;
			}
			new_elem_ptr->pData = temp_key_data;
			new_elem_ptr->pNext = nullptr;

			temp_elem_ptr->pNext = new_elem_ptr;
			temp_elem_ptr = new_elem_ptr;
		}
		else
		{
			break;
		}
	}
}

/* 将单链表反转, 要求只能扫描链表一次.
*@param ppstHead 指向链表首节点的指针
*/
void ReverseList(LPTLIST *ppstHead)
{
	if (!ppstHead)
	{
		cout << "ppstHead is null" << endl;
		return;
	}

	if (!*ppstHead)
	{
		cout << "*ppstHead is null" << endl;
		return;
	}

	// 我们只用上述算法思想中第二轮来说明一下此算法, 即为 "第二轮 : 头结点->B->A->C->D->E"

	// origin_first_elem_ptr指针一直指向着原来链表头指针后面的那个元素
	//（即原第一个元素， 这个指针的指向一直都不会变， 一直都是指向A）
	LPTLIST origin_first_elem_ptr = (*ppstHead)->pNext; 

	LPTLIST temp_elem_ptr = nullptr;

	// 需要两个判断, 不然当 origin_first_elem_ptr 为NULL的时候会出错, 
	// 且 origin_first_elem_ptr ->pNext为NULL的时候也没必要继续循环了
	while (origin_first_elem_ptr && origin_first_elem_ptr->pNext)	 
	{
		// 临时保存一下元素A后面的后面那个元素C
		temp_elem_ptr = origin_first_elem_ptr->pNext->pNext;	

		// 让B指向A : B->A (第1步)
		origin_first_elem_ptr->pNext->pNext = (*ppstHead)->pNext;

		// 把目前第一个元素A替换为原第一个元素的后面那个元素B : 头结点->B (第2步)
		(*ppstHead)->pNext = origin_first_elem_ptr->pNext;

		// 原第一个元素A的pnext指到它后面的后面那个元素C : A->C (第3步)
		origin_first_elem_ptr->pNext = temp_elem_ptr;
	}
	// 综上所述只需要3步, 链表反转需要两个指针， 
	// 见上面两个指针, 一个 origin_first_elem_ptr, 一个 temp_elem_ptr
	// 且要注意while条件中循环的是origin_first_elem_ptr, 而非ppstHead
}

void PrintList(LPTLIST *ppstHead)
{
	if (!ppstHead)
	{
		cout << "ppstHead is null" << endl;
		return;
	}

	if (!*ppstHead)
	{
		cout << "*ppstHead is null" << endl;
		return;
	}

	LPTLIST temp_elem_ptr = *ppstHead;
	while (temp_elem_ptr = temp_elem_ptr->pNext)
	{
		cout << *(char *)(temp_elem_ptr->pData) << "->";
	}
	cout << endl;
}

void DestroyList(LPTLIST *ppstHead)
{
	if (!ppstHead)
	{
		cout << "ppstHead is null" << endl;
		return;
	}

	if (!*ppstHead)
	{
		cout << "*ppstHead is null" << endl;
		return;
	}

	LPTLIST temp_elem_ptr = *ppstHead, temp_next_ptr = nullptr;

	while (temp_elem_ptr)
	{
		temp_next_ptr = temp_elem_ptr->pNext;

		delete (char *)(temp_elem_ptr->pData);
		temp_elem_ptr->pData = nullptr;

		delete temp_elem_ptr;
		temp_elem_ptr = temp_next_ptr;
	}

	cout << "DestroyList finished." << endl;
}
```


```c++ main.cpp
#include "LinkedList.h"
int main()
{
	TList *test_list = nullptr;

	AppendElem(&test_list);
	PrintList(&test_list);

	ReverseList(&test_list);
	PrintList(&test_list);

	DestroyList(&test_list);

	return 0;
}
```


<!-- 
## 栈存储解法

``` c++

#include <stack>
#include <stdio.h>

using std::stack;

struct ListNode
{
	void *pData;
	ListNode *pNext;
};

void AppendListNode(ListNode *pHead, void *Data)
{
	if (!pHead)
	{
		return;
	}
	ListNode *pEndNode = NULL;
	ListNode *pTemp = pHead;
	while (pTemp)
	{
		pEndNode = pTemp;
		pTemp = pTemp->pNext;
	}
	ListNode *NewListNode = new ListNode;
	if (!NewListNode)
	{
		return;
	}
	NewListNode->pData = Data;
	NewListNode->pNext = NULL;
	pEndNode->pNext = NewListNode;
}

void PrintList(ListNode *pHead)
{
	if (!pHead)
	{
		return;
	}
	while (pHead = pHead->pNext)
	{
		printf( "%d ->", *(int *)(pHead->pData) );
	}
}

void PrintListReversingly_Iteratively(ListNode *pHead)
{
	if (!pHead)
	{
		return;
	}
	stack<ListNode> stackListNode;
	while (pHead = pHead->pNext)
	{
		stackListNode.push(*pHead);
	}

	while (!stackListNode.empty())
	{
		printf("%d -> ", *((int *)(stackListNode.top().pData)));
		stackListNode.pop();
	}
}

int main(int argc, char* argv[])
{
	ListNode* TestListNode = new ListNode;
	TestListNode->pData = NULL;
	TestListNode->pNext = NULL;

	int Data1 = 5;
	int Data2 = 6;
	int Data3 = 7;

	AppendListNode(TestListNode, &Data1);
	AppendListNode(TestListNode, &Data2);
	AppendListNode(TestListNode, &Data3);

	PrintListReversingly_Iteratively(TestListNode);

	return 0;
}

``` -->