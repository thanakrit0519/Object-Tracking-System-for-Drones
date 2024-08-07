import math
def  vinc_pt(phi1, lembda1, alpha12, s,f=1/298.257223563,a=6378137.0) : 
    
    """ 
    Returns the lat and long of projected point and reverse azimuth 
    given a reference point and a distance and azimuth to project. 
    lats, longs and azimuths are passed in decimal degrees 
    Returns ( phi2,  lambda2,  alpha21 ) as a tuple
    Parameters:
    ===========
        f: flattening of the ellipsoid
        a: radius of the ellipsoid, meteres
        phil: latitude of the start point, decimal degrees
        lembda1: longitude of the start point, decimal degrees
        alpha12: bearing, decimal degrees
        s: Distance to endpoint, meters
    NOTE: This code could have some license issues. It has been obtained 
    from a forum and its license is not clear. I'll reimplement with
    GPL3 as soon as possible.
    The code has been taken from
    https://isis.astrogeology.usgs.gov/IsisSupport/index.php?topic=408.0
    and refers to (broken link)
    http://wegener.mechanik.tu-darmstadt.de/GMT-Help/Archiv/att-8710/Geodetic_py
    """ 
    piD4 = math.atan( 1.0 ) 
    two_pi = piD4 * 8.0 
    phi1    = phi1    * piD4 / 45.0 
    lembda1 = lembda1 * piD4 / 45.0 
    alpha12 = alpha12 * piD4 / 45.0 
    if ( alpha12 < 0.0 ) : 
        alpha12 = alpha12 + two_pi 
    if ( alpha12 > two_pi ) : 
        alpha12 = alpha12 - two_pi
    b = a * (1.0 - f) 
    TanU1 = (1-f) * math.tan(phi1) 
    U1 = math.atan( TanU1 ) 
    sigma1 = math.atan2( TanU1, math.cos(alpha12) ) 
    Sinalpha = math.cos(U1) * math.sin(alpha12) 
    cosalpha_sq = 1.0 - Sinalpha * Sinalpha 
    u2 = cosalpha_sq * (a * a - b * b ) / (b * b) 
    A = 1.0 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * \
        (320 - 175 * u2) ) ) 
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2) ) ) 
    # Starting with the approx 
    sigma = (s / (b * A)) 
    last_sigma = 2.0 * sigma + 2.0   # something impossible 
        
    # Iterate the following 3 eqs unitl no sig change in sigma 
    # two_sigma_m , delta_sigma 
    while ( abs( (last_sigma - sigma) / sigma) > 1.0e-9 ):
        two_sigma_m = 2 * sigma1 + sigma 
        delta_sigma = B * math.sin(sigma) * ( math.cos(two_sigma_m) \
                + (B/4) * (math.cos(sigma) * \
                (-1 + 2 * math.pow( math.cos(two_sigma_m), 2 ) -  \
                (B/6) * math.cos(two_sigma_m) * \
                (-3 + 4 * math.pow(math.sin(sigma), 2 )) *  \
                (-3 + 4 * math.pow( math.cos (two_sigma_m), 2 )))))
        last_sigma = sigma 
        sigma = (s / (b * A)) + delta_sigma 
    phi2 = math.atan2 ( (math.sin(U1) * math.cos(sigma) +\
        math.cos(U1) * math.sin(sigma) * math.cos(alpha12) ), \
        ((1-f) * math.sqrt( math.pow(Sinalpha, 2) +  \
        pow(math.sin(U1) * math.sin(sigma) - math.cos(U1) * \
        math.cos(sigma) * math.cos(alpha12), 2))))
    lembda = math.atan2( (math.sin(sigma) * math.sin(alpha12 )),\
        (math.cos(U1) * math.cos(sigma) -  \
        math.sin(U1) *  math.sin(sigma) * math.cos(alpha12))) 
    C = (f/16) * cosalpha_sq * (4 + f * (4 - 3 * cosalpha_sq )) 
    omega = lembda - (1-C) * f * Sinalpha *  \
        (sigma + C * math.sin(sigma) * (math.cos(two_sigma_m) + \
        C * math.cos(sigma) * (-1 + 2 *\
        math.pow(math.cos(two_sigma_m), 2) ))) 
    lembda2 = lembda1 + omega 
    alpha21 = math.atan2 ( Sinalpha, (-math.sin(U1) * \
        math.sin(sigma) +
        math.cos(U1) * math.cos(sigma) * math.cos(alpha12))) 
    alpha21 = alpha21 + two_pi / 2.0 
    if ( alpha21 < 0.0 ) : 
        alpha21 = alpha21 + two_pi 
    if ( alpha21 > two_pi ) : 
        alpha21 = alpha21 - two_pi 
    phi2 = phi2 * 45.0 / piD4 
    lembda2 = lembda2 * 45.0 / piD4 
    alpha21 = alpha21 * 45.0 / piD4
    return phi2, lembda2, alpha21

def cal_objectGPS(lat1,lon1,altitude,pitch,yaw):
    distance = altitude * math.tan((90+pitch)/180*math.pi)
    print(distance)
    return vinc_pt(lat1,lon1,yaw,distance)

print(cal_objectGPS(37.4534739401493,38.6699858861775,129.17424,-20.1,326.3))