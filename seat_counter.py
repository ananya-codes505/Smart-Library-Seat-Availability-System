import cv2

#1. Open webcam

cap = cv2.VideoCapture(0)

#check if camera opened correctly
if not cap.isOpened():
    print("Cannot open camera.")
    exit()

#2. Define seat positions: (x, y, width, height)

seats = []

start_x = 450
start_y = 180

width = 80
height = 80

gap_x = 170
gap_y = 150

for row in range(3):
    for col in range(3):

        x = start_x + col * gap_x
        y = start_y + row * gap_y

        seats.append((x, y, width, height))

#3.Empty library frame will act as the reference frame

background = None

#stores how many consecutive frames each seat
#has looked occupied
seat_counter = [0] * len(seats)

print("Press 'S' to capture empty library reference frame.")
print("Press 'Q' to quit.")

#4. Video streaming

while True:

    ret, frame = cap.read()

    if not ret:
        break

    #copy frame for drawing output
    display = frame.copy()

    #5. If background not set, keep displaying the details

    if background is None:

        cv2.putText(
            display,
            "Press S to save empty library image",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        #show seat boxes before detection starts
        for (x, y, w, h) in seats:
            cv2.rectangle(
                display,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

    else:

        #6. Pre-process current frame

        gray_current = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray_current = cv2.GaussianBlur(
            gray_current,
            (5, 5),
            0
        )

        available = 0

        #7. Check each seat

        for i, (x, y, w, h) in enumerate(seats):

            seat_current = gray_current[
                y:y+h,
                x:x+w
            ]

            seat_background = background[
                y:y+h,
                x:x+w
            ]

            #checking the absolute difference between empty and current seat
            diff = cv2.absdiff(
                seat_background,
                seat_current
            )

            #remove tiny brightness fluctuations caused by sunlight
            diff = cv2.GaussianBlur(
                diff,
                (5, 5),
                0
            )

            #convert to binary image
            _, thresh = cv2.threshold(
                diff,
                40,
                255,
                cv2.THRESH_BINARY
            )

            #count changed pixels
            changed_pixels = cv2.countNonZero(
                thresh
            )

            #seat area based threshold (15%)
            seat_area = w * h
            seat_threshold = seat_area * 0.15

            #update counter
            if changed_pixels >= seat_threshold:
                seat_counter[i] += 1
            else:
                seat_counter[i] = 0

            #seat must appear occupied
            #for 5 consecutive frames
            if seat_counter[i] >= 5:
                occupied = True
            else:
                occupied = False

            #reflecting color and updating available count
            if occupied:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
                available += 1

            #draw rectangle around the seats
            cv2.rectangle(
                display,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

        #8. Showing availability summary

        total = len(seats)

        percentage = round(
            100 * available / total,
            1
        )

        text = f"Available: {available}/{total} ({percentage}%)"

        cv2.putText(
            display,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

    #9. Show output window

    cv2.imshow(
        "Library Seat Detector",
        display
    )

    key = cv2.waitKey(1)

    #save empty library frame
    if key == ord('s') or key == ord('S'):

        background = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        background = cv2.GaussianBlur(
            background,
            (5, 5),
            0
        )

        print("Empty library reference saved.")

    #exit program
    if key == ord('q') or key == ord('Q') or key == 27:
        break

#11. Cleanup

cap.release()
cv2.destroyAllWindows()