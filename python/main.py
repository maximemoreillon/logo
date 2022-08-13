import drawSvg as draw
import math
import os



def polarToCartesian(Cx, Cy, r, theta):
    return {
        'x': Cx + r * math.cos(math.radians(theta)),
        'y': Cy + r * math.sin(math.radians(theta)),
    }

def quadraticFormula(a,b,c): 
      return (-b - math.sqrt(math.pow(b, 2) - (4 * a * c))) / (2 * a)



def generateLogoPartPath(x, y, radius, thickness, startAngle, color='purple'):
    innerRadius = radius - thickness

    endAngle = startAngle - 120

    startDX = quadraticFormula(2, 2 * (thickness - innerRadius), math.pow(thickness, 2) )
    endDx = quadraticFormula(2, -2 * (thickness + radius), math.pow(thickness, 2) )

    alpha = math.degrees(math.asin((thickness + startDX) / innerRadius))
    gamma = math.degrees(math.asin((thickness - endDx) / radius))

    path = draw.Path(stroke='transparent', stroke_width=1, fill=color)


    innerStart = polarToCartesian(x, y, innerRadius, endAngle)
    innerEnd = polarToCartesian(x, y, innerRadius, startAngle - alpha)
    outerStart = polarToCartesian(x, y, radius, endAngle + gamma)
    outerEnd = polarToCartesian(x, y, radius, startAngle)


    path\
    .M(innerStart['x'], innerStart['y'])\
    .A(innerRadius, innerRadius, 0, 0, 0, innerEnd['x'], innerEnd['y'])\
    .L(outerEnd['x'], outerEnd['y'])\
    .A(radius, radius, 0, 0, 1, outerStart['x'], outerStart['y'])\
    .L(innerStart['x'], innerStart['y'])

    return path




def generateLogo(height=800, width=600, color='#c00000', backgroundColor="transparent"):


    radius = min(height, width) / 3
    thickness = 0.166667 * radius
    x = 0.5 * width
    y = 0.5 * height

    #drawing = draw.Drawing(width, height, origin="center")
    drawing = draw.Drawing(width, height)

    background = draw.Rectangle(0,0,width, height, fill=backgroundColor)
    drawing.append(background)

    for part in range(3):
        angle = 90 + part * 120
        path = generateLogoPartPath(x=x,y=y ,radius=radius,thickness=thickness,startAngle=angle, color=color)
        drawing.append(path)
    
    output_dir = f'{os.path.dirname(os.path.realpath(__file__))}/output'
    filename = f'{width}x{height}_{color}_on_{backgroundColor}'

    # drawing.setPixelScale(2)  # Set number of pixels per geometry unit
    #d.setRenderSize(400,200)  # Alternative to setPixelScale
    drawing.saveSvg(f'{output_dir}/{filename}.svg')
    drawing.savePng(f'{output_dir}/{filename}.png')



if __name__ == '__main__':
    WIDTH = 800
    HEIGHT = 600
    COLOR = '#c00000'
    BACKGROUND_COLOR = 'black'

    generateLogo(width=WIDTH, height=HEIGHT, color=COLOR, backgroundColor=BACKGROUND_COLOR)


