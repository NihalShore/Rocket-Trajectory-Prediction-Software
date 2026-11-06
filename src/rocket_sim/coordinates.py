"""Coordinate and frame conversion helpers for planar launch studies."""
import math
def heading_components(speed,azimuth_deg):
    a=math.radians(azimuth_deg)
    return speed*math.sin(a),speed*math.cos(a)
def polar_velocity(horizontal,vertical):
    speed=math.hypot(horizontal,vertical)
    return speed,math.degrees(math.atan2(vertical,horizontal))
def rotate_2d(x,y,angle_rad):
    c=math.cos(angle_rad); s=math.sin(angle_rad)
    return c*x-s*y,s*x+c*y
def local_to_ecef(latitude_deg,longitude_deg,altitude=0.):
    lat=math.radians(latitude_deg); lon=math.radians(longitude_deg); r=6371000.+altitude
    return r*math.cos(lat)*math.cos(lon),r*math.cos(lat)*math.sin(lon),r*math.sin(lat)
def ecef_to_geodetic_spherical(x,y,z):
    r=math.sqrt(x*x+y*y+z*z)
    if r==0: raise ValueError("origin has no geodetic coordinate")
    return math.degrees(math.asin(z/r)),math.degrees(math.atan2(y,x)),r-6371000.
