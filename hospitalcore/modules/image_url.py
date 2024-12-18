from PIL import Image #Image Library
import cloudinary # To generate Image url.
import cloudinary.uploader
import os
# from invoiceManager import invoice #Invoice Module.

#Config Cloudinary
cloudinary.config(
    cloud_name = 'dmdkjavlp', #Cloudinary Library
    api_key = '627292566488957', #Cloudinary API KEY
    api_secret = 'xvbg9Xic_AT0FWvbIr4cN63kL8A', # API Secret Key
    secure = True # Set True
)


#Function to generate Image URL
def get_url(image):
    response = cloudinary.uploader.upload(image) #Upload Image to Cloudinary
    url = response['secure_url'] #Get url from JSON response
    #print(url)
    return url
