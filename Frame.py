#object definition for our frame class
#potentially have ratio calculation be a function

import arcpy
arcpy.env.workspace = "C:/Workspace"



class classifiedRaster: #class definition for the frames made from the whole raster
    def __init__(self, in_ras, in_size, in_ratio,in_classification): #inputs: main raster, frame size (5m x 5m), ratio (80%), and desired classification (weeds).
        self.__inras = in_ras
        self.__frame_size = in_size
        self.__frame_ratio = in_ratio
        self.__in_class = in_classification
        self.__max_y = GetRasterProperties_management(in_ras, TOP) #see documentation. Lots of available properties
        self.__min_y = GetRasterProperties_management(in_ras, BOTTOM)
        self.__max_x = GetRasterProperties_management(in_ras, RIGHT)
        self.__min_x = GetRasterProperties_management(in_ras, LEFT)


   
    def processRaster():   
    
        x = __min_x #temp variables for adjusting frames
        y = __min_y
        while(y < __max_y):#flow control based on raster size and requested frame size needed. Issue on edges, ask about.
            while (x < __max_x): #"side to side" processing

                #example of clip tool. We'll need to clip the main raster to create each frame. http://pro.arcgis.com/en/pro-app/tool-reference/data-management/clip.htm 
                #arcpy.Clip_management("image.tif","1952602.23 294196.279 1953546.23 296176.279","clip.gdb/clip", "#", "#", "NONE")

                rectangle = str(x) + " " + str(y) + " " + str(x+__frame_size) + " " + str(y+__frame_size) #bounds of our frame for the clip tool
               # arcpy.Clip_management(inras,rectangle, outras)#create frame -> clip out a section of the main raster
                #stopped here since might not need to create mini rasters if ratio can do it without this

                    #pass the frame to the ratio function to determine if it fits criteria
                        #process frame -> call ratio function and give it our frame, classification, and ratio. Expect True/False returned
                            #reclassify raster if meets criteria
                            #decision point -> adjust counters if frame is valid, and store it in a list of positive frames.

                #decide how we want the final raster output
                  #bunch of tiny rasters? Cursor during decision point
                  #compiled raster? Merge tool http://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/merge-raster-function.htm 

            x += __frame_size#incrementing our counters
        y += __frame_size
        
    def density():

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
        print(dicts)
