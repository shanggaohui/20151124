# 20151124
20151124做的leetcode题目

leetcode中的＃1

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i in range(0, len(nums)-1):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i+1, j+1]
                
        
        return None

leetcode中的＃2

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        a=0
        i=0
        while(l1 != None):
            a += l1.val*10^(i)
            i+=1
            l1=l1.next
        
        b=0
        i=0
        while(l2 != None):
            b += l2.val*10^(i)
            i+=1
            l2=l2.next
            
        sum = a+b
        head=ListNode(sum % 10)
        p=head
        sum //=10
        while sum != 0:
            p.next=ListNode(sum % 10)
            p=p.next
            sum //= 10
        
        return head
        
