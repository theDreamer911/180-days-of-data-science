# IMPORT MODULE

from PIL import Image
from numpy import sqrt
import streamlit as st
import altair as alt
import pandas as pd

# PAGE TITLE

image = Image.open('dna.png')

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app count nucleotide composition of DNA
""")

# INPUT TEXT BOX

st.header("Enter DNA Sequence")

sequence_input = ">DNA Query\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence Input", sequence_input, height=225)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = '\n'.join(sequence)

st.write("""
***
""")

# PRINT OUT THE DNA SEQUENCE
st.header("INPUT (DNA QUERY)")
sequence

# DNA NUCLEOTIDE COUNT
st.header("OUTPUT (DNA NUCLEOTIDE COUNT)")

# 1. Print Dictionary
st.subheader("1. Print Dictionary")


def DNA_nucleotide_count(seq):
    d = dict([
        ('A', seq.count("A")),
        ('T', seq.count("T")),
        ('G', seq.count("G")),
        ('C', seq.count("C")),
    ])
    return d


X = DNA_nucleotide_count(sequence)

X

# 2. Print Text
st.subheader('2. Print Text')
st.write(f"There are {str(X['A'])} adenine (A)")
st.write(f"There are {str(X['T'])} thymine (T)")
st.write(f"There are {str(X['G'])} guanine (G)")
st.write(f"There are {str(X['C'])} cytosine (C)")

# 3. Display DataFrame
st.subheader("3. Display DataFrame")
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
st.write(df)

# 4. Display Bar Chart Using ALtair
st.subheader('4. Display Bar Chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)

p = p.properties(
    width=alt.Step(80)
)

st.write(p)
