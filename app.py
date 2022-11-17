import streamlit as st
import itertools
import json

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

st.set_page_config(
    page_title="FSL Choropleth Helper", page_icon="📊"
)

st.title('FSL Choropleth Helper')

dataset_id = st.text_input('Dataset ID')
fieldname = st.text_input('Fieldname')
colors_str = st.text_input('Colors (array). Example: []')
quantiles_str = st.text_input('Quantiles(array)')

if dataset_id and fieldname and colors_str and quantiles_str:
    quantiles = json.loads(quantiles_str)
    colors = json.loads(colors_str)

    if len(quantiles) != len(colors) + 1:
        raise ValueError(f"Length of colors ({len(colors)}) and quantiles ({len(quantiles)-1}) don't match")

    vizs = []
    for color, (min_val, max_val) in zip(colors, pairwise(quantiles)):
        vizs.append({
          "config": {},
          "dataset": dataset_id,
          "legend": {"displayName": f"{min_val} - {max_val}"},
          "style": {
            "color": color,  
            "filter": f"${fieldname} >= {min_val} && ${fieldname} < {max_val}",
            "isSandwiched": False
          },
          "type": "simple"
        })

    st.code(json.dumps(vizs, indent=2))
