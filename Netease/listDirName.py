import sys, os
path = 'E:\hnzskj\政府风险防控项目\法规\法规文档\法规库无'
fagui_list_name = 'fagui_list.txt'
for i in os.listdir(path):
     with open(fagui_list_name,"a") as f:
        f.write(i+"\n")
  