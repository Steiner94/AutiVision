import json
import numpy as np
import os
from scipy.stats import skew

middle_line = 0.47916666666


def is_valid_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return True
    except IOError:
        return False


def is_point_in_box(x: float, y: float, box: dict) -> bool:
    """
    Check if a point is inside a given box.
    """
    if not box:
        print("Error person object not exist or empty")
        return False
    width = box["Width"]
    height = box["Height"]
    left = box["Left"]
    top = box["Top"]

    return float(left) <= x <= (float(left) + float(width)) and float(top) <= y <= (float(top) + float(height))


def round_float_values(obj):
    for key in obj:
        if isinstance(obj[key], float):
            obj[key] = round(obj[key], 3)
        elif isinstance(obj[key], tuple):
            obj[key] = tuple(round(x, 3) for x in obj[key])
    return obj


def calculate_gaze_features(input_file: str, objects_to_observe: str, saccade_threshold: float = 0.1) -> list:
    """
    Calculate various gaze features from the data.
    """
    if not is_valid_file(input_file):
        print(f"Invalid file: {input_file}")
        return

    if not is_valid_file(objects_to_observe):
        print(f"Invalid file: {objects_to_observe}")
        return

    selected_side = ['r', 'r', 'l', 'l', 'r', 'l', 'l', 'r', 'r', 'l', 'r', 'r', 'l', 'r', 'l', 'r', 'l', 'r', 'r', 'r',
                     'l', 'l', 'r', 'l']

    features_data = []

    with open(input_file, 'r') as f:
        data = json.load(f)

    with open(objects_to_observe) as json_file:
        face_objects = json.load(json_file)

    for i, photo in enumerate(data):
        if photo:
            inside_count, left_points, right_points, eye_mouth_count = 0, 0, 0, 0
            photo_array = np.array(photo)
            photo_id = str(i + 1)  # Adjusted to match the keys in your JSON
            photo_data = face_objects.get(photo_id, {})
            # separate left and right points.
            for value in photo_array:
                timestamp, x, y = value
                if 0 < y < 1:
                    if 0 <= x <= middle_line:
                        left_points += 1
                    elif middle_line < x < 1:
                        right_points += 1
                # check if point is inside a person object box.
                for face_id, face_data in photo_data.items():
                    face_box = face_data['Face']
                    if is_point_in_box(x, y, face_box):
                        inside_count += 1
                    if is_point_in_box(x, y, face_data['leftEye']) or \
                            is_point_in_box(x, y, face_data['rightEye']) or \
                            is_point_in_box(x, y, face_data['mouth']):
                        eye_mouth_count += 1

            try:
                # Calculate fixations
                dispersion_threshold = 0.1  # Change to your chosen threshold
                duration_threshold = 100  # Change to your chosen threshold (in same units as timestamp)
                fixation_data = compute_fixations(photo_array, dispersion_threshold, duration_threshold)

                photo_array_xy = photo_array[:, 1:]
                mean_x, mean_y = np.mean(photo_array_xy, axis=0)
                median_x, median_y = np.median(photo_array_xy, axis=0)
                skew_x, skew_y = skew(photo_array_xy, axis=0)
                std_x, std_y = np.std(photo_array_xy, axis=0)
                range_x, range_y = np.ptp(photo_array_xy, axis=0)
                diff = np.diff(photo_array_xy, axis=0)
                distances = np.sqrt(np.sum(diff ** 2, axis=1))
                total_distance = np.sum(distances)
                saccades = np.where(distances > saccade_threshold)[0].size
                total_points = right_points + left_points
                percentage_inside = (inside_count / total_points) * 100
                eye_mouth_percentage = (eye_mouth_count / total_points) * 100
                left_percentage = (left_points / total_points)
                right_percentage = (right_points / total_points)
                is_right = False
                variance_x, variance_y = np.var(photo_array_xy, axis=0)  # New line for variance

                # Calculate duration
                initial_timestamp = photo_array[0, 0]
                final_timestamp = photo_array[-1, 0]
                duration = final_timestamp - initial_timestamp

                # Calculate average velocity
                average_velocity = total_distance / duration

                # Calculate angular velocity
                angles = np.arctan2(diff[:, 1], diff[:, 0])
                angular_velocity = np.mean(np.abs(np.diff(angles))) / duration
            except Exception as e:
                print(input_file, "photo:", i, str(e))  # Optionally print the error message for debugging purposes

            # determine if person looked at "right" photo
            if (selected_side[i] == 'r' and right_percentage > 0.5) or (
                    selected_side[i] == 'l' and left_percentage > 0.5):
                is_right = True

            features_data.append({
                "Photo": i + 1,
                "Mean Gaze Position": (mean_x, mean_y),
                "Median Gaze Position": (median_x, median_y),
                "Skewness of Gaze Positions": (skew_x, skew_y),
                "Standard Deviation of Gaze Positions": (std_x, std_y),
                "Range of Gaze Positions": (range_x, range_y),
                "Total Gaze Distance": total_distance,
                "Number of Saccades": saccades,
                "Left Part Percentage": left_percentage,
                "Right Part Percentage": right_percentage,
                "Percentage of points inside boxes": percentage_inside / 100,
                "Percentage of points inside eyes and mouth": eye_mouth_percentage / 100,
                "Percentage of correct side": is_right,
                "Variance of Gaze Positions": (variance_x, variance_y),  # New line for variance
                "Average Velocity": average_velocity,
                "Angular Velocity": angular_velocity,
                "Number of Fixations": fixation_data["Number of Fixations"],
                "Average Fixation Duration": np.mean(fixation_data["Average Fixation Duration"]) if fixation_data[
                    "Average Fixation Duration"] else 0,
                "Total Fixation Duration": fixation_data["Total Fixation Duration"],
                "Fixation Dispersion": fixation_data["Fixation Dispersion"],

            })

    return features_data


def compute_fixations(gaze_points, dispersion_threshold, duration_threshold):
    """
    Compute the number of fixations in the gaze points and their durations.

    Args:
    gaze_points: A numpy array of shape (n, 3) where n is the number of gaze points and the columns are (timestamp, x, y).
    dispersion_threshold: The maximum distance between points in a fixation.
    duration_threshold: The minimum duration of a fixation.

    Returns:
    A dictionary with the gaze features.
    """
    n = len(gaze_points)
    fixations = 0
    fixation_durations = []
    fixation_points = []
    saccades = 0
    total_distance = 0
    previous_point = gaze_points[0, 1:]
    time_to_first_fixation = None

    i = 0

    while i < n:
        j = i + 1

        # Find the next gaze point that is far away.
        while j < n:
            distance = np.sqrt(np.sum((gaze_points[j, 1:] - previous_point) ** 2))
            total_distance += distance
            previous_point = gaze_points[j, 1:]
            dispersion = np.sqrt(np.sum((gaze_points[j, 1:] - gaze_points[i, 1:]) ** 2))
            if dispersion > dispersion_threshold:
                break
            j += 1

        # If the gaze stayed in the small distance for a long time, it is a fixation.
        duration = gaze_points[j - 1, 0] - gaze_points[i, 0]
        if duration > duration_threshold:
            fixations += 1
            fixation_durations.append(duration)
            fixation_points.append(gaze_points[i:j, 1:])
            if time_to_first_fixation is None:
                time_to_first_fixation = gaze_points[i, 0]
            saccades += 1

        i = j

    total_fixation_duration = np.sum(fixation_durations)
    average_fixation_duration = np.mean(fixation_durations) if fixation_durations else 0

    # Calculate fixation dispersion
    fixation_points = np.concatenate(fixation_points) if fixation_points else 0
    if fixation_points is not None:
        dists = np.sqrt(np.sum((fixation_points[:, None, :] - fixation_points[None, :, :]) ** 2, axis=-1))
        fixation_dispersion = np.mean(dists)
    else:
        fixation_dispersion = 0

    return {
        "Number of Fixations": fixations,
        "Total Fixation Duration": total_fixation_duration,
        "Average Fixation Duration": average_fixation_duration,
        "Fixation Dispersion": fixation_dispersion

    }


def features_to_svm_input(features_data, output_txt_file):
    num_photos = len(features_data)  # count number of photos
    if num_photos:
        with open(output_txt_file, 'w') as f:
            X = []
            sum_mean_gaze_x, sum_mean_gaze_y = 0, 0
            sum_median_gaze_x, sum_median_gaze_y = 0, 0  # new median sum initialization
            sum_skew_x, sum_skew_y = 0, 0
            sum_deviation_x, sum_deviation_y = 0, 0
            sum_range_x, sum_range_y = 0, 0
            sum_total_distance, sum_saccades = 0, 0
            sum_inside_boxes, sum_correct_side = 0, 0
            sum_variance_x, sum_variance_y = 0, 0  # new variance sum initialization
            sum_inside_eyes_mouth = 0
            sum_average_velocity = 0
            sum_angular_velocity = 0
            sum_fixations = 0
            sum_avg_fixation_duration = 0
            sum_total_fixation_duration = 0
            sum_fixation_dispersion = 0

            for data in features_data:
                features = []
                sum_mean_gaze_x += data["Mean Gaze Position"][0]
                sum_mean_gaze_y += data["Mean Gaze Position"][1]
                sum_median_gaze_x += data["Median Gaze Position"][0]  # new median sum calculation
                sum_median_gaze_y += data["Median Gaze Position"][1]  # new median sum calculation
                sum_skew_x += data["Skewness of Gaze Positions"][0]
                sum_skew_y += data["Skewness of Gaze Positions"][1]
                sum_deviation_x += data["Standard Deviation of Gaze Positions"][0]
                sum_deviation_y += data["Standard Deviation of Gaze Positions"][1]
                sum_range_x += data["Range of Gaze Positions"][0]
                sum_range_y += data["Range of Gaze Positions"][1]
                sum_total_distance += data["Total Gaze Distance"]
                sum_saccades += data["Number of Saccades"]
                sum_inside_boxes += data["Percentage of points inside boxes"]
                sum_inside_eyes_mouth += data["Percentage of points inside eyes and mouth"]
                sum_correct_side += int(data["Percentage of correct side"])  # assuming True = 1 and False = 0
                sum_variance_x += data["Variance of Gaze Positions"][0]  # new variance sum calculation
                sum_variance_y += data["Variance of Gaze Positions"][1]  # new variance sum calculation
                sum_average_velocity += data["Average Velocity"]
                sum_angular_velocity += data["Angular Velocity"]
                sum_fixations += data["Number of Fixations"]
                sum_avg_fixation_duration += data["Average Fixation Duration"]
                sum_total_fixation_duration += data["Total Fixation Duration"]
                sum_fixation_dispersion += data["Fixation Dispersion"]

                features.extend(data["Mean Gaze Position"])
                features.extend(data["Median Gaze Position"])  # new line for median
                features.extend(data["Skewness of Gaze Positions"])
                features.extend(data["Standard Deviation of Gaze Positions"])
                features.extend(data["Range of Gaze Positions"])
                features.append(data["Total Gaze Distance"])
                features.append(data["Number of Saccades"])
                features.append(data["Percentage of points inside boxes"])
                features.append(data["Percentage of points inside eyes and mouth"])
                features.append(data["Percentage of correct side"])
                features.extend(data["Variance of Gaze Positions"])
                features.append(data["Angular Velocity"])
                features.append(data["Average Velocity"])
                features.append(data["Number of Fixations"])
                features.append(data["Average Fixation Duration"])
                features.append(data["Total Fixation Duration"])
                features.append(data["Fixation Dispersion"])

                X.append(features)

            with open(output_txt_file, 'w') as f:
                for features in X:
                    f.write(str(features) + "\n")

            # Calculate averages
            avg_mean_gaze = (sum_mean_gaze_x / num_photos, sum_mean_gaze_y / num_photos)
            avg_median_gaze = (
                sum_median_gaze_x / num_photos, sum_median_gaze_y / num_photos)  # new median average calculation
            avg_skew = (sum_skew_x / num_photos, sum_skew_y / num_photos)
            avg_deviation = (sum_deviation_x / num_photos, sum_deviation_y / num_photos)
            avg_range = (sum_range_x / num_photos, sum_range_y / num_photos)
            avg_total_distance = sum_total_distance / num_photos
            avg_saccades = sum_saccades / num_photos
            avg_inside_boxes = sum_inside_boxes / num_photos
            avg_inside_eyes_mouth = sum_inside_eyes_mouth / num_photos
            avg_correct_side = sum_correct_side / num_photos
            avg_variance = (
                sum_variance_x / num_photos, sum_variance_y / num_photos)  # new variance average calculation
            avg_average_velocity = sum_average_velocity / num_photos
            avg_angular_velocity = sum_angular_velocity / num_photos
            avg_fixations = sum_fixations / num_photos
            avg_avg_fixation_duration = sum_avg_fixation_duration / num_photos
            avg_total_fixation_duration = sum_total_fixation_duration / num_photos
            avg_fixation_dispersion = sum_fixation_dispersion / num_photos

            # SVM input now includes the average variance, average velocity, and angular velocity
            svm_input = np.array([
                *avg_mean_gaze,
                *avg_median_gaze,
                *avg_skew,
                *avg_deviation,
                *avg_range,
                avg_total_distance,
                avg_saccades,
                avg_inside_boxes,
                avg_inside_eyes_mouth,
                avg_correct_side,
                *avg_variance,
                avg_average_velocity,
                avg_angular_velocity,
                avg_fixations,
                avg_avg_fixation_duration,
                avg_total_fixation_duration,
                avg_fixation_dispersion,

            ])

            # Write SVM input to the file
            with open(output_txt_file, "a") as file:
                file.write('[' + ', '.join(map(str, svm_input)) + ']\n')
            return svm_input


def normalize_gaze_point(input_file: str, output_file: str) -> None:
    """
    Process the input file, normalize the gaze points, and save the data to a JSON file.
    """
    if not is_valid_file(input_file):
        print(f"Invalid file: {input_file}")
        return

    width, height = 1920, 1080
    processed_data = [[] for _ in range(24)]
    initial_timestamp = None

    with open(input_file, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 4:
                identifier, timestamp, x, y = parts
                if initial_timestamp is None:
                    initial_timestamp = float(timestamp)
                if 0 <= float(x) <= width and 0 <= float(y) <= height:
                    adjusted_timestamp = float(timestamp) - initial_timestamp
                    interval = int(adjusted_timestamp // 5000)
                    normalized_x = float(x) / width
                    normalized_y = float(y) / height
                    if 0 <= interval < 24:
                        processed_data[interval].append([adjusted_timestamp, normalized_x, normalized_y])

    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=4)


def features_results(filename):
    directory = 'gaze_data_textFiles'
    output_dir = 'processed_data'
    output_dir_svm = 'svm_inputs'
    objects_to_observe = os.path.abspath("../back/objects.json")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(output_dir_svm):
        os.makedirs(output_dir_svm)
    input_file = os.path.join(directory, filename)
    output_file = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_processed.json')
    output_txt_file = os.path.join(output_dir_svm, f'{os.path.splitext(filename)[0]}_features.txt')
    print("Normalize data...")
    normalize_gaze_point(input_file, output_file)

    print("Done normalize.")

    print("Extract features...")
    features_of_normalize_data = calculate_gaze_features(output_file, objects_to_observe)
    # svm_input = features_to_svm_input(features_of_normalize_data,
    #               output_txt_file)

    return features_of_normalize_data
