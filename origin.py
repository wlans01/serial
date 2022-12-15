import os
import originpro as op
import pandas as pd

class OriginPy:
    def __init__(self):
        '''
        오리진 그리기 파이썬
        '''
      

    def draw_graph(self,x_vals,y_vals,file_name)-> None:
        ''''''

        op.set_show()

        

        wks = op.new_sheet('w')

        wks.from_list(0, x_vals, 'Degree','°','controller_X')
        wks.from_list(1, y_vals, 'Power','W','controller_Y')

        gp = op.new_graph(template='polar')
        gl = gp[0]
        plot = gl.add_plot(wks, 1, 0,type='l')
        plot.set_cmd('-c 2', '-w 1000')
        gl.rescale()
        gl.set_ylim(0)


        fpath = file_name +'.png'
        gp.save_fig(fpath)
        print(f'{gl} is exported as {fpath}')

        op.exit()

if __name__ == "__main__":
    op = OriginPy()
    xL = [1,2,3,4,5,6,7,8,9,10]
    yL = [23,45,78,133,178,199,234,278,341,400]

    op.draw_graph(xL,yL,file_name='')