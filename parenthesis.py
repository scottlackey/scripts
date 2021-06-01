#open_list = ["[","{","("]
#close_list = ["]","}",")"]
def check(myStr):
    stack = []
    for i in myStr:
        if i == '(':
            stack.append(i)
        elif i == ')':
            if ((len(stack) > 0) and
                (stack[len(stack)-1] == '(' )):
                stack.pop()
            else:
                return "Unbalanced"
    if len(stack) == 0:
        return "Balanced"
    else:
        return "Unbalanced"
  
  
# Driver code
string = "{[]{()}}"
print(string,"-", check(string))
  
string = "[{}{})(]"
print(string,"-", check(string))
  
string = "((()"
print(string,"-",check(string))
