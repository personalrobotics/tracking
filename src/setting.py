
def init(gs_finger, rescale):
    global RESCALE, N_, M_, x0_, y0_, dx_, dy_, fps_
    RESCALE = rescale

    """
    N_, M_: the row and column of the marker array
    x0_, y0_: the coordinate of upper-left marker (in original size)
    dx_, dy_: the horizontal and vertical interval between adjacent markers (in original size)
    fps_: the desired frame per second, the algorithm will find the optimal solution in 1/fps seconds
    """

    if (gs_finger == 1 and rescale == 2):
    ## Settings for gs finger 1 
        N_ = 8
        M_ = 14
        fps_ = 30
        x0_ = 76
        y0_ = 200
        dx_ = 31
        dy_ = 31
    ## Settings for gs finger 2
    elif (gs_finger == 2 and rescale == 2):
        N_ = 8
        M_ = 14
        fps_ = 30
        x0_ = 95
        y0_ = 150
        dx_ = 30
        dy_ = 30
    elif (gs_finger == 1 and rescale == 3):
    ## Settings for gs finger 1 
        N_ = 8
        M_ = 14
        fps_ = 30
        x0_ = 40
        y0_ = 33
        dx_ = 14
        dy_ = 15

    ## Settings for gs finger 2
    elif (gs_finger == 2 and rescale == 3):
        N_ = 8
        M_ = 14
        fps_ = 30
        x0_ = 48
        y0_ = 65
        dx_ = 14
        dy_ = 14
    else:
        raise ValueError()

