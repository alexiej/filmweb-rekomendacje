
"""
The :mod:`similarities <surprise.similarities>` module includes tools to
compute similarity metrics between users or items. You may need to refer to the
:ref:`notation_standards` page. See also the
:ref:`similarity_measures_configuration` section of the User Guide.
Available similarity measures:
.. autosummary::
    :nosignatures:
    cosine
    msd
    pearson
    pearson_baseline
"""

import numpy as np

from six.moves import range
from six import iteritems




def cosine(n_x, yr, min_support):
    """Compute the cosine similarity between all pairs of users (or items).
    Only **common** users (or items) are taken into account. The cosine
    similarity is defined as:
    .. math::
        \\text{cosine_sim}(u, v) = \\frac{
        \\sum\\limits_{i \in I_{uv}} r_{ui} \cdot r_{vi}}
        {\\sqrt{\\sum\\limits_{i \in I_{uv}} r_{ui}^2} \cdot
        \\sqrt{\\sum\\limits_{i \in I_{uv}} r_{vi}^2}
        }
    or
    .. math::
        \\text{cosine_sim}(i, j) = \\frac{
        \\sum\\limits_{u \in U_{ij}} r_{ui} \cdot r_{uj}}
        {\\sqrt{\\sum\\limits_{u \in U_{ij}} r_{ui}^2} \cdot
        \\sqrt{\\sum\\limits_{u \in U_{ij}} r_{uj}^2}
        }
    depending on the ``user_based`` field of ``sim_options`` (see
    :ref:`similarity_measures_configuration`).
    For details on cosine similarity, see on `Wikipedia
    <https://en.wikipedia.org/wiki/Cosine_similarity#Definition>`__.
    """

    # sum (r_xy * r_x'y) for common ys
    # prods = np.ndarray[np.double_t, ndim=2]
    # # number of common ys
    # freq = np.ndarray[np.int_t, ndim=2]
    # # sum (r_xy ^ 2) for common ys
    # sqi = np.ndarray[np.double_t, ndim=2]
    # # sum (r_x'y ^ 2) for common ys
    # sqj = np.ndarray[np.double_t, ndim=2]
    # # the similarity matrix
    # sim = np.ndarray[np.double_t, ndim=2] 

    # cdef int xi, xj
    xi, xj = 0,0
    ri, rj = 0.0,0.0
    min_sprt = min_support

    n_x = 20

    prods = np.zeros((n_x, n_x), np.double)
    freq = np.zeros((n_x, n_x), np.int)
    sqi = np.zeros((n_x, n_x), np.double)
    sqj = np.zeros((n_x, n_x), np.double)
    sim = np.zeros((n_x, n_x), np.double)

    for y, y_ratings in iteritems(yr):
        for xi, ri in y_ratings:
            for xj, rj in y_ratings:
                freq[xi, xj] += 1
                prods[xi, xj] += ri * rj
                sqi[xi, xj] += ri**2
                sqj[xi, xj] += rj**2

    for xi in range(n_x):
        sim[xi, xi] = 1
        #for xj in range(xi + 1, n_x):
        if freq[xi, xj] < min_sprt:
            sim[xi, xj] = 0
        else:
            denum = np.sqrt(sqi[xi, xj] * sqj[xi, xj])
            sim[xi, xj] = prods[xi, xj] / denum

        sim[xj, xi] = sim[xi, xj]

    return sim
