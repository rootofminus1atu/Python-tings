"""import gradio as gr

gr.Interface.load("models/yangy50/garbage-classification").launch()"""
import ml_api

ml_api.query("images/bottle.jpg")
