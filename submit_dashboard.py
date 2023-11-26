import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
from sklearn.metrics import silhouette_score
import streamlit as st

def access_file(localdir, public_url=None):
  file_id_url = public_url.split('/')[-2]
  try:
    return pd.read_csv(localdir)
  except:
    return pd.read_csv('https://drive.google.com/uc?id=' + file_id_url)

df = access_file('clustered_customers.csv','https://drive.google.com/file/d/1e4HEj3s5mfNUiUp0M1Xgfzk65nTlm7uq/view?usp=sharing')

st.header('E-Commerce Dashboard')

st.subheader('All Time Report')
column01, column02 = st.columns(2)
with column01:
    st.metric("Revenue", value=np.round(df.total_spending.sum(),2))
with column02:
    st.metric("Orders", value=df.order_freq.sum())


column10, column11 = st.columns(2)
with column10:
    monetary = df.groupby('monetary_group').agg(total_customers=('monetary_group','count')).reset_index().iloc[[1,2,0],:]
    fig, ax = plt.subplots(figsize=(50, 40))
    sns.barplot(x='monetary_group', y='total_customers', data=monetary, palette='flare', ax=ax)
    ax.tick_params(labelsize=100, axis='x')
    ax.tick_params(labelsize=100, axis='y')
    ax.set_ylabel('Total Customer', fontsize=120, labelpad=20)
    ax.set_xlabel('Monetary Group', fontsize=120, labelpad=40)
    ax.set_title('Number of Customer By Monetary', fontsize=140, pad=40, fontweight='semibold')
    st.pyplot(fig)
with column11:
    recency = df.groupby('recency_group').agg(total_customers=('recency_group','count')).reset_index()
    fig, ax = plt.subplots(figsize=(50, 40))
    sns.barplot(x='recency_group', y='total_customers', data=recency, palette='flare', ax=ax)
    ax.tick_params(labelsize=100, axis='x')
    ax.tick_params(labelsize=100, axis='y')
    ax.set_ylabel('Total Customer', fontsize=120, labelpad=20)
    ax.set_xlabel('Recency Group (3 Months)', fontsize=120, labelpad=40)
    ax.set_title('Number of Customer By Recency', fontsize=140, pad=40, fontweight='semibold')
    st.pyplot(fig)


fig, ax = plt.subplots(figsize=(50, 20))
sns.kdeplot(x='recency',data=df, linewidth=4, fill=True, hue='cluster', ax=ax, palette='flare')
ax.tick_params(labelsize=100, axis='x')
ax.tick_params(labelsize=100, axis='y')
ax.set_xlabel('Recency', fontsize=120, labelpad=40)
ax.set_title('Recency Distribution by Cluster', fontsize=140, pad=40, fontweight='semibold')
st.pyplot(fig)

column20, column21 = st.columns(2)
with column20:
    cluster_recency = df.groupby('cluster').agg(Min=('recency','min'), Max=('recency','max'), Median=('recency','median')).reset_index()
    st.dataframe(cluster_recency, hide_index=True)
with column21:
    cluster = df.groupby('cluster').agg(total_customers=('cluster','count')).reset_index()
    fig, ax = plt.subplots(figsize=(50, 40))
    sns.barplot(x='cluster', y='total_customers', data=cluster, palette='flare', ax=ax)
    ax.tick_params(labelsize=100, axis='x')
    ax.tick_params(labelsize=100, axis='y')
    ax.set_ylabel('Total Customer', fontsize=120, labelpad=20)
    ax.set_xlabel('Cluster', fontsize=120, labelpad=40)
    ax.set_title('Number of Customer By Cluster', fontsize=140, pad=40, fontweight='semibold')
    st.pyplot(fig)

# with column12:
#     fig, ax = plt.subplots(figsize=(50, 40))
#     sns.kdeplot(x='recency',data=df, linewidth=2, fill=True, hue='cluster', ax=ax, palette='flare')
#     st.pyplot(fig)

fig = px.scatter_3d(df, x='recency', y='order_freq', z='total_spending',color='cluster',
             color_discrete_sequence=px.colors.qualitative.G10, size_max=30, opacity=0.7)
st.plotly_chart(fig, use_container_width=True)