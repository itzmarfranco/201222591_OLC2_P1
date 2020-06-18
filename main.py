import sys
import os

from magicsticklibs import Main


# counter = 0
# def graphAST(tree):
#     if type(tree) == tuple:
#         print('PADRE', tree)
#         for node in tree:
#             print('HIJO', node)
#             graphAST(node)
#     else:
#         pass



root = Main.TextPad_Window(className = " Augus")
os.system('cls')
print('########################## AUGUS ##########################')
# graphAST((('=', '$t0', 5), (('=', '$t1', 9.9), (('=', '$t2', 'hola'), (('array', '$t9'), (('=', 'array_a', '$t9', 0, 'mundo'), (('=', 'array_a', '$t9', 1, 'xD'), (('=', 'array_a', '$t9', 1, 'ja,ja'), (('=', 'array_a', 
# '$t9', 1, 'amigo'), (('=', '$t3', ('convert', 'int', '$t9')), None))))))))))


root.mainloop()