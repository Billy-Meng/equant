import talib


def initialize(context): 
    SetBarInterval('SHFE|F|CU|1907', 'M', 1, 100)


def handle_data(context):

    #PlotVertLine(main=True, axis = True)
    #PlotDot(name="Dot", value=Close()[-1], main=True)
    #PlotBar("BarExample1", Vol()[-1], 0, RGB_Red())
    #PlotStickLine("StickLine", Close()[-1], Open()[-1], RGB_Blue(), True, True, 0)
    '''
    idx1 = CurrentBar()
    p1 = Close()[-1]
    if idx1 >= 100:
        idx2 = 1
        p2 = Close()[-2]
        PlotPartLine("PartLine", idx1, p1, idx2, p2, RGB_Red(), True, True, 1)
    '''
    PlotIcon(value=Close()[-1])



    





































