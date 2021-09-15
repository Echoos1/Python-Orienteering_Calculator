try:
    import math
    import gpxpy
    import gpxpy.gpx
except ModuleNotFoundError:
    print("Module Error\n")
    input("Press ENTER to quit")
    exit()

gpxfile = f'{input("Input GPX filename: ")}.gpx'
output = f'{input("Output TXT filename: ")}.txt'
gpx_file = open(gpxfile, 'r')

gpx = gpxpy.parse(gpx_file)

lat = []
long = []

for waypoint in gpx.waypoints:
    lat.append(waypoint.latitude)
    long.append(waypoint.longitude)

if len(lat) != len(long):
    print("File Error: Latitude count does not equal Longitude count")
    input("\nPress ENTER to exit... ")
    exit()
else:
    pass

points = len(lat)

try:
    file = open(output, "x")
    print(f"Creating File {output}.txt...")
except FileExistsError:
    file = open(output, "w")
    print(f"Could not create {output}.txt: File Already Exists... Overwriting...")

for i in range(points-1):

    Lat1 = math.radians(lat[i])
    Long1 = math.radians(long[i])
    Lat2 = math.radians(lat[i+1])
    Long2 = math.radians(long[i+1])

    LatDiff = abs(Lat1 - Lat2)
    LongDiff = (abs(Long2 - Long1))

    # Bearing
    # --------

    """
    !! Old Math -- Doesn't Work for Westerly Movement/+180 Degrees !!
    
    X = math.cos(Lat2) * math.sin(LongDiff)
    Y = math.cos(Lat1) * math.sin(Lat2) - math.sin(Lat1) * math.cos(Lat2) * math.cos(LongDiff)

    B = math.atan2(X, Y)

    Bearing = int(round(math.degrees(B), 0))
    """

    X = math.sin(Long2 - Long1) * math.cos(Lat2)
    Y = math.cos(Lat1) * math.sin(Lat2) - math.sin(Lat1) * math.cos(Lat2) * math.cos(Long2 - Long1)
    B = math.atan2(X, Y)
    Bearing = int(round(((B * 180 / float(math.pi) + 360) % 360), 0))

    # Distance
    # --------

    a = ((math.sin(LatDiff/2))**2) + math.cos(Lat1)*math.cos(Lat2)*((math.sin(LongDiff / 2)) ** 2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = 20902259.664*c

    Distance = int(round(d, 0))

    print(f"{i+1}. {Distance} Feet at {Bearing}°")
    file.write(f"{i+1}. {Distance} Feet at {Bearing}°\n")
