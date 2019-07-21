import matplotlib.pyplot as plt
import numpy as np

def mae_mfe(orders, x_y_line=True, return_fig_ax=False):
    '''
    parameters:
        orders: list, 所有交易的mae和mfe資料，資料必須放在dict裡面
            資料格式:
            {
                'mae': float,
                'mfe': float,
                ...
                (可以包含其他資料)
            }
        
        x_y_line: bool (預設為True), 是否繪製x=y的虛線
        return_fig_ax: bool (預設為False), 是否回傳matplotlib的繪圖元件

    return:
        (optional)
        fig, ax: matplotlib的基本繪圖元件，來自plt.subplots()
    '''
    fig, ax = plt.subplots()

    mae = []
    mfe = []
    for order in orders:
        mae.append(abs(order['mae']))
        mfe.append(order['mfe'])
    ax.plot(mae, mfe, '+', color='blue')

    if x_y_line:
        x_y_line_x = np.linspace(0, max(max(mae),max(mfe)), 100)
        x_y_line_y = 1 * x_y_line_x + 0
        ax.plot(x_y_line_x, x_y_line_y, '--', color='black', linewidth=0.1)

    if return_fig_ax:
        return fig, ax
    else:
        plt.show()