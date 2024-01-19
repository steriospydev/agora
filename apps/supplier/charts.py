import base64
from io import BytesIO
from typing import List, Tuple, Dict

import seaborn as sns
import matplotlib.pyplot as plt

def construct_image(x_label:str, y_label:str, title:str, 
                    x_data:List[str],
                    y_data:List[str]) -> str:

    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid", {"grid.color": ".2", "grid.linestyle": ":"})  
    palette = sns.color_palette("coolwarm", len(x_data))  # Generate the "coolwarm" palette
    ax = sns.barplot(x=x_data, y=y_data, palette=palette)  

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    legend_label = ['{:.2f}: {}'.format(x,y) for x, y in zip(x_data, y_data)]
    custom_legend = [plt.Line2D([0], [0], color=palette[i], lw=4, label=legend_label[i]) for i in range(len(x_data))]
    ax.legend(handles=custom_legend, title='Legend', loc='upper right')


    buffer = BytesIO()
    plt.savefig(buffer, format='png')

    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def construct_supplier_charts(orders: List[Dict]) -> Tuple[str, str]:     
    names = [p['product__product_name'] for p in orders]
    quantity = [p['total_quantity'] for p in orders]   
    amount = [p['total_amount'] for p in orders]
    
    quantity_chart = construct_image(x_label='Ποσότητα (KG)',
                            y_label='Προιόντα',
                            title='Ποσότητα ανά Προιόν Προμηθευτή',
                            x_data=quantity,
                            y_data=names)
    amount_chart = construct_image(x_label='Κόστος €',
                            y_label='Προιόντα',
                            title='Κόστος ανά Προιόν Προμηθευτή',
                            x_data=amount,
                            y_data=names)
        
    return (quantity_chart, amount_chart)
