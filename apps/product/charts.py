import base64
from io import BytesIO
from typing import List, Tuple, Dict
from django.db.models import Sum

import seaborn as sns
import matplotlib.pyplot as plt

def format_label(date, value):
    formatted_date = date.strftime('%Y-%m-%d')  # Format the date as dd/mm/yyyy
    formatted_value = '{:.2f}'.format(value)   # Format the value with two decimal places
    return f'({formatted_date}, {formatted_value})'


def construct_product_charts(data):
    data_summary = data.values('product__product_name').annotate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('amount'),
            total_taxes=Sum('taxes')
            )   
    data_chart = get_data_chart(['Ποσότητα(kg)', 'Κόστος(€)', 'Φόροι(€)'],
                                [data_summary[0]['total_quantity'], data_summary[0]['total_amount'], data_summary[0]['total_taxes']],
                                'Product Summary',)
    
    x_data_price_chart = data.values_list('created_at', flat=True)  
    y_data_price_chart = data.values_list('unit_price', flat=True)  

    price_chart = get_price_chart(x_data_price_chart, y_data_price_chart,
                                  'Price Chart',
                                  'Unit Price')

    return (data_chart, price_chart)


def get_data_chart(x_data, y_data, title):
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid", {"grid.color": "0", "grid.linestyle": ":"})
    
    ax = sns.barplot(x=x_data, y=y_data, palette="pastel")
    plt.title(title)
    legend_handles = []
    for i, label in enumerate(y_data):
        formatted_label = f'{label:.2f}' 
        legend_handles.append(plt.Line2D([0], [0], color=sns.color_palette("pastel")[i],
                                         lw=6, label=formatted_label))

    # Add the legend to the plot
    ax.legend(handles=legend_handles, title="Tιμές", loc="upper right")
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return image_base64

def get_price_chart(x_data, y_data, title, y_label):
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid", {"grid.color": ".5", "grid.linestyle": ":"})
    plt.scatter(x_data, y_data, marker="o")
 
    plt.title(title)
    plt.ylabel(y_label)
    plt.xticks([])
    for date, value in zip(x_data, y_data):
        label = format_label(date, value)
        plt.annotate(label, (date, value),
                     textcoords="offset points",
                     xytext=(0, 5),
                     ha='left')
    plt.ylim([0, 5])  
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return image_base64
    