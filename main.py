from ultralytics import YOLO
import cv2
import numpy 
import json

# Load the YOLO model for car detection
model = YOLO("best.pt")  

slot_json= 'slots.json'
with open(slot_json, 'r') as file:
    slots = json.load(file)

def check_slots_availability(detection_boxes, slots_details=slots):
    box_centers = []

    # Calculate center of each box
    for box in boxes:
        box_centers.append((sum(box[::2])/2, sum(box[1:4:2])/2))
    
    # Find slots containing each box center
    box_slot_mapping = []
    for i, (center_x, center_y) in enumerate(box_centers):
        for slot, (x, y, w, h) in slots.items():
            if x <= center_x <= x + w and y <= center_y <= y + h:
                if slot not in box_slot_mapping:
                    box_slot_mapping.append(slot)

    return box_slot_mapping

panel_x, panel_y, panel_width, panel_height = 880, 10, 200, 125
availables, occupieds = 0,0

# Open the video file
cam = cv2.VideoCapture('carPark.mp4')
frames=int(cam.get(cv2.CAP_PROP_FRAME_COUNT))



while True:
    # Read a frame from the video
    for _ in range(2):
        ret, frame = cam.read()

    # Break the loop if there are no more frames
        if not ret:
            break

    
    slot_allocations = check_slots_availability(boxes)
   
    
    
    print(slot_allocations)
    # Draw bounding boxes on the frame for car detection
    for i, box in enumerate(boxes):
        x, y, x_max, y_max = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        frame = cv2.rectangle(frame, (x, y), (x_max, y_max), 2)

    for slot, (x, y, w, h) in slots.items():
        if slot in slot_allocations:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            

        else:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    occupieds = sum(1 for slot in slot_allocations)
    availables = len(slots) - occupieds
    breakpoint()
       

    cv2.rectangle(frame, (panel_x, panel_y), (panel_x + panel_width, panel_y + panel_height), (105, 105, 105), -1)

    cv2.putText(frame, f'Occupied: {occupieds}', (panel_x + 10, panel_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(frame, f'Available: {availables}', (panel_x + 10, panel_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display the frame with bounding boxes
    cv2.namedWindow('YOLO Object Detection', cv2.WINDOW_NORMAL)
    cv2.imshow('YOLO Object Detection', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   

# Release the video capture object and close the OpenCV windows
cam.release()
cv2.destroyAllWindows()
