import pandas as pd

def rescale(m):
    rg = ['BMI',
    'AGE_TX',
    'AVG_SYS',
    'AVG_DIAST',
    'KEVAL_SURGHX_sugicalhx_yes',
    'KSOCDON_EDU_AttendedCollege_TechnicalSchool',
    'KSOCDON_EDU_Bachelordegree',
    'KSOCDON_EDU_Grade_School',
    'KSOCDON_EDU_Graduatedegree',
    'KSOCDON_EDU_High_School',
    'KSOCDON_MARSTAT_Married',
    'KSOCDON_MARSTAT_Single',
    'KSOCDON_MARSTAT_Widowed',
    'KHL_TOBACCO_HX_Tobacco_former',
    'KHL_TOBACCO_HX_Tobacco_never',
    'KHL_COMO_CHRPAIN_chronicpain_never',
    'KHL_COMO_CHRPAIN_chronicpain_previous',
    'KHL_COMO_PSYCH_psychiatricdiff_yes',
    'KHL_COMO_UTI_UTI_yes',
    'KHL_KDIS_kiddisrela_yesSTDEG_kiddisrela_yes',
    'KHL_HD_heartdrela_yesSTDEG_heartdrela_yes',
    'KHL_HYPTENS_hypertrela_yesSTDEG_hypertrela_yes']


    std_factor = pd.DataFrame(columns=rg) # make two new scaling DF
    mean_factor = pd.DataFrame(columns=rg)

    # fill all of the columns with either zero or one
    std_factor.loc[1] = 1
    mean_factor.loc[1] = 0

    # add in the scaling factors
    std_factor['AGE_TX'].loc[1] = 11.416749
    std_factor['BMI'].loc[1] = 4.638226
    std_factor['AVG_SYS'].loc[1] = 2.117913
    std_factor['AVG_DIAST'].loc[1] = 8.037357

    mean_factor['AGE_TX'].loc[1] = 40.418706
    mean_factor['BMI'].loc[1] = 26.205583
    mean_factor['AVG_SYS'].loc[1] = 122.116429
    mean_factor['AVG_DIAST'].loc[1] = 74.042905

    m = m - mean_factor.values
    m = m / std_factor.values
    return m

def degree_range(n):
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang):
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

def gauge(labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], \
          colors='jet_r', arrow=1, title='', fname=False):

    ##some sanity checks first

    N = len(labels)

    if arrow > N:
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow, N))

    # if colors is a string, we assume it's a matplotlib colormap
    # and we discretize in N discrete colors

    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list):
        if len(colors) == N:
            colors = colors[::-1]
        else:
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors), N))

    #begins the plotting

    fig, ax = plt.subplots()

    ang_range, mid_points = degree_range(N)

    labels = labels[::-1]

    #plots the sectors and the arcs

    patches = []
    for ang, c in zip(ang_range, colors):
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))

    [ax.add_patch(p) for p in patches]

    ##set the labels (e.g. 'LOW','MEDIUM',...)

    for mid, lab in zip(mid_points, labels):

        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=14, \
            fontweight='bold', rotation = rot_text(mid))


    ###set the bottom banner and the title

    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
    ax.add_patch(r)

    ax.text(0, -0.05, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=22, fontweight='bold')


    ###plots the arrow now


    pos = mid_points[abs(arrow - N)]

    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')

    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))


    ##removes frame and ticks, and makes axis equal and tight


    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    plt.tight_layout()
    if fname:
        fig.savefig(fname, dpi=200)
