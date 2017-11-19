#object definition for our frame class
#output: feature class with polygon for each frame with its determined ratio value

import arcpy, collections ,os




class classifiedRaster: #class definition for the frames made from the whole raster
    
    def __init__(self, in_ras, in_sizeX, in_sizeY, in_ratio,in_classification): #inputs: main raster, frame size (5m x 10m), ratio (80%), and desired classification (weeds).
        self.__inras = in_ras
        self.__frameX = in_sizeX
        self.__frameY = in_sizeY
        self.__frame_ratio = in_ratio
        self.__in_class = in_classification
        self.__max_y = arcpy.GetRasterProperties_management(in_ras, "TOP")
        self.__min_y = arcpy.GetRasterProperties_management(in_ras, "BOTTOM")
        self.__max_x = arcpy.GetRasterProperties_management(in_ras, "RIGHT")
        self.__min_x = arcpy.GetRasterProperties_management(in_ras, "LEFT")


   
    def processRaster(self,output):
		fc = output

		arcpy.env.overwriteOutput = True

		arcpy.AddMessage(str(arcpy.env.workspace) +"  "+ str(os.path.split(output)[1]))
		arcpy.AddMessage(str(fc))
		arcpy.AddMessage(arcpy.Exists(output))
		arcpy.AddMessage(str(output))
		
		
		
		arcpy.management.CreateFeatureclass(arcpy.env.workspace,os.path.split(output)[1],"POLYGON")

		R="Ratio"
		F="FLOAT"
		arcpy.management.AddField(fc,R,F)
		#arcpy.management.AddField("frame_ratio","FRAME_ID","SHORT")
		cursor = arcpy.da.InsertCursor(fc, ["SHAPE@","Ratio"]) #cursor for creating the valid frame feature class
		
		y = self.__min_y #set to bottom of in raster
		while(y < self.__max_y):#flow control based on raster size and requested frame size needed. Issue on edges, ask about.
			x = self.__min_x #set to left bound of in raster
			while (x < self.__max_x): #"side to side" processing
				rectangle = str(x) + " " + str(y) + " " + str(x+self.__frame_size) + " " + str(y+self.__frame_size) #bounds of our frame for the clip tool

                #NEEDS TO BE EDITED. FRAME SHOULD BE A TEMP FILE IN THE SAME WORKSPACE AS THE VALID FRAME FC
				arcpy.Clip_management(inras,rectangle, frame)#create frame -> clip out a section of the main raster 
                
				validFrame, validRatio = density(frame, self.__frame_ratio, self.__in_class) #run ratio function. Expect boolean T if frame meets ratio conditions, and actual ratio
				if validFrame: #Case it passes
					array = arcpy.Array([arcpy.Point(0, 0), arcpy.Point(0, 1000),arcpy.Point(1000, 1000),arcpy.Point(1000, 0)]) #creating the frame polygon
					polygon = arcpy.Polygon(array)
					vaildRatio= 1
					#need to somehow add validRatio to the attribute table
           
					cursor.insertRow([polygon,vaildRatio]) #add frame to feature class

					x += self.__frameX #adjust counter for positive condition
					continue #back to beginning of while loop

				x += int(self.__frameX/2)#move half a frame "right"...case when previous frame invalid "Fast option"
			y += int(self.__frameY/2)#move half a frame "up" ... "Fast option"
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
