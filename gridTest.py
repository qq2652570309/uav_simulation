import numpy as np

from grid import Grid

row = 6
column = 6




g1 = Grid(row=row, col=column, time=60)

# print('left top --> right botton')
# startX = 1
# startY = 1
# endX = 3
# endY = 4
# print('(start)--> (end)')
# print('({0}, {1}) --> ({2},{3})'.format(startX,startY,endX,endY))
# print('necessary time: {0}'.format(abs(startX-endX) + abs(endY-startY) + 1))
# g1.drawPath(startX=startX,startY=startY,endX=endX,endY=endY)


# print('left botton --> right top')
# startX = 4
# startY = 1
# endX = 1
# endY = 4
# print('(start)--> (end)')
# print('({0}, {1}) --> ({2},{3})'.format(startX,startY,endX,endY))
# print('necessary time: {0}'.format(abs(startX-endX) + abs(endY-startY) + 1))
# g1.drawPath(startX=startX,startY=startY,endX=endX,endY=endY)


# print('right top --> left botton')
# startX = 1
# startY = 4
# endX = 4
# endY = 1
# print('(start)--> (end)')
# print('({0}, {1}) --> ({2},{3})'.format(startX,startY,endX,endY))
# print('necessary time: {0}'.format(abs(startX-endX) + abs(endY-startY) + 1))
# g1.drawPath(startX=startX,startY=startY,endX=endX,endY=endY)


print('right botton --> left top')
startX = 4
startY = 4
endX = 1
endY = 1
print('(start)--> (end)')
print('({0}, {1}) --> ({2},{3})'.format(startX,startY,endX,endY))
print('necessary time: {0}'.format(abs(startX-endX) + abs(endY-startY) + 1))
g1.drawPath(startX=startX,startY=startY,endX=endX,endY=endY)



print(g1.getGrid())
