#object definition for our frame class
#output: feature class with polygon for each frame with its determined ratio value

import arcpy, collections ,os

class classifiedRaster: #class definition for the frames made from the whole raster
    
    def __init__(self, in_ras, in_sizeX, in_sizeY, in_ratio,in_classification): #inputs: main raster, frame size (5m x 10m), ratio (80%), and desired classification (weeds).
        self.__inras = in_ras
        self.__frameX = float(in_sizeX)
        self.__frameY = float(in_sizeY)
        self.__frame_ratio = float(in_ratio)
        self.__in_class = in_classification
        self.__max_y = float(arcpy.GetRasterProperties_management(in_ras, "TOP").getOutput(0))
        self.__min_y = float(arcpy.GetRasterProperties_management(in_ras, "BOTTOM").getOutput(0))
        self.__max_x = float(arcpy.GetRasterProperties_management(in_ras, "RIGHT").getOutput(0))
        self.__min_x = float(arcpy.GetRasterProperties_management(in_ras, "LEFT").getOutput(0))
		

		
    def processRaster(self,output, User_Field_Count, Class_List, User_Field, Fields_List):
		arcpy.AddMessage("Processing raster.")
		fc = output

		arcpy.env.overwriteOutput = True

		#arcpy.AddMessage(str(arcpy.env.workspace) +"  "+ str(os.path.split(output)[1]))
		#arcpy.AddMessage(str(fc))
		#arcpy.AddMessage(arcpy.Exists(output))
		#arcpy.AddMessage(str(output))
		
		arcpy.management.CreateFeatureclass(arcpy.env.workspace,os.path.split(output)[1],"POLYGON")
		frame = "TempClip"#defining the location where the temporary frame will be saved       might need arcpy.env.workspace + 
		#may need a \\ before temp
		
		R="Ratio"
		F="FLOAT"
		arcpy.management.AddField(fc,R,F)
		#arcpy.management.AddField("frame_ratio","FRAME_ID","SHORT")
		projection = arcpy.Describe(self.__inras).spatialReference
		arcpy.DefineProjection_management(fc,projection)
		cursor = arcpy.da.InsertCursor(fc, ["SHAPE@","Ratio"]) #cursor for creating the valid frame feature class
		#arcpy.AddMessage("Passed the cursor")
		y = float(self.__min_y) #set to bottom of in raster
		
		frameCount = 0 #some nice counters for output while prcessing
		validFrameCount = 0
		totalFrames = int(((self.__max_y-self.__min_y)/self.__frameY//2) * ((self.__max_x-self.__min_x)/self.__frameX//2))
		
		#arcpy.AddMessage("y = " +str(y))
		#arcpy.AddMessage("max Y = " +str(self.__max_y))
		while(y < self.__max_y):#flow control based on raster size and requested frame size needed. Issue on edges, ask about.
			x = float(self.__min_x) #set to left bound of in raster
			#arcpy.AddMessage("Passed 1 while")
			#arcpy.AddMessage("x = " +str(x))
			#arcpy.AddMessage("max X = " +str(self.__max_x))
			while (x < self.__max_x): #"side to side" processing
				#arcpy.AddMessage("Passed 2 while")
				rectangle = str(x) + " " + str(y) + " " + str(x + self.__frameX) + " " + str(y + self.__frameY) #bounds of our frame for the clip tool
				#arcpy.AddMessage("Current rectangle: " + str(rectangle))
				arcpy.Clip_management(self.__inras,rectangle, frame)#create frame -> clip out a section of the main raster 
                		frameCount += 1
				arcpy.AddMessage("Processing frame #" + str(frameCount) + " out of " + str(totalFrames))
				
				validFrame, validRatio = density(frame, self.__frame_ratio, self.__in_class, User_Field_Count, Class_List, User_Field, Fields_List) #run ratio function. Expect boolean T if frame meets ratio conditions, and actual ratio
				if validFrame: #Case it passes
					arcpy.AddMessage("Valid frame.")
					validFrameCount += 1
					array = arcpy.Array([arcpy.Point(x, y), arcpy.Point(x, y + self.__frameY),arcpy.Point(x + self.__frameX, y + self.__frameY),arcpy.Point(x + self.__frameX, y)]) #creating the frame polygon
					polygon = arcpy.Polygon(array)
		          
					cursor.insertRow([polygon,validRatio]) #add frame to feature class

					x += self.__frameX #adjust counter for positive condition
					continue #back to beginning of while loop

				x = int(x) + int(float(self.__frameX)//2)#move half a frame "right"...case when previous frame invalid "Fast option"
			y = float(y) + int(float(self.__frameY)//2)#move half a frame "up" ... "Fast option"
			
		del cursor #prevent data corruption by deleting cursor when finished
		arcpy.AddMessage("Finished processing raster. " + str(validFrameCount) + " valid frames found.")
		
		
		
def density(inras, ratio, inclass, User_Field_Count, Class_List, User_Field_Value,Fields_List): #added the needed inputs
	fc = inras #Determines file path from user input
	#arcpy.AddMessage("Processing frame.")
	#arcpy.AddMessage("fc = " + str(fc))
	
	countField= User_Field_Count
	arcpy.BuildRasterAttributeTable_management(fc, "Overwrite") #updates attribute table to reflect frame, rather than whole
	#F="FLOAT"
	#arcpy.management.AddField(fc,field,F) #creating attribute table to store frequencies in
	cursor = arcpy.SearchCursor(fc,Fields_List)
	
	frequency = 0
	total = 0
	#CountColumn = 0
	#ValueColumn = 0
	#i = 0
	#for column in Fields_List: #determines which column contains the counts for data retrieval
	#	if column == User_Field_Count:
	#		CountColumn = i
	#	if column == User_Field_Value:
	#		ValueColumn = i
	#	i += 1	
	
	for row in cursor: #Calculates information on each classification
		arcpy.AddMessage("inclass = " + str(inclass))
		arcpy.AddMessage("row.getValue(User_Field_Value) = " + str(row.getValue(User_Field_Value)))
		#arcpy.AddMessage("row[ValueColumn] = " + str(row[ValueColumn]))
		try:
			#if row[ValueColumn] == inclass: #calc frequency of the classification requested
			if int(row.getValue(User_Field_Value)) == int(inclass): #calc frequency of the classification requested
				frequency = row.getValue(User_Field_Count)
				arcpy.AddMessage("Frequency = " + str(row.getValue(User_Field_Count)))
			total += row.getValue(User_Field_Count) #calc sum
			arcpy.AddMessage("Total = " + str(total))
		except:
			arcpy.AddMessage("Not in frame.")
			return False, 0
	if total == 0: #preventing dividing by 0, case where there is nothing in the frame
		arcpy.AddMessage("Frame empty.")
		return False, 0
	
	final_ratio = float(frequency)/float(total) #Calculates ratio for user input classification
	arcpy.AddMessage("Frame has density " + str(final_ratio))
	if final_ratio >= ratio: 
		return True, final_ratio #Returns true and final ratio if user input is met
	else:
		return False, final_ratio #Returns false and final ratio if user input is not met

	
    
