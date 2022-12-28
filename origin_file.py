import os
import originpro as op
import glob
import pandas as pd

class OriginPy:
    def __init__(self):
        '''
        오리진 그리기 파이썬
        '''
      

    def draw_graph(self,x_vals,y_vals,file_name,path)-> None:
        ''''''

        op.set_show()

        

        wks = op.new_sheet('w')

        wks.from_list(0, x_vals, 'Degree','°','controller_X')
        wks.from_list(1, y_vals, 'Power','W',f'{file_name}')

        gp = op.new_graph(template='polar')
        gl = gp[0]
        plot = gl.add_plot(wks, 1, 0,type='l')
        plot.set_cmd('-c 2', '-w 1000')
        gl.rescale()
        gl.set_ylim(0)


        fpath = path
        gp.save_fig(fpath)
        print(f'{gl} is exported as {fpath}')

        op.exit()

if __name__ == "__main__":
    opy = OriginPy()
    abspath_path = os.path.dirname(os.path.abspath(__file__))
    data_path = 'data'
    img_path = 'img'

    file_list = os.listdir(data_path)

    for i in range(len(file_list)):
        file_path = file_list[i]
        file_name = os.path.splitext(file_path)[0]
        data = pd.read_csv(f'{data_path}\{file_path}')
        # print(data)

        dirListing = os.listdir(img_path)
        result_len = len(dirListing)

        result_file_path = f'{abspath_path}\{img_path}\{file_name}.png'
    

        opy.draw_graph(data['Theta'],data['Power'],f'Slit_V_{str(result_len+1).zfill(2)}',result_file_path)