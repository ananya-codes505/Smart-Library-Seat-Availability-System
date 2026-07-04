# Smart Library Seat Availability System

## Problem Statement

During end-semester examinations, students often walk to the library only to find that no seats are available. This project aims to estimate seat availability in real time and help users make informed decisions before entering the library.

## Features

* Real-time seat occupancy detection using a webcam
* Displays the number of available and occupied seats
* Uses classical computer vision and image processing techniques
* Reduces false detections caused by lighting changes and temporary movement

## Tech Stack

* Python
* OpenCV

## How It Works

1. Capture an empty library frame as the reference image.
2. Compare the current frame with the reference frame.
3. Detect changes within predefined seat regions.
4. Mark seats as occupied or available and display live availability.

## Scalability

* Multi-camera deployment for larger libraries and multi-floor buildings
* Integration with a web or mobile application
* Occupancy analytics for peak-hour analysis and resource planning

## Potential Applications

* University libraries and study halls
* Co-working spaces and reading rooms
* Computer labs and classrooms
* Cafeterias and food courts
* Waiting areas in hospitals, airports, and railway stations
* Parking occupancy systems and other shared spaces

## Author

Ananya Prasad
