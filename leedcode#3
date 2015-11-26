class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        d=[0]*256
        
        max_len = 0
        start = 0
        for i in range(0,len(s)):
            if d[ord(s[i])] == 0:  
                d[ord(s[i])] = 1  
                max_len = max(max_len, i-start+1);   
            else: 
                while s[start] != s[i]: 
                    d[ord(s[start])] = 0  
                    start +=1
                start+=1
                
        return max_len
