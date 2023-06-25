import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

from extract_features import is_valid_file


class heatmap_on_JPG:
    def __init__(self, data_filename):
        print("Processing heatmap..")
        data_filename = data_filename
        base_path = os.path.abspath("../back/gaze_data_textFiles")
        self.processed_data = self.process_file(base_path + "\\" + str(data_filename))

    def heatmap_on_image(self, image_index, processed_data):
        # Check if image_index is within the bounds of processed_data
        if not 0 <= image_index < len(processed_data):
            print(f"Invalid image index: {image_index}")
            return

        # Load the JPG image
        print("Loading picture ",image_index," for heatmap drawing..")
        base_path = os.path.abspath(os.path.join("../back/diagnostic_video_images"))
        image_path = os.path.join(base_path, f"{image_index + 1}.png")
        image = plt.imread(image_path)

        # Convert the image to RGBA format if it doesn't have an alpha channel
        if image.shape[2] == 3:
            image = np.dstack((image, np.ones((image.shape[0], image.shape[1]))))

        # Create a blank heatmap of the same size as the image
        heatmap = np.zeros_like(image[:, :, 0])

        # sample normalized x and y values
        x = [point[0] for point in processed_data[image_index]]
        y = [point[1] for point in processed_data[image_index]]

        # Convert normalized coordinates to pixel coordinates
        h, w, _ = image.shape
        x_pixels = np.array(x) * w
        y_pixels = np.array(y) * h

        # Add the heatmap points
        for i in range(len(x_pixels)):
            heatmap[int(y_pixels[i]), int(x_pixels[i])] = 1

        # Apply Gaussian smoothing to the heatmap with higher sigma value
        heatmap = gaussian_filter(heatmap, sigma=25)

        # Normalize the heatmap values between 0 and 1
        heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap))

        # Apply colormap with higher alpha value to the heatmap
        heatmap = plt.cm.hot(heatmap)
        heatmap[:, :, 3] = 1  # Increase alpha value for more opacity

        # Overlay the heatmap on the image
        overlay = (0.5 * image) + (0.5 * heatmap)  # Adjust weight for desired intensity

        # Save the image with the heatmap overlay
        output_path = os.path.abspath(os.path.join('..', "back", "temp_user_heatmap_images", f"{image_index + 1}.jpg"))
        plt.imsave(output_path, overlay)

    """
    Process the input file, normalize the gaze points, and save the data to a JSON file.
    """

    def process_file(self, input_file):
        if not is_valid_file(input_file):
            print(f"Invalid file: {input_file}")
            return
        print("Process raw gaze data file..")
        # Set the width and height of your display
        width, height = 1920, 1080

        # Prepare a list of 24 empty lists to store the processed data
        processed_data = [[] for _ in range(24)]

        # Define a variable to hold the initial timestamp
        initial_timestamp = None

        # Open the input file
        with open(input_file, 'r') as f:
            # Loop over each line in the file
            for line in f:
                # Split the line into parts
                parts = line.split()

                # Check if there are exactly four parts
                if len(parts) == 4:
                    # Extract the parts
                    identifier, timestamp, x, y = parts
                    if 0 <= float(x) <= width and 0 <= float(y) <= height:
                        if initial_timestamp is None:
                            initial_timestamp = float(timestamp)
                        # Adjust the timestamp to be relative to the first timestamp
                        adjusted_timestamp = float(timestamp) - initial_timestamp

                        # Calculate the interval (in milliseconds)
                        interval = int(adjusted_timestamp // 5000)

                        # Normalize the x and y coordinates
                        normalized_x = float(x) / width
                        normalized_y = float(y) / height

                        # Add the data to the list, if the interval is within 0-23
                        if 0 <= interval < 24:
                            processed_data[interval].append([normalized_x, normalized_y])
            print("Done Process.")
            return processed_data
