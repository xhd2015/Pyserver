#!/bin/python3

def generate_html(s):
    html=s.hf.format_html(body='<pre>'+s.helpinfo+'</pre>')
    return ['',html]