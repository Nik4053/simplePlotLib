import plotly.graph_objects as go
import pandas as pd
import numpy as np

def __callFunction(func,args,x):
    import collections.abc
    if isinstance(x, dict):
        return func(*args,**x)
    elif isinstance(x, collections.Sequence):
        return func(*args,*x)
    else:
        return func(*args,x)

def __parseInputData(x = None, y = None,z=None, data= None, points = None,):
    retData = {}
    if x is not None and y is not None  and data is None and points is None:
        retData["x"] = x
        retData["y"] = y
        if z is not None:
            retData["z"] = z
        return retData
    elif x is not None and y is None and z is None and data is None and points is None:
        if not isinstance(x,dict) and not isinstance(x[0], (collections.Sequence, np.ndarray)):
            retData["x"] = x
            return retData
        data = x
        x = None
    
    if data is not None and x is None and y is None and z is None and points is None:
        if isinstance(data, dict):
            return data
        for i in range(len(data)):
            retData[f"x{i}"] = data[i]
        return retData
    elif points is not None and x is None and y is None and z is None and data is None:
        for i in range(len(points[0])):
            retData[f"x{i}"] = [t[i] for t in points]
        return retData
    
    import warnings
    warnings.warn("could not parse input data")

def function_2d(func, fig = None, name= "",color="royalblue", lineWidth= 4, lineType = None,dash = None, startX= 0,endX= 2, numX= 200,nameX = None, nameY = None,title="",fontSize=15, params= ()):
    import numpy as np
    import plotly.graph_objects as go
    import plotly.offline as pyo
    import warnings
    import plotly.express as px
    if(startX > endX):
        warnings.warn("startX smaller or equal to endX")
    if(numX<=0):
        warnings.warn("numX is zero or negative")
    x = np.linspace(startX, endX, numX)
    y = np.empty(numX)

    for xi in range(numX):
            y[xi] = __callFunction(func,[x[xi]],params)
            
    return function_2d_data(x=x,y=y,fig=fig,name=name,color=color,lineWidth=lineWidth,lineType=lineType,dash=dash,nameX=nameX,nameY=nameY,title=title,fontSize=fontSize)
    
def function_2d_data(x = None, y = None, data= None, points = None, fig = None, name= "",color="royalblue", lineWidth= 4, lineType = None,dash = None,nameX = None, nameY = None,title="",fontSize=15):
    import numpy as np
    import plotly.graph_objects as go
    import plotly.offline as pyo
    import warnings
    import plotly.express as px
    inData = __parseInputData(x,y,None,data,points)
    if inData is None: 
        return
    key = list(inData.keys())[0]
    x = inData[key]
    if nameX is None:
        nameX = key
    key = list(inData.keys())[1]
    y= inData[key]
    if nameY is None:
        nameY = key
    if len(inData.keys()) > 2:
        warnings.warn(f"Data dimensionality of {len(inData.keys())} is too high. Will only show first 2 dimensions")
    if fig is None:
        fig =go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name=name,
                         line=dict(color=color, width=lineWidth, dash=dash))) # dash options include None, 'dash', 'dot', and 'dashdot'
    fig.update_layout( xaxis = dict(titlefont = dict(size = fontSize), tickfont = dict(size = fontSize)),
          yaxis = dict(titlefont = dict(size = fontSize), tickfont = dict(size = fontSize)) )
    fig.update_layout(title=title,
                   xaxis_title=nameX,
                   yaxis_title=nameY)

    return fig

# showscale disables the scale. usefull for multiplots
# surfacecolor uses a function reference with 3 inputs (x,y,z)
def function_3d(func, fig = None, showColorbar = None, showContours = False, colorbarPos= 1, surfacecolor = None,opacity=1, name= None, startX= 0,endX= 2, numX= 200, startY= 0,endY= 2, numY= 200, title="", params= ()):
    import numpy as np
    import plotly.graph_objects as go
    import warnings
    
    if(startX > endX):
        warnings.warn("startX smaller or equal to endX")
    if(numX<=0):
        warnings.warn("numX is zero or negative")
    
    if(startY > endY):
        warnings.warn("startX smaller or equal to endX")
    if(numY<=0):
        warnings.warn("numX is zero or negative")
        
    x, y = np.linspace(startX, endX, numX), np.linspace(startY, endY, numY)
    z = np.empty([numY, numX])

    for xi in range(numX):
        for yi in range(numY):
            z[yi][xi] = __callFunction(func,[x[xi],y[yi]],params)
    
    return function_3d_data(x=x,y=y,z=z,fig=fig,showColorbar=showColorbar,showContours=showContours,colorbarPos=colorbarPos,surfacecolor=surfacecolor,opacity=opacity,name=name,title=title)

# showscale disables the scale. usefull for multiplots
# surfacecolor uses a function reference with 3 inputs (x,y,z)
def function_3d_data(x= None,y=None,z=None,data=None,points=None, fig = None, showColorbar = None, showContours = False, colorbarPos= 1, surfacecolor = None,opacity=1, name= None, title=""):
    import numpy as np
    import plotly.graph_objects as go
    import warnings
    
    inData = __parseInputData(x,y,z,data,points)
    if inData is None: 
        return
    key = list(inData.keys())[0]
    x = inData[key]
    key = list(inData.keys())[1]
    y= inData[key]
    key = list(inData.keys())[2]
    z= inData[key]
    if len(inData.keys()) > 3:
        warnings.warn(f"Data dimensionality of {len(inData.keys())} is too high. Will only show first 3 dimensions")
    
    
    if fig is None:
        fig =go.Figure()
    elif showColorbar == None:
        print("INFO: Multiple colorbar may overwrite each other. Disable them or change their positions.")
        
    args = {}
    if(surfacecolor is not None):
        args["surfacecolor"] = surfacecolor(x,y,z)
    if name is not None:
        args["name"] = name
    fig.add_trace(go.Surface(z=z, x=x, y=y, showscale = showColorbar,colorbar_x=colorbarPos,opacity=0.9,**args))
    if showContours == True:
        fig.update_traces(contours_z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project_z=True))
        
    fig.update_layout(title=title)
    
    return fig

def bar(data):
    import plotly.express as px
    fig = px.bar(data)
    return fig

def hist(data, bins=10, spacing= True ,axis = "on"):
    import matplotlib.pyplot as plt
    if spacing:
        import seaborn as sns
        sns.set(rc={'figure.figsize':(11.7,8.27)})
    fig, axs = plt.subplots(1, 1, sharey=True)   
    # We can set the number of bins with the `bins` kwarg   
    plt.axis(axis)
    axs.hist(data, bins=bins)
    if spacing:
        sns.reset_defaults()
def hist2(data,bins=10):
    import plotly.express as px
    # Here we use a column with categorical data
    fig = px.histogram(data,nbins=bins)
    fig.show()

def scatter_2d(component1, component2, label= None, colorscale = 'Rainbow',showscale = True, width= 800,height=800,template = 'plotly_dark'):
    import plotly.graph_objects as go
    fig = go.Figure(data=go.Scatter(
        x = component1,
        y = component2,
        mode='markers',
        marker=dict(
            size=10,
            color=label, #set color equal to a variable
            colorscale=colorscale, # one of plotly colorscales
            showscale=showscale,
            line_width=1,
        )
    ))
    layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1))
    fig.update_layout(margin=dict( l=100,r=100,b=100,t=100),width=width,height=height,yaxis=dict(scaleanchor="x", scaleratio=1))                 
    fig.layout.template = template
    
    return fig

def scatter_3d(component1,component2,component3,label=None, colorscale = 'Rainbow',showscale = True, width= 900,height=600,template = 'plotly_dark'):
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Scatter3d(
        x=component1,
        y=component2,
        z=component3,
        mode='markers',
        marker=dict(
            size=10,
            color=label,                # set color to an array/list of desired values
            colorscale=colorscale,   # choose a colorscale
            showscale=showscale,
            opacity=1,
            line_width=1
        )
    )])
    # tight layout
    fig.update_layout(margin=dict(l=50,r=50,b=50,t=50),width=width,height=height)
    fig.layout.template = template
    return fig