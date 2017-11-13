#object definition for our frame class
#output: feature class with polygon for each frame with its determined ratio value

import arcpy, collections
arcpy.env.workspace = "C:/Workspace"



class classifiedRaster: #class definition for the frames made from the whole raster
    def __init__(self, in_ras, in_sizeX, in_sizeY, in_ratio,in_classification): #inputs: main raster, frame size (5m x 10m), ratio (80%), and desired classification (weeds).
        self.__inras = in_ras
        self.__frameX = in_sizeX
        self.__frameY = in_sizeY
        self.__frame_ratio = in_ratio
        self.__in_class = in_classification
        self.__max_y = GetRasterProperties_management(in_ras, TOP) #see documentation. Lots of available properties
        self.__min_y = GetRasterProperties_management(in_ras, BOTTOM)
        self.__max_x = GetRasterProperties_management(in_ras, RIGHT)
        self.__min_x = GetRasterProperties_management(in_ras, LEFT)


   
    def processRaster():   
        fc = r"c:/data/gdb.gdb/valid_frames" #talk to Jacob -> make this an input file location
        cursor = arcpy.da.InsertCursor(fc, ["SHAPE@"]) #cursor for creating the valid frame feature class

        y = __min_y #set to bottom of in raster
        while(y < __max_y):#flow control based on raster size and requested frame size needed. Issue on edges, ask about.
            x = __min_x #set to left bound of in raster
            while (x < __max_x): #"side to side" processing
                rectangle = str(x) + " " + str(y) + " " + str(x+__frame_size) + " " + str(y+__frame_size) #bounds of our frame for the clip tool

                #NEEDS TO BE EDITED. FRAME SHOULD BE A TEMP FILE IN THE SAME WORKSPACE AS THE VALID FRAME FC
                arcpy.Clip_management(inras,rectangle, frame)#create frame -> clip out a section of the main raster 
                
                validFrame, validRatio = density(frame, __frame_ratio, __in_class) #run ratio function. Expect boolean T if frame meets ratio conditions, and actual ratio
                if validFrame: #Case it passes
                    array = arcpy.Array([arcpy.Point(0, 0), arcpy.Point(0, 1000),arcpy.Point(1000, 1000),arcpy.Point(1000, 0)]) #creating the frame polygon
                    polygon = arcpy.Polygon(array)
                    #need to somehow add validRatio to the attribute table
           
                    cursor.insertRow([polygon]) #add frame to feature class

                    x += __frameX #adjust counter for positive condition
                    continue #back to beginning of while loop

                x += int(__frameX/2)#move half a frame "right"...case when previous frame invalid "Fast option"
            y += int(__frameY/2)#move half a frame "up" ... "Fast option"
        del cursor #prevent data corruption by deleting cursor when finished

    def density(inras, ratio, classification): #added the needed inputs

        my_items = collections.defaultdict(set)
        for row in cur1:
            id = row.getValue(CaseField)
            value = row.getValue(ReadFromField)
            my_items[id].add(value)


        total = sum(my_items.values())
        dicts = {}
        n = 1
        for i in my_items.values:
            dicts[n] = values[i / total]
            n += 1
        print(dicts) #edit this to a return statement (true/false) based on the input classification as the index and the ratio for the logic
