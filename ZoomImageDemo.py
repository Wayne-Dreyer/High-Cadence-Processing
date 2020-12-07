#This file was created by Wayne Dreyer
#It serves to demonstrate and manually test the functionality of the ZoomImage function
#As this serves as a manual test it serves to supplement the unittesting


from PIL import Image
import ZoomImage

def main():
    print("This file is for the purpose of demonstrating the image zooming functionality")
    image = input("Please enter image location: ") #eg ./moon1024x1024.jpg
    xCoord = int(input("Please enter candidates x axis location: ")) #The x coordinate of the candidate
    yCoord = int(input("Please enter candidates y axis location: ")) #The y coordinate of the candidate 
    zoomFactor = int(input("Please enter the amount you wish to zoom eg 2 for 2x: "))

    zoomedImage = ZoomImage.zoomImage(image, xCoord, yCoord, zoomFactor) #gets the new zoomed image from the function we are testing
    zoomedImage.show() #calls on operating system to open the image in default image viewer
    saveImage = input("Would you like to save the image: (Enter Yes or No :")
    print(image, xCoord, yCoord, zoomFactor)

    #saves the image with the users specified name if they chose to do so.
    if(saveImage == "Yes" or saveImage == "yes"):
        saveName = input("Enter output filename: eg) output.jpg ")
        zoomedImage.save(saveName, format=None) #saveName will include the desired image format

    return 0

if __name__ == "__main__":
    main()