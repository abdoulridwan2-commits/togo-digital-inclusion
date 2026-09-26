import sys
try:
    import pptx
    print("PPTX_OK")
except Exception as e:
    print("PPTX_ERR:", e)
