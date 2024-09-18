from enum import Enum
 
class ProblemType(Enum):
    FB = 1
    FC = 2

# id: problem name, fb or fc
id_name_map = {
    'DTLToString_ISO': ('DTLToString_ISO', ProblemType.FC),
    'ExtractStringFromCharArray': ('ExtractStringFromCharArray', ProblemType.FC),
    'FIFO': ('FIFO', ProblemType.FB),
    'FloatingAverage': ('FloatingAverage', ProblemType.FB),
    'Frequency': ('Frequency', ProblemType.FB),
    'GetBitStates': ('GetBitStates', ProblemType.FB),
    'Integration': ('Integration', ProblemType.FB),
    'LightsControl': ('LightsControl', ProblemType.FB),
    'MatrixAddition': ('MatrixAddition', ProblemType.FC),
    'RandomRange_DInt': ('RandomRange_DInt', ProblemType.FC),
    'SearchMinMax_DInt': ('SearchMinMax_DInt', ProblemType.FC),
    'ShellSort_DInt': ('ShellSort_DInt', ProblemType.FB),
    'StackMin': ('StackMin', ProblemType.FB),
    'StringToTaddr': ('StringToTaddr', ProblemType.FC),
    'TempCtrl': ('TempCtrl', ProblemType.FB),
}

names = [(k, v[0]) for k, v in id_name_map.items()]
# testorder = sorted(names, key=lambda x: x[1])
testorder = names
id_testorder_map = {name[0]: i for i, name in enumerate(testorder)}
print(id_testorder_map)
