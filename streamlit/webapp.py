import time

import streamlit as st
from streamlit_sortables import sort_items
from streamlit_ace import st_ace

import pandas as pd

from modules import adder, multiplier

st.set_page_config(layout="wide")

dataset1 = {
    "key1": 1,
    "key2": 2,
    "key3": 3,
}
dataset2 = {
    "key1": 4,
    "key2": 3,
    "key3": 2,
}
dataset3 = {
    "key1": 6,
    "key2": 8,
    "key3": 10,
    "key4": 12,
}


if 'selected_datasets' not in st.session_state:
    st.session_state.selected_datasets = []
    st.session_state.selected_modules = []


datasets = [dataset1, dataset2, dataset3]
dataset_amount = len(datasets)
processed_datasets = []


def add_remove_dataset(dataset_index):
    cur_data = {f"Dataset {dataset_index+1}": datasets[dataset_index]}
    selected_datasets = st.session_state.selected_datasets

    if cur_data in selected_datasets:
        selected_datasets.remove(cur_data)
    else:
        selected_datasets.append(cur_data)

    st.session_state.selected_datasets = selected_datasets


def context_menu():
    st.write("This is the context menu.")


st.title("TAQO")

with st.spinner("Loading"):
    time.sleep(5)

with st.expander(label="Dataset Selection", expanded=True):
    columns = st.columns(dataset_amount)

    for index, column in enumerate(columns):
        cont = column.container()

        cont.subheader(f"Dataset {index + 1}")
        cont.checkbox(label="Use dataset", key=f"data{index}",
                      on_change=add_remove_dataset, args=(index,))
        cont.write(datasets[index])
        # if st.context_menu()

with st.expander(label="Module Selection", expanded=True):
    st.subheader("Adder")
    st.write("Adds 1 to all values")
    st.subheader("Multiplier")
    st.write("Multiplies all values by 2")
    st.subheader("Select:")
    original_items = [
        {'header': 'Available Modules', 'items': ['Adder', 'Multiplier']},
        {'header': 'Selected Modules', 'items': []}
    ]

    user_selection = sort_items(original_items, multi_containers=True)
    st.session_state.selected_modules = user_selection[1].get("items")

with st.expander(label="Results", expanded=True):

    processed_datasets = [pd.DataFrame.from_dict(dataset) for dataset in st.session_state.selected_datasets]
    modules = st.session_state.selected_modules

    for dataset in processed_datasets:
        for module in modules:
            match module:
                case "Adder":
                    dataset = adder.add(dataset)
                case "Multiplier":
                    dataset = multiplier.multiply(dataset)

    if len(processed_datasets) > 1:
        processed_datasets = pd.concat(processed_datasets, axis=1)
        st.line_chart(processed_datasets)
    elif len(processed_datasets) == 1:
        st.line_chart(processed_datasets[0])
    else:
        st.write("Select at least one dataset")
