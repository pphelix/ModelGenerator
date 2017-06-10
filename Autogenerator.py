from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random

class window( Frame ):
    def __init__( self, master = None ):
        Frame.__init__( self, master )

        self.mapmaxtext = 0
        self.maptext = 0
        self.master = master

        self.init_window()

    def init_window( self ):
        self.master.title( "Auto-Generation v1.1" )
        self.pack( fill = BOTH, expand = 1 )

        self.MapChosen = False
        self.ModelChosen = False
        self.SelectedQuantity = StringVar()
        self.SelectedX = StringVar()
        self.SelectedY = StringVar()

        MainImage = Image.open( 'auto.png' )
        RenderImage = ImageTk.PhotoImage( MainImage )

        img = Label( self, image  =RenderImage)
        img.image = RenderImage
        img.place(x=20, y=5)

        Phelix = Label( self, text = "--- Program by Phelix. --- Auto-generator V1.1 ---" )
        Phelix.place( x = 60, y = 120 )

        self.ProceedButton = ttk.Button( self, text = "Click this button once you're done", command = self.Check )
        self.ProceedButton.place( x = 5, y = 290 )

        MapButton = ttk.Button( self, text = "Select Map", command = self.ChooseMap )
        MapButton.place( x = 5, y = 170 )
 
        ModelButton = ttk.Button( self, text= "Select Model", command = self.ChooseModel )
        ModelButton.place( x = 5, y = 195 )

        XCoordinateText = Label(self, text="Please input the X co-ordinate for where you want the models: ")
        XCoordinateText.place(x=5, y=220)

        XCoordinate = ttk.Entry( self, width = 6, textvariable = self.SelectedX )
        XCoordinate.place(x = 345, y = 220 )

        YCoordinateText = Label( self, text = "Please input the Y co-ordinate for where you want the models: " )
        YCoordinateText.place( x = 5, y = 245 )

        YCoordinate = ttk.Entry( self, width = 6, textvariable = self.SelectedY )
        YCoordinate.place( x = 345, y = 245 )

        ModelQuantityText = Label( self, text = "Please input the amount of models you wish to have: " )
        ModelQuantityText.place( x = 5, y = 270 )

        ModelQuantityBox = ttk.Entry( self, width = 6, textvariable = self.SelectedQuantity )
        ModelQuantityBox.place( x = 345, y = 270 )

    def ChooseMap( self ):
        self.filename = askopenfilename( filetypes = ( ( "Map File", "*.map" ), ( "All files", "*.*" ) ) )
        self.MapName = os.path.split( self.filename )[ 1 ]
        if self.MapName:
            print( str( "Map: " + self.MapName ) )
            MapSelected = Label( self, text = "Map selected!", padx = 5 )
            MapSelected.place( x = 85, y = 172 )
            self.MapChosen = True

    def ChooseModel( self ):
        filename = askopenfilename( filetypes = ( ( "Model File", "*.*" ), ( "All files", "*.*" ) ) )
        self.ModelName = os.path.split(filename)[1]
        if self.ModelName:
            print( str( "Model: " + self.ModelName ) )
            ModelSelected = Label( self, text = "Model selected!", padx = 5 )
            ModelSelected.place( x = 85, y = 197 )
            self.ModelChosen = True

    def Check( self ):

        self.DoneCheck = 0

        self.XComplete = False
        self.YComplete = False
        self.ModelQuantityComplete = False

        self.Error = "Error!"

        if not self.MapChosen:
            print( 'Please choose a map!' )

        if not self.ModelChosen:
            print( 'Please choose a model!' )

        if self.SelectedX:
            self.X = self.SelectedX.get()
            self.OldX = self.X
            if any( c.isalpha() for c in self.X ):
                print( 'This is not an integer!' )
            elif not self.X:
                print( 'Empty field! Please input a number' )
            else:
                self.XComplete = True

        if self.SelectedY:
            self.Y = self.SelectedY.get()
            if any( c.isalpha() for c in self.Y ):
                print( 'This is not an integer!' )
            elif not self.Y:
                print( 'Empty field! Please input a number' )
            else:
                self.YComplete = True

        if self.SelectedQuantity:
            self.ModelQuantity = self.SelectedQuantity.get()
            if any( c.isalpha() for c in self.ModelQuantity ):
                print( 'This is not an integer!' )
            elif not self.ModelQuantity:
                print( 'Empty field! Please input a number' )
            else:
                self.ModelQuantityComplete = True

        if self.MapChosen and self.ModelChosen and self.XComplete and self.YComplete and self.ModelQuantityComplete:
            self.DoneCheck = 1

        if self.DoneCheck:
            self.StartGenerating()

    def StartGenerating( self ):
        print ( 'Moved Onto Start Generating' )
        self.ProceedButton.destroy()

        self.progress = ttk.Progressbar( self, orient = "horizontal", length = 200, mode = "determinate" )
        self.progress.place( x = 5, y = 290 )

        self.writefile = open( self.filename, 'a' )
        self.XRandomModel = int( self.X ) / int( self.ModelQuantity )
        self.YRandomModel = int( self.Y ) / int( self.ModelQuantity )
        while int( self.XRandomModel ) <= int( self.X ) and int( self.YRandomModel ) <= int( self.Y ):
            a = random.randrange( 0, int( self.X ) )
            b = random.randrange( 0, int( self.Y ) )
            self.XRandomModel = int( self.X ) / int( self.ModelQuantity ) + int( self.XRandomModel )
            self.YRandomModel = int( self.Y ) / int( self.ModelQuantity ) + int( self.YRandomModel )
            self.writefile.write ( ( "\n//Auto-Generated Model" + str( self.XRandomModel ) ) + ( "\n{\n" ) + ( "\"origin\" \"%s %s 16.0\"\n" ) % ( a, b ) + ( "\"model\" \"" ) + str( self.ModelName ) + ( "\"\n" ) + ( "\"classname\" \"misc_model\"\n" ) + ( "}" ) )
        self.writefile.close()
        root.quit()

root = Tk()
root.geometry( "400x320" )
root.wm_iconbitmap( "icon.ico" )
app = window( root )
root.mainloop()


