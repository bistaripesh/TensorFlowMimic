#!/usr/bin/env python
# coding: utf-8
#---------------@credits Pierian Data(Udemy)---------
#---------------@autohor Ripesh Bista----------------
# In[195]:


class Operation():
    def __init__(self, input_nodes =[]):
        self.input_nodes= input_nodes
        #takes input_nodes from the __init___ function
        self.output_nodes =[]
        #self.output is empty 
        for node in input_nodes:
            # loops input_nodes 
            print(node)
            node.output_nodes.append(self)
            #node.output_nodes.append(self) refers to Operation()
            #means once the operation is done it will send to refered operation 
        _default_graph.operations.append(self)    
    def compute(self):
        #this fucntion is gonna be overwritten by the child class
        pass


# In[196]:


class add(Operation):
    def __init__(self,x,y):
        super().__init__([x,y])
    def compute(self,x_var,y_var):
        #operation class compute function is over written 
        self.inputs =[x_var,y_var]
        return x_var+y_var


# In[197]:


class multiply(Operation):
    def __init__(self,x,y):
        super().__init__([x,y])
    def compute(self,x_var,y_var):
        self.inputs =[x_var,y_var]
        return x_var*y_var


# In[198]:


class matmul(Operation):
    def __init__(self,x,y):
        super().__init__([x,y])
    def compute(self,x_var,y_var):
        self.inputs =[x_var,y_var]
        return x_var.dot(y_var)


# In[199]:


class Placeholder():
    #Placeholder 
    def __init__(self):
        self.output_nodes =[]
        #so output_node has not got it's value till graph function
        _default_graph.placeholders.append(self)
        # graph class list will get the placeholder value


# In[200]:


class Variable():
    def __init__(self, initial_value = None):
        self.value = initial_value
        self.output_nodes = []
        #same as place holder output node is empty
        _default_graph.variables.append(self)


# In[201]:


class Graph():
    def __init__(self):
        self.operations=[]
        #it gets what operation to do from operation class
        self.variables=[]
        #it gets variable from variable class
        self.placeholders=[]
        #it gets place holder from placeholder class
        
    def set_as_default(self):
        global _default_graph
        _default_graph = self


# In[202]:


g =Graph()
g.set_as_default()
#setting graph as default 

# to be remembered ,still the self.output_nodes is empty so it needs to be filled for the operation
# A=10
# b=1
# z=10x+1

# In[203]:


A = Variable(10)
b= Variable(1)


# In[204]:


x= Placeholder()


# In[205]:


y = multiply(A,x)


# In[206]:


z= add(y,b)

# Session will extecute the graph also no outputnode is filled.
# PostOrder Tree Traversal computes in the correct order
# In[207]:


#this algorithm is not necessary and just implemented it
#it makes sure that we execute the computation in correct order
def traverse_postorder(operation):
    nodes_postorder =[]
    def recurse(node):
        if isinstance(node, Operation):
            # (obj, class_or_tuple) node is object and Operation is class
            
            for input_node in node.input_nodes:
                recurse(input_node)
        nodes_postorder.append(node)    
    recurse(operation)    
    return nodes_postorder


# In[211]:


class Session():
    def run(self,operation,feed_dict={}):
      
        nodes_postorder = traverse_postorder(operation)
        
            
        for node in nodes_postorder:
            if type(node) == Placeholder:
                node.output = feed_dict[node]
      
            elif type(node) ==  Variable:
                node.output = node.value
     
            else:
                node.inputs = [input_node.output for input_node in node.input_nodes]
                node.output = node.compute(*node.inputs)
            
            if type(node.output) ==list:
                node.output =np.array(node.output)
                    
        return operation.output        
            
            


# In[212]:


sess = Session()


# In[213]:


result = sess.run(operation=z,feed_dict={x:10})


# In[214]:


result


# In[ ]:




