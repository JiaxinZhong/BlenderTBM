"""
Common color palettes for scientific visualization.
Includes:
- BrewerPastel1: Soft, distinct colors.
- NPG: Nature Publishing Group classic colors.
- OkabeIto: Colorblind-safe palette.
"""

# BrewerPastel1 (Source: ColorBrewer 9-class Pastel1)
# Order: Red, Blue, Green, Purple, Orange, Yellow, Brown, Pink, Gray
BrewerPastel1 = [
    (251/255, 180/255, 174/255, 1),            # 0. Pale Red
    (179/255, 205/255, 227/255, 1),            # 1. Pale Blue
    (204/255, 235/255, 197/255, 1),            # 2. Pale Green
    (222/255, 203/255, 228/255, 1),            # 3. Pale Purple
    (254/255, 217/255, 166/255, 1),            # 4. Pale Orange
    (255/255, 255/255, 204/255, 1),            # 5. Pale Yellow
    (229/255, 216/255, 189/255, 1),            # 6. Pale Brown
    (253/255, 218/255, 236/255, 1),            # 7. Pale Pink
    (242/255, 242/255, 242/255, 1),            # 8. Pale Gray
]

# Nature Publishing Group (NPG) Classic Colors
# Order: Red, Blue, Green, Dark Blue, Light Red, Grey Blue, Teal, Dark Red, Brown, Beige
NPG = [
    (230/255, 75/255, 53/255, 1),             # 0. Vermilion (Red) - Emphasis
    (77/255, 187/255, 213/255, 1),            # 1. Lake Blue (Blue) - Emphasis
    (0/255, 160/255, 135/255, 1),             # 2. Emerald Green (Green)
    (60/255, 84/255, 136/255, 1),             # 3. Dark Blue
    (243/255, 155/255, 127/255, 1),           # 4. Light Salmon (Light Red)
    (132/255, 145/255, 180/255, 1),           # 5. Grey Blue
    (145/255, 209/255, 194/255, 1),           # 6. Teal
    (220/255, 0/255, 0/255, 1),               # 7. Dark Red
    (126/255, 97/255, 72/255, 1),             # 8. Brown
    (176/255, 156/255, 133/255, 1)            # 9. Beige
]

# Okabe-Ito Colorblind-Safe Palette
# Order: Orange, Sky Blue, Bluish Green, Yellow, Blue, Vermilion, Reddish Purple, Black
OkabeIto = [
    (230/255, 159/255, 0/255, 1),             # 0. Orange
    (86/255, 180/255, 233/255, 1),            # 1. Sky Blue
    (0/255, 158/255, 115/255, 1),             # 2. Bluish Green
    (240/255, 228/255, 66/255, 1),            # 3. Yellow
    (0/255, 114/255, 178/255, 1),             # 4. Blue
    (213/255, 94/255, 0/255, 1),              # 5. Vermilion
    (204/255, 121/255, 167/255, 1),           # 6. Reddish Purple
    (0/255, 0/255, 0/255, 1)                  # 7. Black
]

# Common Colors
White = (1, 1, 1, 1)
Black = (0, 0, 0, 1)
Silver = (0.8, 0.8, 0.8, 1)
Grey = (0.5, 0.5, 0.5, 1)

# Axis Colors (High saturation for visibility)
# Standard RGB mapping: X=Red, Y=Green, Z=Blue
AxisRed   = (0.8, 0.05, 0.05, 1)
AxisGreen = (0.05, 0.6, 0.05, 1)
AxisBlue  = (0.05, 0.05, 0.8, 1)