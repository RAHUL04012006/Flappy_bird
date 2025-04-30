import cv2

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load an image
image_path = r'C:\Users\Admin\OneDrive\Desktop\face recognition\WhatsApp Image 2024-08-03 at 7.51.43 PM.jpeg'
images = cv2.imread(image_path)
newsize=(600,400)
image=cv2.resize(images,newsize)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Display the output
cv2.imshow('Face Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


