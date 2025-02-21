import cv2
from bs4 import BeautifulSoup
import numpy as np
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_xml', required=False, default="./week1_anot.xml", help='Input xml')
    parser.add_argument('--path_video', required=False, default="../AICity_data/AICity_data/train/S03/c010/vdo.avi", help='Input xml')
    args = parser.parse_args()

    # Read the XAML file
    with open(args.path_xml, "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Parse the XAML content
    soup = BeautifulSoup(xml_content, "xml")

    # Dictionary to store boxes per frame
    frames_data = {}

    # Find all 'box' elements
    boxes = soup.find_all("box")

    for box in boxes:
        frame = int(box.get("frame"))

        # Get bounding box coordinates
        xtl = float(box.get("xtl"))
        ytl = float(box.get("ytl"))
        xbr = float(box.get("xbr"))
        ybr = float(box.get("ybr"))

        if frame not in frames_data:
            frames_data[frame] = []
        
        # Add box information for this frame
        frames_data[frame].append((xtl, ytl, xbr, ybr))
    
    # Open the video
    video_path = args.path_video
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create a VideoWriter to save the output video (optional)
    output_video = cv2.VideoWriter('output_video_with_boxes.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Process each frame
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break
        
        # Draw boxes for the current frame
        if frame_number in frames_data:
            for box in frames_data[frame_number]:
                xtl, ytl, xbr, ybr = box

                # Draw rectangle (bounding box) on the frame
                cv2.rectangle(frame, (int(xtl), int(ytl)), (int(xbr), int(ybr)), (0, 255, 0), 2)  # Green box with thickness 2

        #cv2.rectangle(frame, (int(frame_width/4), int(frame_height/4)), (int(frame_width*3/4), int(frame_height*3/4)), (0, 255, 0), 5)

        # Write the frame with boxes to the output video
        output_video.write(frame)

        # Optional: Display the frame
        cv2.imshow('Frame with Bounding Boxes', frame)

        # Break the loop if you press 'q' (quit) during the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_number += 1

    # Release the video capture and writer objects
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    print("Video with bounding boxes saved successfully!")
