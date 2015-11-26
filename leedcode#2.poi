#class ListNode(object):
#    def __init__(self, x):
#        self.val = x
#        self.next = None


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
            a += l1.val*10**(i)
            i+=1
            l1=l1.next
        
        b=0
        i=0
        while(l2 != None):
            b += l2.val*10**(i)
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
