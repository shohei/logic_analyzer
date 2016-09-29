import pandas as pd
import numpy as np

values = [0,
        16,
        48,
        4,
        20,
        52,
        12,
        28,
        60,
        1,
        17,
        49,
        5,
        21,
        53,
        13,
        29,
        61,
        3,
        19,
        51,
        7,
        23,
        55,
        15,
        31,
        63]

xyz = [[0	,0	,0 ],
        [0	,0	,1 ],
        [0	,0	,-1 ],
        [0	,1	,0 ],
        [0	,1	,1 ],
        [0	,1	,-1 ],
        [0	,-1	,0 ],
        [0	,-1	,1 ],
        [0	,-1	,-1 ],
        [1	,0	,0 ],
        [1	,0	,1 ],
        [1	,0	,-1 ],
        [1	,1	,0 ],
        [1	,1	,1 ],
        [1	,1	,-1 ],
        [1	,-1	,0 ],
        [1	,-1	,1 ],
        [1	,-1	,-1 ],
        [-1	,0	,0 ],
        [-1	,0	,1 ],
        [-1	,0	,-1 ],
        [-1	,1	,0 ],
        [-1	,1	,1 ],
        [-1	,1	,-1 ],
        [-1	,-1	,0 ],
        [-1	,-1	,1 ],
        [-1	,-1	,-1 ]]

decodemap = pd.DataFrame(xyz,index=values,columns = ["x","y","z"])
print(decodemap)

#example
print(decodemap.ix[63,"x"])