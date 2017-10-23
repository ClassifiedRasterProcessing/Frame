#object definition for our frame class
#potentially have ratio calculation be a function

import arcpy
arcpy.env.workspace = "C:/Workspace"
    
#example of clip tool. We'll need to clip the main raster to create each frame. http://pro.arcgis.com/en/pro-app/tool-reference/data-management/clip.htm 
#arcpy.Clip_management("image.tif","1952602.23 294196.279 1953546.23 296176.279","clip.gdb/clip", "#", "#", "NONE")

#inputs: main raster, frame size (5m x 5m), ratio (80%), and desired classification (weeds).

#flow control based on raster size and requested frame size
    #create frame -> clip out a section of the main raster
    #process frame -> call ratio function and give it our frame, classification, and ratio. Expect True/False returned
      #reclassify raster if meets criteria
    #decision point -> adjust counters if frame is valid, and store it in a list of positive frames.
    
#decide how we want the final raster output
  #bunch of tiny rasters? Cursor during decision point
  #compiled raster? Merge tool http://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/merge-raster-function.htm 
