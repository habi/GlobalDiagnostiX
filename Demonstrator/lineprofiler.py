def lineprofile(Image, debug=False):
    """
    Function to draw a line profile from a selection in the image.
    Comes in handy to look at the resolution phantom in x-ray images shot with
    the iAi electronics prototype in the x-ray lab.
    Based on http://stackoverflow.com/a/7880726/323100
    """
    import numpy
    import scipy.ndimage
    import matplotlib.pyplot as plt

    # Debug
    if not debug:
        Image = scipy.misc.lena()

    # Prepare image
    fig, axes = plt.subplots(nrows=2)
    plt.ion()
    axes[0].imshow(Image, cmap='gray')

    # Let the user select a line to plot the profile from
    pts = []
    while len(pts) < 2:
        pts = numpy.asarray(plt.ginput(2, timeout=-1))
        x0 = pts[1, 0]
        x1 = pts[0, 0]
        y0 = pts[1, 1]
        y1 = pts[0, 1]
        axes[0].plot((x0, x1), (y0, y1), 'ro-')
        axes[0].axis('image')
        plt.draw()

    # Interpolate a line between x0, y0 and x1, y1 with double the length of
    # the line
    length = 2 * int(np.hypot(x1 - x0, y1 - y0))
    x, y = numpy.linspace(x0, x1, length), numpy.linspace(y0, y1, length)

    # Extract the values along the line, using cubic interpolation
    lineprofile = scipy.ndimage.map_coordinates(numpy.transpose(lena),
                                                numpy.vstack((x, y)))
    profile = Image[x.astype(np.int), y.astype(np.int)]

    # Draw the line profile
    axes[1].plot(lineprofile)
    axes[1].plot(profile)
    plt.draw()
    plt.ioff()
    plt.show()
