'''
Takes a csv file ('Observations') with['name', 'x', 'y'] as fields and plots multiple paths from that data

The name field is set to 'Rhino' (plots Rhinos) so search and replace every instance of 'Rhino'
Takes input and output file names from the command line


Uses sys.exit() for returning status values back to a batch file
'''

import arcpy, os, sys

GCS_North_American_1983 = 4269

# Change this to what ever the field label is in the csv file
NAME_FIELD = "Rhino" 

X_FIELD = "X"
Y_FIELD = "Y"

# Read though csv file containing rhino tracks (or any set of polylines) and create a hash such as:
# hash = {'name1' : [[x1,y1], [x2, y2], [x3, y3],...], 'name2' : [[x1, x2], ...], ...}

def getCoordinates(inFile):
    Hash = {}

    # Read the header
    headerLine = inFile.readline()
    headerArray = headerLine.split(",")

    # Get indexes of fields in rhino coordinate file
    nameIndex = headerArray.index(NAME_FIELD)
    xIndex = headerArray.index(X_FIELD)
    yIndex = headerArray.index(Y_FIELD)

    # Read first line of rhino coordinate file
    Record = inFile.readline().rstrip()

    # Loop through all records in the coordinate file and create hash from them
    while Record:

        Data = Record.split(",")

        # Read the name and determine if it is already a hash key
        Name = Data[nameIndex]

        if Name not in Hash:
            # Create an array that will be referenced by hash key (aka rhino name)
            Hash[Name] = []

        # Get the X, Y location of rhino and create a coordinate list
        x = Data[xIndex]
        y = Data[yIndex]

        coordList = [x,y]

        # append the coordinate list to rhino's polyline
        Hash[Name].append(coordList)

        # Read the next line in the csv file
        Record =  inFile.readline().rstrip()

    return Hash

# Create a polyline shapefile to hold SHAPE field (Rhino tracks) and name

def createPath(Hash, Shapefile):
    count = 0
    polylineArray = arcpy.Array()

    # Create an insert cursor for writing rhino name and tracks (polyline) to output shape file
    cursor = arcpy.InsertCursor(Shapefile)

    # loop through all of the rhinos in the hash
    for key in Hash:
        # Add array of coordinate pairs to array holding polyline
        polylineArray.add(Hash[key])
        count += 1

        # Create polyline from array of points
        polyline = arcpy.Polyline(polylineArray, GCS_North_American_1983)

        # Insert row with SHAPE (track) and rhino name 
        row = cursor.newRow()  
        row.SHAPE = polyline
        
        # Change 
        row.Rhino = key
        row.id = Count
        cursor.insertRow(row)

        # De-Allocate array of points
        polylineArray.removeAll()

    del row
    del cursor

    return count

def main():


    # Get the name of the observations file, the output directory and shapefile 
    # that rhinos and thier tracks will be written to

    try:
        Observations = arcpy.GetParameterAsText(0)
        outputDir = arcpy.GetParameterAsText(1)
        outputShape = arcpy.GetParameterAsText(2)
    except:
        print "Error getting parameters"

    # --------------------------------
    
    outShape = outputDir + outputShape
    
    # Determine if output shapefile already exists, exit if it does
    if os.path.isfile(outShape):
        print "Shapefile " + outShape + " already exists"
        sys.exit(3)
    
    # Determine if observations file exists, exit if it does'nt
    if not os.path.isfile(Observations):
        print "Observations file " + Observations + " does not exist"
        sys.exit(2)
    
    # -----------------------------------
    
    #print "\nProcessing Observations from: " + Observations + "..."
    numObservations = 0
    
    try:
        # Open file with coordinates of rhino tracks
        rhinoObservations = open(Observations, "r")
        # Create a hash of rhinos and thier path
        rhinoHash = getCoordinates(rhinoObservations)
    
        # close file
        rhinoObservations.close()
    except:
        pass
    
    # ---------------------------------------
    
    print "Creating shapefile: " + outShape 
    
    # Create ouput shapefile with GCS_NAD_1983 (4269) spatial reference
    try:
        arcpy.CreateFeatureclass_management(outputDir, outputShape, "POLYLINE", "", "DISABLED", "DISABLED", GCS_North_American_1983)
        
        '''
        Create a field in the polyline shapefile to hold rhino's name
        In cases where an observations file follow a field name standard
        this line of code would not be neccesssary
        '''

        arcpy.AddField_management(outShape, NAME_FIELD, "TEXT")
       
    
        # write the path to a file
        numObservations = createPath(rhinoHash, outShape)
    except:
        print "Error creating shapefile"
        sys.exit(1)
    
    print "Processed " + str(len(rhinoHash)) + " rhinos and " + str(numObservations) + " observations"
    
    sys.exit(0)
if __name__ == "__main__":

    main()

