from flask import Flask
import ghhops_server as hs
import rhino3dm
import myml



app = Flask(__name__)
hops = hs.Hops(app)

@hops.component(
    "/addition",
    name = 'samplecomponent',
    description = 'this is a sample component',
    inputs = [
        hs.HopsInteger('Input X', 'X10', 'Input X of sample'),
        hs.HopsInteger('Input Y', 'Y2', 'Input Y of sample'),  
    ],
    outputs = [
        hs.HopsInteger('Output S', 'S3', 'Output R of sample'),
    ]
)

@hops.component(
    "/multiplication",
    name = 'samplecomponent',
    description = 'this is a sample component',
    inputs = [
        hs.HopsInteger('Input X', 'X10', 'Input X of sample'),
        hs.HopsInteger('Input Y', 'Y2', 'Input Y of sample'),  
    ],
    outputs = [
        hs.HopsInteger('Output S', 'S3', 'Output R of sample'),
        hs.HopsInteger('Output M', 'M4', 'Output R of sample'),
    ]
)


#def samplefunction(X, Y):
#    add = X + Y
#    mult = X * Y
#
#    return add, mult


def addition(x, y):
    addi = myml.addition(x,y)
    return addi


add = addition(10,20)
print(add)


if __name__ == "__main__":
    app.run(debug=True)
