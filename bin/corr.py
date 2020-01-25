import numpy as np


# COV(X, Y) =  E[(X - E[X])(Y-E[X])]

# r = sum()


# def mean(x): return sum(x) / len(x)
# def coff(x, y): 
# 	mx = mean(x)
# 	my = mean(y)

# 	vx = mean( )
# 	xx = map(lambda x: x - mx)
# 	yy = map(lambda x: x - my)
# 	numerator = sum(map(lambda xy: xy[0] * xy[1], zip(xx, yy))


if __name__ == "__main__":
	main()


 x1 = 15,12,8,8,7,7,7,6,5,3
 x2 = 10,25,17,11,13,17,20,13,9,15
	


print(np.corrcoeff(x1, x2))



