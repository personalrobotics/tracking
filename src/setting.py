
def init():
    global RESCALE, N_, M_, x0_, y0_, dx_, dy_, fps_
    RESCALE = 2

    """
    N_, M_: the row and column of the marker array
    x0_, y0_: the coordinate of upper-left marker (in original size)
    dx_, dy_: the horizontal and vertical interval between adjacent markers (in original size)
    fps_: the desired frame per second, the algorithm will find the optimal solution in 1/fps seconds
    """
    ## Settings for gelsight finger 1
    '''
    N_ = 8
    M_ = 14
    fps_ = 30
    x0_ = 50
    y0_ = 200
    dx_ = 25
    dy_ = 24
    '''

    ## Settings for gelsight finger 2

    N_ = 8
    M_ = 14
    fps_ = 30
    x0_ = 60
    y0_ = 100
    dx_ = 30
    dy_ = 24

    #x0_ = 100 / RESCALE
    #y0_ = 100/ RESCALE
    #dx_ = 60 / RESCALE
    #dy_ = 60 / RESCALE