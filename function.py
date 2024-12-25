import  numpy  as np
import cv2 
import matplotlib.pyplot as plt




#   low and high frequency  

def low_high_freq ( ft_imag=[], X_indices =[] ,y_indices =[]): 
    
    for x, y in zip(X_indices, y_indices):
        ft_imag[x, y] = 0  # Set specified indices to zero
    return ft_imag

 

# ft_img = np.ones((10, 10))
# X_indices = [2 , 2 , 2, 3, 3 , 3 , 4 , 4 , 4]
# y_indices = [2 , 3 , 4, 2 , 3 , 4 , 2 , 3 , 4]

# print ( low_high_freq (ft_img , X_indices ,y_indices))

 
 
 
   
    
def check_size(imag_1 , imag_2 , imag_3 , imag_4):
    
    images = [ imag_1 , imag_2 , imag_3 , imag_4]
    
    # Get the smallest width and height among all images
    min_height = min(img.shape[0] for img in images)
    min_width = min(img.shape[1] for img in images)
    
    imag_1 = cv2.resize( imag_1 , (min_width, min_height))
    imag_2 = cv2.resize( imag_2 , (min_width, min_height))
    imag_3 = cv2.resize( imag_3 , (min_width, min_height))
    imag_4 = cv2.resize( imag_4 , (min_width, min_height))
   
    return   imag_1, imag_2 , imag_3, imag_4
    
    
    
    

    
    
#   read image  

img_1 = cv2.imread("imgaes/Screen Shot 2024-11-10 at 10.27.12 AM.png" , cv2.IMREAD_GRAYSCALE)
img_2= cv2.imread("imgaes/IMG_20230807_000054_971.jpg" , cv2.IMREAD_GRAYSCALE)
img_3 = cv2.imread("imgaes/IMG_20230807_000054_971.jpg" , cv2.IMREAD_GRAYSCALE)
img_4 = cv2.imread("imgaes/IMG_20230807_000054_971.jpg" , cv2.IMREAD_GRAYSCALE)


#  shape before resize 
# print (img_1.shape, img_2.shape , img_3.shape, img_4.shape)
# Display before resizing
fig, axs = plt.subplots(1, 4, figsize=(15, 5))
axs[0].imshow(img_1, cmap='gray')
axs[0].set_title('Image 1')
axs[1].imshow(img_2, cmap='gray')
axs[1].set_title('Image 2')
axs[2].imshow(img_3, cmap='gray')
axs[2].set_title('Image 3')
axs[3].imshow(img_4, cmap='gray')
axs[3].set_title('Image 4')
for ax in axs:
    ax.axis('off')
plt.show()






# shape after resize  

# img_1 , img_2, img_3, img_4 = check_size ( img_1 , img_2, img_3, img_4)
# print (img_1.shape, img_2.shape , img_3.shape, img_4.shape)


# Display after resizing
fig, axs = plt.subplots(1, 4, figsize=(15, 5))
axs[0].imshow(img_1, cmap='gray')
axs[0].set_title('Image 1')
axs[1].imshow(img_2, cmap='gray')
axs[1].set_title('Image 2')
axs[2].imshow(img_3, cmap='gray')
axs[2].set_title('Image 3')
axs[3].imshow(img_4, cmap='gray')
axs[3].set_title('Image 4')
for ax in axs:
    ax.axis('off')
plt.show()








