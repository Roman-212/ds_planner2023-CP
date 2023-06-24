import streamlit as st
import pandas as pd
from components.sidebar import sidebar
import plotly.express as px
import plotly.graph_objects as go


name = pd.read_excel ('data/names.xlsx',index_col='Кодзадачи')

def get_plot_data(selected_object,dataset):
    dataset = dataset[dataset['obj_key'] == selected_object]
    data_for_plot = dataset[dataset['Кодзадачи'].isin(name.index)]
    data_for_plot['Кодзадачи'] = data_for_plot['Кодзадачи'].replace(name['НазваниеЗадачи'])
    return data_for_plot

def get_plot(data_for_plot):
    fig = px.timeline(data_for_plot, x_start="ДатаНачалаЗадачи", x_end="ДатаОкончанияЗадачи", y="Кодзадачи", height=600)
    fig.update_yaxes(autorange="reversed") 
    return fig

def upload_file(file):
    dataset = None
    if file is not None:
        try:
            dataset = pd.read_excel(file,parse_dates=True)
            dataset = dataset.fillna(0)
            dataset['ДатаНачалаЗадачи'] = pd.to_datetime(dataset['ДатаНачалаЗадачи'])
            dataset['ДатаОкончанияЗадачи'] = pd.to_datetime(dataset['ДатаОкончанияЗадачи'])
            dataset['ДатаначалаБП0'] = pd.to_datetime(dataset['ДатаначалаБП0'])
            dataset['ДатаокончанияБП0'] = pd.to_datetime(dataset['ДатаокончанияБП0'])
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {e}")
    else:
        dataset = pd.read_csv('data/dataset_hackaton_ksg__v2__23062023__1710_GMT3.csv', sep=';', parse_dates=True, low_memory=False)
        dataset['ДатаНачалаЗадачи'] = pd.to_datetime(dataset['ДатаНачалаЗадачи'])
        dataset['ДатаОкончанияЗадачи'] = pd.to_datetime(dataset['ДатаОкончанияЗадачи'])
        dataset['ДатаначалаБП0'] = pd.to_datetime(dataset['ДатаначалаБП0'])
        dataset['ДатаокончанияБП0'] = pd.to_datetime(dataset['ДатаокончанияБП0'])
    return dataset

# dataset = pd.read_csv('data/dataset_hackaton_ksg__v2__23062023__1710_GMT3.csv',sep=';',parse_dates=True,low_memory=False)
# dataset = pd.read_csv('data/dataset_hackaton_ksg__v2__23062023__1710_GMT3.csv',sep=';',parse_dates=True,low_memory=False)
# dataset['ДатаНачалаЗадачи'] = pd.to_datetime(dataset['ДатаНачалаЗадачи'])
# dataset['ДатаОкончанияЗадачи'] = pd.to_datetime(dataset['ДатаОкончанияЗадачи'])
# dataset['ДатаначалаБП0'] = pd.to_datetime(dataset['ДатаначалаБП0'])
# dataset['ДатаокончанияБП0'] = pd.to_datetime(dataset['ДатаокончанияБП0'])
# #attr = pd.read_csv('data/data_mgz_attributes.csv')
# #dataforplot = get_plot_data(selected_object,dataset)
# # gantt = get_plot(dataforplot)





def main():
    st.set_page_config(page_title="ds_planner", page_icon="🏗️", layout="wide")
    st.header("🏗️ Анализ сроков строительства")
    sidebar()
    dataset = upload_file(st.file_uploader("Выберите файл .xlsx", type="xlsx"))
    dataset1 = dataset
    selected_object = st.selectbox('выберите номер объекта', dataset1['obj_key'].unique(), index=0)
    dataforplot = get_plot_data(selected_object,dataset1)
    gantt = get_plot(dataforplot)
    #dataset_for_table = dataset[dataset['obj_key'] == selected_object]
    dataset_for_table = get_plot_data(selected_object,dataset1)
   
    selected_columns = ['Кодзадачи','ДатаНачалаЗадачи','ДатаОкончанияЗадачи']
    edited_dataset = st.data_editor(dataset_for_table)
    st.plotly_chart(gantt, use_container_width=True)
   # st.plotly_char()
    
    edited_plot = get_plot(get_plot_data(selected_object,edited_dataset))
    edited_plot = edited_plot.add_traces(gantt.data + edited_plot.data)
    edited_plot.update_traces(marker=dict(color='green'))
   # edited_plot = edited_plot.add_traces(edited_dataset)
    st.plotly_chart(edited_plot, use_container_width=True)
    #go.Figure(data=fig1.data + fig2.data)



if __name__ == "__main__":
    main()