import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler


def svm_result(input_features):
    print("Start svm process..")
    # `X` is your feature matrix where each row is a feature vector
    X = np.array([[0.5259134422580606, 0.48812216867439734, 0.5194381055056155, 0.4567417829122487, 0.0946732238999383, 0.34574028758797476, 0.1729818348409, 0.19229453940081812, 0.5715818583607251, 0.6677212755911657, 3.1810856124573, 4.75, 0.16391747771442036, 0.03768694619016264, 0.6666666666666666, 0.03437067955176523, 0.04686974501427769, 0.0006570305221371438, 0.00026535387824660106, 8.75, 530.7652333882625, 4121.696658343077, 0.3056724054510172], [0.5233962697561196, 0.5703707357294244, 0.492604522903012, 0.5824055923978095, 0.1667318634796069, 0.13101364839679885, 0.20598432188744642, 0.17476523566255278, 0.6659284954622725, 0.6542456370520758, 3.5811097667961014, 7.875, 0.23628339802672815, 0.0332812190726803, 0.7083333333333334, 0.04636700478548685, 0.03457480820575107, 0.0007177917541701133, 0.0002482034847074727, 9.833333333333334, 465.8711657360104, 4383.533562499989, 0.32426891981449185], [0.562520581241876, 0.4218226364744957, 0.5607510219972978, 0.3792463918814068, -0.31642166740465455, 0.43620287394304397, 0.21086219848524954, 0.18009743974272005, 0.7496761520603612, 0.6436050699030135, 4.573754193836481, 9.875, 0.23126997610771569, 0.027746719726555426, 0.7916666666666666, 0.04750173438625959, 0.03633187244701754, 0.0009397891461860173, 0.0002594081864897815, 11.375, 382.94873331033267, 3993.463125002881, 0.32959691661412366], [0.4943192725947054, 0.46482313102877, 0.4941246434736835, 0.4627867468316558, -0.12348455535341511, 0.595685309778371, 0.2007890234993791, 0.1574334010121743, 0.6961777566492904, 0.738179689771142, 3.908991588227217, 8.166666666666666, 0.26076456779555474, 0.02493037969397037, 0.5833333333333334, 0.04230264947470275, 0.0282754650325964, 0.0008121434064799971, 0.0002497032367608264, 9.0, 481.6464011309538, 3962.2760000000108, 0.2876449538033327], [0.4922401881844887, 0.4556464494726347, 0.5016068543256659, 0.43201720126181725, 0.042712572319188825, 0.5306669096605445, 0.20508583717059126, 0.15651115062888318, 0.6504920650091437, 0.6173241914397786, 3.7441884610318716, 8.208333333333334, 0.3831282395960411, 0.061098089337430446, 0.7916666666666666, 0.043570024492604824, 0.02746694877792658, 0.0007505371744287257, 0.00022855642356265057, 10.0, 490.8714738831777, 4473.717429166674, 0.2987976779419384], [0.4424572218578478, 0.6434201701168422, 0.433282680348732, 0.6199640436297523, 0.2875526664330537, 0.6013247643453207, 0.1643907386220052, 0.12234961737746741, 0.5524412345669799, 0.47264323565186056, 3.0102619852481207, 5.375, 0.04547904868862892, 0.023532183044739478, 0.8333333333333334, 0.029897136011831842, 0.017873422063642775, 0.0006038230650954429, 0.0002546740411023875, 8.708333333333334, 644.6050771863812, 4571.343795833372, 0.2356336921811699], [0.5372567726125866, 0.3868527291040255, 0.5639063880015804, 0.4002521626802506, -0.17452752721483913, 0.5508009920496124, 0.17189664511376204, 0.20724682597554228, 0.5679882852751856, 0.7108519075928706, 3.822400145968394, 5.666666666666667, 0.059463388052155494, 0.0030844786085876233, 0.6, 0.057445314471623606, 0.0686292716573146, 0.0010864018711380105, 0.00030271945931590087, 7.533333333333333, 432.12293758068665, 2917.9709533333526, 0.30686039971780266]])

    # Normalize the data to [0,1] range
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    # Print the normalized data
    print("Normalized data..")

    # `y` is your array of labels (the scores)
    y = np.array([
        # Your scores go here
        # For example:
        32, 34, 36, 28, 27, 38, 26
    ])

    # Create and fit the model
    model = svm.SVC(kernel='linear')
    model.fit(X, y)

    print("SVM model created and fitted..")

    # Predict
    new_X = np.array(
        [input_features])

    # Don't forget to normalize your new data
    new_X = scaler.transform(new_X)

    # Print the normalized new data
    print("Normalized new data..")

    # Use the trained model to predict the scores
    predictions = model.predict(new_X)
    print("Done, grade is: ", predictions[0])
    return predictions[0]


def features_to_svm(features_data):
    print("Process features to svm..")
    num_photos = len(features_data)  # count number of photos
    if num_photos:
            X = []
            sum_mean_gaze_x, sum_mean_gaze_y = 0, 0
            sum_median_gaze_x, sum_median_gaze_y = 0, 0
            sum_skew_x, sum_skew_y = 0, 0
            sum_deviation_x, sum_deviation_y = 0, 0
            sum_range_x, sum_range_y = 0, 0
            sum_total_distance, sum_saccades = 0, 0
            sum_inside_boxes, sum_correct_side = 0, 0
            sum_variance_x, sum_variance_y = 0, 0
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
                sum_median_gaze_x += data["Median Gaze Position"][0]
                sum_median_gaze_y += data["Median Gaze Position"][1]
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
                sum_variance_x += data["Variance of Gaze Positions"][0]
                sum_variance_y += data["Variance of Gaze Positions"][1]
                sum_average_velocity += data["Average Velocity"]
                sum_angular_velocity += data["Angular Velocity"]
                sum_fixations += data["Number of Fixations"]
                sum_avg_fixation_duration += data["Average Fixation Duration"]
                sum_total_fixation_duration += data["Total Fixation Duration"]
                sum_fixation_dispersion += data["Fixation Dispersion"]

                features.extend(data["Mean Gaze Position"])
                features.extend(data["Median Gaze Position"])
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



            # Calculate averages
            avg_mean_gaze = (sum_mean_gaze_x / num_photos, sum_mean_gaze_y / num_photos)
            avg_median_gaze = (
                sum_median_gaze_x / num_photos, sum_median_gaze_y / num_photos)
            avg_skew = (sum_skew_x / num_photos, sum_skew_y / num_photos)
            avg_deviation = (sum_deviation_x / num_photos, sum_deviation_y / num_photos)
            avg_range = (sum_range_x / num_photos, sum_range_y / num_photos)
            avg_total_distance = sum_total_distance / num_photos
            avg_saccades = sum_saccades / num_photos
            avg_inside_boxes = sum_inside_boxes / num_photos
            avg_inside_eyes_mouth = sum_inside_eyes_mouth / num_photos
            avg_correct_side = sum_correct_side / num_photos
            avg_variance = (
                sum_variance_x / num_photos, sum_variance_y / num_photos)
            avg_average_velocity = sum_average_velocity / num_photos
            avg_angular_velocity = sum_angular_velocity / num_photos
            avg_fixations = sum_fixations / num_photos
            avg_avg_fixation_duration = sum_avg_fixation_duration / num_photos
            avg_total_fixation_duration = sum_total_fixation_duration / num_photos
            avg_fixation_dispersion = sum_fixation_dispersion / num_photos

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

            return svm_input
