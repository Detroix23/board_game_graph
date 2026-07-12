"""
# Board game graphing: Tic-Tac-Toe.
/src/utilities/graphics.py
"""

def hsv(hue: float, saturation: float, value: float) -> str:
    """
    Format a `hsv` color to `str` for `graphviz`.
    """
    return f"{hue:.3f} {saturation:.3f} {value:.3f}"

def hsv_to_rgb255(
    hue: float, 
    saturation: float, 
    value: float,  
) -> tuple[int, int, int]:
    """
    Convert HSV to RGB.

    Parameters:
        `hue`: `float`: [0; 1]
        `saturation`: `float`: [0; 1]
        `value`: `float`: [0; 1]

    Returns:
        `tuple[int, int, int]`: R, G, B in [0; 255]
    """
    if saturation:
        if hue == 1.0: 
            hue = 0.0
        i: int = int(hue * 6.0) 
        f: float = hue * 6.0 - i
        
        w: int = int(255 * ( value * (1.0 - saturation) ))
        q: int = int(255 * ( value * (1.0 - saturation * f) ))
        t: int = int(255 * ( value * (1.0 - saturation * (1.0 - f)) ))
        value = int(255 * value)
        
        if i==0: 
            return (value, t, w)
        if i==1: 
            return (q, value, w)
        if i==2: 
            return (w, value, t)
        if i==3: 
            return (w, q, value)
        if i==4: 
            return (t, w, value)
        else:
            return (value, w, q)
    else: 
        value = int(255 * value)
        return (value, value, value)

def hsv_to_rgb_hex(    
    hue: float, 
    saturation: float, 
    value: float,  
) -> str:
    return "".join([
        hex(component)[2:].zfill(2) 
        for component in hsv_to_rgb255(hue, saturation, value)
    ])
